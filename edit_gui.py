import tkinter as tk
from tkinter import ttk

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 10)
CABLE_TYPES = [
    "12V", "GND", "H", "L", "VX", "P", "C", "5V", "RG",
    "MicroSD", "12V+", "GND-", "Ground", "Ethernet", "RS232", "CSIO", "USB"
]

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
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.entries.clear()

            sensor = sensor_var.get()
            if not sensor:
                return

            port_color_map = data[sensor]
            for i, (port, color) in enumerate(port_color_map.items()):
                port_entry = ttk.Combobox(self.frame, values=CABLE_TYPES)
                port_entry.insert(0, port)
                port_entry.grid(row=i, column=0, padx=5, pady=2)

                color_var = tk.StringVar(value=color)
                color_entry = tk.Entry(
                    self.frame, textvariable=color_var,
                    state="readonly", width=20, font=FONT
                )
                color_entry.grid(row=i, column=1, padx=5, pady=2)

                self.entries.append((port_entry, color))

        def save_changes():
            sensor = sensor_var.get()
            new_data = {}
            for port_entry, color in self.entries:
                new_port = port_entry.get().strip()
                if new_port:
                    new_data[new_port] = color
            data[sensor] = new_data
            self.result.update(data)
            controller.draw()  # switch back to home frame

        sensor_menu.bind("<<ComboboxSelected>>", lambda e: load_sensor())
        load_sensor()

        ttk.Button(self, text="Save Changes", command=save_changes).pack(pady=15)
