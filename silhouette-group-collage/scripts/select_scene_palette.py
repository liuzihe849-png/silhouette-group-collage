#!/usr/bin/env python3
"""Suggest three scene-aware paper colours from the bundled heritage system."""

from __future__ import annotations

import argparse
import colorsys
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PATH = ROOT / "assets/design-system/color-system.json"


def rgb(hex_value: str) -> tuple[int, int, int]:
    value = hex_value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def relative_luminance(hex_value: str) -> float:
    channels = []
    for channel in rgb(hex_value):
        value = channel / 255.0
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def hue(hex_value: str) -> float:
    r, g, b = (channel / 255.0 for channel in rgb(hex_value))
    return colorsys.rgb_to_hsv(r, g, b)[0]


def hue_distance(a: float, b: float) -> float:
    distance = abs(a - b)
    return min(distance, 1.0 - distance)


def colour_distance(a: str, b: str) -> float:
    ar, ag, ab = rgb(a)
    br, bg, bb = rgb(b)
    return math.sqrt((ar - br) ** 2 + (ag - bg) ** 2 + (ab - bb) ** 2) / 441.673


def analyse_source(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    image.thumbnail((96, 96), Image.Resampling.LANCZOS)
    quantized = image.quantize(colors=8, method=Image.Quantize.MEDIANCUT).convert("RGB")
    colours = quantized.getcolors(maxcolors=96 * 96) or []
    ranked = sorted(colours, reverse=True)
    total = max(1, sum(count for count, _ in ranked))
    dominant = [
        {"hex": "#%02X%02X%02X" % colour, "share": round(count / total, 4)}
        for count, colour in ranked[:6]
    ]
    weighted_hues: list[tuple[float, float]] = []
    for item in dominant:
        r, g, b = (channel / 255.0 for channel in rgb(item["hex"]))
        h, s, _ = colorsys.rgb_to_hsv(r, g, b)
        if s >= 0.08:
            weighted_hues.append((h, item["share"] * s))
    if weighted_hues:
        x = sum(math.cos(2 * math.pi * h) * weight for h, weight in weighted_hues)
        y = sum(math.sin(2 * math.pi * h) * weight for h, weight in weighted_hues)
        scene_hue = (math.atan2(y, x) / (2 * math.pi)) % 1.0
    else:
        scene_hue = 0.0
    average_luma = sum(relative_luminance(item["hex"]) * item["share"] for item in dominant)
    return {
        "width": Image.open(path).width,
        "height": Image.open(path).height,
        "dominant_colours": dominant,
        "scene_hue_degrees": round(scene_hue * 360, 1),
        "average_luminance": round(average_luma, 4),
    }


def select(path: Path, scene: str | None) -> dict[str, Any]:
    system = json.loads(SYSTEM_PATH.read_text(encoding="utf-8"))
    source = analyse_source(path)
    swatches = system["anchors"] + system["extensions"]
    by_id = {item["id"]: item for item in swatches}
    inks = {item["id"]: item for item in system["inks"]}
    source_hexes = [item["hex"] for item in source["dominant_colours"]]
    source_hue = source["scene_hue_degrees"] / 360.0

    recipe = system["scene_recipes"].get(scene) if scene else None
    preferred = set(recipe["preferred"]) if recipe else set()
    avoided = set(recipe["avoid_dominant"]) if recipe else set()

    def legibility(item: dict[str, Any]) -> float:
        return min(colour_distance(item["hex"], source_hex) for source_hex in source_hexes)

    def recipe_bias(item: dict[str, Any]) -> float:
        return (0.22 if item["id"] in preferred else 0.0) - (0.5 if item["id"] in avoided else 0.0)

    echo = max(
        swatches,
        key=lambda item: (1.0 - min(colour_distance(item["hex"], value) for value in source_hexes))
        + 0.45 * legibility(item)
        + recipe_bias(item),
    )
    counterpoint = max(
        swatches,
        key=lambda item: (1.0 - abs(hue_distance(hue(item["hex"]), source_hue) - 0.5) * 2.0)
        + 0.45 * legibility(item)
        + recipe_bias(item),
    )
    atmosphere_pool = [by_id[item] for item in recipe["preferred"]] if recipe else swatches
    atmosphere = max(
        atmosphere_pool,
        key=lambda item: 0.65 * legibility(item)
        + (0.35 if (relative_luminance(item["hex"]) < 0.42) != (source["average_luminance"] < 0.42) else 0.0)
        + recipe_bias(item),
    )

    chosen: list[dict[str, Any]] = []
    used: set[str] = set()
    for role, first in (("echo", echo), ("counterpoint", counterpoint), ("atmosphere", atmosphere)):
        item = first
        if item["id"] in used:
            alternatives = sorted(
                (candidate for candidate in swatches if candidate["id"] not in used),
                key=lambda candidate: legibility(candidate) + recipe_bias(candidate),
                reverse=True,
            )
            item = alternatives[0]
        used.add(item["id"])
        ink = inks[item["recommended_ink"]]
        chosen.append({
            "role": role,
            "token": item["id"],
            "name": item["name"],
            "paper_hex": item["hex"],
            "ink_token": ink["id"],
            "ink_hex": ink["hex"],
            "text_contrast": round(contrast(item["hex"], ink["hex"]), 2),
            "environment_separation": round(legibility(item), 3),
            "human_review_required": True,
        })

    return {
        "source": str(path.resolve()),
        "scene_route": scene or "unclassified",
        "scene_reason": recipe["reason"] if recipe else "No explicit route; compare all three candidates manually.",
        "source_analysis": source,
        "candidates": chosen,
        "selection_instruction": "Choose one after full-page mockup review; do not auto-accept the highest score.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--scene", choices=[
        "snow-winter", "sea-sky", "grass-garden", "warm-indoor",
        "city-neutral", "night-party", "sunset-road",
    ])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.source.is_file():
        raise SystemExit(f"source not found: {args.source}")
    result = select(args.source, args.scene)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
