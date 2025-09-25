import tkinter as tk
from tkinter import ttk
from dictionary import dataloggers

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 10)

COLORS = ["Red", "Blue", "Green", "Black", "Gray", "Yellow", "Brown", "Orange", "White", "Purple", "Other"]


class EditFrame(ttk.Frame):
    def __init__(self, parent, controller, data, logger):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.result = {}
        self.configure(style="TFrame")

        sensor_var = tk.StringVar(value=list(data.keys())[0])
        self.entries = []

        ttk.Label(self, text="Select Sensor:").pack(pady=(15, 5))
        sensor_menu = ttk.Combobox(
            self, textvariable=sensor_var,
            values=list(data.keys()), state="readonly", width=30
        )
        sensor_menu.pack(pady=5)

        self.frame = ttk.Frame(self)
        self.frame.pack(pady=10, padx=10)

        def load_sensor():
            port_options = dataloggers[logger]["connection"]["ports"]
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.entries.clear()

            sensor = sensor_var.get()
            if not sensor:
                return

            port_color_map = data[sensor]
            for i, (port, color) in enumerate(port_color_map.items()):
                # Combobox for port type
                port_entry = ttk.Combobox(self.frame, values=port_options, width=15)
                port_entry.set(port)
                port_entry.bind("<<ComboboxSelected>>", lambda e: save_changes())
                port_entry.grid(row=i, column=0, padx=5, pady=2)

                # Combobox for color
                color_var = tk.StringVar(value=color)
                color_entry = ttk.Combobox(self.frame, values=COLORS, width=15)
                color_entry.set(color)
                color_entry.bind("<<ComboboxSelected>>", lambda e: save_changes())
                color_entry.grid(row=i, column=1, padx=5, pady=2)

                # Save references to both comboboxes
                self.entries.append((port_entry, color_entry))
            

        def save_changes():
            sensor = sensor_var.get()
            new_data = {}
            for port_entry, color_entry in self.entries:
                new_port = port_entry.get().strip()
                new_color = color_entry.get().strip()
                if new_port:
                    new_data[new_port] = new_color
            data[sensor] = new_data
            self.result.update(data)

        def done():
            save_changes()
            controller.draw()


        sensor_menu.bind("<<ComboboxSelected>>", lambda e: load_sensor())
        load_sensor()

        ttk.Button(self, text="Save Changes", command=done).pack(pady=15)
