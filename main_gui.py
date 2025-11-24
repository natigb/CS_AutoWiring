import tkinter as tk
from tkinter import filedialog, Menu, ttk, PhotoImage
from wiring_functions import get_wiring_from_SC, get_auto_wiring
from wiring_gui import WiringFrame
from edit_gui import EditFrame
from add_sensor_gui import AddSensorFrame   # <-- Frame version
from ports_coordenates import logger_ports
import os, sys
from auto_gui import open_selection_interface
from PIL import Image, ImageTk
import pyautogui
from title_block import TitleBlock
import webbrowser

# ------------------- Colors and Style -------------------
PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 10, "bold")
SECONDARY_FONT = ("Segoe UI", 10)

wiring = "no wires"
def resource_path(relative):
    """Get absolute path for PyInstaller and development."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative)
"""
Main App Tk window
"""
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wiring Tool")
        self.geometry("1700x900")
        self.configure(bg=DARK_COLOR)
        self.icon = PhotoImage(file=resource_path("img/icons/CS_logo.png"))

        # Set as window icon
        self.iconphoto(False, self.icon)

        # ---------------- Style ----------------
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=WHITE)
        style.configure("Left.TFrame", background=DARK_COLOR)
        style.configure("Right.TFrame", background=WHITE)

        style.configure("TLabel", background=WHITE, foreground=DARK_COLOR, font=FONT)

        style.configure("TButton",
                        font=FONT,
                        padding=6,
                        background=PRIMARY_COLOR,
                        foreground=DARK_COLOR)
        style.map("TButton",
                  background=[("active", "#FFD633")],
                  foreground=[("active", DARK_COLOR)])

        style.configure("TCombobox",
                        padding=5,
                        font=FONT,
                        selectbackground=PRIMARY_COLOR,
                        fieldbackground=WHITE,
                        foreground=DARK_COLOR,
                        background=WHITE,
                        arrowsize=20)
        style.configure(
            "Custom.TCheckbutton",
            font=FONT,
            foreground=WHITE,
            background=DARK_COLOR,
            focuscolor=DARK_COLOR,
            indicatormargin=5,
            padding=6
        )
        style.map(
            "Custom.TCheckbutton",
            foreground=[("active", WHITE), ("selected", DARK_COLOR)],
            background=[("active", PRIMARY_COLOR), ("selected", PRIMARY_COLOR)]
        )

        # ---------------- Menu Bar ----------------
        SC_icon = Image.open(resource_path("img/icons/SC_icon.png")).resize((20, 20))
        SC_icon_tk = ImageTk.PhotoImage(SC_icon)
        Save_icon = Image.open(resource_path("img/icons/Save_icon.png")).resize((20, 20))
        Save_icon_tk = ImageTk.PhotoImage(Save_icon)
        New_icon = Image.open(resource_path("img/icons/New_icon.png")).resize((20, 20))
        New_icon_tk = ImageTk.PhotoImage(New_icon)
        Restart_icon = Image.open(resource_path("img/icons/Restart_icon.png")).resize((20, 20))
        Restart_icon_tk = ImageTk.PhotoImage(Restart_icon)

        menubar = Menu(self,font=FONT, bg=PRIMARY_COLOR, fg=WHITE,
                       activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)

        file_menu = Menu(menubar,font=SECONDARY_FONT, tearoff=0, bg=WHITE, fg=DARK_COLOR,
                         activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)
        file_menu.add_command(label="New Wiring", image=New_icon_tk, compound="left", command=self.automatic_action)
        file_menu.add_command(label="Open from ShortCut", image=SC_icon_tk, compound="left", command=self.choose_def_file)
        file_menu.add_command(label="Save Diagram", image=Save_icon_tk, compound="left", command=self.save_current_diagram)
        file_menu.add_command(label="Restart program", compound="left", command=self.restart_program)
        file_menu.add_command(label="Exit Program", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self._SC_icon = SC_icon_tk
        self._Save_icon = Save_icon_tk
        self._New_icon = New_icon_tk
        self._Restart_icon =Restart_icon_tk

        tools_menu = Menu(menubar,font=SECONDARY_FONT, tearoff=0, bg=WHITE, fg=DARK_COLOR,
                          activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)
        tools_menu.add_command(label="Edit", command=self.edit_action)
        tools_menu.add_command(label="Add Sensor", command=self.add_sensor)
        tools_menu.add_command(label="Add Tag", command=self.add_tag)
        menubar.add_cascade(label="Tools", menu=tools_menu)


        help_menu = Menu(menubar,font=SECONDARY_FONT, tearoff=0, bg=WHITE, fg=DARK_COLOR,
                          activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)
        help_menu.add_command(label="Open documentation", command=self.open_doc)
        help_menu.add_command(label="Draw manual wire", command=self.open_wire_mode_help)
        menubar.add_cascade(label="Help", menu=help_menu)


        self.config(menu=menubar)

        # ---------------- Main Layout ----------------
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        # Left panel (persistent buttons)
        self.left_panel = ttk.Frame(main_frame, padding=20, style="Left.TFrame")
        self.left_panel.pack(side="left", fill="y")
        self.compact_mode_flag = tk.BooleanVar(value=False)
        self.mode = "Default"

        cs_logo = Image.open(resource_path("img/decorations/cs_logo.png")).resize((219, 196))
        cs_logo_tk = ImageTk.PhotoImage(cs_logo)

        # Create the label and store a reference to the image
        self.cs_logo_label = ttk.Label(
            self.left_panel,
            image=cs_logo_tk,
            background=DARK_COLOR
        )
        self.cs_logo_label.image = cs_logo_tk 
        self.cs_logo_label.pack(fill="x", pady=5)
        ttk.Button(self.left_panel, text="Draw Wiring", command=self.draw).pack(fill="x", pady=20)
        
        # Title block + regulator toggles
        self.show_regulator = tk.BooleanVar(value=False)
        self.regulator = None
        self.title_block = None
        self.show_title_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self.left_panel,
            text="Show Title Block",
            variable=self.show_title_var,
            command=self.toggle_title_block,
            style="Custom.TCheckbutton"
        ).pack(fill="x", pady=5)

        ttk.Checkbutton(
            self.left_panel,
            text="Show Regulator",
            variable=self.show_regulator,
            command=self.toggle_regulator,
            style="Custom.TCheckbutton"
        ).pack(fill="x", pady=5)

        ttk.Checkbutton(
            self.left_panel,
            text="Compact Mode",
            variable=self.compact_mode_flag,
            command=self.toggle_mode,
            style="Custom.TCheckbutton"
        ).pack(fill="x", pady=5)

        ttk.Button(self.left_panel, text="Save as image", command=self.save_current_diagram).pack(side = "bottom", fill="x", pady=5)

        # Right panel (dynamic content, grid layout)
        self.right_panel = ttk.Frame(main_frame, padding=20, style="Right.TFrame")
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Configure grid inside right_panel
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=1)  # content row
        self.right_panel.rowconfigure(1, weight=0)  # bottom row (title block / regulator)

        self.show_home()
    def open_doc(self):
        webbrowser.open("https://github.com/natigb/CS_AutoWiring/wiki")

    def open_wire_mode_help(self):
        webbrowser.open("https://github.com/natigb/CS_AutoWiring/wiki/E.-Manual-Wire-Drawing-Mode")

    def toggle_mode(self):
        if self.compact_mode_flag.get():
            self.mode = "compact"
        else:
            self.mode = "Default"
        self.draw()

    def toggle_regulator(self):
        """Show/hide regulator image widget at bottom of right panel."""
        if self.regulator:
            self.regulator.destroy()
            self.regulator = None

        if self.show_regulator.get():
            image = Image.open(resource_path("img/regulator.png")).resize((311, 360))
            self.regulator_img = ImageTk.PhotoImage(image)
            self.regulator = ttk.Label(self.right_panel, image=self.regulator_img, background=WHITE)
            self.regulator.grid(row=0, column=0, sticky="e", pady=10)

            # --- Make it draggable ---
            self.drag_data = {"x": 0, "y": 0}

            def on_press(event):
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y

            def on_drag(event):
                dx = event.x - self.drag_data["x"]
                dy = event.y - self.drag_data["y"]

                # get current position and move
                x = self.regulator.winfo_x() + dx
                y = self.regulator.winfo_y() + dy
                self.regulator.place(x=x, y=y)  # switch to place for free movement

            self.regulator.bind("<ButtonPress-1>", on_press)
            self.regulator.bind("<B1-Motion>", on_drag)


    def toggle_title_block(self):
        """Show/hide editable TitleBlock at bottom of right panel."""
        if self.title_block:
            self.title_block.destroy()
            self.title_block = None
        if self.show_title_var.get():
            self.title_block = TitleBlock(
                self.right_panel,
                company="Company Name",
                content="Sensor Wiring Diagram",
                project="Weather Station CR1000X",
                made_by="Campbell Scientific"
            )
            self.title_block.grid(row=1, column=0, sticky="ew", pady=10)

    def clear_right_panel(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self.show_regulator.set(False)
        self.show_title_var.set(False)

    def show_home(self):
        self.clear_right_panel()
        background = Image.open(resource_path("img/decorations/background.png"))#.resize((2000, 912))
        background_tk = ImageTk.PhotoImage(background)

        self.result_label = ttk.Label(
            self.right_panel,
            image=background_tk,
            text="Create new wiring or open from Short Cut",
            compound="center",
            foreground= WHITE 
        )
        self.result_label.image = background_tk 
        self.result_label.grid(row=0, column=0, pady=0, sticky="ew")

    def choose_def_file(self):
        global wiring
        filepath = filedialog.askopenfilename(
            title="Select a .DEF file", filetypes=[("DEF files", "*.DEF")]
        )
        if filepath:
            filename = os.path.basename(filepath)
            wiring = get_wiring_from_SC(filepath)
        
          #self.result_label.config(text=filename)
        self.draw()

    def automatic_action(self):
        global wiring
        selection = open_selection_interface()
        wiring = [get_auto_wiring(logger_ports[selection[0]], selection[1]), selection[0]]
        print("from main: ", wiring)
        #self.result_label.config(text="auto wiring")

    def edit_action(self):
        global wiring
        if wiring == "no wires":
            self.result_label.config(text="no wiring selected")
        else:
            self.clear_right_panel()
            edit_frame = EditFrame(self.right_panel, self, wiring[0],wiring[1])
            edit_frame.grid(row=0, column=0, sticky="nsew")

    def add_sensor(self):
        self.clear_right_panel()
        add_frame = AddSensorFrame(self.right_panel, self)
        add_frame.grid(row=0, column=0, sticky="nsew")

    def add_tag(self):
        """Open small window to enter text, then create draggable/removable tag."""
        top = tk.Toplevel(self)
        top.title("Add Tag")
        top.geometry("250x120")
        top.configure(bg=WHITE)
        top.iconphoto(False, self.icon)

        tk.Label(top, text="Enter tag text:", bg=WHITE, fg=DARK_COLOR).pack(pady=5)
        entry = tk.Entry(top)
        entry.pack(pady=5, padx=10, fill="x")

        def create_tag():
            text = entry.get().strip()
            if not text:
                return
            top.destroy()
            tag = tk.Label(self.right_panel, text=text, bg=WHITE,
                           fg=DARK_COLOR, font=("Segoe UI", 14, "bold"), bd=0, relief="solid")
            tag.place(x=50, y=50)  # initial position

            drag_data = {"x": 0, "y": 0}

            def on_press(event):
                drag_data["x"] = event.x
                drag_data["y"] = event.y

            def on_drag(event):
                dx = event.x - drag_data["x"]
                dy = event.y - drag_data["y"]
                x = tag.winfo_x() + dx
                y = tag.winfo_y() + dy
                tag.place(x=x, y=y)

            def on_right_click(event):
                tag.destroy()

            tag.bind("<ButtonPress-1>", on_press)
            tag.bind("<B1-Motion>", on_drag)
            tag.bind("<Button-3>", on_right_click)

        tk.Button(top, text="Add", command=create_tag).pack(pady=10)

    def draw(self):
        global wiring
        if wiring == "no wires":
            self.result_label.config(text="no wiring selected")
        else:
            self.clear_right_panel()
            wf = WiringFrame(self.right_panel, self, wiring[0], wiring[1],self.mode)
            wf.grid(row=0, column=0, sticky="nsew")

    def restart_program(self):
        python = sys.executable
        os.execv(python, [python] + sys.argv)

    def save_current_diagram(self):
        self.update()
        x = self.right_panel.winfo_rootx()
        y = self.right_panel.winfo_rooty()
        w = self.right_panel.winfo_width()
        h = self.right_panel.winfo_height()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Right Panel"
        )
        if not file_path:
            return

        img = pyautogui.screenshot(region=(x, y, w, h))
        img.save(file_path)
        #self.result_label.config(text=f"Saved: {file_path}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
