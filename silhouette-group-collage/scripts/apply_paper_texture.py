#!/usr/bin/env python3
"""Create a deterministic tactile paper-colour layer from a bundled texture."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "assets/design-system/paper-texture-profiles.json"


def parse_hex(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("colour must use six-digit hex, for example #c94b3f")
    try:
        return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("invalid hex colour") from exc


def mirrored_tile(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    width, height = size
    tile_w, tile_h = source.size
    canvas = Image.new("RGB", size)
    for y in range(0, height, tile_h):
        for x in range(0, width, tile_w):
            tile = source
            if (x // tile_w) % 2:
                tile = ImageOps.mirror(tile)
            if (y // tile_h) % 2:
                tile = ImageOps.flip(tile)
            canvas.paste(tile, (x, y))
    return canvas


def texture_metrics(image: Image.Image) -> dict[str, float]:
    luma = ImageOps.grayscale(image)
    stats = ImageStat.Stat(luma)
    difference_x = ImageChops.difference(luma, ImageChops.offset(luma, 1, 0))
    difference_y = ImageChops.difference(luma, ImageChops.offset(luma, 0, 1))
    dx = float(ImageStat.Stat(difference_x).mean[0])
    dy = float(ImageStat.Stat(difference_y).mean[0])
    low = luma.filter(ImageFilter.GaussianBlur(max(2.0, min(image.size) / 42)))
    mean = float(stats.mean[0])
    standard = float(stats.stddev[0])
    low_threshold = mean - 2 * standard
    high_threshold = mean + 2 * standard
    histogram = luma.histogram()
    total_pixels = image.width * image.height
    running = 0
    median = 128
    for value, count in enumerate(histogram):
        running += count
        if running >= total_pixels / 2:
            median = value
            break
    extreme = sum(count for value, count in enumerate(histogram) if value < low_threshold or value > high_threshold)
    total = max(1, total_pixels)
    deviation_gt_3 = sum(count for value, count in enumerate(histogram) if abs(value - median) > 3)
    light_gt_8 = sum(count for value, count in enumerate(histogram) if value - median > 8)
    dark_gt_8 = sum(count for value, count in enumerate(histogram) if median - value > 8)
    return {
        "luma_std": round(standard, 4),
        "high_frequency_mean": round((dx + dy) / 2, 4),
        "low_frequency_std": round(float(ImageStat.Stat(low).stddev[0]), 4),
        "fleck_fraction": round(extreme / total, 5),
        "directional_ratio_y_over_x": round(dy / max(dx, 0.0001), 4),
        "deviation_gt_3": round(deviation_gt_3 / total, 5),
        "light_deviation_gt_8": round(light_gt_8 / total, 5),
        "dark_deviation_gt_8": round(dark_gt_8 / total, 5),
    }


def profile_gate(metrics: dict[str, float], gate: dict[str, list[float]]) -> bool:
    return all(bounds[0] <= metrics[key] <= bounds[1] for key, bounds in gate.items())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--texture", type=Path)
    parser.add_argument("--profile", help="paper profile ID from paper-texture-profiles.json")
    parser.add_argument("--colour", required=True, type=parse_hex)
    parser.add_argument("--width", required=True, type=int)
    parser.add_argument("--height", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mask", type=Path)
    parser.add_argument("--strength", type=float)
    parser.add_argument("--grain", type=float)
    parser.add_argument("--seed", type=int, default=849)
    parser.add_argument("--min-luma-std", type=float)
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0:
        raise SystemExit("width and height must be positive")
    if args.texture and args.profile:
        raise SystemExit("choose --texture or --profile, not both")

    profile = None
    if args.profile:
        profile_data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        profile = next((item for item in profile_data["profiles"] if item["id"] == args.profile), None)
        if profile is None:
            available = ", ".join(item["id"] for item in profile_data["profiles"])
            raise SystemExit(f"unknown profile {args.profile!r}; choose: {available}")
        texture_path = ROOT / profile["asset"]
    elif args.texture:
        texture_path = args.texture
        if not texture_path.is_absolute():
            texture_path = ROOT / texture_path
    else:
        profile_data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        profile = next(item for item in profile_data["profiles"] if item["id"] == "soft-fibre-paper")
        texture_path = ROOT / profile["asset"]

    strength = args.strength if args.strength is not None else (profile["default_strength"] if profile else 0.22)
    grain = args.grain if args.grain is not None else (profile["default_grain"] if profile else 0.025)
    min_luma_std = args.min_luma_std if args.min_luma_std is not None else (profile["min_output_luma_std"] if profile else 4.0)
    if not 0.05 <= strength <= 0.45:
        raise SystemExit("strength must be between 0.05 and 0.45")
    if not texture_path.is_file():
        raise SystemExit(f"texture asset not found: {texture_path}; run build_paper_texture_library.py")

    texture = Image.open(texture_path).convert("RGB")
    source_metrics = texture_metrics(texture)
    profile_gate_passed = profile_gate(source_metrics, profile["asset_gate"]) if profile else True
    if not profile_gate_passed:
        raise SystemExit(f"paper profile asset gate failed for {profile['id']}: {source_metrics}")
    tiled = mirrored_tile(texture, (args.width, args.height))
    luma = ImageOps.grayscale(tiled)
    source_stats = ImageStat.Stat(luma)
    mean = float(source_stats.mean[0])
    standard = float(source_stats.stddev[0]) or 1.0
    rng = random.Random(args.seed)
    noise_bytes = bytes(
        max(0, min(255, int(128 + rng.gauss(0, grain * 255))))
        for _ in range(args.width * args.height)
    )
    noise = Image.frombytes("L", (args.width, args.height), noise_bytes)
    channels = []
    for base_channel in args.colour:
        lookup = []
        for value in range(256):
            normalized = max(-2.5, min(2.5, (value - mean) / standard))
            modulation = 1.0 + strength * normalized / 2.5
            lookup.append(max(0, min(255, int(base_channel * modulation))))
        channel = luma.point(lookup)
        channel = ImageChops.add(channel, noise, scale=1.0, offset=-128)
        channels.append(channel)
    result_image = Image.merge("RGB", channels)

    if args.mask:
        alpha_image = Image.open(args.mask).convert("L").resize(
            (args.width, args.height), Image.Resampling.LANCZOS
        )
    else:
        alpha_image = Image.new("L", (args.width, args.height), 255)
    output_luma = ImageOps.grayscale(result_image)
    luma_std = float(ImageStat.Stat(output_luma, mask=alpha_image).stddev[0])
    if luma_std < min_luma_std:
        raise SystemExit(
            f"paper texture gate failed: luma std {luma_std:.2f} < {min_luma_std:.2f}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result_image.putalpha(alpha_image)
    result_image.save(args.output)
    manifest = {
        "texture": str(texture_path),
        "profile": profile["id"] if profile else "custom-texture",
        "colour": "#" + "".join(f"{channel:02x}" for channel in args.colour),
        "size": [args.width, args.height],
        "strength": strength,
        "grain": grain,
        "luma_std": round(luma_std, 4),
        "minimum_luma_std": min_luma_std,
        "source_texture_metrics": source_metrics,
        "profile_gate_passed": profile_gate_passed,
        "texture_gate_passed": True,
    }
    args.output.with_suffix(".json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
