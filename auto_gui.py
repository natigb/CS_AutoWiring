import tkinter as tk
from tkinter import ttk
from dictionary import dataloggers, sensors2
# Dataloggers and sensors definitions (paste your full data here)
PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")
sensor_counter=0
def open_selection_interface():
    selection_list = {}
    top = tk.Toplevel()
    top.title("Select Datalogger and Sensor")
    top.geometry("650x750")
    top.configure(bg=DARK_COLOR)
    
    # Datalogger Selection
    ttk.Label(top, text="Select Datalogger:", font=FONT, background=DARK_COLOR, foreground=PRIMARY_COLOR).pack(pady=(10, 0))
    datalogger_var = tk.StringVar(value=list(dataloggers.keys())[0])
    datalogger_menu = ttk.Combobox(top, textvariable=datalogger_var, style="Custom.TCombobox", values=list(dataloggers.keys()), state="readonly")
    datalogger_menu.pack(pady=5)

    # Sensor Selection
    ttk.Label(top, text="Select Sensor:").pack(pady=(10, 0))
    sensor_var = tk.StringVar(value=list(sensors2.keys())[0])
    sensor_menu = ttk.Combobox(top, textvariable=sensor_var, style="Custom.TCombobox", values=list(sensors2.keys()), state="readonly")
    sensor_menu.pack(pady=5)

    # Protocol selection
    ttk.Label(top, text="Select Protocol:").pack(pady=(10, 0))
    protocol_var = tk.StringVar()
    protocol_menu = ttk.Combobox(top, textvariable=protocol_var, state="readonly",style="Custom.TCombobox")
    protocol_menu.pack(pady=5)

    def update_protocol_menu(*args):
        sensor_key = sensor_var.get()
        if sensor_key in sensors2:
            protocols = list(sensors2[sensor_key]["connection"].keys())
            protocol_menu["values"] = protocols
            protocol_var.set(protocols[0] if protocols else "")

    sensor_var.trace_add("write", update_protocol_menu)
    update_protocol_menu()

    # Display selection list
    ttk.Label(top, text="Selections:").pack(pady=(15, 0))
    display_box = tk.Text(top, height=10, width=60)
    display_box.pack()

    def add_selection():
        global sensor_counter
        sensor = str(sensor_counter)+"-"+sensor_var.get()
        protocol = protocol_var.get()
        connections = sensors2[sensor_var.get()]["connection"][protocol]
        datalogger = datalogger_var.get()

        connections_format={}
        for item in connections:
            connections_format[item[0]]=item[1:]
            
        selection_list[sensor]= connections_format
        #selection_list.append(selection)
        sensor_counter+=1   
        display_box.insert(tk.END, f"{sensor} ({protocol}) on {datalogger}\n")

    def save_selections():
        #fromato de sensores y datalogger

        top.destroy()
 
    # Add and Save buttons
    ttk.Button(top, text="Add Selection", command=add_selection).pack(pady=5)
    ttk.Button(top, text="Save", command=save_selections).pack(pady=(5, 15))
    #print("ddd")
    top.grab_set()
    top.wait_window() 
    return [datalogger_var.get(), selection_list]


# # Main window (for testing)
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Main Window")
#     root.geometry("300x200")
#     selection = open_selection_interface()
#     #ttk.Button(root, text="Open Selection Interface", command=open_selection_interface).pack(pady=50)
#     print(selection)
#     root.mainloop()
