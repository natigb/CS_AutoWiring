from PIL import Image, ImageDraw, ImageFont
from ports_coordenates import logger_ports

def draw_ports(image_path, output_path="output.png"):
    # Load coordinates from logger_ports
    coords = logger_ports[image_path]
    
    # Open image
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))  # transparent layer
    draw = ImageDraw.Draw(overlay)

    # Load font (small for less overlap)
    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()

    for port, position in coords.items():
        if port == "image":  # skip image size metadata
            continue
        
        x, y = position
        r = 5  # radius of the dot

        # Draw dot centered on (x, y)
        draw.ellipse(
            [(x - r, y - r), (x + r, y + r)],
            fill=(0, 128, 255, 180),  # semi-transparent blue
            outline=(0, 0, 0, 200)
        )

        # Draw label in front (to the right) of the dot
        try:
            text_w, text_h = font.getsize(port)
        except AttributeError:
            bbox = font.getbbox(port)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        text_x = x + r + 2  # a small gap to the right of the dot
        text_y = y - text_h // 2  # vertically center with the dot

        draw.text((text_x, text_y), port, font=font, fill=(255, 255, 255, 255))

    # Merge overlay with base image
    out = Image.alpha_composite(img, overlay)
    out.save(output_path)
    print(f"Saved annotated image as {output_path}")


if __name__ == "__main__":
    # Example: pick one logger image
    image_file = "img/cr1000x.png"  # must exist in your working directory
    draw_ports(image_file, "cr1000x_labeled.png")
