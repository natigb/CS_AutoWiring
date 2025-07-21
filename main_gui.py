import tkinter as tk
from tkinter import filedialog, Menu
from wiring_functions import get_wiring_from_SC
from wiring_gui import draw_wiring_diagram_gui
from edit_gui import open_edit_interface
import os
import ast 

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
        #draw_wiring_diagram_gui(wiring[0], wiring[1])

def automatic_action():
    global wiring
    wiring = "auto function"
    result_label.config(text=wiring)

def edit_action():
    global wiring
    #data = ast.literal_eval(wiring[0])
    
    wiring[0] = open_edit_interface(wiring[0]) #fix here, returning none
    print(wiring)
    result_label.config(text=wiring)
def draw():
    global wiring
    print(wiring)
    draw_wiring_diagram_gui(wiring[0], wiring[1])

# Main window
root = tk.Tk()
root.title("Wiring Tool")
root.geometry("400x200")

# Menu bar
menubar = Menu(root)

# File menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Open from ShortCut", command=choose_def_file)
menubar.add_cascade(label="File", menu=file_menu)

# Tools menu
tools_menu = Menu(menubar, tearoff=0)
tools_menu.add_command(label="Automatic", command=automatic_action)
tools_menu.add_command(label="Edit", command=edit_action)
menubar.add_cascade(label="Tools", menu=tools_menu)

# Attach menu bar to root
root.config(menu=menubar)

# Result label
result_label = tk.Label(root, text="", fg="blue")
result_label.pack(pady=60)

tk.Button(root, text="Get Wiring", command= draw).pack(padx=20, pady=20)
root.mainloop()
