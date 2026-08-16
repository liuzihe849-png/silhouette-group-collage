#!/usr/bin/env python3
"""Check person occupancy and opaque-mask coverage without changing either mask."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops


def binary(path: Path, size: tuple[int, int] | None = None) -> Image.Image:
    image = Image.open(path).convert("L")
    if size and image.size != size:
        raise ValueError(f"mask sizes differ: expected {size}, got {image.size} for {path}")
    return image.point(lambda value: 255 if value >= 128 else 0)


def white_pixels(image: Image.Image) -> int:
    return image.histogram()[255]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("person_mask", type=Path)
    parser.add_argument("colour_mask", type=Path)
    parser.add_argument("--minimum", type=float, default=0.995)
    args = parser.parse_args()

    person = binary(args.person_mask)
    colour = binary(args.colour_mask, person.size)
    person_area = white_pixels(person)
    colour_area = white_pixels(colour)
    if person_area == 0:
        raise SystemExit("FAIL: person mask is empty")

    intersection = ImageChops.darker(person, colour)
    covered = white_pixels(intersection)
    coverage = covered / person_area
    occupancy = person_area / (person.width * person.height)
    spill = (colour_area - covered) / colour_area if colour_area else 0.0

    print(f"person_occupancy={occupancy:.4f}")
    print(f"person_coverage={coverage:.4f}")
    print(f"colour_spill={spill:.4f}")
    if coverage < args.minimum:
        raise SystemExit(f"FAIL: coverage {coverage:.4f} is below {args.minimum:.4f}")
    print("PASS: opaque mask fully covers the protected person region")


if __name__ == "__main__":
    main()
