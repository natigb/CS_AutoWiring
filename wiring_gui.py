import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from ports_coordenates import logger_ports
import pyautogui
import time
from tkinter import filedialog

"""
An example of wiring form
{'237': {'GND_1': 'Purple', 'GND_2': 'Clear', 'H_1': 'Red', 'VX_1': 'Black'}, 
 'SnowVUE10': {'C_1': 'White', 'G_1': 'Black', 'G_2': 'Clear', '12V': 'Brown'}, 
 'JC Depth': {'GND_3': 'Clear', 'L_2': 'Brown', 'H_2': 'White', 'C_2': 'Green', 'G_3': 'Black', '12V': 'Red'}, 
 'ClimaVUE50': {'C_1': 'White', 'G_4': 'Black', 'G_5': 'Clear', '12V': 'Brown'}}
"""

def draw_wiring_diagram_gui(wiring, datalogger_image):
    root = tk.Toplevel()
    root.title("Sensor Wiring Diagram")

    canvas_width = 1920
    canvas_height = 1080
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#ffffff")
    canvas.pack()

    # Datalogger image position
    center_x = canvas_width // 2
    center_y = canvas_height //2
    #center_y = canvas_height - (canvas_height // 3)
    logger_width = logger_ports[datalogger_image]["image"][0]
    logger_height = logger_ports[datalogger_image]["image"][1]
    logger_top_left = (center_x - logger_width // 2, center_y - logger_height // 2)

    # Load and place datalogger image
    try:
        image = Image.open(datalogger_image).resize((logger_width, logger_height))
        logger_img = ImageTk.PhotoImage(image)
        canvas.image = logger_img
        canvas.create_image(center_x, center_y, image=logger_img)
    except FileNotFoundError:
        canvas.create_rectangle(center_x - 100, center_y - 100,
                                center_x + 100, center_y + 100, outline="black", fill="#eee")
        canvas.create_text(center_x, center_y, text="CR1000X", font=("Arial", 14))

    # Layout sensors around logger
    left_x = 100
    right_x = canvas_width - 100
    spacing_y = 150
    top_margin = 80
    sensor_positions = {}
    sensor_items = {}   # maps sensor -> canvas item ids
    wire_items = {}     # maps sensor -> list of wire item ids

    for i, sensor in enumerate(wiring):
        side = "left" if i % 2 == 0 else "right"
        y = top_margin + (i // 2) * spacing_y + (4 * i)
        x = left_x if side == "left" else right_x

        pin_count = len(wiring[sensor])
        block_height = 30 + pin_count * 12 + (pin_count * 4)

        rect = canvas.create_rectangle(x - 50, y - block_height / 2,
                                       x + 50, y + block_height / 2,
                                       fill="#ffffff", outline="black", width=2)
        label = canvas.create_text(x, y - block_height / 2 - 10,
                                   text=sensor.split("-")[1], font=("Arial", 12))
        sensor_positions[sensor] = (x, y, block_height)
        sensor_items[sensor] = (rect, label)
        wire_items[sensor] = []  # will hold lines and text ids later

    # function to draw wires for a sensor
    def draw_sensor_wires(sensor):
        # clear old wires
        for wid in wire_items[sensor]:
            canvas.delete(wid)
        wire_items[sensor].clear()

        sx, sy, sheight = sensor_positions[sensor]
        side = "left" if sx < center_x else "right"
        pins = wiring[sensor]

        num_pins = len(pins)
        spacing = sheight / (num_pins + 1) + 3
        offsets = [sy - sheight / 2 + spacing * (i + 1) for i in range(num_pins)]

        for i, (port, color_tag) in enumerate(pins.items()):
            exit_y = offsets[i]

            # normalize color
            color = color_tag.split(",")[1].replace(" ", "") if len(color_tag.split(",")) > 1 else color_tag
            color = color.lower() if color.lower() in [
                "red", "blue", "green", "black", "gray", "yellow", "brown", "orange", "white", "purple"
            ] else "NavajoWhite2"
            color = "thistle3" if color == "white" else color

            if port in logger_ports[datalogger_image]:
                logger_x = logger_ports[datalogger_image][port][0] + (center_x - (logger_width / 2))
                logger_y = logger_ports[datalogger_image][port][1] + (center_y - (logger_height / 2))
            else:
                logger_x, logger_y = sx, exit_y

            mid_x = sx + 60 if side == "left" else sx - 60

            line = canvas.create_line(sx, exit_y, mid_x, exit_y, logger_x, exit_y, logger_x, logger_y,
                                      fill=color, width=3)
            dot_radius = 3
            dot = canvas.create_oval(logger_x - dot_radius, logger_y - dot_radius,
                                     logger_x + dot_radius, logger_y + dot_radius,
                                     fill=color, outline="")

            label_x = (sx + mid_x) / 2
            label_x_offset = 60 if side == "left" else -60
            text1 = canvas.create_text(label_x, exit_y - 6, text=color_tag, font=("Arial", 7), fill="black")
            text2 = canvas.create_text(label_x + label_x_offset, exit_y - 6, text=port, font=("Arial", 7), fill=color)

            wire_items[sensor].extend([line, dot, text1, text2])

    # initial wire drawing
    for sensor in wiring:
        draw_sensor_wires(sensor)

    # dragging logic
    drag_data = {"sensor": None, "x": 0, "y": 0}

    def on_press(event):
        for sensor, (rect, label) in sensor_items.items():
            items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
            if rect in items or label in items:
                drag_data["sensor"] = sensor
                drag_data["x"] = event.x
                drag_data["y"] = event.y
                break

    def on_drag(event):
        sensor = drag_data["sensor"]
        if sensor:
            dx = event.x - drag_data["x"]
            dy = event.y - drag_data["y"]
            rect, label = sensor_items[sensor]
            canvas.move(rect, dx, dy)
            canvas.move(label, dx, dy)

            # update position
            x, y, h = sensor_positions[sensor]
            sensor_positions[sensor] = (x + dx, y + dy, h)

            drag_data["x"] = event.x
            drag_data["y"] = event.y

            # redraw wires
            draw_sensor_wires(sensor)

    def on_release(event):
        drag_data["sensor"] = None

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    # coords tracker
    coords_label = tk.Label(root, text="Mouse at (0, 0)", font=("Arial", 14))
    coords_label.pack(pady=10)

    def save_canvas(event=None):
        root.update()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save canvas as image"
        )
        if not file_path:
            return
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        time.sleep(0.2)
        image = pyautogui.screenshot(region=(x, y, w, h))
        image.save(file_path)

    canvas.bind("<Button-3>", save_canvas)

    def mouse_move(event):
        coords_label.config(text=f"Mouse at ({event.x}, {event.y})")

    root.bind('<Motion>', mouse_move)
