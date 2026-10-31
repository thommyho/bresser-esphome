"""Render the OLED pages of examples/lilygo-lora32-oled.yaml with sample values.

The pages mirror the display lambda of the example. Usage:
    python render_oled_pages.py Roboto-Regular.ttf output_dir
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, SCALE = 128, 64, 4
SMALL, BIG = 13, 24

PAGES = {
    "klima": ("Klima", "vor 12s", [("big", "8.8 °C"), (49, "Feuchte", "87 %")]),
    "wind": ("Wind", "vor 12s", [("big", "3.2 m/s"), (49, "NW 315°", "Böe 5.1")]),
    "regen-licht": ("Regen & Licht", "vor 59m", [
        (17, "Regen", "1234.5 mm"), (33, "UV-Index", "1.5"), (49, "Licht", "12500 lx")]),
    "umgebung": ("Umgebung", "3 Stat.", [
        (17, "Temperatur", "9.1 °C"), (33, "Feuchte", "84 %"), (49, "Wind", "2.7 m/s")]),
    "status": ("Status", "vor 12s", [
        (17, "Funk", "-71 dBm"), (33, "WLAN", "-65 dBm"), (49, "Batterie", "OK")]),
}


def render(title, status, rows, small, big):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.fontmode = "1"
    draw.text((0, 0), title, 1, small, anchor="la")
    draw.text((WIDTH - 1, 0), status, 1, small, anchor="ra")
    draw.line((0, 15, WIDTH - 1, 15), 1)
    for row in rows:
        if row[0] == "big":
            draw.text((WIDTH // 2, 16), row[1], 1, big, anchor="ma")
        else:
            draw.text((0, row[0]), row[1], 1, small, anchor="la")
            draw.text((WIDTH - 1, row[0]), row[2], 1, small, anchor="ra")
    return image.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.NEAREST)


def main():
    font_path, output = sys.argv[1], Path(sys.argv[2])
    small = ImageFont.truetype(font_path, SMALL)
    big = ImageFont.truetype(font_path, BIG)
    output.mkdir(parents=True, exist_ok=True)
    for name, (title, status, rows) in PAGES.items():
        render(title, status, rows, small, big).save(output / f"{name}.png")


if __name__ == "__main__":
    main()
