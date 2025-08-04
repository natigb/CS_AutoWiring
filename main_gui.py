import tkinter as tk
from tkinter import filedialog, Menu, ttk
from wiring_functions import get_wiring_from_SC
from wiring_gui import draw_wiring_diagram_gui
from edit_gui import open_edit_interface
import os
from auto_gui import open_selection_interface
# ------------------- Colors and Style -------------------
PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")

# ------------------- Logic -------------------
wiring = "no wires"

def choose_def_file():
    global wiring
    filepath = filedialog.askopenfilename(
        title="Select a .DEF file",
        filetypes=[("DEF files", "*.DEF")],
    )
    if filepath:
        filename = os.path.basename(filepath)
        wiring = get_wiring_from_SC(filepath)
        result_label.config(text=filename)

def automatic_action():
    global wiring
    selection = open_selection_interface()
    wiring = selection
    print(wiring)
    result_label.config(text="auto wiring")

def edit_action():
    global wiring
    result = open_edit_interface(wiring[0])
    if result:
        wiring[0] = result
    print(wiring)
    result_label.config(text="Edited wiring")

def draw():
    global wiring
    print(wiring)
    draw_wiring_diagram_gui(wiring[0], wiring[1])

# ------------------- Main UI -------------------
root = tk.Tk()
root.title("Wiring Tool")
root.geometry("450x250")
root.configure(bg=DARK_COLOR)

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=FONT, padding=6, background=PRIMARY_COLOR, foreground=DARK_COLOR)
style.configure("TLabel", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR)
style.configure(
    "Custom.TCombobox",
    foreground=DARK_COLOR,
    background=WHITE,
    fieldbackground=DARK_COLOR,
    arrowcolor = PRIMARY_COLOR,
    padding=5,
    font= FONT
)
# Menu bar
menubar = Menu(root, bg=WHITE, fg=DARK_COLOR, activebackground=PRIMARY_COLOR, activeforeground=DARK_COLOR)
file_menu = Menu(menubar, tearoff=0, bg=WHITE, fg=DARK_COLOR)
file_menu.add_command(label="Open from ShortCut", command=choose_def_file)
tools_menu = Menu(menubar, tearoff=0, bg=WHITE, fg=DARK_COLOR)
tools_menu.add_command(label="Automatic", command=automatic_action)
tools_menu.add_command(label="Edit", command=edit_action)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Tools", menu=tools_menu)
root.config(menu=menubar)

# ------------------- Layout -------------------
frame = ttk.Frame(root, padding=20, style="TFrame")
frame.pack(expand=True)

result_label = ttk.Label(frame, text="Select a DEF file...")
result_label.grid(row=0, column=0, columnspan=2, pady=10)

ttk.Button(frame, text="Get Wiring", command=draw).grid(row=1, column=0, padx=10, pady=20)
ttk.Button(frame, text="Quit", command=root.quit).grid(row=1, column=1, padx=10, pady=20)

root.mainloop()
