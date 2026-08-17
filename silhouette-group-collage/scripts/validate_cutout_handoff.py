#!/usr/bin/env python3
"""Validate a Human Cutout Engine handoff before collage composition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--alpha", type=Path, required=True)
    parser.add_argument("--rgba", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def fail(message: str) -> None:
    raise SystemExit(f"HANDOFF FAIL: {message}")


def main() -> None:
    args = parse_args()
    for path in (args.source, args.alpha, args.rgba, args.manifest):
        if not path.is_file():
            fail(f"missing file: {path}")

    source = np.asarray(Image.open(args.source).convert("RGB"))
    alpha = np.asarray(Image.open(args.alpha).convert("L"))
    rgba = np.asarray(Image.open(args.rgba).convert("RGBA"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    height, width = source.shape[:2]
    if alpha.shape != (height, width):
        fail(f"Alpha dimensions {alpha.shape[::-1]} do not match source {(width, height)}")
    if rgba.shape[:2] != (height, width):
        fail(f"RGBA dimensions {rgba.shape[1::-1]} do not match source {(width, height)}")
    if not np.array_equal(source, rgba[:, :, :3]):
        fail("RGBA RGB channels are not byte-identical to the source")
    if not np.array_equal(alpha, rgba[:, :, 3]):
        fail("standalone Alpha does not match the RGBA alpha channel")
    if not bool(manifest.get("rgb_lock_passed", False)):
        fail("manifest does not report rgb_lock_passed: true")

    manifest_width = manifest.get("width")
    manifest_height = manifest.get("height")
    if manifest_width is not None and int(manifest_width) != width:
        fail("manifest width does not match source")
    if manifest_height is not None and int(manifest_height) != height:
        fail("manifest height does not match source")

    foreground_fraction = float(np.count_nonzero(alpha)) / float(alpha.size)
    if foreground_fraction <= 0.0:
        fail("Alpha contains no subject pixels")

    if "count_gate_passed" in manifest and not bool(manifest["count_gate_passed"]):
        fail("manifest reports count_gate_passed: false")
    if args.expected_count is not None:
        detected = manifest.get("detected_count")
        recorded_expected = manifest.get("expected_count")
        if detected is None:
            fail("expected-count was supplied but manifest has no detected_count")
        if int(detected) != args.expected_count:
            fail(f"detected_count {detected} does not match expected {args.expected_count}")
        if recorded_expected is not None and int(recorded_expected) != args.expected_count:
            fail(
                f"manifest expected_count {recorded_expected} does not match requested "
                f"{args.expected_count}"
            )

    report = {
        "handoff_passed": True,
        "source": str(args.source.resolve()),
        "alpha": str(args.alpha.resolve()),
        "rgba": str(args.rgba.resolve()),
        "manifest": str(args.manifest.resolve()),
        "width": width,
        "height": height,
        "foreground_fraction_nonzero": round(foreground_fraction, 8),
        "rgb_lock_passed": True,
        "alpha_lock_passed": True,
        "count_gate_passed": manifest.get("count_gate_passed"),
        "expected_count": args.expected_count,
        "detected_count": manifest.get("detected_count"),
        "manual_visual_review_required": True,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
