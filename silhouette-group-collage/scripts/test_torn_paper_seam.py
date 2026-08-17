#!/usr/bin/env python3
"""Smoke-test deterministic, restrained torn-paper seam masks."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="torn-seam-") as temporary:
        directory = Path(temporary)
        paths = []
        for name, edge in (("a", "top"), ("b", "top"), ("c", "bottom")):
            path = directory / f"{name}.png"
            subprocess.run([
                sys.executable, "scripts/build_torn_paper_seam.py", "--width", "1080", "--height", "96",
                "--edge", edge, "--seed", "849", "--output", str(path)
            ], cwd=ROOT, check=True, capture_output=True, text=True)
            paths.append(path)
        a, b, c = (Image.open(path).convert("L") for path in paths)
        if ImageChops.difference(a, b).getbbox() is not None:
            raise SystemExit("FAIL: same seed did not reproduce the seam")
        if ImageChops.difference(a, c).getbbox() is None:
            raise SystemExit("FAIL: top and bottom masks are identical")
        histogram = a.histogram()
        if sum(histogram[1:255]) == 0:
            raise SystemExit("FAIL: torn seam has no fibrous soft-alpha edge")
        if not 0.35 <= histogram[255] / (1080 * 96) <= 0.65:
            raise SystemExit("FAIL: torn seam paper coverage is not restrained")
    print("PASS: deterministic restrained torn-paper seam")


if __name__ == "__main__":
    main()
