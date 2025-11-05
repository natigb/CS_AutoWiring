import re
from collections import defaultdict

count_gnd = 0
count_g = 0
def normalize_port_name(port):
    """
    The `normalize_port_name` function in Python normalizes port names based on specific rules and
    patterns.
    
    :param port: The `normalize_port_name` function takes a port name as input and normalizes it
    according to specific rules. The function handles different types of port names and formats them in
    a standardized way
    :return: The `normalize_port_name` function takes a port name as input, normalizes it according to
    specific rules, and returns the normalized port name. If the input port matches any of the defined
    patterns, it will be transformed accordingly (e.g., "GND" becomes "GND_1", "G" becomes "G_1", "VX1"
    becomes "VX_1
    """
    global count_gnd, count_g
    port = port.strip()
    # Mapping and ID of ports
    # GND or Ground
    if port.upper() in ["GROUND", "GND"]:
        count_gnd +=1
        return f"GND_{count_gnd}"

    # G becomes G_#
    elif port == "G":
        count_g+=1
        return f"G_{count_g}"

    # VX1 → VX_1, P1 → P_1, C1 → C_1, RG1 → RG_1
    match = re.match(r"^(VX|P|C|RG)(\d+)$", port)
    if match:
        return f"{match.group(1)}_{match.group(2)}"

    # 1H → H_1, 2L → L_1 
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
    """
    The function `get_wiring_from_SC` reads a .DEF Short Cut file to extract wiring information for sensors and returns
    the wiring dictionary along with an image name.
    
    :param filename: The function `get_wiring_from_SC` reads a file specified by the `filename`
    parameter and extracts wiring information for sensors from it. The function parses the file line by
    line to identify sensor names, port connections, and wire colors. It then organizes this information
    into a dictionary format and returns
    :return: The function `get_wiring_from_SC` returns a list containing two elements: 
    1. A dictionary `wiring` that represents the wiring information extracted from the input file.
    2. A string `image_name` that specifies the image file name associated with the wiring information.
    """
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
                normalized_port = normalize_port_name(port)
                wiring[current_sensor][normalized_port] = color

            else:
                current_sensor = str(sensor_counter)+"-"+line.split(" (")[0].strip()
                wiring[current_sensor] = {}
                ground_counter[current_sensor] = 1
                g_counter[current_sensor] = 1
                sensor_counter+=1
    
    return [wiring, image_name]


def get_auto_wiring(datalogger_ports, sensors):
    """
    The function `get_auto_wiring` assigns available ports to sensors based on color and returns a
    dictionary representing the wiring configuration.
    
    :param datalogger_ports: The `datalogger_ports` parameter is a dictionary that contains information
    about available ports on a data logger device. The keys in the dictionary represent the port
    numbers, and the values represent the status of each port (e.g., available, in use)
    :param sensors: The `sensors` parameter in the `get_auto_wiring` function is a dictionary that
    contains sensor names as keys and a nested dictionary as values. The nested dictionary contains
    colors as keys and a list of ports as values
    :return: The function `get_auto_wiring` returns a dictionary representing the wiring connections
    between sensors and data logger ports. Each sensor is mapped to a dictionary where the keys are the
    data logger ports and the values are the corresponding colors of the sensor wires connected to those
    ports.
    """
    
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
    """
    The function `get_port_type` extracts the type of a port from its name by splitting the name at the
    underscore character and returning the first part.
    
    :param port: The function `get_port_type` takes a `port` as input and returns the type of the port.
    The type is determined by splitting the port name at the underscore character and returning the
    first part of the split
    :return: The function `get_port_type` takes a string `port` as input and returns the part of the
    string before the underscore character.
    """
    return port.split("_")[0]

def find_port_match_index(port_list, port):
    """
    The function `find_port_match_index` searches for a specific port in a list and returns the index of
    the first matching port type, or -1 if not found.
    
    :param port_list: A list of ports to search through
    :param port: The `port` parameter in the `find_port_match_index` function is the port type that you
    are searching for within the `port_list`. The function iterates through the `port_list` and checks
    if the port type of each element matches the specified `port`. If a match is found,
    :return: The function `find_port_match_index` returns the index of the first occurrence of a port in
    the `port_list` that matches the given `port`. If no match is found, it returns -1.
    """
    for i in range(0, len(port_list)):

        if(get_port_type(port_list[i]) == port):
            return i
        
    return -1