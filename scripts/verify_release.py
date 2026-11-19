#!/usr/bin/env python3
"""Deterministic checks for the public Branding Skills package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".txt",
    ".yaml",
    ".yml",
}

IGNORED_PARTS = {".git", "__pycache__"}

FORBIDDEN_PARTS = {
    ".venv",
    "node_modules",
    "dist",
    "data",
    "customers",
    "exports",
}

FORBIDDEN_SUFFIXES = {
    ".csv",
    ".db",
    ".doc",
    ".docx",
    ".dump",
    ".gif",
    ".jpeg",
    ".jpg",
    ".key",
    ".pdf",
    ".pem",
    ".png",
    ".sql",
    ".sqlite",
    ".webp",
    ".xlsx",
    ".zip",
}

REQUIRED_PUBLIC_FILES = {
    ".env.example",
    "CONTRIBUTING.md",
    "EXCLUDE.md",
    "LICENSE",
    "OSS-SCOPE.md",
    "README.md",
    "SECURITY-TODO.md",
    "SECURITY.md",
}

REQUIRED_SKILLS = {
    "brand-foundation",
    "brand-expression",
    "brand-visual-board",
    "brand-journey",
}

# Directories whose files must all be marked as synthetic, with the label used in failures.
SYNTHETIC_DIRECTORIES = (("examples", "example"), ("evals", "eval"))

PATTERNS = {
    "macOS absolute user path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    "Linux absolute home path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
    "Windows absolute user path": re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\\s]+", re.I),
    "OpenAI credential": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub credential": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", "NOTICE"}:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a sanitized Branding Skills release")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--deny-file",
        type=Path,
        help="Optional newline-delimited private terms file stored outside this repository",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures: list[str] = []
    forbidden_terms: set[str] = set()

    for name in sorted(REQUIRED_PUBLIC_FILES):
        if not (root / name).is_file():
            failures.append(f"missing public file: {name}")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if path.is_symlink():
            failures.append(f"symbolic link is not allowed: {relative}")
            continue
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            failures.append(f"excluded path: {relative}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"excluded file type: {relative}")
        if path.is_file() and path.name.startswith(".env") and path.name != ".env.example":
            failures.append(f"excluded environment file: {relative}")

    if args.deny_file:
        deny_file = args.deny_file.expanduser().resolve()
        if is_relative_to(deny_file, root):
            parser.error("--deny-file must be stored outside the repository")
        forbidden_terms = {
            line.strip()
            for line in deny_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }

    for skill_name in sorted(REQUIRED_SKILLS):
        skill_file = root / "skills" / skill_name / "SKILL.md"
        if not skill_file.is_file():
            failures.append(f"missing required skill: {skill_file.relative_to(root)}")

    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF-8 text file: {path.relative_to(root)}")
            continue

        relative = path.relative_to(root)
        for term in sorted(forbidden_terms):
            if term in text:
                failures.append(f"forbidden private term {term!r}: {relative}")
        for label, pattern in PATTERNS.items():
            if pattern.search(text) and relative != Path("scripts/verify_release.py"):
                failures.append(f"{label}: {relative}")

    for directory, label in SYNTHETIC_DIRECTORIES:
        for path in iter_text_files(root / directory):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8").lower()
            if "fictional" not in text and "虚构" not in text:
                failures.append(f"{label} lacks fictional marker: {path.relative_to(root)}")

    if failures:
        print("RELEASE CHECK FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    checked = sum(1 for _ in iter_text_files(root))
    print(f"RELEASE CHECK PASSED: {checked} text files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
