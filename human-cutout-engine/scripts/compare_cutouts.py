#!/usr/bin/env python3
"""Create a visual contact sheet for candidate cutout runs."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--run", action="append", required=True, help="LABEL=OUTPUT_DIR")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--column-width", type=int, default=520)
    return parser.parse_args()


def fit(image: Image.Image, box: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(box, Image.Resampling.LANCZOS)
    return copy


def main() -> None:
    args = parse_args()
    source = Image.open(args.source).convert("RGB")
    runs: list[tuple[str, Path]] = []
    for item in args.run:
        if "=" not in item:
            raise SystemExit(f"Invalid --run value: {item}")
        label, directory = item.split("=", 1)
        runs.append((label, Path(directory)))

    cell_h = 540
    header_h = 58
    columns = 1 + len(runs) * 2
    sheet = Image.new("RGB", (columns * args.column_width, header_h + cell_h), "#ebe7dc")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=24)

    cells: list[tuple[str, Image.Image]] = [("source", source)]
    for label, directory in runs:
        cells.append((f"{label} alpha", Image.open(directory / "alpha.png").convert("RGB")))
        cells.append((f"{label} cutout", Image.open(directory / "checker-preview.png").convert("RGB")))

    for index, (label, image) in enumerate(cells):
        x0 = index * args.column_width
        draw.text((x0 + 16, 14), label, font=font, fill="#171717")
        thumb = fit(image, (args.column_width - 20, cell_h - 20))
        px = x0 + (args.column_width - thumb.width) // 2
        py = header_h + (cell_h - thumb.height) // 2
        sheet.paste(thumb, (px, py))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(args.output)


if __name__ == "__main__":
    main()
