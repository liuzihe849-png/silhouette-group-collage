#!/usr/bin/env python3
"""Render a compact visual board from the colour-system JSON."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "assets/design-system/color-system.json").read_text(encoding="utf-8"))
OUTPUT = ROOT / "assets/design-system/color-system-preview.png"
FONT = ROOT / "assets/fonts/kalam/Kalam-Bold.ttf"
REGULAR = ROOT / "assets/fonts/kalam/Kalam-Regular.ttf"


def text_colour(value: str) -> str:
    r, g, b = (int(value[index:index + 2], 16) for index in (1, 3, 5))
    return "#FFF9F3" if (0.2126 * r + 0.7152 * g + 0.0722 * b) < 145 else "#332F2C"


def main() -> None:
    swatches = DATA["anchors"] + DATA["extensions"]
    columns = 4
    cell_w, cell_h = 420, 220
    margin, header = 60, 180
    rows = (len(swatches) + columns - 1) // columns
    canvas = Image.new("RGB", (margin * 2 + columns * cell_w, header + margin + rows * cell_h), "#FFF9F3")
    draw = ImageDraw.Draw(canvas)
    title = ImageFont.truetype(str(FONT), 58)
    body = ImageFont.truetype(str(REGULAR), 30)
    small = ImageFont.truetype(str(REGULAR), 24)
    draw.text((margin, 42), "Heirloom Scene Colour System", font=title, fill="#332F2C")
    draw.text((margin, 112), "4 reference anchors + scene-adaptive heritage extensions", font=body, fill="#596D73")
    for index, item in enumerate(swatches):
        row, column = divmod(index, columns)
        x = margin + column * cell_w
        y = header + row * cell_h
        pad = 14
        draw.rounded_rectangle((x + pad, y + pad, x + cell_w - pad, y + cell_h - pad), radius=26, fill=item["hex"])
        ink = text_colour(item["hex"])
        draw.text((x + 34, y + 54), item["name"], font=body, fill=ink)
        draw.text((x + 34, y + 108), item["hex"], font=small, fill=ink)
        draw.text((x + 34, y + 148), item["id"], font=small, fill=ink)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
