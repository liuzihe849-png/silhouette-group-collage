#!/usr/bin/env python3
"""Build five deterministic, quiet and tintable paper texture tiles."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "assets/design-system/paper-texture-profiles.json"


def noise_field(size: int, sigma: float, rng: random.Random) -> Image.Image:
    data = bytes(max(0, min(255, round(128 + rng.gauss(0, sigma)))) for _ in range(size * size))
    return Image.frombytes("L", (size, size), data)


def add_microdots(draw: ImageDraw.ImageDraw, size: int, rng: random.Random, light: int, dark: int) -> None:
    for count, sign in ((light, 1), (dark, -1)):
        for _ in range(count):
            draw.point((rng.randrange(size), rng.randrange(size)), fill=128 + sign * rng.randint(5, 18))


def build_soft_fibre(spec: dict, size: int, rng: random.Random) -> Image.Image:
    result = noise_field(size, spec["base_grain_sigma"], rng)
    draw = ImageDraw.Draw(result)
    for _ in range(spec["fibre_count"]):
        x, y = rng.randrange(size), rng.randrange(size)
        length = rng.randint(*spec["fibre_length"])
        angle = rng.uniform(0, math.tau)
        bend = rng.uniform(-0.28, 0.28)
        delta = rng.randint(*spec["fibre_delta"])
        sign = 1 if rng.random() < 0.55 else -1
        points = []
        for step in range(4):
            t = step / 3
            local_angle = angle + bend * (t - 0.5)
            points.append((x + math.cos(local_angle) * length * t, y + math.sin(local_angle) * length * t))
        draw.line(points, fill=128 + sign * delta, width=1)
    add_microdots(draw, size, rng, spec["micro_light"], spec["micro_dark"])
    return result.filter(ImageFilter.GaussianBlur(0.22))


def build_fine_matte(spec: dict, size: int, rng: random.Random) -> Image.Image:
    raw = noise_field(size, spec["base_grain_sigma"], rng)
    result = Image.blend(raw, raw.filter(ImageFilter.GaussianBlur(spec["matte_blur_radius"])), 0.58)
    add_microdots(ImageDraw.Draw(result), size, rng, spec["micro_light"], spec["micro_dark"])
    return result


def build_speckle(spec: dict, size: int, rng: random.Random) -> Image.Image:
    result = noise_field(size, spec["base_grain_sigma"], rng)
    draw = ImageDraw.Draw(result)

    def flecks(count: int, light: bool, micro: bool = False) -> None:
        for _ in range(count):
            x, y = rng.randrange(size), rng.randrange(size)
            if micro:
                radius, delta = 0, rng.randint(5, 22)
            else:
                radius = rng.choices(range(1, spec["max_fleck_radius"] + 1), weights=[8, 5, 2, 1][:spec["max_fleck_radius"]])[0]
                delta = rng.randint(16, 72)
            value = 128 + delta if light else 128 - delta
            if radius == 0:
                draw.point((x, y), fill=value)
            else:
                vertices = rng.randint(5, 8)
                angles = sorted(rng.uniform(0, math.tau) for _ in range(vertices))
                points = []
                for angle in angles:
                    local_radius = radius * rng.uniform(0.55, 1.25)
                    points.append((x + math.cos(angle) * local_radius, y + math.sin(angle) * local_radius))
                draw.polygon(points, fill=value)

    def scratches(count: int, light: bool) -> None:
        for _ in range(count):
            x, y = rng.randrange(size), rng.randrange(size)
            angle = rng.uniform(-0.45, 0.45) if rng.random() < 0.72 else rng.uniform(1.15, 1.95)
            length = rng.randint(max(5, size // 120), max(15, size // 22))
            delta = rng.randint(18, 58)
            draw.line((x, y, x + math.cos(angle) * length, y + math.sin(angle) * length), fill=128 + delta if light else 128 - delta, width=rng.choice((1, 1, 1, 2)))

    flecks(spec["light_flecks"], True)
    flecks(spec["dark_flecks"], False)
    flecks(spec["micro_light"], True, True)
    flecks(spec["micro_dark"], False, True)
    scratches(spec["light_scratches"], True)
    scratches(spec["dark_scratches"], False)
    return result


def build(profile: dict, size: int) -> Image.Image:
    spec = profile["generator"]
    rng = random.Random(spec["seed"])
    builders = {"soft-fibre": build_soft_fibre, "fine-matte": build_fine_matte, "speckle": build_speckle}
    return builders[spec["mode"]](spec, size, rng)


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
