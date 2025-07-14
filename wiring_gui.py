import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from ports_coordenates import logger_ports
import pyautogui
import time  

def draw_wiring_diagram_gui(wiring, datalogger_image):
    root = tk.Tk()
    root.title("Sensor Wiring Diagram")

    canvas_width = 1000
    canvas_height = 500
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#ffffff")
    canvas.pack()

    # Datalogger image position
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    logger_width = logger_ports[datalogger_image]["image"][0]
    logger_height = logger_ports[datalogger_image]["image"][1]
    logger_top_left = (center_x - logger_width // 2, center_y - logger_height // 2)

    # Load and place datalogger image
    try:
        image = Image.open(datalogger_image).resize((logger_width, logger_height))
        logger_img = ImageTk.PhotoImage(image)
        canvas.create_image(center_x, center_y, image=logger_img)
    except FileNotFoundError:
        canvas.create_rectangle(center_x - 100, center_y - 100,
                                center_x + 100, center_y + 100, outline="black", fill="#eee")
        canvas.create_text(center_x, center_y, text="CR1000X", font=("Arial", 12))
    
    # Layout sensors around logger
    left_x = 100
    right_x = canvas_width - 100
    spacing_y = 100
    top_margin = 80
    sensor_positions = {}

    for i, sensor in enumerate(wiring):
        side = "left" if i % 2 == 0 else "right"
        y = top_margin + (i // 2) * spacing_y
        x = left_x if side == "left" else right_x

        pin_count = len(wiring[sensor])
        block_height = 20 + pin_count * 12

        canvas.create_rectangle(x - 50, y - block_height / 2,
                                x + 50, y + block_height / 2,
                                fill="#ffffff", outline="black")
        canvas.create_text(x, y - block_height / 2 - 10, text=sensor, font=("Arial", 12))
        sensor_positions[sensor] = (x, y, block_height)

    # Draw wires
    counter = 3
    used_x_values =[]
    for sensor, pins in wiring.items():
        sx, sy, sheight = sensor_positions[sensor]
        side = "left" if sx < center_x else "right"

        num_pins = len(pins)
        spacing = sheight / (num_pins + 1)
        offsets = [sy - sheight / 2 + spacing * (i + 1) for i in range(num_pins)]

        for i, (port, color) in enumerate(pins.items()):
            exit_y = offsets[i]
            color_tag = color
            
            color = color.lower() if color.lower() in [
                "red", "blue", "green", "black", "gray", "yellow", "brown", "orange", "white"
                ]else "NavajoWhite2"
            color = "thistle3" if color=="white" else color
            # Datalogger port coordinates
            #print(port)
            if port in logger_ports[datalogger_image]:
                logger_x = logger_ports[datalogger_image][port][0] +((canvas_width-logger_width)/2)
                logger_y =  logger_ports[datalogger_image][port][1]+((canvas_height-logger_height)/2)
            else:
                logger_x, logger_y = center_x, center_y  # fallback

            # Exit horizontal path
            mid_x = sx + 60 if side == "left" else sx - 60
            # if(logger_x not in used_x_values):
            #     canvas.create_line(sx, exit_y, mid_x, exit_y,logger_x, exit_y,logger_x, logger_y, fill=color, width=2)
            # else:
            #     canvas.create_line(sx, exit_y, mid_x, exit_y,logger_x+counter, exit_y, fill=color, width=2)
            #     counter+=3
            # used_x_values.append(logger_x)

            canvas.create_line(sx, exit_y, mid_x, exit_y,logger_x, exit_y,logger_x, logger_y, fill=color, width=2)
            #canvas.create_line(sx, exit_y, mid_x, exit_y, fill=color, width=2)
            #canvas.create_line(mid_x, exit_y, logger_x, logger_y, fill=color, width=2)

            # Port label
            label_x = (sx + mid_x) / 2
            label_x_offset =  60 if side == "left" else - 60
            canvas.create_text(label_x, exit_y - 6, text=color_tag, font=("Arial", 7), fill="black")
            canvas.create_text(label_x + label_x_offset, exit_y - 6, text=port, font=("Arial", 7), fill=color)
    
    coords_label = tk.Label(root, text="Mouse at (0, 0)", font=("Arial", 14))
    coords_label.pack(pady=10)

    def save_canvas(event=None):
        root.update()  # Make sure everything is drawn
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        time.sleep(0.2)  # Small delay to ensure canvas is stable
        image = pyautogui.screenshot(region=(x, y, w, h))
        image.save("canvas_capture.png")

    canvas.bind("<Button-3>", save_canvas)

    def mouse_move(event):
    # Update the label with the current mouse coordinates
     coords_label.config(text=f"Mouse at ({event.x}, {event.y})")
# Bind mouse motion to the handler
    root.bind('<Motion>', mouse_move)
    root.mainloop()
