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


import brandlib  # noqa: E402  needs scripts/ on sys.path, set above
import validate_skills  # noqa: E402


def make_skill_tree(root: Path) -> Path:
    """Write a minimal valid entry for every distributed Skill under ``root``."""
    for name in validate_skills.SKILL_NAMES:
        write(
            root / "skills" / name / "SKILL.md",
            f"---\nname: {name}\n"
            "description: A minimal but valid fixture entry used only by the repository tests.\n"
            "---\n\n# Fixture\n",
        )
        write(root / "skills" / name / "agents" / "openai.yaml", "interface:\n  display_name: fixture\n")
    return root


def _pack_text() -> str:
    parts = ["# 细分包（测试夹具，虚构）\n"]
    for number, title in enumerate(brandlib.SEGMENT_HEADINGS, start=1):
        parts.append(f"\n## {number}. {title}\n\n夹具内容。\n")
    for label in brandlib.PART_LABELS.values():
        parts.append(f"\n### {label}\n\n- 夹具问题？\n")
    return "".join(parts)


# A segment pack that satisfies every structural rule.
PACK_OK = _pack_text()


def make_segments(
    root: Path, packs: dict[str, str], index_rows: dict[str, str] | None = None
) -> Path:
    """Write segment pack files and an INDEX.md; ``index_rows`` maps id to file name."""
    directory = root / brandlib.SEGMENTS_DIR
    for segment, text in packs.items():
        write(directory / f"{segment}.md", text)
    rows = index_rows if index_rows is not None else {segment: f"{segment}.md" for segment in packs}
    lines = ["# 细分包登记表", "", "| segment | 名称 | 识别信号摘要 | file |", "|---|---|---|---|"]
    lines += [f"| {segment} | 夹具 | 夹具 | {file_name} |" for segment, file_name in rows.items()]
    write(directory / "INDEX.md", "\n".join(lines) + "\n")
    return root
