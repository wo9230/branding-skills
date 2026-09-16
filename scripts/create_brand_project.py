#!/usr/bin/env python3
"""Create a brand-project workspace outside the installed Skill directories."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an isolated brand project with a blank intake workbook."
    )
    parser.add_argument("destination", help="New project directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    destination = Path(args.destination).expanduser().resolve()

    if destination == repo_root or is_relative_to(destination, repo_root):
        parser.error("destination must be outside the branding-skills repository")
    if destination.exists() and any(destination.iterdir()):
        parser.error("destination already exists and is not empty")

    (destination / "intake").mkdir(parents=True, exist_ok=True)
    (destination / "sources").mkdir()
    (destination / "reports").mkdir()
    (destination / "output").mkdir()

    workbook = repo_root / "skills" / "brand-foundation" / "assets" / "BRAND-WORKBOOK.md"
    shutil.copy2(workbook, destination / "intake" / "BRAND-WORKBOOK.md")

    readme = destination / "README.md"
    readme.write_text(
        "# Brand Project\n\n"
        "这是一个独立品牌项目，不属于 branding-skills 仓库。\n\n"
        "- 在 `intake/BRAND-WORKBOOK.md` 填写原始信息。\n"
        "- 在 `sources/` 保存已获授权并完成必要脱敏的资料。\n"
        "- 使用 `$brand-foundation` 生成根目录的 `BRAND.md`；它是唯一品牌真源。\n"
        "- `MESSAGING.md`、`reports/` 和 `output/` 都是派生物。\n"
        "- 不要保存认证凭据或未经授权的私人材料。\n",
        encoding="utf-8",
    )

    print(f"Created brand project: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
