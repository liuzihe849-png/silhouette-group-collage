#!/usr/bin/env python3
"""Create a phase-2 review sheet from source, detection, and cutout previews."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--phase1", type=Path, required=True)
    parser.add_argument("--phase2-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    panels = [
        ("source", Image.open(args.source).convert("RGB")),
        ("phase 1: BiRefNet HR", Image.open(args.phase1).convert("RGB")),
        ("phase 2: six detections", Image.open(args.phase2_dir / "detections.png").convert("RGB")),
        ("phase 2: refined alpha", Image.open(args.phase2_dir / "refined-checker-preview.png").convert("RGB")),
    ]
    cell_w, cell_h, header_h = 590, 600, 52
    sheet = Image.new("RGB", (cell_w * 2, (cell_h + header_h) * 2), "#e5e1d7")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=24)
    for index, (label, panel) in enumerate(panels):
        col, row = index % 2, index // 2
        x0, y0 = col * cell_w, row * (cell_h + header_h)
        draw.text((x0 + 16, y0 + 13), label, font=font, fill="#111111")
        panel.thumbnail((cell_w - 20, cell_h - 20), Image.Resampling.LANCZOS)
        x = x0 + (cell_w - panel.width) // 2
        y = y0 + header_h + (cell_h - panel.height) // 2
        sheet.paste(panel, (x, y))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(args.output)


if __name__ == "__main__":
    main()
