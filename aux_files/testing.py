from dictionary import sensors
from ports_coordenates import logger_ports
from wiring_functions import get_wiring_from_SC, get_auto_wiring
from wiring_gui import draw_wiring_diagram_gui

#wiring = get_wiring(dataloggers["CR100Xe"], sensors)
wiring = get_auto_wiring(logger_ports["img/cr1000x.png"], sensors)
print(wiring)

