import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from ports_coordenates import logger_ports

datalogger_image = "img/cr1000xe.png"
root = tk.Tk()
root.title("Sensor Wiring Diagram")

canvas_width = logger_ports[datalogger_image]["image"][0]
canvas_height = logger_ports[datalogger_image]["image"][1]
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

coords_label = tk.Label(root, text="Mouse at (0, 0)", font=("Arial", 14))
coords_label.pack(pady=10)



def mouse_move(event):
# Update the label with the current mouse coordinates
    coords_label.config(text=f"Mouse at ({event.x}, {event.y})")
# Bind mouse motion to the handler
root.bind('<Motion>', mouse_move)
root.mainloop()

