#!/usr/bin/env python3
"""Build a deterministic torn-paper boundary mask for a photo/paper seam."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "assets/design-system/torn-seam-profile.json"


def build_mask(width: int, height: int, edge: str, seed: int, amplitude: int | None = None) -> tuple[Image.Image, dict]:
    config = json.loads(PROFILE.read_text(encoding="utf-8"))["defaults"]
    rng = random.Random(seed)
    calculated = round(width * config["amplitude_canvas_width_fraction"])
    amp = amplitude if amplitude is not None else max(config["minimum_amplitude_px"], min(config["maximum_amplitude_px"], calculated))
    baseline = height // 2
    points: list[tuple[float, float]] = [(0, baseline + rng.uniform(-amp * 0.25, amp * 0.25))]
    x = 0
    previous = points[0][1]
    while x < width:
        x = min(width, x + rng.randint(*config["segment_px"]))
        target = baseline + rng.triangular(-amp, amp, 0)
        y = previous * 0.38 + target * 0.62
        if rng.random() < 0.13:
            y += rng.choice((-1, 1)) * rng.uniform(amp * 0.35, amp * 0.8)
        y = max(baseline - amp, min(baseline + amp, y))
        points.append((x, y))
        previous = y

    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    if edge == "top":
        polygon = [(0, height), *points, (width, height)]
    else:
        polygon = [(0, 0), *points, (width, 0)]
    draw.polygon(polygon, fill=255)

    fibre_count = round(width / 1000 * rng.randint(*config["fibre_density_per_1000px"]))
    for _ in range(fibre_count):
        px = rng.randrange(width)
        nearest = min(points, key=lambda item: abs(item[0] - px))
        py = int(nearest[1])
        length = rng.randint(*config["fibre_length_px"])
        outward = -1 if edge == "top" else 1
        if rng.random() < 0.56:
            draw.line((px, py, px + rng.randint(-2, 2), py + outward * length), fill=rng.randint(150, 230), width=1)
        else:
            draw.line((px, py, px + rng.randint(-2, 2), py - outward * length), fill=rng.randint(20, 90), width=1)

    mask = mask.filter(ImageFilter.GaussianBlur(config["soften_radius_px"]))
    values = mask.histogram()
    total = width * height
    soft = sum(values[1:255]) / total
    manifest = {
        "size": [width, height], "edge": edge, "seed": seed, "amplitude_px": amp,
        "baseline_y": baseline, "point_count": len(points), "fibre_count": fibre_count,
        "soft_alpha_fraction": round(soft, 6), "shared_path_key": f"torn-seam-{seed}-{width}-{amp}"
    }
    return mask, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--edge", choices=("top", "bottom"), default="top")
    parser.add_argument("--seed", type=int, default=849)
    parser.add_argument("--amplitude", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.width < 64 or args.height < 32:
        raise SystemExit("torn seam canvas must be at least 64x32")
    mask, manifest = build_mask(args.width, args.height, args.edge, args.seed, args.amplitude)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    mask.save(args.output)
    args.output.with_suffix(".json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
