#!/usr/bin/env python3
"""Render exact, readable seam lettering as a separate transparent layer."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]


def parse_hex(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("colour must use six-digit hex")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def relative_luminance(colour: tuple[int, int, int]) -> float:
    channels = []
    for channel in colour:
        value = channel / 255.0
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    high, low = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def measure(font: ImageFont.FreeTypeFont, text: str) -> tuple[int, int]:
    box = font.getbbox(text, stroke_width=0)
    return box[2] - box[0], box[3] - box[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--family", required=True, choices=["T1", "T2", "T3", "T4", "T5"])
    parser.add_argument("--width", required=True, type=int)
    parser.add_argument("--height", required=True, type=int)
    parser.add_argument("--ink", required=True, type=parse_hex)
    parser.add_argument("--background-colour", required=True, type=parse_hex)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=849)
    parser.add_argument("--min-contrast", type=float, default=3.0)
    args = parser.parse_args()

    phrase = " ".join(args.text.split())
    if not phrase or len(phrase.split()) > 6:
        raise SystemExit("phrase must contain 1–6 words")
    if args.width <= 0 or args.height <= 0:
        raise SystemExit("width and height must be positive")

    config = json.loads(
        (ROOT / "assets/design-system/typography-families.json").read_text(encoding="utf-8")
    )
    family = next(item for item in config["families"] if item["id"] == args.family)
    font_path = ROOT / family["font"]
    if not font_path.is_file():
        raise SystemExit(f"missing bundled font: {font_path}")

    contrast = contrast_ratio(args.ink, args.background_colour)
    if contrast < args.min_contrast:
        raise SystemExit(
            f"lettering contrast gate failed: {contrast:.2f} < {args.min_contrast:.2f}"
        )

    scale = 4
    width, height = args.width * scale, args.height * scale
    target_fraction = sum(family["recommended_width_fraction"]) / 2
    target_width = int(width * target_fraction)
    max_height = int(height * 0.76)
    words = phrase.split()
    rng = random.Random(args.seed)

    low, high = 12 * scale, max(13 * scale, int(height * 0.72))
    chosen = low
    while low <= high:
        size = (low + high) // 2
        font = ImageFont.truetype(str(font_path), size)
        widths = [measure(font, word)[0] for word in words]
        gap = max(int(size * 0.20), 4 * scale)
        total = sum(widths) + gap * (len(words) - 1)
        word_height = max(measure(font, word)[1] for word in words)
        if total <= target_width and word_height <= max_height:
            chosen = size
            low = size + 1
        else:
            high = size - 1

    font = ImageFont.truetype(str(font_path), chosen)
    gap = max(int(chosen * 0.20), 4 * scale)
    rendered_words: list[Image.Image] = []
    rotations: list[float] = []
    for index, word in enumerate(words):
        word_width, word_height = measure(font, word)
        pad = int(chosen * 0.32)
        layer = Image.new("L", (word_width + pad * 2, word_height + pad * 2), 0)
        draw = ImageDraw.Draw(layer)
        box = font.getbbox(word)
        draw.text((pad - box[0], pad - box[1]), word, font=font, fill=255)
        angle_limit = family.get("rotation_degrees", 2.0)
        angle = rng.uniform(-angle_limit, angle_limit)
        if len(words) == 1:
            angle = 0.0
        layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        rendered_words.append(layer)
        rotations.append(round(angle, 3))

    total_width = sum(layer.width for layer in rendered_words) + gap * (len(words) - 1)
    if total_width > int(width * 0.94):
        factor = int(width * 0.94) / total_width
        rendered_words = [
            layer.resize((max(1, int(layer.width * factor)), max(1, int(layer.height * factor))), Image.Resampling.LANCZOS)
            for layer in rendered_words
        ]
        total_width = sum(layer.width for layer in rendered_words) + gap * (len(words) - 1)

    alpha = Image.new("L", (width, height), 0)
    x = (width - total_width) // 2
    baseline = height // 2
    boxes = []
    for index, layer in enumerate(rendered_words):
        baseline_shift = int(rng.uniform(-0.035, 0.035) * height)
        y = baseline - layer.height // 2 + baseline_shift
        alpha.paste(layer, (x, y), layer)
        boxes.append([x, y, x + layer.width, y + layer.height])
        x += layer.width + gap

    ink_rng = random.Random(args.seed + 1)
    ink_noise = Image.frombytes(
        "L",
        alpha.size,
        bytes(ink_rng.randint(224, 255) for _ in range(alpha.width * alpha.height)),
    )
    alpha = ImageChops.multiply(alpha, ink_noise)

    bbox = alpha.getbbox()
    if bbox is None:
        raise SystemExit("lettering render is empty")
    width_fraction = (bbox[2] - bbox[0]) / width
    height_fraction = (bbox[3] - bbox[1]) / height
    if width_fraction < 0.58 or height_fraction < 0.20:
        raise SystemExit(
            f"lettering scale gate failed: width={width_fraction:.3f}, height={height_fraction:.3f}"
        )

    rgba = Image.new("RGBA", (width, height), (*args.ink, 0))
    rgba.putalpha(alpha)
    rgba = rgba.resize((args.width, args.height), Image.Resampling.LANCZOS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(args.output)

    manifest = {
        "text": phrase,
        "family": args.family,
        "family_name": family["family"],
        "font": family["font"],
        "size": [args.width, args.height],
        "ink": "#" + "".join(f"{channel:02x}" for channel in args.ink),
        "background_colour": "#" + "".join(
            f"{channel:02x}" for channel in args.background_colour
        ),
        "contrast_ratio": round(contrast, 4),
        "width_fraction": round(width_fraction, 4),
        "height_fraction": round(height_fraction, 4),
        "rotations": rotations,
        "spelling_locked": True,
        "readability_gate_passed": True,
    }
    args.output.with_suffix(".json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
