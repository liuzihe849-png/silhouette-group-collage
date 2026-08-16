#!/usr/bin/env python3
"""Run zero-dependency structural checks for silhouette-group-collage."""

from __future__ import annotations

import re
import sys
from pathlib import Path


EXPECTED_NAME = "silhouette-group-collage"
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/style-system.md",
    "references/prompt-recipes.md",
    "references/reference-breakdown.md",
    "references/person-preservation.md",
    "references/art-direction-qc.md",
    "references/adaptive-layout.md",
    "scripts/check_mask_coverage.py",
)
REQUIRED_SKILL_PHRASES = (
    "Count all people explicitly from left to right",
    "Preserve the exact person count",
    "Preserve original photographic texture",
    "add 8–12 sparse handmade stars",
    "scene-matched handwritten phrase",
    "Person pixel lock",
    "protected source pixels",
    "Do not redraw, beautify",
    "INVARIANT",
    "three scene-derived palette candidates",
    "controlled handwritten variation",
    "giant blob",
    "9:16",
    "Accept every source photo",
    "Never shrink, crop, reshape, or reposition a mask independently",
    "99.5%",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    if root.name != EXPECTED_NAME:
        fail(f"folder must be named {EXPECTED_NAME!r}, got {root.name!r}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            fail(f"missing required file: {relative}")

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(skill_text)
    if set(frontmatter) != {"name", "description"}:
        fail("SKILL.md frontmatter must contain only name and description")
    if frontmatter["name"] != EXPECTED_NAME:
        fail("frontmatter name does not match folder name")
    if not frontmatter["description"]:
        fail("frontmatter description is empty")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", frontmatter["name"]):
        fail("skill name must use lowercase letters, digits, and hyphens")

    skill_text_lower = skill_text.lower()
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase.lower() not in skill_text_lower:
            fail(f"SKILL.md is missing required rule: {phrase}")

    agent_text = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    if 'display_name: "剪影群像风格 Skill"' not in agent_text:
        fail("agents/openai.yaml has the wrong display name")
    if f"${EXPECTED_NAME}" not in agent_text:
        fail("default_prompt does not invoke the renamed skill")

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml"}
    )
    old_name = "reciprocal" + "-photo-cutout-collage"
    if old_name in combined:
        fail("old skill name remains in the package")
    if "TODO" in combined or "[TODO" in combined:
        fail("unfinished placeholder remains in the package")

    print(f"PASS: {EXPECTED_NAME}")
    art_text = (root / "references/art-direction-qc.md").read_text(encoding="utf-8").lower()
    for phrase in (
        "mask fidelity",
        "scene-derived palette selection",
        "controlled variation",
        "texture hierarchy",
        "decoration rhythm",
        "final rejection gate",
    ):
        if phrase not in art_text:
            fail(f"art-direction-qc.md is missing section: {phrase}")

    adaptive_text = (root / "references/adaptive-layout.md").read_text(encoding="utf-8").lower()
    for phrase in (
        "never reject a source",
        "coupled-transform invariant",
        "environment-led",
        "balanced group",
        "portrait-dense or selfie",
        "priority order",
        "coverage test",
    ):
        if phrase not in adaptive_text:
            fail(f"adaptive-layout.md is missing rule: {phrase}")

    print(f"PASS: {len(REQUIRED_FILES)} required files")
    print("PASS: metadata, references, person-pixel lock, adaptive occupancy layouts, coupled masks, 9:16 art direction, typography, palette, texture, and rejection rules")


if __name__ == "__main__":
    main()
