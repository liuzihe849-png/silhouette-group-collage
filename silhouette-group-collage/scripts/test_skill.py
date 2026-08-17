#!/usr/bin/env python3
"""Run zero-dependency structural checks for silhouette-group-collage."""

from __future__ import annotations

import re
import sys
import json
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
    "references/edge-refinement.md",
    "references/gold-standard-system.md",
    "references/human-cutout-handoff.md",
    "references/typography-system.md",
    "references/deterministic-finishing.md",
    "scripts/check_mask_coverage.py",
    "scripts/validate_cutout_handoff.py",
    "scripts/apply_paper_texture.py",
    "scripts/render_seam_phrase.py",
    "scripts/test_finishing.py",
    "assets/design-system/palettes.json",
    "assets/design-system/mask-edge-profile.json",
    "assets/design-system/typography-families.json",
    "assets/design-system/paper-textures/neutral-uncoated-paper.png",
    "assets/fonts/caveat-brush/CaveatBrush-Regular.ttf",
    "assets/fonts/caveat-brush/OFL.txt",
    "assets/fonts/kalam/Kalam-Regular.ttf",
    "assets/fonts/kalam/Kalam-Bold.ttf",
    "assets/fonts/kalam/OFL.txt",
    "assets/fonts/knewave/Knewave-Regular.ttf",
    "assets/fonts/knewave/OFL.txt",
    "assets/fonts/kaushan-script/KaushanScript-Regular.ttf",
    "assets/fonts/kaushan-script/OFL.txt",
    "assets/design-system/typography-reference/01-tall-dry-brush.png",
    "assets/design-system/typography-reference/02-casual-dry-script.png",
    "assets/design-system/typography-reference/03-chunky-rounded-marker.png",
    "assets/design-system/typography-reference/04-bold-motion-brush.png",
    "assets/design-system/typography-reference/05-wide-diary-brush.png",
    "assets/design-system/paper-textures/saffron-winter.png",
    "assets/design-system/paper-textures/icy-blue-cabin.png",
    "assets/design-system/paper-textures/plum-winter.png",
    "assets/design-system/paper-textures/teal-rhythm.png",
    "assets/design-system/paper-textures/crimson-team.png",
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
    "controlled word-to-word changes",
    "giant blob",
    "9:16",
    "Accept every source photo",
    "Never shrink, crop, reshape, or reposition a mask independently",
    "99.5%",
    "instance segmentation or matting",
    "1–3 pixels",
    "limit excess mask area",
    "gold-standard-system.md",
    "Invoke `$human-cutout-engine` before art direction",
    "validate_cutout_handoff.py",
    "accepted Human Cutout Engine Alpha",
    "necessary foreground context",
    "output width equal to the source pixel width",
    "do not default to 9:16",
    "typography-system.md",
    "named typography family",
    "apply_paper_texture.py",
    "render_seam_phrase.py",
    "Never accept image-generated final lettering",
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

    edge_text = (root / "references/edge-refinement.md").read_text(encoding="utf-8").lower()
    for phrase in (
        "instance-level person or object segmentation",
        "alpha matting",
        "depth discontinuity",
        "single design-mask workflow",
        "maximum excess",
    ):
        if phrase not in edge_text:
            fail(f"edge-refinement.md is missing rule: {phrase}")

    gold_text = (root / "references/gold-standard-system.md").read_text(encoding="utf-8").lower()
    for phrase in (
        "saffron winter horizon",
        "icy-blue cabin warmth",
        "plum winter company",
        "teal movement chain",
        "crimson dual-depth team",
        "original artworks remain private",
    ):
        if phrase not in gold_text:
            fail(f"gold-standard-system.md is missing recipe: {phrase}")

    print(f"PASS: {len(REQUIRED_FILES)} required files")
    typography_text = (root / "references/typography-system.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in (
        "tall dry brush",
        "casual dry script",
        "chunky rounded marker",
        "bold motion brush",
        "wide diary brush",
        "typography quality gate",
    ):
        if phrase not in typography_text:
            fail(f"typography-system.md is missing family or gate: {phrase}")

    typography_data = json.loads(
        (root / "assets/design-system/typography-families.json").read_text(
            encoding="utf-8"
        )
    )
    families = typography_data.get("families", [])
    if [family.get("id") for family in families] != ["T1", "T2", "T3", "T4", "T5"]:
        fail("typography-families.json must define T1 through T5 in order")
    for family in families:
        reference = family.get("reference")
        if not reference or not (root / reference).is_file():
            fail(f"typography family has a missing reference asset: {reference}")
        font = family.get("font")
        license_file = family.get("font_license")
        if not font or not (root / font).is_file():
            fail(f"typography family has a missing bundled font: {font}")
        if not license_file or not (root / license_file).is_file():
            fail(f"typography family has a missing font license: {license_file}")

    print("PASS: five reference-backed typography families")
    finishing_text = (root / "references/deterministic-finishing.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in (
        "deterministic compositing layers",
        "texture_gate_passed",
        "luma_std >= 4.0",
        "readability_gate_passed",
        "contrast ratio at least `3.0`",
        "never use generated lettering as the final copy",
    ):
        if phrase not in finishing_text:
            fail(f"deterministic-finishing.md is missing gate: {phrase}")
    handoff_text = (root / "references/human-cutout-handoff.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in (
        "exact source-to-rgba rgb lock",
        "exact alpha-to-rgba alpha agreement",
        "people + necessary foreground context",
        "coupled reciprocal use",
        "never ask image generation to estimate the people boundary again",
    ):
        if phrase not in handoff_text:
            fail(f"human-cutout-handoff.md is missing rule: {phrase}")

    print("PASS: metadata, Human Cutout Engine handoff, private-safe gold standards, reusable design assets, contour-tight reciprocal masks, person-pixel lock, retained foreground context, source-width default geometry, optional 9:16 art direction, reference-backed typography, palette, texture, and rejection rules")


if __name__ == "__main__":
    main()
