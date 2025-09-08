import tkinter as tk
from tkinter import filedialog, Menu, ttk
from wiring_functions import get_wiring_from_SC, get_auto_wiring
from wiring_gui import WiringFrame
from edit_gui import EditFrame
from add_sensor_gui import AddSensorFrame   # <-- Frame version
from ports_coordenates import logger_ports
import os, sys
from auto_gui import open_selection_interface
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pyautogui
from title_block import TitleBlock

# ------------------- Colors and Style -------------------
PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 10, "bold")

wiring = "no wires"


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wiring Tool")
        self.geometry("1000x600")
        self.configure(bg=DARK_COLOR)

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
                        foreground=PRIMARY_COLOR,
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
        menubar = Menu(self, bg=PRIMARY_COLOR, fg=WHITE,
                       activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)

        file_menu = Menu(menubar, tearoff=0, bg=WHITE, fg=DARK_COLOR,
                         activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)
        file_menu.add_command(label="Open from ShortCut", command=self.choose_def_file)
        file_menu.add_command(label="New Wiring", command=self.automatic_action)
        menubar.add_cascade(label="File", menu=file_menu)

        tools_menu = Menu(menubar, tearoff=0, bg=WHITE, fg=DARK_COLOR,
                          activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)
        tools_menu.add_command(label="Edit", command=self.edit_action)
        tools_menu.add_command(label="Add Sensor", command=self.add_sensor)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        file_menu.add_command(label="Save Diagram", command=self.save_current_diagram)


        self.config(menu=menubar)

        # ---------------- Main Layout ----------------
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        # Left panel (persistent buttons)
        self.left_panel = ttk.Frame(main_frame, padding=20, style="Left.TFrame")
        self.left_panel.pack(side="left", fill="y")

        ttk.Button(self.left_panel, text="Draw Wiring", command=self.draw).pack(fill="x", pady=5)
        ttk.Button(self.left_panel, text="Restart", command=self.restart_program).pack(fill="x", pady=5)
       
        # Title block toggle
        self.show_titleblock = tk.BooleanVar(value=False)
        self.title_block = None
        self.show_title_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.left_panel,
            text="Show Title Block",
            variable=self.show_title_var,
            command=self.toggle_title_block,
            style="Custom.TCheckbutton"
        ).pack(fill="x", pady=5)

        ttk.Button(self.left_panel, text="Quit", command=self.quit).pack(fill="x", side="bottom",pady=5)
        # Right panel (dynamic content)
        self.right_panel = ttk.Frame(main_frame, padding=20, style="Right.TFrame")
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.show_home()

    def toggle_title_block(self):
        """Show/hide editable TitleBlock at bottom of right panel."""
         # Remove existing first
        print(self.show_title_var.get())
        if self.title_block:
            self.title_block.destroy()
            self.title_block = None
        # Add only if checkbox is ON
        if self.show_title_var.get():
            
            from title_block import TitleBlock
            self.title_block = TitleBlock(self.right_panel,
                        company="Company Name",
                        content="Sensor Wiring Diagram",
                        project="Weather Station CR1000X",
                        made_by="Campbell Scientific")
            self.title_block.pack(side="bottom", fill="x", pady=10)

    def clear_right_panel(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_right_panel()
        self.result_label = ttk.Label(self.right_panel, text="Select a DEF file...")
        self.result_label.pack(pady=20)

    def choose_def_file(self):
        global wiring
        filepath = filedialog.askopenfilename(
            title="Select a .DEF file", filetypes=[("DEF files", "*.DEF")]
        )
        if filepath:
            filename = os.path.basename(filepath)
            wiring = get_wiring_from_SC(filepath)
            self.result_label.config(text=filename)

    def automatic_action(self):
        global wiring
        selection = open_selection_interface()
        wiring = [get_auto_wiring(logger_ports[selection[0]], selection[1]), selection[0]]
        print("from main: ", wiring)
        self.result_label.config(text="auto wiring")

    def edit_action(self):
        global wiring
        if wiring == "no wires":
            self.result_label.config(text="no wiring selected")
        else:
            self.clear_right_panel()
            edit_frame = EditFrame(self.right_panel, self, wiring[0])
            edit_frame.pack(fill="both", expand=True)

    def add_sensor(self):
        self.clear_right_panel()
        add_frame = AddSensorFrame(self.right_panel, self)
        add_frame.pack(fill="both", expand=True)

    def draw(self):
        global wiring
        if wiring == "no wires":
            self.result_label.config(text="no wiring selected")
        else:
            self.clear_right_panel()
            wf = WiringFrame(self.right_panel, self, wiring[0], wiring[1])
            wf.pack(fill="both", expand=True)
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
        self.result_label.config(text=f"Saved: {file_path}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
