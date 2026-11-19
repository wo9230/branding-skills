#!/usr/bin/env python3
"""Shared vocabulary and Markdown parsing for the Branding Skills helper scripts.

The stage ids, status values, and column names defined here are the same
tokens the Skill reference files use. Contract tests keep the two in step.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator


REQUIRED_STAGES = ("0", "1", "2", "3", "4", "5", "6", "7")
GATE_STAGES = ("4", "7")
MODULE_STAGES = {"execution": ("E1", "E2"), "website": ("W1",)}
STAGE_NAMES = {
    "0": "立项与预读",
    "1": "业务现状",
    "2": "客户与成交场景",
    "3": "竞争与替代",
    "4": "诊断与定位",
    "5": "证明与信任",
    "6": "身份、声音与品牌表述",
    "7": "汇总确认",
    "E1": "产品与价格",
    "E2": "渠道与推广",
    "W1": "网站目标与约束",
}
STAGE_STATUSES = ("pending", "in-progress", "awaiting-evidence", "done", "not-selected")
STAGE_STATUS_PREFIXES = ("deferred: ", "skipped: ")

FORMED_BY = ("client-original", "ai-refined", "co-edited")
NEW_DECISION_PREFIXES = (
    "DEC-DIAGNOSIS",
    "DEC-POLICY",
    "DEC-PRICE",
    "DEC-CHANNEL",
    "DEC-PROMO",
    "DEC-GOAL",
    "DEC-SITE",
)
STATEMENT_PREFIXES = (
    "DEC-DIAGNOSIS",
    "DEC-POLICY",
    "DEC-POSITIONING",
    "DEC-AUDIENCE",
    "DEC-MESSAGE",
    "DEC-VOICE",
)
SCHEMAS = {
    "BRAND.md": ("brand-foundation/v1", "brand-foundation/v2"),
    "MESSAGING.md": ("brand-expression/v1",),
    "COMPANY.md": ("company-context/v1",),
    "SITE-BRIEF.md": ("site-brief/v1",),
    "PROGRESS.md": ("brand-journey-progress/v1",),
}

FRONTMATTER = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?(?:\n|\Z)", re.S)
# Python treats CJK characters as word characters, so "\b" finds no boundary
# in text such as "见DEC-PRICE-001"; lookarounds on ASCII id characters do.
ID_PATTERN = re.compile(
    r"(?<![A-Za-z0-9-])(?:DEC-[A-Z]+-\d{3}|CLM-\d{3}|SRC-\d{3}|COPY-\d{3})(?![0-9])"
)
TRAILING_COMMENT = re.compile(r"\s+#")
SEPARATOR_CELL = re.compile(r":?-+:?")
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return the flat ``key: value`` pairs of a leading YAML frontmatter block."""
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for raw in match.group("body").splitlines():
        if not raw.strip() or raw[0] in " \t-#" or ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        value = value.strip()
        if value and value[0] not in "\"'":
            value = TRAILING_COMMENT.split(value, maxsplit=1)[0]
        values[key.strip()] = _unquote(value)
    return values


def parse_inline_list(value: str) -> list[str]:
    """Turn an inline YAML list such as ``[a, b]`` into ``["a", "b"]``."""
    inner = value.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    return [_unquote(item.strip()) for item in inner.split(",") if item.strip()]


def version_tuple(value: str) -> tuple[int, ...]:
    """Convert ``"0.10"`` to ``(0, 10)``; raise ValueError for non-numeric input."""
    return tuple(int(part) for part in value.strip().split("."))


def _cells(line: str) -> list[str]:
    parts = UNESCAPED_PIPE.split(line.strip())
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    return [part.strip().replace("\\|", "|") for part in parts]


def iter_table_rows(text: str, required_headers: Iterable[str]) -> Iterator[dict[str, str]]:
    """Yield header-to-cell mappings for rows of every table that has the given headers."""
    required = set(required_headers)
    headers: list[str] | None = None
    wanted = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            headers = None
            continue
        cells = _cells(line)
        if headers is None:
            headers = cells
            wanted = required.issubset(headers)
            continue
        if cells and all(SEPARATOR_CELL.fullmatch(cell) for cell in cells):
            continue
        if wanted:
            padded = cells + [""] * (len(headers) - len(cells))
            yield dict(zip(headers, padded))


def is_valid_stage_status(value: str) -> bool:
    """Accept an exact status or a ``deferred: ``/``skipped: `` prefix with a reason."""
    if value in STAGE_STATUSES:
        return True
    return any(
        value.startswith(prefix) and value[len(prefix):].strip()
        for prefix in STAGE_STATUS_PREFIXES
    )


def find_ids(text: str) -> set[str]:
    """Return every decision, claim, source, and copy id mentioned in the text."""
    return set(ID_PATTERN.findall(text))
