def get_wiring(datalogger, sensors):
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
