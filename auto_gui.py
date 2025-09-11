import tkinter as tk
from tkinter import ttk
from dictionary import dataloggers, sensors2

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")
sensor_counter = 0

def open_selection_interface():
    global sensor_counter
    selection_list = {}

    top = tk.Toplevel()
    top.title("Select Datalogger and Sensor")
    top.geometry("800x800")
    top.configure(bg=DARK_COLOR)

    # --- Left and Right panels ---
    left_frame = tk.Frame(top, bg=DARK_COLOR)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    right_frame = tk.Frame(top, bg=DARK_COLOR)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- Datalogger Selection ---
    ttk.Label(left_frame, text="Select Datalogger:", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR).pack(anchor="w", pady=(0,5))
    datalogger_var = tk.StringVar(value=list(dataloggers.keys())[0])
    datalogger_menu = ttk.Combobox(left_frame, textvariable=datalogger_var, style="Custom.TCombobox",
                                   values=list(dataloggers.keys()), state="readonly")
    datalogger_menu.pack(anchor="w", pady=(0,10), fill="x")

    # --- Filter by Measurement ---
    ttk.Label(left_frame, text="Filter by Measurement:", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR).pack(anchor="w", pady=(0,5))
    measurement_var = tk.StringVar(value="All")
    measurements = ["All"] + sorted(list({s.get("measurement", "Unknown") for s in sensors2.values()}))
    measurement_menu = ttk.Combobox(left_frame, textvariable=measurement_var, values=measurements, state="readonly", style="Custom.TCombobox")
    measurement_menu.pack(anchor="w", pady=(0,10), fill="x")

    # --- Sensor Selection ---
    ttk.Label(left_frame, text="Select Sensor:", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR).pack(anchor="w", pady=(0,5))
    sensor_var = tk.StringVar()
    sensor_menu = ttk.Combobox(left_frame, textvariable=sensor_var, style="Custom.TCombobox", state="readonly")
    sensor_menu.pack(anchor="w", pady=(0,10), fill="x")

    # --- Protocol Selection ---
    ttk.Label(left_frame, text="Select Protocol:", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR).pack(anchor="w", pady=(0,5))
    protocol_var = tk.StringVar()
    protocol_menu = ttk.Combobox(left_frame, textvariable=protocol_var, state="readonly", style="Custom.TCombobox")
    protocol_menu.pack(anchor="w", pady=(0,10), fill="x")

    # --- Sensor Description ---
    description_text = tk.Text(left_frame, height=6, width=50, bg=DARK_COLOR, fg=WHITE)
    description_text.pack(anchor="w", pady=(5,10), fill="x")
    description_text.configure(state="disabled")

    def update_description(*args):
        sensor_key = sensor_var.get()
        description_text.configure(state="normal")
        description_text.delete("1.0", tk.END)
        if sensor_key in sensors2:
            s = sensors2[sensor_key]
            desc = f"ID: {sensor_key}\nName: {s.get('name', 'N/A')}\nModel: {s.get('model', 'N/A')}\nType: {s.get('type', 'N/A')}\nMeasurement: {s.get('measurement', 'N/A')}"
            description_text.insert(tk.END, desc)
        description_text.configure(state="disabled")

    sensor_var.trace_add("write", update_description)

    # --- Update sensor menu based on measurement filter ---
    def update_sensor_menu(*args):
        filtered_sensors = []
        for key, sensor in sensors2.items():
            sensor_measurement = sensor.get("measurement", "Unknown")
            if measurement_var.get() == "All" or sensor_measurement == measurement_var.get():
                filtered_sensors.append(key)
        sensor_menu["values"] = filtered_sensors
        if filtered_sensors:
            sensor_var.set(filtered_sensors[0])
        else:
            sensor_var.set("")
        update_protocol_menu()

    measurement_var.trace_add("write", update_sensor_menu)

    # --- Update protocol menu based on sensor selection ---
    def update_protocol_menu(*args):
        sensor_key = sensor_var.get()
        if sensor_key in sensors2:
            protocols = list(sensors2[sensor_key]["connection"].keys())
            protocol_menu["values"] = protocols
            protocol_var.set(protocols[0] if protocols else "")
        else:
            protocol_menu["values"] = []
            protocol_var.set("")

    sensor_var.trace_add("write", update_protocol_menu)

    # --- Right panel: selection list ---
    ttk.Label(right_frame, text="Selections:", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR).pack(anchor="w")
    selection_listbox = tk.Listbox(right_frame, height=25, width=40)
    selection_listbox.pack(anchor="w", pady=(5,10), fill="both", expand=True)

    # --- Add selection ---
    def add_selection():
        global sensor_counter
        sensor = str(sensor_counter) + "-" + sensor_var.get()
        protocol = protocol_var.get()
        if not sensor_var.get() or not protocol:
            return
        connections = sensors2[sensor_var.get()]["connection"][protocol]
        connections_format = {item[0]: item[1:] for item in connections}
        selection_list[sensor] = connections_format
        selection_listbox.insert(tk.END, f"{sensor} ({protocol})")
        sensor_counter += 1

    # --- Delete selected item ---
    def delete_selection():
        selected_indices = selection_listbox.curselection()
        for index in reversed(selected_indices):
            item_text = selection_listbox.get(index)
            key = item_text.split(" ")[0]
            if key in selection_list:
                del selection_list[key]
            selection_listbox.delete(index)

    # --- Buttons ---
    ttk.Button(left_frame, text="Add Selection", command=add_selection).pack(anchor="w", pady=5, fill="x")
    ttk.Button(left_frame, text="Delete Selected", command=delete_selection).pack(anchor="w", pady=5, fill="x")
    ttk.Button(left_frame, text="Save & Close", command=top.destroy).pack(anchor="w", pady=10, fill="x")

    top.grab_set()
    top.wait_window()
    return [datalogger_var.get(), selection_list]
