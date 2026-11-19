"""Shared helpers for the repository tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"

# Tests import the helper scripts as modules (for example ``import brandlib``).
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def run_script(name: str, *args: str | Path) -> subprocess.CompletedProcess[str]:
    """Run ``scripts/<name>`` with the current interpreter and capture its output."""
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
        check=False,
        capture_output=True,
        text=True,
    )


def write(path: Path, text: str) -> Path:
    """Write UTF-8 text, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def repo_text(relative: str) -> str:
    """Return the text of a repository file given its repo-relative path."""
    return (REPO_ROOT / relative).read_text(encoding="utf-8")
