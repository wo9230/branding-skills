#!/usr/bin/env python3
"""Create a brand-project workspace outside the installed Skill directories."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path

import brandlib


MODULE_ORDER = tuple(brandlib.MODULE_STAGES)
PART_MARK = "<!-- part:{part} -->"
SEGMENT_MARK = "<!-- segment:{segment} part:{part} -->"
JOURNEY_ASSETS = Path("skills/brand-journey/assets")
HANDOFF_ASSETS = Path("skills/brand-handoff/assets")


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def split_parts(text: str) -> tuple[str, dict[str, str]]:
    """Split the generic questionnaire into its preamble and its marked parts."""
    positions = [(text.index(PART_MARK.format(part=part)), part) for part in brandlib.PART_LABELS]
    parts: dict[str, str] = {}
    for index, (start, part) in enumerate(positions):
        end = positions[index + 1][0] if index + 1 < len(positions) else len(text)
        parts[part] = text[start:end]
    return text[: positions[0][0]], parts


def pack_questions(pack_text: str) -> dict[str, str]:
    """Return the question list under each group of a segment pack's last section."""
    number = len(brandlib.SEGMENT_HEADINGS)
    section = pack_text.split(f"## {number}. {brandlib.SEGMENT_HEADINGS[-1]}", 1)[1]
    groups: dict[str, str] = {}
    for part, label in brandlib.PART_LABELS.items():
        _, found, body = section.partition(f"### {label}")
        if found:
            groups[part] = re.split(r"^#{2,3} ", body, maxsplit=1, flags=re.M)[0].strip()
    return groups


def build_questionnaire(repo_root: Path, segment: str | None, modules: list[str]) -> str:
    """Assemble the client questionnaire: core part, selected modules, segment add-ons."""
    template = (repo_root / JOURNEY_ASSETS / "CLIENT-QUESTIONNAIRE.md").read_text(encoding="utf-8")
    preamble, parts = split_parts(template)
    extra: dict[str, str] = {}
    if segment and segment != brandlib.GENERIC_SEGMENT:
        pack = repo_root / brandlib.SEGMENTS_DIR / brandlib.read_segment_index(repo_root)[segment]
        extra = pack_questions(pack.read_text(encoding="utf-8"))

    chunks = [preamble.rstrip()]
    for part in ("core", *modules):
        chunks.append(parts[part].rstrip())
        if extra.get(part):
            mark = SEGMENT_MARK.format(segment=segment, part=part)
            chunks.append(f"{mark}\n\n### 关于您这一行的几个问题\n\n{extra[part]}")
    return "\n\n".join(chunks) + "\n"


def build_progress(repo_root: Path, segment: str | None, modules: list[str]) -> str:
    """Fill the progress template with the chosen segment and modules."""
    text = (repo_root / JOURNEY_ASSETS / "PROGRESS-TEMPLATE.md").read_text(encoding="utf-8")
    if segment:
        text = text.replace(f"segment: {brandlib.UNKNOWN_SEGMENT}", f"segment: {segment}", 1)
    text = text.replace("modules: []", f"modules: [{', '.join(modules)}]", 1)
    text = text.replace("updated: YYYY-MM-DD", f"updated: {date.today().isoformat()}", 1)
    for module in modules:
        for stage in brandlib.MODULE_STAGES[module]:
            row = f"| {stage} | {brandlib.STAGE_NAMES[stage]} | not-selected |"
            if row not in text:
                raise SystemExit(f"progress template has no '{row}' row")
            text = text.replace(row, f"| {stage} | {brandlib.STAGE_NAMES[stage]} | pending |", 1)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an isolated brand project with intake files and a progress tracker."
    )
    parser.add_argument("destination", help="New project directory")
    parser.add_argument(
        "--segment",
        help="Client type, if already known: a registered segment pack id or 'generic'",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=MODULE_ORDER,
        default=[],
        help="Optional modules to open in addition to the required stages",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    destination = Path(args.destination).expanduser().resolve()
    modules = [module for module in MODULE_ORDER if module in args.modules]

    # Validate everything before creating anything, so a bad argument leaves no folder behind.
    valid_segments = sorted({*brandlib.read_segment_index(repo_root), brandlib.GENERIC_SEGMENT})
    if args.segment and args.segment not in valid_segments:
        parser.error(
            f"unknown segment '{args.segment}'; choose one of: {', '.join(valid_segments)}"
        )
    if destination == repo_root or is_relative_to(destination, repo_root):
        parser.error("destination must be outside the branding-skills repository")
    if destination.exists() and any(destination.iterdir()):
        parser.error("destination already exists and is not empty")

    progress = build_progress(repo_root, args.segment, modules)
    questionnaire = build_questionnaire(repo_root, args.segment, modules)

    (destination / "intake").mkdir(parents=True, exist_ok=True)
    (destination / "sources").mkdir()
    (destination / "reports").mkdir()
    (destination / "output").mkdir()

    workbook = repo_root / "skills" / "brand-foundation" / "assets" / "BRAND-WORKBOOK.md"
    shutil.copy2(workbook, destination / "intake" / "BRAND-WORKBOOK.md")
    shutil.copy2(repo_root / HANDOFF_ASSETS / "AGENTS-TEMPLATE.md", destination / "AGENTS.md")
    (destination / "PROGRESS.md").write_text(progress, encoding="utf-8")
    (destination / "intake" / "CLIENT-QUESTIONNAIRE.md").write_text(questionnaire, encoding="utf-8")

    readme = destination / "README.md"
    readme.write_text(
        "# Brand Project\n\n"
        "这是一个独立品牌项目，不属于 branding-skills 仓库。\n\n"
        "- `AGENTS.md`：给 AI 的指路文件，任何 AI 进入这个文件夹先读它。\n"
        "- `PROGRESS.md`：访谈进度。用 `$brand-journey` 开始或继续访谈，它会从这里续接。\n"
        "- `intake/CLIENT-QUESTIONNAIRE.md`：可以发给客户预填的问卷。\n"
        "- `intake/BRAND-WORKBOOK.md`：自己分次填写的工作簿，可以不用。\n"
        "- 在 `sources/` 保存已获授权并完成必要脱敏的资料。\n"
        "- 根目录的 `BRAND.md` 是唯一品牌真源，由 `$brand-journey` 或 `$brand-foundation` 生成。\n"
        "- `MESSAGING.md`、`COMPANY.md`、`SITE-BRIEF.md`、`reports/` 和 `output/` 都是派生物。\n"
        "- 不要保存认证凭据或未经授权的私人材料。\n",
        encoding="utf-8",
    )

    print(f"Created brand project: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
