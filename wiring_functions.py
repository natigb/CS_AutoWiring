import re

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
    image_name = "notfound.png"
    start_flag = True
    with open(filename, "r", encoding="latin-1") as f:
        lines = f.readlines()

    in_wiring_section = False
    for line in lines:
        line = line.strip()

        if "-Cableado para" in line and start_flag:
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
                current_sensor = line.split(" (")[0].strip()
                wiring[current_sensor] = {}
                ground_counter[current_sensor] = 1
                g_counter[current_sensor] = 1

    return [wiring, image_name]



def get_auto_wiring(datalogger, sensors):
    from copy import deepcopy

    # Make a modifiable copy of available ports
    available_ports = deepcopy(datalogger["connection"]["ports"])
    used_ports = set()

    def find_and_assign(protocol_wires, allow_shared_sdi=False):
        assigned = {}
        temp_used = set()

        for wire in protocol_wires:
            color = wire[0]
            candidates = wire[1:]

            port_found = False
            for port_type in candidates:
                for port in available_ports:
                    if port_type in port:
                        # Shared allowed only for SDI-12-type ports
                        if port not in used_ports or (allow_shared_sdi and "SDI" in port_type):
                            assigned[port] = color
                            if not (allow_shared_sdi and "SDI" in port_type):
                                temp_used.add(port)
                            port_found = True
                            break
                if port_found:
                    break

            if not port_found:
                return None  # Protocol failed: some wire has no available port

        used_ports.update(temp_used)
        return assigned

    wiring = {}

    for sensor_name, sensor in sensors.items():
        protocols = sensor["connection"]

        for protocol_name, protocol_wires in protocols.items():
            allow_shared = protocol_name == "SDI-12"
            assignment = find_and_assign(protocol_wires, allow_shared_sdi=allow_shared)
            if assignment:
                wiring[sensor_name] = assignment
                break  # Use only first successful protocol

    return wiring
