import re

# def get_wiring(datalogger, sensors):
#     from copy import deepcopy

   
#     available_ports = deepcopy(datalogger["connection"]["ports"])
#     used_ports = set()
#     print(sensors)
#     wiring = {}
#     # Ir conectando cada sensor
#     for sensor_name, sensor in sensors.items():

#         print("--------------")
#         print(sensor_name)
#         print(sensor)
#         print("--------------")

#     #print(available_ports)

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

    # Return as-is
    return port


def get_wiring_from_SC(filename):
    wiring = {}
    current_sensor = None
    ground_counter = {}
    g_counter = {}

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_wiring_section = False
    for line in lines:
        line = line.strip()

        if "-Cableado para" in line:
            in_wiring_section = True
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
                current_sensor = line.split(" (")[0].strip()
                wiring[current_sensor] = {}
                ground_counter[current_sensor] = 1
                g_counter[current_sensor] = 1

    return wiring
