#!/usr/bin/env python3
"""Minimal dependency-free validation for the three distributed Skills."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKILL_NAMES = ("brand-foundation", "brand-expression", "brand-visual-board")
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.S)


def frontmatter_value(body: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", body, re.M)
    return match.group(1).strip() if match else None


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

        metadata = root / "skills" / expected_name / "agents" / "openai.yaml"
        if not metadata.is_file():
            failures.append(f"missing UI metadata: {metadata.relative_to(root)}")

    if failures:
        print("SKILL VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"SKILL VALIDATION PASSED: {len(SKILL_NAMES)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
