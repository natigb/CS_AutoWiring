import re
from collections import defaultdict

count_gnd = 0
count_g = 0
def normalize_port_name(port, ground_counter, g_counter, sensor):
    global count_gnd, count_g
    port = port.strip()

    # GND or Ground
    if port.upper() in ["GROUND", "GND"]:
        #count = ground_counter.setdefault(sensor, 1)
        #print(count)
        #ground_counter[sensor] += 1
        count_gnd +=1
        return f"GND_{count_gnd}"

    # G becomes G_#
    elif port == "G":
        #count = g_counter.setdefault(sensor, 1)
        #g_counter[sensor] += 1
        count_g+=1
        return f"G_{count_g}"

    # VX1 → VX_1, P1 → P_1, C1 → C_1, RG1 → RG_1
    match = re.match(r"^(VX|P|C|RG)(\d+)$", port)
    if match:
        return f"{match.group(1)}_{match.group(2)}"

    # 1H → H_1, 2L → L_1 (simple format)
    match_hl = re.match(r"^(\d+)([HLhl])$", port)
    if match_hl:
        num = match_hl.group(1)
        side = match_hl.group(2).upper()
        return f"{side}_{num}"

    # C3 → C_3
    match_generic = re.match(r"^([A-Za-z]+)(\d+)$", port)
    if match_generic:
        return f"{match_generic.group(1)}_{match_generic.group(2)}"
    
    # SW12V → SW_12
    match_sw = re.match(r"^(SW)(\d+)[A-Za-z]?$", port)
    if match_sw:
        return f"{match_sw.group(1)}_{match_sw.group(2)}"

    # Return as-is
    return port


def get_wiring_from_SC(filename):
    global count_gnd
    global count_g
    count_gnd = 0
    count_g = 0
    wiring = {}
    current_sensor = None
    ground_counter = {}
    g_counter = {}
    sensor_counter = 0
    image_name = "notfound.png"
    start_flag = True
    with open(filename, "r", encoding="latin-1") as f:
        lines = f.readlines()

    in_wiring_section = False
    for line in lines:
        line = line.strip()

        if ("-Cableado para" or "-Wiring for") in line and start_flag:
            image_name = "img/"+line.split(" ")[2].strip("-").lower()+".png"
            in_wiring_section = True
            start_flag = False
            continue
        if in_wiring_section and line.startswith("-Measurement"):
            break

        if in_wiring_section:
            if not line:
                continue

            if ":" in line and current_sensor:
                port, color = map(str.strip, line.split(":", 1))
                color = color.split('(')[0].strip()
                normalized_port = normalize_port_name(port, ground_counter, g_counter, current_sensor)
                wiring[current_sensor][normalized_port] = color

            else:
                current_sensor = str(sensor_counter)+"-"+line.split(" (")[0].strip()
                wiring[current_sensor] = {}
                ground_counter[current_sensor] = 1
                g_counter[current_sensor] = 1
                sensor_counter+=1
    
    return [wiring, image_name]

#
def get_auto_wiring(datalogger_ports, sensors):
    
    available_ports = list(datalogger_ports.keys())[1:]
    wiring = {}
    for sensor_name in sensors:
        object = {sensor_name:{}}
        for color in sensors[sensor_name]:
            dl_port = "no ports left"
            ports = sensors[sensor_name][color]
            for port in ports:
                port_index= find_port_match_index(available_ports, port)
                if port_index != -1:
                    dl_port = available_ports[port_index]
                    available_ports.pop(port_index)
                    break
                else:
                    dl_port = port +  " (unavailable): " + color
            object[sensor_name].update({dl_port : color})   
        wiring.update(object)
    
    return wiring

def get_port_type(port):
    return port.split("_")[0]

def find_port_match_index(port_list, port):
    for i in range(0, len(port_list)):

        if(get_port_type(port_list[i]) == port):
            #print(str(i) + ":" + port_list[i] + "-" + port)
            return i
        
    return -1