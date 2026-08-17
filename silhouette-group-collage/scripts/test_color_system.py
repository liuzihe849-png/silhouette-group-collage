#!/usr/bin/env python3
"""Validate colour-system structure, contrast, and scene coverage."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "assets/design-system/color-system.json"
HEX = re.compile(r"^#[0-9A-F]{6}$")


def rgb(value: str) -> tuple[int, int, int]:
    value = value[1:]
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def luminance(value: str) -> float:
    result = []
    for channel in rgb(value):
        part = channel / 255
        result.append(part / 12.92 if part <= 0.04045 else ((part + 0.055) / 1.055) ** 2.4)
    return 0.2126 * result[0] + 0.7152 * result[1] + 0.0722 * result[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    swatches = data.get("anchors", []) + data.get("extensions", [])
    inks = {item["id"]: item for item in data.get("inks", [])}
    ids = [item.get("id") for item in swatches]
    if len(swatches) < 18 or len(ids) != len(set(ids)):
        fail("expected at least 18 unique colour tokens")
    required = {"shepherds-red", "hearth-smoke", "butter-yellow", "heirloom-linen"}
    if not required.issubset(ids):
        fail("four reference anchors are required")
    by_id = {item["id"]: item for item in swatches}
    expected = {
        "shepherds-red": "#8E372F",
        "hearth-smoke": "#BFC4B9",
        "butter-yellow": "#E8D297",
        "heirloom-linen": "#FFF9F3",
    }
    for token, value in expected.items():
        if by_id[token]["hex"] != value:
            fail(f"anchor {token} must remain {value}")
    for item in swatches + list(inks.values()):
        if not HEX.fullmatch(item["hex"]):
            fail(f"invalid hex for {item['id']}: {item['hex']}")
    for item in swatches:
        ink_id = item.get("recommended_ink")
        if ink_id not in inks:
            fail(f"missing recommended ink for {item['id']}")
        ratio = contrast(item["hex"], inks[ink_id]["hex"])
        if ratio < 3.0:
            fail(f"contrast below 3.0 for {item['id']} with {ink_id}: {ratio:.2f}")
    recipes = data.get("scene_recipes", {})
    if len(recipes) < 7:
        fail("expected seven scene routes")
    for scene, recipe in recipes.items():
        if len(recipe.get("preferred", [])) < 4:
            fail(f"scene {scene} needs four preferred candidates")
        unknown = set(recipe["preferred"] + recipe.get("avoid_dominant", [])) - set(ids)
        if unknown:
            fail(f"scene {scene} references unknown tokens: {sorted(unknown)}")
    print(f"PASS: {len(swatches)} tokens, {len(recipes)} scene routes, all text pairs >= 3.0")


if __name__ == "__main__":
    main()
