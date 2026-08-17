#!/usr/bin/env python3
"""Build deterministic neutral paper tiles from bundled profile parameters."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "assets/design-system/paper-texture-profiles.json"


def noise_layer(size: tuple[int, int], sigma: float, rng: random.Random, distribution: str = "gaussian") -> Image.Image:
    if distribution == "uniform":
        amplitude = sigma * math.sqrt(3)
        sample = lambda: rng.uniform(-amplitude, amplitude)
    else:
        sample = lambda: rng.gauss(0, sigma)
    data = bytes(max(0, min(255, round(128 + sample()))) for _ in range(size[0] * size[1]))
    return Image.frombytes("L", size, data)


def add_neutral(base: Image.Image, layer: Image.Image) -> Image.Image:
    return ImageChops.add(base, layer, scale=1.0, offset=-128)


def build(profile: dict, size: int) -> Image.Image:
    spec = profile["generator"]
    rng = random.Random(spec["seed"])
    result = Image.new("L", (size, size), 128)

    fine = noise_layer((size, size), spec["fine_sigma"], rng, spec.get("fine_distribution", "gaussian"))
    result = add_neutral(result, fine)

    coarse_size = max(24, size // 18)
    coarse = noise_layer((coarse_size, coarse_size), spec["coarse_sigma"], rng)
    coarse = coarse.resize((size, size), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(size / 90))
    result = add_neutral(result, coarse)

    fibres = Image.new("L", (size, size), 128)
    draw = ImageDraw.Draw(fibres)
    for _ in range(spec.get("scan_lines", 0)):
        y = rng.randrange(size)
        value = 128 + rng.choice((-1, 1)) * rng.randint(1, 4)
        draw.line((0, y, size, y), fill=value, width=1)
    for _ in range(spec["horizontal_fibres"]):
        y = rng.randrange(size)
        x = rng.randrange(size)
        length = rng.randint(max(8, size // 80), max(24, size // 7))
        value = 128 + rng.choice((-1, 1)) * rng.randint(2, 7)
        draw.line((x, y, min(size - 1, x + length), y + rng.choice((-1, 0, 0, 0, 1))), fill=value, width=1)
    for _ in range(spec["vertical_fibres"]):
        x = rng.randrange(size)
        y = rng.randrange(size)
        length = rng.randint(max(8, size // 100), max(20, size // 9))
        value = 128 + rng.choice((-1, 1)) * rng.randint(2, 7)
        draw.line((x, y, x + rng.choice((-1, 0, 0, 1)), min(size - 1, y + length)), fill=value, width=1)
    result = add_neutral(result, fibres.filter(ImageFilter.GaussianBlur(0.25)))

    material = Image.new("L", (size, size), 128)
    draw = ImageDraw.Draw(material)
    for _ in range(spec["flecks"]):
        x, y = rng.randrange(size), rng.randrange(size)
        radius = rng.choice((1, 1, 1, 2, 2, 3))
        value = 128 + rng.choice((-1, 1)) * rng.randint(5, 18)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=value)
    for _ in range(spec["scratches"]):
        x, y = rng.randrange(size), rng.randrange(size)
        angle = rng.uniform(-0.25, 0.25) if rng.random() < 0.6 else rng.uniform(1.25, 1.9)
        length = rng.randint(max(10, size // 60), max(28, size // 8))
        x2 = x + math.cos(angle) * length
        y2 = y + math.sin(angle) * length
        value = 128 + rng.choice((-1, 1)) * rng.randint(5, 13)
        draw.line((x, y, x2, y2), fill=value, width=rng.choice((1, 1, 2)))
    result = add_neutral(result, material.filter(ImageFilter.GaussianBlur(0.35)))

    if spec["folds"]:
        folds = Image.new("L", (size, size), 128)
        draw = ImageDraw.Draw(folds)
        for index in range(spec["folds"]):
            if index % 2 == 0:
                x = rng.randint(size // 4, size * 3 // 4)
                draw.line((x, 0, x, size), fill=121, width=max(1, size // 190))
                draw.line((x + size // 100, 0, x + size // 100, size), fill=134, width=max(1, size // 220))
            else:
                y = rng.randint(size // 4, size * 3 // 4)
                draw.line((0, y, size, y), fill=123, width=max(1, size // 210))
                draw.line((0, y + size // 110, size, y + size // 110), fill=133, width=max(1, size // 230))
        result = add_neutral(result, folds.filter(ImageFilter.GaussianBlur(size / 120)))

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", help="build one profile ID; default builds all")
    parser.add_argument("--size", type=int, default=768)
    args = parser.parse_args()
    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    profiles = [item for item in data["profiles"] if not args.profile or item["id"] == args.profile]
    if not profiles:
        raise SystemExit(f"unknown profile: {args.profile}")
    for profile in profiles:
        output = ROOT / profile["asset"]
        output.parent.mkdir(parents=True, exist_ok=True)
        build(profile, args.size).save(output, optimize=True)
        print(f"{profile['id']}: {output}")


if __name__ == "__main__":
    main()
