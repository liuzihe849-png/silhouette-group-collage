#!/usr/bin/env python3
"""Create a deterministic tactile paper-colour layer from a bundled texture."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageOps, ImageStat


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--texture", required=True, type=Path)
    parser.add_argument("--colour", required=True, type=parse_hex)
    parser.add_argument("--width", required=True, type=int)
    parser.add_argument("--height", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mask", type=Path)
    parser.add_argument("--strength", type=float, default=0.22)
    parser.add_argument("--grain", type=float, default=0.025)
    parser.add_argument("--seed", type=int, default=849)
    parser.add_argument("--min-luma-std", type=float, default=4.0)
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0:
        raise SystemExit("width and height must be positive")
    if not 0.05 <= args.strength <= 0.45:
        raise SystemExit("strength must be between 0.05 and 0.45")

    texture = Image.open(args.texture).convert("RGB")
    tiled = mirrored_tile(texture, (args.width, args.height))
    luma = ImageOps.grayscale(tiled)
    source_stats = ImageStat.Stat(luma)
    mean = float(source_stats.mean[0])
    standard = float(source_stats.stddev[0]) or 1.0
    rng = random.Random(args.seed)
    noise_bytes = bytes(
        max(0, min(255, int(128 + rng.gauss(0, args.grain * 255))))
        for _ in range(args.width * args.height)
    )
    noise = Image.frombytes("L", (args.width, args.height), noise_bytes)
    channels = []
    for base_channel in args.colour:
        lookup = []
        for value in range(256):
            normalized = max(-2.5, min(2.5, (value - mean) / standard))
            modulation = 1.0 + args.strength * normalized / 2.5
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
    if luma_std < args.min_luma_std:
        raise SystemExit(
            f"paper texture gate failed: luma std {luma_std:.2f} < {args.min_luma_std:.2f}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result_image.putalpha(alpha_image)
    result_image.save(args.output)
    manifest = {
        "texture": str(args.texture),
        "colour": "#" + "".join(f"{channel:02x}" for channel in args.colour),
        "size": [args.width, args.height],
        "strength": args.strength,
        "grain": args.grain,
        "luma_std": round(luma_std, 4),
        "texture_gate_passed": True,
    }
    args.output.with_suffix(".json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
