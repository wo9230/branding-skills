#!/usr/bin/env python3
"""Minimal dependency-free validation for the distributed Skills and segment packs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import brandlib


SKILL_NAMES = ("brand-foundation", "brand-expression", "brand-visual-board", "brand-journey")
MAX_SKILL_LINES = 120
RESERVED_SEGMENTS = (brandlib.GENERIC_SEGMENT, brandlib.UNKNOWN_SEGMENT)
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.S)


def frontmatter_value(body: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", body, re.M)
    return match.group(1).strip() if match else None


def validate_pack(path: Path) -> list[str]:
    """Check one segment pack: eight fixed sections, three questionnaire groups."""
    name = path.name
    lines = [line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()]
    expected = [
        f"## {number}. {title}"
        for number, title in enumerate(brandlib.SEGMENT_HEADINGS, start=1)
    ]
    level_two = [line for line in lines if line.startswith("## ")]

    failures = [f"{name}: expected '{heading}'" for heading in expected if heading not in level_two]
    if not failures and level_two != expected:
        failures.append(
            f"{name}: level-two headings must be exactly the {len(expected)} sections, in order"
        )

    last = expected[-1]
    if last in lines:
        section = lines[lines.index(last) + 1:]
        for offset, line in enumerate(section):
            if line.startswith("## "):
                section = section[:offset]
                break
        groups = [line for line in section if line.startswith("### ")]
        wanted = [f"### {label}" for label in brandlib.PART_LABELS.values()]
        if groups != wanted:
            failures.append(f"{name}: section 8 must contain {', '.join(wanted)} in order")
    return failures


def validate_segments(root: Path) -> list[str]:
    """Check the segment registry against the pack files next to it."""
    directory = root / brandlib.SEGMENTS_DIR
    try:
        index = brandlib.read_segment_index(root)
    except FileNotFoundError:
        return [f"segments index missing: {(brandlib.SEGMENTS_DIR / 'INDEX.md').as_posix()}"]

    failures: list[str] = []
    for segment, file_name in index.items():
        if segment in RESERVED_SEGMENTS:
            failures.append(f"reserved segment id: {segment}")
        elif file_name != f"{segment}.md":
            failures.append(f"segment id must match file name: {segment}")
        elif not (directory / file_name).is_file():
            failures.append(f"segment file missing: {file_name}")
        else:
            failures.extend(validate_pack(directory / file_name))

    registered = set(index.values())
    for path in sorted(directory.glob("*.md")):
        if path.name != "INDEX.md" and path.name not in registered:
            failures.append(f"unregistered segment pack: {path.name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate distributed Skill entrypoints")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    failures: list[str] = []

    for expected_name in SKILL_NAMES:
        path = root / "skills" / expected_name / "SKILL.md"
        if not path.is_file():
            failures.append(f"missing {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            failures.append(f"missing YAML frontmatter: {path.relative_to(root)}")
            continue
        name = frontmatter_value(match.group("body"), "name")
        description = frontmatter_value(match.group("body"), "description")
        if name != expected_name:
            failures.append(f"name mismatch in {path.relative_to(root)}: {name!r}")
        if not description or len(description) < 40:
            failures.append(f"description is missing or too vague: {path.relative_to(root)}")
        if any(marker in text for marker in ("TODO", "PLACEHOLDER", "Example Skill")):
            failures.append(f"unfinished scaffold marker: {path.relative_to(root)}")
        if len(text.splitlines()) > MAX_SKILL_LINES:
            failures.append(f"{path.relative_to(root)}: exceeds {MAX_SKILL_LINES} lines")

        metadata = root / "skills" / expected_name / "agents" / "openai.yaml"
        if not metadata.is_file():
            failures.append(f"missing UI metadata: {metadata.relative_to(root)}")

    segment_failures = validate_segments(root)
    failures.extend(segment_failures)

    if failures:
        print("SKILL VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    packs = len(brandlib.read_segment_index(root))
    print(f"SKILL VALIDATION PASSED: {len(SKILL_NAMES)} skills, {packs} segment packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
