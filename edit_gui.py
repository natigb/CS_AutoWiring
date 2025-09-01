import tkinter as tk
from tkinter import ttk

# Estilos de colores y fuente
PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 10)
CABLE_TYPES = ["12V", "GND", "H", "L", "VX", "P", "C", "5V", "RG", "MicroSD", "12V+", "GND-", "Ground", "Ethernet", "RS232", "CSIO", "USB"]

def open_edit_interface(data):
    result = {}  # Will hold the updated data

    editor = tk.Toplevel()
    editor.title("Edit Wiring")
    editor.geometry("450x750")
    editor.configure(bg=WHITE)

    # Estilo visual
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=WHITE)
    style.configure("TLabel", background=WHITE, foreground=DARK_COLOR, font=FONT)
    style.configure("TEntry", font=FONT)
    style.configure("TCombobox", padding=5, font=FONT)
    style.configure("TButton", background=PRIMARY_COLOR, foreground=DARK_COLOR, font=FONT)

    sensor_var = tk.StringVar(value=list(data.keys())[0])
    entries = []

    # Dropdown to select sensor
    ttk.Label(editor, text="Select Sensor:").pack(pady=(15, 5))
    sensor_menu = ttk.Combobox(
        editor, textvariable=sensor_var, values=list(data.keys()), state="readonly", width=30
    )
    sensor_menu.pack(pady=5)

    frame = ttk.Frame(editor)
    frame.pack(pady=10, padx=10)

    def load_sensor():
        for widget in frame.winfo_children():
            widget.destroy()
        entries.clear()

        sensor = sensor_var.get()
        if not sensor:
            return

        port_color_map = data[sensor]
        for i, (port, color) in enumerate(port_color_map.items()):
            port_entry = ttk.Combobox(frame, values=CABLE_TYPES)
            port_entry.insert(0, port)
            port_entry.grid(row=i, column=0, padx=5, pady=2)

            color_var = tk.StringVar(value=color)
            color_entry = tk.Entry(frame, textvariable=color_var, state="readonly", width=20, font=FONT)
            color_entry.grid(row=i, column=1, padx=5, pady=2)

            entries.append((port_entry, color))

    def save_changes():
        sensor = sensor_var.get()
        new_data = {}
        for port_entry, color in entries:
            new_port = port_entry.get().strip()
            if new_port:
                new_data[new_port] = color
        data[sensor] = new_data
        result.update(data)  # Update result
        editor.destroy()

    sensor_menu.bind("<<ComboboxSelected>>", lambda e: load_sensor())
    load_sensor()

    ttk.Button(editor, text="Save Changes", command=save_changes).pack(pady=15)

    editor.grab_set()
    editor.wait_window()  # Wait for window to close

    return result
