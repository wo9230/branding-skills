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


# --- A minimal, internally consistent client project (all content fictional) ---

_BRAND = """---
schema: brand-foundation/v2
brand_id: sample-fictional
brand_name: Sample
subject: company
market_model: b2b
stage: active
segment: export-b2b
operator: fictional-studio
record_status: working
version: 0.3
updated: 2025-01-10
fictional: true
---

# Sample BRAND（虚构）

## 4. 战略选择

| Decision ID | choice | decision_status | owner | date | reason | scope | formed_by | origin_ref |
|---|---|---|---|---|---|---|---|---|
| DEC-POSITIONING-001 | 给小批量买家做可追溯打样 | approved | fictional-owner | 2025-01-08 | 见访谈 | demo | ai-refined | SRC-001 |
| DEC-PRICE-001 | 网站不公开价格 | candidate | | | | demo | | |

## 6. 证据、冲突与未知

| Source ID | 文件/URL/记录 | 日期 |
|---|---|---|
| SRC-001 | intake/interview.md | 2025-01-05 |

| Claim ID | 主张 | fact_status | 来源与范围 | permission | 阻塞什么 |
|---|---|---|---|---|---|
| CLM-001 | 有一条打样线 | user-stated | SRC-001 | internal | 公开前需记录 |
"""

_MESSAGING = """---
schema: brand-expression/v1
brand_id: sample-fictional
message_status: working
version: 0.1
foundation_version: 0.3
fictional: true
---

# Sample MESSAGING（虚构）

| Copy ID | 公开表达/用途 | 来源 Claim/Decision ID | 来源状态 | permission | 放行结论与限制 |
|---|---|---|---|---|---|
| COPY-001 | 小批量也能追溯的打样 | DEC-POSITIONING-001 | approved | internal | approved-internal |
"""

_COMPANY = """---
schema: company-context/v1
brand_id: sample-fictional
foundation_file: BRAND.md
foundation_version: 0.3
messaging_version: 0.1
generated: 2025-01-11
fictional: true
---

# Sample 速读（虚构）

[已批准决策] 定位见 DEC-POSITIONING-001；证明见 CLM-001。
"""

_SITE_BRIEF = """---
schema: site-brief/v1
brand_id: sample-fictional
brief_status: working
foundation_file: BRAND.md
foundation_version: 0.3
messaging_version: 0.1
generated: 2025-01-11
language: en
primary_conversion: inquiry-form
platform: ""
fictional: true
---

# Sample 建站交接（虚构）

首页主信息用 COPY-001，证明用 CLM-001。
"""

# A v1 record: no segment or operator, seven-column decision table.
V1_BRAND_TEXT = """---
schema: brand-foundation/v1
brand_id: legacy-fictional
brand_name: Legacy
subject: company
market_model: b2b
stage: active
record_status: working
version: 0.1
updated: 2024-06-01
fictional: true
---

# Legacy BRAND（虚构）

| Decision ID | choice | decision_status | owner | date | reason | scope |
|---|---|---|---|---|---|---|
| DEC-POSITIONING-001 | 本地企业的应急印刷 | approved | fictional-owner | 2024-06-01 | 见访谈 | demo |

| Claim ID | 主张 | fact_status | 来源与范围 | permission | 阻塞什么 |
|---|---|---|---|---|---|
| CLM-001 | 当天可取件 | user-stated | 访谈 2024-05-30 | internal | 公开前需记录 |
"""


def _progress_text() -> str:
    text = repo_text("skills/brand-journey/assets/PROGRESS-TEMPLATE.md")
    for old, new in (
        ('brand_id: ""', "brand_id: sample-fictional"),
        ("segment: unknown", "segment: export-b2b"),
        ("modules: []", "modules: [execution, website]"),
        ('current_stage: "0"', 'current_stage: "7"'),
        ("| pending |", "| done |"),
        ("| not-selected |", "| done |"),
        ("## 关键决策\n", "## 关键决策\n\n- DEC-POSITIONING-001\n"),
    ):
        assert old in text, old
        text = text.replace(old, new)
    return text


def make_project(
    root: Path,
    *,
    remove: tuple[str, ...] | list[str] = (),
    edits: dict[str, list[tuple[str, str]]] | None = None,
) -> Path:
    """Write the default fictional project, drop ``remove``, then apply text ``edits``."""
    files = {
        "BRAND.md": _BRAND,
        "PROGRESS.md": _progress_text(),
        "MESSAGING.md": _MESSAGING,
        "COMPANY.md": _COMPANY,
        "SITE-BRIEF.md": _SITE_BRIEF,
    }
    for name in remove:
        del files[name]
    for name, replacements in (edits or {}).items():
        for old, new in replacements:
            assert old in files[name], f"{name}: {old!r} not found"
            files[name] = files[name].replace(old, new)
    for name, text in files.items():
        write(root / name, text)
    return root
