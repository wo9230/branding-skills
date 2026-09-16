#!/usr/bin/env python3
"""Copy the synthetic example into an isolated demo workspace."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DEMO_FILES = ("SOURCE-MATERIAL.md", "BRAND.md", "MESSAGING.md")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a runnable Branding Skills demo from synthetic data."
    )
    parser.add_argument("--output", required=True, help="Empty demo output directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    fixture_root = repo_root / "examples" / "fictional-b2b"
    destination = Path(args.output).expanduser().resolve()

    if destination.exists() and any(destination.iterdir()):
        parser.error("demo output directory is not empty")

    for name in DEMO_FILES:
        source = fixture_root / name
        if not source.is_file():
            parser.error(f"missing synthetic fixture: {source.relative_to(repo_root)}")
        text = source.read_text(encoding="utf-8").lower()
        if "fictional: true" not in text and "虚构" not in text:
            parser.error(f"fixture is not marked as fictional: {source.relative_to(repo_root)}")

    destination.mkdir(parents=True, exist_ok=True)
    for name in DEMO_FILES:
        shutil.copy2(fixture_root / name, destination / name)

    print(f"DEMO PASSED: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
