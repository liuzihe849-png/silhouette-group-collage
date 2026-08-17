#!/usr/bin/env python3
"""Validate all paper profiles, assets, selectors, and tinted outputs."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageStat

from select_scene_palette import texture_profile


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "assets/design-system/paper-texture-profiles.json"


def metrics(image: Image.Image) -> dict[str, float]:
    luma = ImageOps.grayscale(image)
    stat = ImageStat.Stat(luma)
    dx = float(ImageStat.Stat(ImageChops.difference(luma, ImageChops.offset(luma, 1, 0))).mean[0])
    dy = float(ImageStat.Stat(ImageChops.difference(luma, ImageChops.offset(luma, 0, 1))).mean[0])
    low = luma.filter(ImageFilter.GaussianBlur(max(2.0, min(image.size) / 42)))
    mean = float(stat.mean[0])
    standard = float(stat.stddev[0])
    histogram = luma.histogram()
    extreme = sum(count for value, count in enumerate(histogram) if value < mean - 2 * standard or value > mean + 2 * standard)
    return {
        "luma_std": standard,
        "high_frequency_mean": (dx + dy) / 2,
        "low_frequency_std": float(ImageStat.Stat(low).stddev[0]),
        "fleck_fraction": extreme / max(1, image.width * image.height),
        "directional_ratio_y_over_x": dy / max(dx, 0.0001),
    }


def main() -> None:
    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    profiles = data.get("profiles", [])
    if [item["id"] for item in profiles] != [
        "heirloom-linen", "field-fibre", "hearth-smoke-stock", "sun-faded-stock", "winter-wool-stock"
    ]:
        raise SystemExit("FAIL: expected five ordered paper profiles")
    colours = {
        "heirloom-linen": "#FFF9F3",
        "field-fibre": "#8E9A76",
        "hearth-smoke-stock": "#BFC4B9",
        "sun-faded-stock": "#E8D297",
        "winter-wool-stock": "#6F3E52",
    }
    routing_cases = [
        ({"family": "linen", "value": "very-light"}, "grass-garden", "heirloom-linen"),
        ({"family": "plum", "value": "dark-mid"}, "snow-winter", "winter-wool-stock"),
        ({"family": "teal", "value": "mid"}, "grass-garden", "field-fibre"),
        ({"family": "yellow", "value": "light"}, "grass-garden", "sun-faded-stock"),
        ({"family": "blue", "value": "mid"}, "grass-garden", "hearth-smoke-stock"),
    ]
    for item, scene, expected in routing_cases:
        actual = texture_profile(item, scene)
        if actual != expected:
            raise SystemExit(f"FAIL: texture route {item}/{scene} returned {actual}, expected {expected}")
    with tempfile.TemporaryDirectory(prefix="paper-profiles-") as temporary:
        directory = Path(temporary)
        for profile in profiles:
            asset = ROOT / profile["asset"]
            if not asset.is_file() or Image.open(asset).size != (768, 768):
                raise SystemExit(f"FAIL: missing or wrong-size profile asset: {profile['id']}")
            measured = metrics(Image.open(asset))
            for key, bounds in profile["asset_gate"].items():
                if not bounds[0] <= measured[key] <= bounds[1]:
                    raise SystemExit(f"FAIL: {profile['id']} {key}={measured[key]:.4f} outside {bounds}")
            output = directory / f"{profile['id']}.png"
            subprocess.run([
                sys.executable,
                "scripts/apply_paper_texture.py",
                "--profile", profile["id"],
                "--colour", colours[profile["id"]],
                "--width", "360", "--height", "480",
                "--output", str(output),
            ], cwd=ROOT, check=True, capture_output=True, text=True)
            manifest = json.loads(output.with_suffix(".json").read_text(encoding="utf-8"))
            if not manifest.get("texture_gate_passed") or not manifest.get("profile_gate_passed"):
                raise SystemExit(f"FAIL: output gate failed for {profile['id']}")
            if manifest.get("profile") != profile["id"]:
                raise SystemExit(f"FAIL: wrong manifest profile for {profile['id']}")
    print("PASS: five reference-derived paper profiles and tinted output gates")


if __name__ == "__main__":
    main()
