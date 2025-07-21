import tkinter as tk
from tkinter import ttk


def open_edit_interface(data):
    result = {}  # Will hold the updated data

    editor = tk.Toplevel()
    editor.title("Edit Wiring")
    editor.geometry("400x300")

    sensor_var = tk.StringVar(value=list(data.keys())[0])
    entries = []

    # Dropdown to select sensor
    sensor_menu = ttk.Combobox(editor, textvariable=sensor_var, values=list(data.keys()), state="readonly")
    sensor_menu.pack(pady=10)

    frame = tk.Frame(editor)
    frame.pack(pady=10)

    def load_sensor():
        for widget in frame.winfo_children():
            widget.destroy()
        entries.clear()

        sensor = sensor_var.get()
        if not sensor:
            return

        port_color_map = data[sensor]
        for i, (port, color) in enumerate(port_color_map.items()):
            port_entry = tk.Entry(frame, width=20)
            port_entry.insert(0, port)
            port_entry.grid(row=i, column=0, padx=5, pady=2)

            color_var = tk.StringVar(value=color)
            color_entry = tk.Entry(frame, textvariable=color_var, state="readonly", width=20)
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

    tk.Button(editor, text="Save Changes", command=save_changes).pack(pady=10)

    editor.grab_set()
    editor.wait_window()  # Wait for window to close

    return result
