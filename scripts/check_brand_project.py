#!/usr/bin/env python3
"""Read-only self-check for a client brand project.

Reports files that are stale against BRAND.md, references to ids that do not
exist, progress states the journey does not allow, and approvals that lack an
approver or date. It never writes to the project.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import brandlib


V2_SCHEMA = "brand-foundation/v2"
DERIVED_FILES = ("MESSAGING.md", "COMPANY.md", "SITE-BRIEF.md")
REQUIRED_FIELDS = {
    "BRAND.md": ("schema", "brand_id", "record_status", "version"),
    "PROGRESS.md": ("schema", "brand_id", "segment", "current_stage"),
    # MESSAGING.md predates this check; older files leave foundation_version empty,
    # so its absence is a warning (see check_versions), not a missing field.
    "MESSAGING.md": ("schema", "brand_id"),
    "COMPANY.md": ("schema", "brand_id", "foundation_version", "generated"),
    "SITE-BRIEF.md": (
        "schema",
        "brand_id",
        "brief_status",
        "foundation_version",
        "language",
        "primary_conversion",
    ),
}
STAGE_SECTION = re.compile(r"^## 阶段[^\n]*\n(?P<body>.*?)(?=^## |\Z)", re.S | re.M)


def read_project_files(project: Path) -> tuple[dict[str, str], list[str]]:
    """Read the known project files; return their text and the names that are not UTF-8."""
    texts: dict[str, str] = {}
    unreadable: list[str] = []
    for name in brandlib.SCHEMAS:
        path = project / name
        if not path.is_file():
            continue
        try:
            # utf-8-sig drops the byte-order mark some Windows editors add.
            texts[name] = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            unreadable.append(name)
    return texts, unreadable


def defined_ids(text: str, id_columns: tuple[str, ...]) -> set[str]:
    """Return the ids declared in the first column of the tables with these headers."""
    ids: set[str] = set()
    for column in id_columns:
        for row in brandlib.iter_table_rows(text, [column]):
            ids |= brandlib.find_ids(row[column])
    return ids


def is_older(version: tuple[int, ...], than: tuple[int, ...]) -> bool:
    """Compare versions numerically, treating 1 and 1.0 as equal."""
    width = max(len(version), len(than))
    return version + (0,) * (width - len(version)) < than + (0,) * (width - len(than))


def check_headers(headers: dict[str, dict[str, str]], segments: set[str]) -> list[str]:
    errors: list[str] = []
    brand_id = headers["BRAND.md"].get("brand_id", "")
    for name, fm in headers.items():
        schema = fm.get("schema", "")
        if schema and schema not in brandlib.SCHEMAS[name]:
            errors.append(f"{name}: unknown schema '{schema}'")
        required = REQUIRED_FIELDS[name]
        if name == "BRAND.md" and schema == V2_SCHEMA:
            required += ("segment",)
        errors += [f"{name}: missing required field '{key}'" for key in required if not fm.get(key)]
        if name == "PROGRESS.md" and "modules" not in fm:
            errors.append(f"{name}: missing required field 'modules'")
        if name != "BRAND.md" and brand_id and fm.get("brand_id") not in ("", None, brand_id):
            errors.append(
                f"{name}: brand_id '{fm['brand_id']}' does not match BRAND.md '{brand_id}'"
            )
        segment = fm.get("segment", "")
        if name in ("BRAND.md", "PROGRESS.md") and segment and segment not in segments:
            errors.append(f"{name}: unknown segment '{segment}'")

    # Until stage 0 settles the client type one side may still be unknown; that is not a mismatch.
    brand_segment = headers["BRAND.md"].get("segment", "")
    progress_segment = headers.get("PROGRESS.md", {}).get("segment", "")
    settled = {brand_segment, progress_segment} - {"", brandlib.UNKNOWN_SEGMENT}
    if brand_segment and progress_segment and len(settled) == 2:
        errors.append(
            f"PROGRESS.md: segment '{progress_segment}' does not match BRAND.md '{brand_segment}'"
        )
    return errors


def check_versions(headers: dict[str, dict[str, str]]) -> tuple[list[str], list[str]]:
    """Compare the version each derived file was built from with its source's current version."""
    errors: list[str] = []
    warnings: list[str] = []

    def current_version(source: str) -> tuple[str, tuple[int, ...] | None]:
        value = headers.get(source, {}).get("version", "")
        try:
            return value, brandlib.version_tuple(value) if value else None
        except ValueError:
            errors.append(f"{source}: invalid version '{value}'")
            return value, None

    def compare(name: str, field: str, source: str, current: tuple[str, tuple[int, ...] | None]):
        built_from = headers[name].get(field, "")
        if not built_from:
            if (name, field) == ("MESSAGING.md", "foundation_version"):
                warnings.append(f"{name}: no foundation_version, cannot tell whether it is stale")
            return
        try:
            built_tuple = brandlib.version_tuple(built_from)
        except ValueError:
            errors.append(f"{name}: invalid version '{built_from}'")
            return
        if current[1] is not None and is_older(built_tuple, current[1]):
            warnings.append(
                f"{name}: stale (generated from {source} {built_from}, current {current[0]})"
            )

    brand = current_version("BRAND.md")
    for name in DERIVED_FILES:
        if name in headers:
            compare(name, "foundation_version", "BRAND.md", brand)

    # COMPANY.md and SITE-BRIEF.md also record the MESSAGING.md version they were built from.
    messaging = current_version("MESSAGING.md") if "MESSAGING.md" in headers else ("", None)
    for name in ("COMPANY.md", "SITE-BRIEF.md"):
        if name in headers:
            compare(name, "messaging_version", "MESSAGING.md", messaging)
    return errors, warnings


def check_references(texts: dict[str, str], brand_ids: set[str]) -> list[str]:
    errors: list[str] = []
    copy_ids = defined_ids(texts.get("MESSAGING.md", ""), ("Copy ID",))
    for name in ("PROGRESS.md", *DERIVED_FILES):
        for reference in sorted(brandlib.find_ids(texts.get(name, ""))):
            if reference.startswith("COPY-"):
                known = name == "MESSAGING.md" or reference in copy_ids
            else:
                known = reference in brand_ids
            if not known:
                errors.append(f"{name}: unknown reference {reference}")
    return errors


def read_stage_rows(text: str) -> tuple[dict[str, str], list[str]]:
    """Return ``{stage: status}`` from the stage table and an error per duplicated stage.

    Only the table under the "## 阶段" heading counts, so a table elsewhere in the
    file cannot override it. The first row for a stage is the one that is checked.
    """
    section = STAGE_SECTION.search(text)
    body = section.group("body") if section else text
    statuses: dict[str, str] = {}
    duplicates: list[str] = []
    for row in brandlib.iter_table_rows(body, ["stage", "status"]):
        stage = row["stage"]
        if stage in statuses:
            if stage not in duplicates:
                duplicates.append(stage)
        else:
            statuses[stage] = row["status"]
    return statuses, [f"PROGRESS.md: duplicate stage {stage}" for stage in duplicates]


def check_progress(rows: dict[str, str], header: dict[str, str]) -> list[str]:
    errors: list[str] = []
    modules = brandlib.parse_inline_list(header.get("modules", ""))
    errors += [
        f"PROGRESS.md: unknown module '{module}'"
        for module in modules
        if module not in brandlib.MODULE_STAGES
    ]
    stage_module = {
        stage: module for module, stages in brandlib.MODULE_STAGES.items() for stage in stages
    }
    for stage in (*brandlib.REQUIRED_STAGES, *stage_module):
        if stage not in rows:
            errors.append(f"PROGRESS.md: missing stage {stage}")
            continue
        status = rows[stage]
        if not brandlib.is_valid_stage_status(status):
            errors.append(f"PROGRESS.md: invalid status '{status}' for stage {stage}")
        elif stage in brandlib.REQUIRED_STAGES:
            if status == "not-selected" or status.startswith("skipped"):
                errors.append(f"PROGRESS.md: required stage {stage} cannot be '{status}'")
        else:
            module = stage_module[stage]
            if module in modules and status == "not-selected":
                errors.append(
                    f"PROGRESS.md: stage {stage} is 'not-selected' "
                    f"but module '{module}' is selected"
                )
            elif module not in modules and status != "not-selected":
                errors.append(
                    f"PROGRESS.md: stage {stage} is '{status}' "
                    f"but module '{module}' is not selected"
                )
    return errors


def check_gates(record_status: str, rows: dict[str, str]) -> list[str]:
    """An approved record requires every gate stage to be done."""
    if record_status != "approved":
        return []
    return [
        f"BRAND.md: record_status is 'approved' but gate stage {gate} is '{rows[gate]}'"
        for gate in brandlib.GATE_STAGES
        if gate in rows and rows[gate] != "done"
    ]


def check_decisions(text: str, is_v2: bool, evidence_ids: set[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for row in brandlib.iter_table_rows(text, ["Decision ID", "decision_status"]):
        decision = row["Decision ID"]
        if not decision:
            continue
        status = row["decision_status"]
        if status not in brandlib.DECISION_STATUSES:
            # A decorated or translated status would slip past the approval checks below.
            problem = f"BRAND.md: invalid decision_status '{status}' on {decision}"
            (errors if is_v2 else warnings).append(problem)
            continue
        approved = status == "approved"
        if approved and not (row.get("owner") and row.get("date")):
            errors.append(f"BRAND.md: approved decision {decision} lacks owner or date")
        if not is_v2:
            continue
        formed_by = row.get("formed_by", "")
        origin_ref = row.get("origin_ref", "")
        if formed_by and formed_by not in brandlib.FORMED_BY:
            errors.append(f"BRAND.md: invalid formed_by '{formed_by}' on {decision}")
        # A statement may draw on more than one source, so the cell may list several ids.
        origin_ids = brandlib.find_ids(origin_ref)
        if origin_ref and (not origin_ids or not origin_ids <= evidence_ids):
            errors.append(
                f"BRAND.md: origin_ref '{origin_ref}' on {decision} is not a known source or claim"
            )
        is_statement = decision.rsplit("-", 1)[0] in brandlib.STATEMENT_PREFIXES
        if approved and is_statement and not formed_by:
            warnings.append(f"BRAND.md: approved decision {decision} has no formed_by")
    return errors, warnings


def check_project(project: Path, repo_root: Path) -> tuple[list[str], list[str], int]:
    """Return ``(errors, warnings, files_checked)`` for one client project directory."""
    texts, unreadable = read_project_files(project)
    checked = len(texts) + len(unreadable)
    errors = [f"{name}: not UTF-8" for name in unreadable]
    if "BRAND.md" not in texts:
        if "BRAND.md" not in unreadable:
            errors.append("missing BRAND.md")
        return errors, [], checked

    headers = {name: brandlib.parse_frontmatter(text) for name, text in texts.items()}
    segments = {
        *brandlib.read_segment_index(repo_root),
        brandlib.GENERIC_SEGMENT,
        brandlib.UNKNOWN_SEGMENT,
    }
    brand_text = texts["BRAND.md"]
    evidence_ids = defined_ids(brand_text, ("Claim ID", "Source ID"))
    brand_ids = evidence_ids | defined_ids(brand_text, ("Decision ID",))

    errors += check_headers(headers, segments)
    version_errors, warnings = check_versions(headers)
    errors += version_errors
    errors += check_references(texts, brand_ids)
    if "PROGRESS.md" in texts:
        rows, duplicate_errors = read_stage_rows(texts["PROGRESS.md"])
        errors += duplicate_errors
        errors += check_progress(rows, headers["PROGRESS.md"])
        errors += check_gates(headers["BRAND.md"].get("record_status", ""), rows)
    is_v2 = headers["BRAND.md"].get("schema") == V2_SCHEMA
    record_status = headers["BRAND.md"].get("record_status", "")
    if record_status and record_status not in brandlib.RECORD_STATUSES:
        problem = f"BRAND.md: invalid record_status '{record_status}'"
        (errors if is_v2 else warnings).append(problem)
    decision_errors, decision_warnings = check_decisions(brand_text, is_v2, evidence_ids)
    errors += decision_errors
    warnings += decision_warnings

    if "SITE-BRIEF.md" in texts and "PROGRESS.md" in texts:
        modules = brandlib.parse_inline_list(headers["PROGRESS.md"].get("modules", ""))
        if "website" not in modules:
            warnings.append("SITE-BRIEF.md exists but the website module is not selected")
    return errors, warnings, checked


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a client brand project without changing it")
    parser.add_argument("project", help="Client project directory containing BRAND.md")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        parser.error(f"not a directory: {args.project}")
    repo_root = Path(__file__).resolve().parents[1]

    errors, warnings, checked = check_project(project, repo_root)
    if errors:
        print("PROJECT CHECK FAILED")
    else:
        print(f"PROJECT CHECK PASSED: {checked} files checked, {len(warnings)} warnings")
    for error in errors:
        print(f"- ERROR: {error}")
    for warning in warnings:
        print(f"- WARN: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
