#!/usr/bin/env python3
"""Copy the synthetic example into an isolated demo workspace and self-check it."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from check_brand_project import check_project


DEMO_FILES = (
    "SOURCE-MATERIAL.md",
    "AGENTS.md",
    "PROGRESS.md",
    "BRAND.md",
    "MESSAGING.md",
    "COMPANY.md",
    "SITE-BRIEF.md",
    "reports/2025-01-15-client-confirmation.md",
    "reports/2025-01-20-consistency-audit.md",
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a runnable Branding Skills demo from synthetic data."
    )
    parser.add_argument("--output", required=True, help="Empty demo output directory")
    parser.add_argument(
        "--fixture",
        help="Example directory to copy; defaults to examples/fictional-b2b",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    if args.fixture:
        fixture_root = Path(args.fixture).expanduser().resolve()
    else:
        fixture_root = repo_root / "examples" / "fictional-b2b"
    destination = Path(args.output).expanduser().resolve()

    if destination.exists() and any(destination.iterdir()):
        parser.error("demo output directory is not empty")

    for name in DEMO_FILES:
        source = fixture_root / name
        if not source.is_file():
            parser.error(f"missing synthetic fixture: {name}")
        text = source.read_text(encoding="utf-8").lower()
        if "fictional: true" not in text and "虚构" not in text:
            parser.error(f"fixture is not marked as fictional: {name}")

    destination.mkdir(parents=True, exist_ok=True)
    for name in DEMO_FILES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fixture_root / name, target)

    errors, warnings, checked = check_project(destination, repo_root)
    for error in errors:
        print(f"- ERROR: {error}")
    for warning in warnings:
        print(f"- WARN: {warning}")
    if errors:
        print(f"DEMO FAILED: the copied example does not pass the project check ({destination})")
        return 1

    print(f"DEMO PASSED: {destination}")
    print(f"Project check: {checked} files checked, {len(warnings)} warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
