#!/usr/bin/env python3
"""Render a labelled preview board for the five paper profiles."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "assets/design-system/paper-texture-profiles.json"
OUTPUT = ROOT / "assets/design-system/paper-texture-system-preview.png"
FONT = ROOT / "assets/fonts/kalam/Kalam-Bold.ttf"
REGULAR = ROOT / "assets/fonts/kalam/Kalam-Regular.ttf"


def main() -> None:
    profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))["profiles"]
    colours = ["#C9543F"] * 5
    width, card_h, margin, header = 1500, 250, 52, 170
    canvas = Image.new("RGB", (width, header + len(profiles) * card_h + margin), "#FFF9F3")
    draw = ImageDraw.Draw(canvas)
    title = ImageFont.truetype(str(FONT), 56)
    body = ImageFont.truetype(str(REGULAR), 30)
    small = ImageFont.truetype(str(REGULAR), 23)
    draw.text((margin, 34), "Five Quiet Paper Textures", font=title, fill="#332F2C")
    draw.text((margin, 102), "soft fibre, matte grain, and three restrained fleck densities — shown on one red field", font=body, fill="#596D73")
    with tempfile.TemporaryDirectory(prefix="texture-board-") as temporary:
        directory = Path(temporary)
        for index, (profile, colour) in enumerate(zip(profiles, colours)):
            sample = directory / f"{profile['id']}.png"
            subprocess.run([
                sys.executable, "scripts/apply_paper_texture.py",
                "--profile", profile["id"], "--colour", colour,
                "--width", "880", "--height", "208", "--output", str(sample),
            ], cwd=ROOT, check=True, capture_output=True, text=True)
            y = header + index * card_h
            canvas.paste(Image.open(sample).convert("RGB"), (margin, y + 18))
            text_x = 980
            text_colour = "#332F2C"
            draw.text((text_x, y + 44), profile["name"], font=body, fill=text_colour)
            draw.text((text_x, y + 96), profile["id"], font=small, fill="#596D73")
            draw.text((text_x, y + 140), "parent: " + profile["reference_parent"], font=small, fill="#596D73")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
