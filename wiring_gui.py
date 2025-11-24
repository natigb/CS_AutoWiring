

import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
import ast

# You must have a `ports_coordenates.py` in your path that provides logger_ports dict,
# or adapt this code to your project structure.
try:
    from ports_coordenates import logger_ports
except Exception:
    # Minimal fallback to avoid hard crash during development/testing;
    # replace with your real logger_ports mapping.
    logger_ports = {
        "placeholder.png": {
            "image": (200, 120),
            # Example port coords (x, y) relative to logger image
            "P1": (10, 20),
            "P2": (40, 60),
        }
    }

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")


class WiringFrame(ttk.Frame):
    def __init__(self, parent, controller, wiring, datalogger_image, mode="normal"):
        """
        parent: tk parent
        controller: application controller (unused here but kept for compatibility)
        wiring: dict with sensor -> {port: color_tag, ...}
        datalogger_image: path to image used for datalogger ports mapping in logger_ports
        mode: "normal" or "compact" (keeps compatibility with original code)
        """
        super().__init__(parent, style="Right.TFrame")
        self.controller = controller
        self.wiring = wiring or {}
        self.datalogger_image = datalogger_image
        self.mode = mode

        # Canvas size (tweak as needed)
        self.canvas_width = 1700
        self.canvas_height = 900

        # Scrollable area
        self.canvas = Canvas(self, bg=WHITE, highlightthickness=0,
                             width=self.canvas_width - 100, height=500,
                             scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame inside canvas (so we can use pack/place for children if needed)
        self.inner = ttk.Frame(self.canvas, style="Right.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Mousewheel scrolling
        def _on_mousewheel(event):
            if event.state & 0x0001:  # Shift pressed -> horizontal
                self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # linux
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        # Actual drawing canvas
        self.drawing = Canvas(self.inner, width=self.canvas_width, height=self.canvas_height,
                              bg=WHITE, highlightthickness=0)
        self.drawing.pack()

        # Center for logger image placement
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2

        # Load logger image metadata (size) and attempt to display image
        try:
            self.logger_width = logger_ports[self.datalogger_image]["image"][0]
            self.logger_height = logger_ports[self.datalogger_image]["image"][1]
        except Exception:
            # fallback default
            self.logger_width = 300
            self.logger_height = 150

        try:
            image = Image.open(self.datalogger_image).resize((self.logger_width, self.logger_height))
            self.logger_img = ImageTk.PhotoImage(image)
            self.drawing.create_image(self.center_x, self.center_y, image=self.logger_img)
        except Exception:
            # placeholder rectangle
            self.drawing.create_rectangle(self.center_x - 100, self.center_y - 50,
                                          self.center_x + 100, self.center_y + 50,
                                          outline="black", fill="#eee")
            self.drawing.create_text(self.center_x, self.center_y, text="Datalogger", font=("Arial", 14))

        # Structures to hold sensors and wires
        self.sensor_positions = {}  # sensor -> (x, y, block_height)
        self.sensor_items = {}      # sensor -> (rect_id, text_id)
        self.wire_items = {}        # sensor -> [canvas_ids]  (automatic wires)
        self.manual_wires = {}      # wire_id -> {"items": [ids], "color": str}
        self.next_wire_id = 1

        # Manual wire drawing state
        self.drawing_wire = False
        self.current_wire_points = []          # list of (x, y)
        self.current_wire_preview_items = []   # canvas ids for preview dashed lines
        self.selected_wire_color = "red"


        # Layout sensors and draw automatic wires initially
        self._layout_sensors(self.mode)
        self._draw_all_wires(self.mode)

        # Dragging data
        self.drag_data = {"sensor": None, "x": 0, "y": 0}
        # Bind canvas events (dragging)
        self.drawing.bind("<ButtonPress-1>", self.on_press)
        self.drawing.bind("<B1-Motion>", self.on_drag)
        self.drawing.bind("<ButtonRelease-1>", self.on_release)

        # Bind wire-mode keys and mouse
        self.drawing.bind_all("<Key-w>", self.toggle_wire_mode)
        self.drawing.bind_all("<Return>", self.finalize_current_wire)
        self.drawing.bind_all("<Escape>", self.cancel_and_exit_wire_mode)
        self.drawing.bind("<Button-3>", self.on_right_click, add="+")

        

    # -------------------------
    # Sensor layout & auto-wire
    # -------------------------
    def _layout_sensors(self, mode):
        left_x = 100
        right_x = self.canvas_width - 100
        spacing_y = 150
        top_margin = 80

        for i, sensor in enumerate(self.wiring):
            side = "left" if i % 2 == 0 else "right"
            y = top_margin + (i // 2) * spacing_y + (4 * i)
            x = left_x if side == "left" else right_x

            pin_count = len(self.wiring[sensor])
            block_height = 30 + pin_count * 12 + (pin_count * 4)
            half_block = block_height / 2

            # Clamp into canvas
            if y - half_block < 0:
                y = half_block
            elif y + half_block > self.canvas_height:
                y = self.canvas_height - half_block
            if x - 50 < 0:
                x = 50
            elif x + 50 > self.canvas_width:
                x = self.canvas_width - 50

            if mode == "compact":
                color = WHITE
                state_mode = "hidden"
            else:
                color = DARK_COLOR
                state_mode = "normal"

            rect = self.drawing.create_rectangle(
                x - 50, y - half_block,
                x + 50, y + half_block,
                fill=WHITE, outline=color, width=2
            )
            label = self.drawing.create_text(
                x, y - half_block - 10,
                text=sensor.split("-")[1] if "-" in sensor else sensor,
                font=FONT, fill=color, state=state_mode
            )

            self.sensor_positions[sensor] = (x, y, block_height)
            self.sensor_items[sensor] = (rect, label)
            self.wire_items[sensor] = []

    def _draw_all_wires(self, mode):
        for sensor in self.wiring:
            self._draw_sensor_wires(sensor, mode)

    def _draw_sensor_wires(self, sensor, mode):
        # Clear previous auto-wires for sensor
        for wid in self.wire_items[sensor]:
            try:
                self.drawing.delete(wid)
            except Exception:
                pass
        self.wire_items[sensor].clear()

        sx, sy, sheight = self.sensor_positions[sensor]
        side = "left" if sx < self.center_x else "right"
        pins = self.wiring[sensor]
        num_pins = len(pins)

        spacing = sheight / (num_pins + 1) if mode == "compact" else sheight / (num_pins + 1) + 3
        offsets = [sy - sheight / 2 + spacing * (i + 1) for i in range(num_pins)]

        for i, (port, color_tag) in enumerate(pins.items()):
            exit_y = offsets[i]

            color = color_tag.split(",")[1].replace(" ", "") if len(color_tag.split(",")) > 1 else color_tag
            color = color.lower() if isinstance(color, str) and color.lower() in [
                "red", "blue", "green", "black", "gray", "yellow",
                "brown", "orange", "white", "purple"
            ] else "snow4"
            color = "thistle3" if color == "white" else color

            # find logger position
            if port in logger_ports.get(self.datalogger_image, {}):
                logger_x = logger_ports[self.datalogger_image][port][0] + (self.center_x - (self.logger_width / 2))
                logger_y = logger_ports[self.datalogger_image][port][1] + (self.center_y - (self.logger_height / 2))
            elif isinstance(port, str) and port.startswith("("):
                try:
                    logger_x, logger_y = ast.literal_eval(port)
                except Exception:
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
            if mode == "compact":
                compact_label = sensor + " (" + color_tag + ") -> " + port
                text1 = self.drawing.create_text(sx + (-60 if side == "left" else 60), exit_y - 7,
                                                text=compact_label, font=("Arial", 7), fill="black")
                text2 = self.drawing.create_text(((sx + mid_x) / 2) + (60 if side == "left" else -60),
                                                exit_y - 6, font=("Arial", 7), fill=WHITE)
            else:
                text1 = self.drawing.create_text((sx + mid_x) / 2, exit_y - 6,
                                                text=color_tag, font=("Arial", 7), fill="black")
                text2 = self.drawing.create_text(((sx + mid_x) / 2) + (60 if side == "left" else -60),
                                                exit_y - 6, text=port, font=("Arial", 7), fill=color)

            self.wire_items[sensor].extend([line, dot, text1, text2])

    # -------------------------
    # Dragging handlers
    # -------------------------
    def on_press(self, event):
        # If wire mode active, left-click adds point to the current wire (no dragging)
        if self.drawing_wire:
            self.add_point_to_current_wire((event.x, event.y))
            return

        # Otherwise check if clicking a sensor rectangle or label to start dragging
        for sensor, (rect, label) in self.sensor_items.items():
            items = self.drawing.find_overlapping(event.x, event.y, event.x, event.y)
            if rect in items or label in items:
                self.drag_data["sensor"] = sensor
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                break

    def on_drag(self, event):
        # Disable dragging while in wire mode (Option A)
        if self.drawing_wire:
            return

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

            # redraw auto wires for this sensor
            self._draw_sensor_wires(sensor, self.mode)

    def on_release(self, event):
        self.drag_data["sensor"] = None

    # -------------------------
    # Manual Wire Drawing
    # -------------------------
    def toggle_wire_mode(self, event=None):
        """Toggle wire-drawing mode on/off. When ON, sensor dragging disabled."""
        self._create_color_picker_window()
        self.drawing_wire = not self.drawing_wire
        if self.drawing_wire:
            self.current_wire_points = []
            self.clear_current_preview()
            try:
                self.drawing.focus_set()
            except Exception:
                pass
            
        else:
            # exit wire mode, clear any preview
            self.current_wire_points = []
            self.clear_current_preview()

    def add_point_to_current_wire(self, point):
        """Add a point and update preview (called on left-click while in wire mode)."""
        self.current_wire_points.append(point)
        self.draw_wire_preview()

    def draw_wire_preview(self):
        """Draw dashed preview segments in 90-degree style for the current points."""
        self.clear_current_preview()
        pts = self.current_wire_points
        if len(pts) < 2:
            return

        color = self.selected_wire_color
        preview_items = []
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            # 90-degree path (horizontal then vertical): (x1,y1) -> (x2,y1) -> (x2,y2)
            mid_x = x2
            mid_y = y1
            l1 = self.drawing.create_line(x1, y1, mid_x, mid_y, fill=color, width=3, dash=(6, 4), tags=("preview",))
            l2 = self.drawing.create_line(mid_x, mid_y, x2, y2, fill=color, width=3, dash=(6, 4), tags=("preview",))
            preview_items.extend([l1, l2])
            # small dot markers
            preview_items.append(self.drawing.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=color, outline="", tags=("preview",)))
        # last point dot
        last_x, last_y = pts[-1]
        preview_items.append(self.drawing.create_oval(last_x - 2, last_y - 2, last_x + 2, last_y + 2, fill=color, outline="", tags=("preview",)))
        self.current_wire_preview_items = preview_items

    def clear_current_preview(self):
        for it in list(self.current_wire_preview_items):
            try:
                self.drawing.delete(it)
            except Exception:
                pass
        self.current_wire_preview_items = []

    def finalize_current_wire(self, event=None):
        """Convert preview into permanent solid manual wire. Stays in wire mode for further drawing."""
        if not self.drawing_wire:
            return
        pts = self.current_wire_points
        if len(pts) < 2:
            return

        color = self.selected_wire_color
        wire_id = self.next_wire_id
        self.next_wire_id += 1
        created_items = []
        tag_name = f"wire_{wire_id}"

        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            mid_x = x2
            mid_y = y1
            l1 = self.drawing.create_line(x1, y1, mid_x, mid_y, fill=color, width=3, tags=("manual_wire", tag_name))
            l2 = self.drawing.create_line(mid_x, mid_y, x2, y2, fill=color, width=3, tags=("manual_wire", tag_name))
            created_items.extend([l1, l2])
            # connector dots
            created_items.append(self.drawing.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=color, outline="", tags=("manual_wire", tag_name)))
        # last point dot
        lx, ly = pts[-1]
        created_items.append(self.drawing.create_oval(lx - 2, ly - 2, lx + 2, ly + 2, fill=color, outline="", tags=("manual_wire", tag_name)))

        self.manual_wires[wire_id] = {"items": created_items, "color": color}
        # Clear preview and current points but remain in wire mode
        self.current_wire_points = []
        self.clear_current_preview()

    def cancel_and_exit_wire_mode(self, event=None):
        """Cancel any in-progress preview and exit wire mode."""
        if self.drawing_wire:
            self.current_wire_points = []
            self.clear_current_preview()
            self.drawing_wire = False

    # -------------------------
    # Manual wire deletion
    # -------------------------
    def on_right_click(self, event):
        """
        If in wire mode: cancel & exit (Option A).
        If not in wire mode: find a manual wire at click position and delete it.
        """
        if self.drawing_wire:
            self.cancel_and_exit_wire_mode()
            return

        clicked_items = self.drawing.find_overlapping(event.x, event.y, event.x, event.y)
        if not clicked_items:
            return

        for it in clicked_items:
            tags = self.drawing.gettags(it)
            for t in tags:
                if t.startswith("wire_"):
                    # tag like wire_3
                    try:
                        wire_id = int(t.split("_", 1)[1])
                    except Exception:
                        continue
                    self.delete_manual_wire(wire_id)
                    return

    def delete_manual_wire(self, wire_id):
        if wire_id not in self.manual_wires:
            return
        items = self.manual_wires[wire_id]["items"]
        for it in list(items):
            try:
                self.drawing.delete(it)
            except Exception:
                pass
        # Also delete by tag if any remain
        try:
            for it in self.drawing.find_withtag(f"wire_{wire_id}"):
                try:
                    self.drawing.delete(it)
                except Exception:
                    pass
        except Exception:
            pass
        del self.manual_wires[wire_id]

    # -------------------------
    # Color picker TopLevel
    # -------------------------
    def _create_color_picker_window(self):
        # Create a small floating window for color selection
        self.color_window = tk.Toplevel(self)
        self.color_window.title("Wire Color")
        self.color_window.geometry("170x96")
        self.color_window.resizable(False, False)
        # Keep it on top so user can change color while drawing
        try:
            self.color_window.attributes("-topmost", True)
        except Exception:
            pass

        # Prevent closing accidental? You can allow it; here we allow closing.
        frame = ttk.Frame(self.color_window, padding=6)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Color:", font=("Segoe UI", 10)).pack(anchor="w")
        colors = ["red", "blue", "green", "black", "gray", "yellow",
                "brown", "orange", "white", "purple"]
        self.color_combo = ttk.Combobox(frame, values=colors, width=14, state="readonly")
        self.color_combo.set(self.selected_wire_color)
        self.color_combo.pack(pady=(6, 2))

        # optional preview box
        self.preview_canvas = Canvas(frame, width=40, height=20, highlightthickness=1, bd=0)
        self.preview_canvas.pack(pady=(4, 0))
        self._update_color_preview()

        def on_color_select(event):
            self.selected_wire_color = self.color_combo.get()
            self._update_color_preview()

        self.color_combo.bind("<<ComboboxSelected>>", on_color_select)

        # Close button
        ttk.Button(frame, text="Close", command=self.color_window.withdraw).pack(pady=(6, 0))

    def _update_color_preview(self):
        self.preview_canvas.delete("all")
        c = self.selected_wire_color if self.selected_wire_color else "red"
        self.preview_canvas.create_rectangle(0, 0, 40, 20, fill=c, outline="black")

    # -------------------------
    # Utility helpers
    # -------------------------
    def get_manual_wires_data(self):
        """Return a serializable representation of manual wires (e.g., for saving)."""
        out = {}
        for wid, info in self.manual_wires.items():
            # We only store color and points could be inferred if desired (not stored here)
            out[wid] = {"color": info["color"]}
        return out



