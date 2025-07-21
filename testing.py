from dictionary import dataloggers, sensors
from wiring_functions import get_wiring_from_SC
from wiring_gui import draw_wiring_diagram_gui

#wiring = get_wiring(dataloggers["CR100Xe"], sensors)
wiring = get_wiring_from_SC("C:/Users/NataliaGonzalezBermu/Documents/shortcut/tets.DEF")
print(wiring)
draw_wiring_diagram_gui(wiring[0], wiring[1])
wiring = get_wiring_from_SC("C:/Users/NataliaGonzalezBermu/Documents/shortcut/cr6test.DEF")
print(wiring)
draw_wiring_diagram_gui(wiring[0], wiring[1])
wiring = get_wiring_from_SC("C:/Users/NataliaGonzalezBermu/Documents/shortcut/cr350test.DEF")
print(wiring)
draw_wiring_diagram_gui(wiring[0], wiring[1])
