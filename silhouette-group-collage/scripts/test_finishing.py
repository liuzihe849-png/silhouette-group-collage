#!/usr/bin/env python3
"""Smoke-test deterministic paper and seam-lettering assets."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], check=True, cwd=ROOT)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="silhouette-finish-") as temporary:
        directory = Path(temporary)
        paper = directory / "paper.png"
        phrase = directory / "phrase.png"
        run(
            "scripts/apply_paper_texture.py",
            "--profile",
            "winter-wool-stock",
            "--colour",
            "#c94b3f",
            "--width",
            "1178",
            "--height",
            "700",
            "--output",
            str(paper),
        )
        run(
            "scripts/render_seam_phrase.py",
            "--text",
            "we found the blue",
            "--family",
            "T5",
            "--width",
            "1178",
            "--height",
            "190",
            "--ink",
            "#f4e7c8",
            "--background-colour",
            "#c94b3f",
            "--output",
            str(phrase),
        )

        paper_manifest = json.loads(paper.with_suffix(".json").read_text(encoding="utf-8"))
        phrase_manifest = json.loads(phrase.with_suffix(".json").read_text(encoding="utf-8"))
        if not paper_manifest.get("texture_gate_passed") or not paper_manifest.get("profile_gate_passed"):
            raise SystemExit("paper finish test failed")
        if paper_manifest.get("profile") != "winter-wool-stock":
            raise SystemExit("paper profile manifest failed")
        if not phrase_manifest.get("readability_gate_passed"):
            raise SystemExit("lettering finish test failed")
        if phrase_manifest.get("text") != "we found the blue":
            raise SystemExit("lettering spelling lock failed")
        if phrase_manifest["contrast_ratio"] < 3.0:
            raise SystemExit("lettering contrast gate failed")
        if Image.open(paper).size != (1178, 700) or Image.open(phrase).size != (1178, 190):
            raise SystemExit("finishing output dimensions failed")

    print("PASS: deterministic paper texture and readable seam lettering")


if __name__ == "__main__":
    main()
