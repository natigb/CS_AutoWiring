from PIL import Image, ImageDraw, ImageFont
from ports_coordenates import logger_ports

def label_ports_rotated(image_key, output="labeled_rotated.png"):
    """
    Draws port labels rotated 90° counter-clockwise above each port dot.
    Compatible with Pillow >=10.
    """
    if image_key not in logger_ports:
        raise ValueError(f"{image_key} not found in logger_ports")

    ports = logger_ports[image_key]
    img_size = ports["image"]
    
    img = Image.open(image_key).resize(img_size)
    draw = ImageDraw.Draw(img)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    for port, coords in ports.items():
        if port == "image":
            continue
        x, y = coords

        # Draw a small red dot
        r = 2
        draw.ellipse((x-r, y-r, x+r, y+r), fill="red")

        # Get text size using textbbox
        bbox = draw.textbbox((0, 0), port, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Create a separate image for the text
        text_img = Image.new("RGBA", (text_w, text_h), (0,0,0,255))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0,0), port, font=font, fill="#EABE0D")

        # Rotate the text 90° counter-clockwise
        rotated = text_img.rotate(90, expand=1)

        # Paste it above the dot (centered)
        paste_x = int(x - rotated.width / 2)
        paste_y = int(y - rotated.height - 5)
        img.paste(rotated, (paste_x, paste_y), rotated)

    img.save(output)
    img.show()
    print(f"Labeled image saved as {output}")


if __name__ == "__main__":
    label_ports_rotated("img/AM1632B.png", "aux_files/labeled.png")
