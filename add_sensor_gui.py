import tkinter as tk
from tkinter import ttk, messagebox

DICT_FILE = "dictionary.py"
COLORS = ["Red", "Blue", "Green", "Black", "Gray", "Yellow", "Brown", "Orange", "White", "Purple", "Other"]
CABLE_TYPES = ["12V", "GND", "H", "L", "VX", "P", "C", "5V", "RG", "MicroSD", "12V+", "GND-", "Ground", "Ethernet", "RS232", "CSIO", "USB"]
PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")

def open_add_sensor_interface():
    top = tk.Toplevel()
    top.title("Add New Sensor")
    top.geometry("600x800")
    top.configure(bg=WHITE)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=WHITE)
    style.configure("TLabel", background=WHITE, foreground=DARK_COLOR, font=FONT)
    style.configure("TEntry", font=FONT)
    style.configure("TCombobox", padding=5, font=FONT)
    style.configure("TButton", background=PRIMARY_COLOR, foreground=DARK_COLOR, font=FONT)

    # --- Sensor basic info ---
    ttk.Label(top, text="Sensor Key (ID)").pack(fill="x")
    key_entry = tk.Entry(top)
    key_entry.pack(fill="x", padx=10, pady=5)

    ttk.Label(top, text="Name").pack(fill="x")
    name_entry = tk.Entry(top)
    name_entry.pack(fill="x", padx=10, pady=5)

    ttk.Label(top, text="Measurement").pack(fill="x")
    meas_entry = tk.Entry(top)
    meas_entry.pack(fill="x", padx=10, pady=5)

    ttk.Label(top, text="Model").pack(fill="x")
    model_entry = tk.Entry(top)
    model_entry.pack(fill="x", padx=10, pady=5)

    ttk.Label(top, text="Type").pack(fill="x")
    type_combo = ttk.Combobox(top, values=["digital", "analog"])
    type_combo.pack(fill="x", padx=10, pady=5)

    # --- Protocols ---
    ttk.Label(top, text="Protocols").pack(fill="x")
    protocols_frame = tk.Frame(top)
    protocols_frame.pack(fill="both", expand=True, padx=10, pady=10)

    protocol_blocks = []

    def add_protocol_block():
        block = tk.Frame(protocols_frame, bd=2, relief="groove", pady=5)
        block.pack(fill="x", pady=5)

        tk.Label(block, text="Protocol Name").pack()
        proto_name = ttk.Combobox(block, values=["SDI-12", "RS-232", "RS-485", "Pulse", "Control", "4-wire", "2-wire", "Default", "SE-Measurement", "Diff-Measurement"])
        proto_name.set("-Choose protocol-")
        proto_name.pack(fill="x", padx=5, pady=2)

        wires_frame = tk.Frame(block)
        wires_frame.pack(fill="x", padx=5, pady=5)
        wires = []

        def add_wire_row():
            row = tk.Frame(wires_frame)
            row.pack(fill="x", pady=2)
            color_e = ttk.Combobox(row, values=COLORS, width=12)
            color_e.set("-Cable color-")
            color_e.pack(side="left", padx=2)
            port_e = ttk.Combobox(row, values=CABLE_TYPES, width=12)
            port_e.set("-Port 1-")
            port_e.pack(side="left", padx=2)
            pin_e = ttk.Combobox(row, values=CABLE_TYPES, width=12)
            pin_e.pack(side="left", padx=2)
            pin3_e = ttk.Combobox(row, values=CABLE_TYPES, width=12)
            pin3_e.pack(side="left", padx=2)
            wires.append((color_e, port_e, pin_e, pin3_e))

        ttk.Button(block, text="Add Wire", command=add_wire_row).pack(pady=2)
        add_wire_row()  # start with one wire
        protocol_blocks.append((proto_name, wires))

    ttk.Button(top, text="Add Protocol", command=add_protocol_block).pack(pady=5)
    add_protocol_block()  # start with one protocol

    # --- Save function ---
    def save_sensor():
        key = key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Sensor Key (ID) required")
            return

        # Build the sensor dictionary string
        sensor_lines = []
        sensor_lines.append(f'    "{key}": {{')
        sensor_lines.append(f'        "name": "{name_entry.get().strip()}",')
        sensor_lines.append(f'        "measurement": "{meas_entry.get().strip()}",')
        sensor_lines.append(f'        "model": "{model_entry.get().strip()}",')
        sensor_lines.append(f'        "type": "{type_combo.get().strip()}",')
        sensor_lines.append(f'        "connection": {{')

        for proto_name, wires in protocol_blocks:
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

        # Find the last line with the closing '}' of sensors2 dictionary
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

        
        top.destroy()

    ttk.Button(top, text="Save Sensor", command=save_sensor).pack(pady=10)
