import tkinter as tk
from tkinter import ttk, Canvas, filedialog
from PIL import Image, ImageTk
from ports_coordenates import logger_ports
import io
import ast

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")

class WiringFrame(ttk.Frame):
    def __init__(self, parent, controller, wiring, datalogger_image):
        super().__init__(parent, style="Right.TFrame")
        self.controller = controller
        self.wiring = wiring
        self.datalogger_image = datalogger_image
        self.canvas_width = 1700
        self.canvas_height = 900

        # --- Scrollable canvas setup (hidden scrollbars) ---
        self.canvas = Canvas(self, bg=WHITE, highlightthickness=0,
                             width=self.canvas_width-100, height=500,
                             scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame
        self.inner = ttk.Frame(self.canvas, style="Right.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # Update scrollregion whenever inner frame changes
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # --- Mouse wheel scrolling ---
        def _on_mousewheel(event):
            if event.state & 0x0001:  # Shift key pressed -> horizontal scroll
                self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            else:  # Vertical scroll
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows / Mac
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux up
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux down

        # --- Drawing canvas inside inner frame ---
        self.drawing = Canvas(self.inner, width=self.canvas_width, height=self.canvas_height,
                              bg=WHITE, highlightthickness=0)
        self.drawing.pack()

        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.logger_width = logger_ports[datalogger_image]["image"][0]
        self.logger_height = logger_ports[datalogger_image]["image"][1]

        # Load logger image or placeholder
        try:
            image = Image.open(datalogger_image).resize((self.logger_width, self.logger_height))
            self.logger_img = ImageTk.PhotoImage(image)
            self.drawing.create_image(self.center_x, self.center_y, image=self.logger_img)
        except FileNotFoundError:
            self.drawing.create_rectangle(self.center_x - 100, self.center_y - 100,
                                          self.center_x + 100, self.center_y + 100,
                                          outline="black", fill="#eee")
            self.drawing.create_text(self.center_x, self.center_y, text="CR1000X", font=("Arial", 14))

        # Data structures
        self.sensor_positions = {}
        self.sensor_items = {}
        self.wire_items = {}

        self._layout_sensors()
        self._draw_all_wires()

        # Dragging
        self.drag_data = {"sensor": None, "x": 0, "y": 0}
        self.drawing.bind("<ButtonPress-1>", self.on_press)
        self.drawing.bind("<B1-Motion>", self.on_drag)
        self.drawing.bind("<ButtonRelease-1>", self.on_release)

        # Right-click save
        self.drawing.bind("<Button-3>", self.save_canvas)

    # --- Layout sensors ---
    def _layout_sensors(self):
        """
        The `_layout_sensors` function positions sensors on a canvas based on specified coordinates
        and ensures that the sensor rectangles stay within canvas bounds.
        """
        left_x = 100
        right_x = self.canvas_width - 100  # adjust based on canvas width
        spacing_y = 150
        top_margin = 80

        for i, sensor in enumerate(self.wiring):
            side = "left" if i % 2 == 0 else "right"

            # Initial placement
            y = top_margin + (i // 2) * spacing_y + (4 * i)
            x = left_x if side == "left" else right_x

            pin_count = len(self.wiring[sensor])
            block_height = 30 + pin_count * 12 + (pin_count * 4)

            half_block = block_height / 2

            # --- Clamp positions to keep everything inside the canvas ---
            # Clamp Y so the rectangle doesn't go above top or below bottom
            if y - half_block < 0:
                y = half_block
            elif y + half_block > self.canvas_height:
                y = self.canvas_height - half_block

            # Clamp X so rectangles stay inside left/right margins
            if x - 50 < 0:
                x = 50
            elif x + 50 > self.canvas_width:
                x = self.canvas_width - 50

            # --- Draw rectangle and label ---
            rect = self.drawing.create_rectangle(
                x - 50, y - half_block,
                x + 50, y + half_block,
                fill=WHITE, outline=DARK_COLOR, width=2
            )

            label = self.drawing.create_text(
                x, y - half_block - 10,
                text=sensor.split("-")[1] if "-" in sensor else sensor,
                font=FONT, fill=DARK_COLOR
            )

            # Save positions
            self.sensor_positions[sensor] = (x, y, block_height)
            self.sensor_items[sensor] = (rect, label)
            self.wire_items[sensor] = []


    # --- Draw wires ---
    def _draw_all_wires(self):
        for sensor in self.wiring:
            self._draw_sensor_wires(sensor)

    def _draw_sensor_wires(self, sensor):
        for wid in self.wire_items[sensor]:
            self.drawing.delete(wid)
        self.wire_items[sensor].clear()

        sx, sy, sheight = self.sensor_positions[sensor]
        side = "left" if sx < self.center_x else "right"
        pins = self.wiring[sensor]

        num_pins = len(pins)
        spacing = sheight / (num_pins + 1) + 3
        offsets = [sy - sheight / 2 + spacing * (i + 1) for i in range(num_pins)]

        for i, (port, color_tag) in enumerate(pins.items()):
            exit_y = offsets[i]

            color = color_tag.split(",")[1].replace(" ", "") if len(color_tag.split(",")) > 1 else color_tag
            color = color.lower() if color.lower() in [
                "red", "blue", "green", "black", "gray", "yellow",
                "brown", "orange", "white", "purple"
            ] else "snow4"
            color = "thistle3" if color == "white" else color
            
            if port in logger_ports[self.datalogger_image]:
                logger_x = logger_ports[self.datalogger_image][port][0] + (self.center_x - (self.logger_width / 2))
                logger_y = logger_ports[self.datalogger_image][port][1] + (self.center_y - (self.logger_height / 2))
            elif port[0] == "(":
                try:
                    logger_x, logger_y = ast.literal_eval(port)
                except:
                    logger_x, logger_y = sx, exit_y
            else:
                logger_x, logger_y = sx, exit_y

            mid_x = sx + 60 if side == "left" else sx - 60

            line = self.drawing.create_line(sx, exit_y, mid_x, exit_y,
                                            logger_x, exit_y, logger_x, logger_y,
                                            fill=color, width=3)
            dot = self.drawing.create_oval(logger_x - 3, logger_y - 3,
                                           logger_x + 3, logger_y + 3,
                                           fill=color, outline="")
            text1 = self.drawing.create_text((sx + mid_x) / 2, exit_y - 6,
                                             text=color_tag, font=("Arial", 7), fill="black")
            
            text2 = self.drawing.create_text(((sx + mid_x) / 2) + (60 if side == "left" else -60),
                                             exit_y - 6, text=port, font=("Arial", 7), fill=color)

            self.wire_items[sensor].extend([line, dot, text1, text2])

    # --- Dragging ---
    def on_press(self, event):
        for sensor, (rect, label) in self.sensor_items.items():
            items = self.drawing.find_overlapping(event.x, event.y, event.x, event.y)
            if rect in items or label in items:
                self.drag_data["sensor"] = sensor
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                break

    def on_drag(self, event):
        sensor = self.drag_data["sensor"]
        if sensor:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            rect, label = self.sensor_items[sensor]
            self.drawing.move(rect, dx, dy)
            self.drawing.move(label, dx, dy)

            x, y, h = self.sensor_positions[sensor]
            self.sensor_positions[sensor] = (x + dx, y + dy, h)

            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            self._draw_sensor_wires(sensor)

    def on_release(self, event):
        self.drag_data["sensor"] = None

    # --- Save ---
    def save_canvas(self, event=None):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save canvas as image"
        )
        if not file_path:
            return

        self.drawing.update()
        ps = self.drawing.postscript(colormode='color')
        image = Image.open(io.BytesIO(ps.encode('utf-8')))
        image.save(file_path)
