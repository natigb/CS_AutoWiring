import tkinter as tk
from tkinter import ttk, messagebox

DICT_FILE = "dictionary.py"
COLORS = ["Red", "Blue", "Green", "Black", "Gray", "Yellow", "Brown", "Orange", "White", "Purple", "Other"]
CABLE_TYPES = ["12V", "GND", "H", "L", "VX", "P", "C", "5V", "RG", "MicroSD", "12V+", "GND-", "Ground", "Ethernet", "RS232", "CSIO", "USB"]
MEASUREMENT_TYPE = ["analog", "digital", "power", "other"]
MEASUREMENT = ["rain", "baro_pressure", "all", "temperature", "humidity", "wind"]

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")


class AddSensorFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")

        # --- Scrollable area ---
        canvas = tk.Canvas(self, bg=WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=WHITE)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Sensor basic info ---
        ttk.Label(scroll_frame, text="Sensor Key (ID)").pack(fill="x")
        self.key_entry = tk.Entry(scroll_frame)
        self.key_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(scroll_frame, text="Name").pack(fill="x")
        self.name_entry = tk.Entry(scroll_frame)
        self.name_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(scroll_frame, text="Measurement").pack(fill="x")
        self.meas_combo = ttk.Combobox(scroll_frame, values=MEASUREMENT)
        self.meas_combo.pack(fill="x", padx=10, pady=5)

        ttk.Label(scroll_frame, text="Model").pack(fill="x")
        self.model_entry = tk.Entry(scroll_frame)
        self.model_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(scroll_frame, text="Type").pack(fill="x")
        self.type_combo = ttk.Combobox(scroll_frame, values=MEASUREMENT_TYPE)
        self.type_combo.set("digital")  # default value
        self.type_combo.pack(fill="x", padx=10, pady=5)

        # --- Protocols ---
        ttk.Label(scroll_frame, text="Protocols").pack(fill="x")
        self.protocols_frame = tk.Frame(scroll_frame, bg=WHITE)
        self.protocols_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.protocol_blocks = []

        def add_protocol_block():
            block = tk.Frame(self.protocols_frame, bd=2, relief="groove", pady=5, bg=WHITE)
            block.pack(fill="x", pady=5)

            tk.Label(block, text="Protocol Name", bg=WHITE).pack()
            proto_name = ttk.Combobox(
                block,
                values=[
                    "SDI-12", "RS-232", "RS-485", "Pulse", "Control",
                    "4-wire", "2-wire", "Default", "SE-Measurement", "Diff-Measurement"
                ]
            )
            proto_name.set("SDI-12")  # default protocol
            proto_name.pack(fill="x", padx=5, pady=2)

            wires_frame = tk.Frame(block, bg=WHITE)
            wires_frame.pack(fill="x", padx=5, pady=5)
            wires = []

            def add_wire_row():
                row = tk.Frame(wires_frame, bg=WHITE)
                row.pack(fill="x", pady=2)
                color_e = ttk.Combobox(row, values=COLORS, width=12)
                color_e.set("Red")
                color_e.pack(side="left", padx=2)
                port_e = ttk.Combobox(row, values=CABLE_TYPES, width=12)
                port_e.set("12V")
                port_e.pack(side="left", padx=2)
                pin_e = ttk.Combobox(row, values=CABLE_TYPES, width=12)
                pin_e.pack(side="left", padx=2)
                pin3_e = ttk.Combobox(row, values=CABLE_TYPES, width=12)
                pin3_e.pack(side="left", padx=2)
                wires.append((color_e, port_e, pin_e, pin3_e))

            ttk.Button(block, text="Add Wire", command=add_wire_row).pack(pady=2)
            add_wire_row()  # start with one wire
            self.protocol_blocks.append((proto_name, wires))

        ttk.Button(scroll_frame, text="Add Protocol", command=add_protocol_block).pack(pady=5)
        add_protocol_block()

        # --- Save button ---
        ttk.Button(scroll_frame, text="Save Sensor", command=self.save_sensor).pack(pady=10)

    def save_sensor(self):
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Sensor Key (ID) required")
            return

        sensor_lines = []
        sensor_lines.append(f'    "{key}": {{')
        sensor_lines.append(f'        "name": "{self.name_entry.get().strip()}",')
        sensor_lines.append(f'        "measurement": "{self.meas_combo.get().strip()}",')
        sensor_lines.append(f'        "model": "{self.model_entry.get().strip()}",')
        sensor_lines.append(f'        "type": "{self.type_combo.get().strip()}",')
        sensor_lines.append(f'        "connection": {{')

        for proto_name, wires in self.protocol_blocks:
            proto_val = proto_name.get().strip()
            if not proto_val:
                continue
            sensor_lines.append(f'            "{proto_val}": [')
            for c, p, pin, pin3 in wires:
                color = c.get().strip()
                port = p.get().strip()
                pinv = pin.get().strip()
                pin3v = pin3.get().strip()
                if color and port:
                    if pinv:
                        if pin3v:
                            sensor_lines.append(f'                ("{color}", "{port}", "{pinv}", "{pin3v}"),')
                        else:
                            sensor_lines.append(f'                ("{color}", "{port}", "{pinv}"),')
                    else:
                        sensor_lines.append(f'                ("{color}", "{port}"),')
            sensor_lines.append("            ],")
        sensor_lines.append("        }")
        sensor_lines.append("    },\n")

        # Append to dictionary.py inside sensors2
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i in reversed(range(len(lines))):
            if lines[i].strip() == "}":
                insert_index = i
                break
        else:
            messagebox.showerror("Error", "Could not find end of sensors2 dictionary")
            return

        lines.insert(insert_index, "\n".join(sensor_lines))

        with open(DICT_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

        messagebox.showinfo("Saved", f"Sensor {key} appended successfully.")
        self.controller.show_home()
