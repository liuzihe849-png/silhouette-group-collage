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
    parser.add_argument(
        "--maximum-excess",
        type=float,
        default=0.08,
        help="maximum area(C-P)/area(P); use up to 0.15 for intentional connected clusters",
    )
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
    excess = (colour_area - covered) / person_area

    print(f"person_occupancy={occupancy:.4f}")
    print(f"person_coverage={coverage:.4f}")
    print(f"mask_excess={excess:.4f}")
    if coverage < args.minimum:
        raise SystemExit(f"FAIL: coverage {coverage:.4f} is below {args.minimum:.4f}")
    if excess > args.maximum_excess:
        raise SystemExit(
            f"FAIL: excess {excess:.4f} is above {args.maximum_excess:.4f}; mask is too bulky"
        )
    print("PASS: opaque mask covers the protected region and remains contour-tight")


if __name__ == "__main__":
    main()
