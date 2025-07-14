import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

from ports_coordenates import logger_ports  



# -----------------------------------------------------------
#  Convenience: colour palette for common wire colours
# -----------------------------------------------------------
WIRE_COLORS = {
    "Black": "#000000",
    "White": "#ffffff",
    "Red": "#ff0000",
    "Blue": "#0000ff",
    "Green": "#008000",
    "Yellow": "#ffff00",
    "Brown": "#8b4513",
    "Clear": "#aaaaaa"  # transparent/silver screen — show as grey
}


class WiringDiagramGUI(tk.Tk):
    """Tkinter application that draws a wiring diagram given a mapping"""

    SENSOR_X_OFFSET = 30      # x position of sensor labels
    SENSOR_SPACING = 30       # vertical spacing between sensors

    def __init__(self, wiring: dict, datalogger_image: str = "cr1000xe.png"):
        super().__init__()
        self.title("Wiring Diagram")
        self.resizable(False, False)

        # Load datalogger image
        image_path = Path(datalogger_image)
        if not image_path.exists():
            raise FileNotFoundError(image_path)

        pil_img = Image.open(image_path)
        self.logger_im = ImageTk.PhotoImage(pil_img)

        width, height = pil_img.size
        canvas_width = width + 300  # Extra space on left for sensor list
        canvas_height = max(height, len(wiring) * self.SENSOR_SPACING + 40)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Draw the logger image
        self.canvas.create_image(300, 20, anchor="nw", image=self.logger_im)

        # Draw sensors and connections
        self._draw_sensors_and_wires(wiring, datalogger_image)

    # ------------------------------------------------------------------
    #  Helper methods
    # ------------------------------------------------------------------
    def _draw_sensors_and_wires(self, wiring: dict, image_name: str):
        ports = logger_ports[image_name]
        y_current = 40
        self.canvas.create_text(10, 15, anchor="w", text="Sensors", font=("Helvetica", 12, "bold"))

        for sensor, connections in wiring.items():
            # Draw sensor label
            self.canvas.create_text(self.SENSOR_X_OFFSET, y_current, anchor="w", text=sensor, font=("Helvetica", 10, "bold"))
            sensor_anchor = (self.SENSOR_X_OFFSET + 100, y_current)

            # For each connection draw a line from sensor anchor to logger port
            for port_name, wire_color in connections.items():
                if port_name not in ports:
                    print(f"Warning: port '{port_name}' not found in logger definition. Skipping.")
                    continue
                port_coords = ports[port_name]
                color = WIRE_COLORS.get(wire_color, "#888888")

                # Draw the wire (straight horizontal then vertical)
                x1, y1 = sensor_anchor
                x2, y2 = port_coords[0] + 300, port_coords[1] + 20  # account for image offset
                mid_x = (x1 + x2) / 2

                # polyline with two segments: sensor->mid, mid->port
                self.canvas.create_line(x1, y1, mid_x, y1, fill=color, width=2)
                self.canvas.create_line(mid_x, y1, mid_x, y2, fill=color, width=2)
                self.canvas.create_line(mid_x, y2, x2, y2, fill=color, width=2)

                # Small dot at port
                self.canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3, fill=color, outline=color)

            y_current += self.SENSOR_SPACING


# ----------------------------------------------------------------------
#  Public API function
# ----------------------------------------------------------------------

def draw_wiring_diagram_gui(wiring: dict, datalogger_image: str = "cr1000xe.png"):
    """Entry point to launch the wiring diagram GUI.

    Parameters
    ----------
    wiring : dict
        Dictionary of {sensor_name: {port_name: wire_colour, ...}, ...}
    datalogger_image : str
        Filename of the datalogger PNG (must match an entry in logger_ports)
    """
    app = WiringDiagramGUI(wiring, datalogger_image)
    app.mainloop()
