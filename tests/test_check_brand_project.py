from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import V1_BRAND_TEXT, make_project, run_script


DERIVED = ("PROGRESS.md", "MESSAGING.md", "COMPANY.md", "SITE-BRIEF.md")
ALL_DERIVED_AT = {
    name: [("foundation_version: 0.3", "foundation_version: {version}")]
    for name in ("MESSAGING.md", "COMPANY.md", "SITE-BRIEF.md")
}


def derived_at(version: str) -> dict[str, list[tuple[str, str]]]:
    return {
        name: [(old, new.format(version=version)) for old, new in pairs]
        for name, pairs in ALL_DERIVED_AT.items()
    }


class CheckBrandProjectTests(unittest.TestCase):
    def check(self, mutate=None, **kwargs):
        with tempfile.TemporaryDirectory() as temporary_root:
            project = make_project(Path(temporary_root) / "客户 项目", **kwargs)
            if mutate:
                mutate(project)
            return run_script("check_brand_project.py", project)

    def assert_error(self, message: str, **kwargs) -> None:
        result = self.check(**kwargs)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("PROJECT CHECK FAILED", result.stdout)
        self.assertIn(f"- ERROR: {message}", result.stdout)

    def assert_warning(self, message: str, **kwargs) -> None:
        result = self.check(**kwargs)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"- WARN: {message}", result.stdout)

    def test_valid_project_passes(self) -> None:
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PROJECT CHECK PASSED: 5 files checked, 0 warnings", result.stdout)

    def test_missing_brand_fails(self) -> None:
        self.assert_error("missing BRAND.md", remove=("BRAND.md",))

    def test_brand_only_project_passes(self) -> None:
        result = self.check(remove=DERIVED)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 files checked, 0 warnings", result.stdout)

    def test_accepts_v1_brand_without_v2_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            project = Path(temporary_root) / "legacy"
            project.mkdir()
            (project / "BRAND.md").write_text(V1_BRAND_TEXT, encoding="utf-8")
            result = run_script("check_brand_project.py", project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("1 files checked, 0 warnings", result.stdout)

    def test_reports_stale_using_numeric_versions(self) -> None:
        edits = derived_at("0.10")
        edits["BRAND.md"] = [("version: 0.3", "version: 0.10")]
        edits["MESSAGING.md"] = [("foundation_version: 0.3", "foundation_version: 0.9")]
        self.assert_warning(
            "MESSAGING.md: stale (generated from BRAND.md 0.9, current 0.10)", edits=edits
        )

    def test_numeric_comparison_does_not_flag_newer_derived_files(self) -> None:
        # Compared as text, "0.10" < "0.9" and every derived file would look stale.
        edits = derived_at("0.10")
        edits["BRAND.md"] = [("version: 0.3", "version: 0.9")]
        result = self.check(edits=edits)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 warnings", result.stdout)

    def test_trailing_zero_does_not_make_a_version_newer(self) -> None:
        edits = derived_at("1")
        edits["BRAND.md"] = [("version: 0.3", "version: 1.0")]
        result = self.check(edits=edits)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 warnings", result.stdout)

    def test_non_numeric_version_fails(self) -> None:
        self.assert_error(
            "BRAND.md: invalid version 'draft'",
            edits={"BRAND.md": [("version: 0.3", "version: draft")]},
        )

    def test_unknown_references_fail(self) -> None:
        self.assert_error(
            "SITE-BRIEF.md: unknown reference COPY-999",
            edits={"SITE-BRIEF.md": [("COPY-001", "COPY-999")]},
        )
        self.assert_error(
            "COMPANY.md: unknown reference DEC-SITE-404",
            edits={"COMPANY.md": [("CLM-001", "DEC-SITE-404")]},
        )
        self.assert_error(
            "SITE-BRIEF.md: unknown reference COPY-001", remove=("MESSAGING.md",)
        )
        self.assert_error(
            "PROGRESS.md: unknown reference DEC-GOAL-009",
            edits={"PROGRESS.md": [("- DEC-POSITIONING-001", "- DEC-GOAL-009")]},
        )

    def test_required_stage_cannot_be_skipped_or_unselected(self) -> None:
        self.assert_error(
            "PROGRESS.md: required stage 4 cannot be 'skipped: 客户赶时间'",
            edits={
                "PROGRESS.md": [("| 4 | 诊断与定位 | done", "| 4 | 诊断与定位 | skipped: 客户赶时间")]
            },
        )
        self.assert_error(
            "PROGRESS.md: required stage 5 cannot be 'not-selected'",
            edits={"PROGRESS.md": [("| 5 | 证明与信任 | done", "| 5 | 证明与信任 | not-selected")]},
        )

    def test_gate_can_be_deferred(self) -> None:
        result = self.check(
            edits={
                "PROGRESS.md": [("| 4 | 诊断与定位 | done", "| 4 | 诊断与定位 | deferred: 等王总回复")]
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_module_rows_must_match_selected_modules(self) -> None:
        self.assert_error(
            "PROGRESS.md: stage W1 is 'done' but module 'website' is not selected",
            edits={"PROGRESS.md": [("modules: [execution, website]", "modules: [execution]")]},
        )
        self.assert_error(
            "PROGRESS.md: stage E1 is 'not-selected' but module 'execution' is selected",
            edits={"PROGRESS.md": [("| E1 | 产品与价格 | done", "| E1 | 产品与价格 | not-selected")]},
        )

    def test_selected_module_stage_may_be_skipped_with_reason(self) -> None:
        result = self.check(
            edits={"PROGRESS.md": [("| E2 | 渠道与推广 | done", "| E2 | 渠道与推广 | skipped: 客户取消")]}
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_or_missing_stage_rows(self) -> None:
        self.assert_error(
            "PROGRESS.md: invalid status 'complete' for stage 2",
            edits={"PROGRESS.md": [("| 2 | 客户与成交场景 | done", "| 2 | 客户与成交场景 | complete")]},
        )
        self.assert_error(
            "PROGRESS.md: missing stage 3",
            edits={"PROGRESS.md": [("| 3 | 竞争与替代 | done | | |\n", "")]},
        )

    def test_approved_decision_needs_owner_and_date(self) -> None:
        self.assert_error(
            "BRAND.md: approved decision DEC-POSITIONING-001 lacks owner or date",
            edits={
                "BRAND.md": [
                    ("| approved | fictional-owner | 2025-01-08 |", "| approved | fictional-owner | |")
                ]
            },
        )

    def test_formed_by_and_origin_ref_rules(self) -> None:
        self.assert_error(
            "BRAND.md: invalid formed_by 'ai' on DEC-POSITIONING-001",
            edits={"BRAND.md": [("| ai-refined |", "| ai |")]},
        )
        self.assert_error(
            "BRAND.md: origin_ref 'SRC-999' on DEC-POSITIONING-001 is not a known source or claim",
            edits={"BRAND.md": [("| ai-refined | SRC-001 |", "| ai-refined | SRC-999 |")]},
        )
        self.assert_warning(
            "BRAND.md: approved decision DEC-POSITIONING-001 has no formed_by",
            edits={"BRAND.md": [("| ai-refined | SRC-001 |", "| | |")]},
        )

    def test_origin_ref_may_list_several_known_ids(self) -> None:
        # Found in the end-to-end walkthrough: a statement drawn from a questionnaire and a
        # later call was recorded as "SRC-001、CLM-001", which the check rejected.
        result = self.check(
            edits={"BRAND.md": [("| ai-refined | SRC-001 |", "| ai-refined | SRC-001、CLM-001 |")]}
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 warnings", result.stdout)
        self.assert_error(
            "BRAND.md: origin_ref 'SRC-001、SRC-999' on DEC-POSITIONING-001 "
            "is not a known source or claim",
            edits={"BRAND.md": [("| ai-refined | SRC-001 |", "| ai-refined | SRC-001、SRC-999 |")]},
        )
        self.assert_error(
            "BRAND.md: origin_ref '见访谈' on DEC-POSITIONING-001 is not a known source or claim",
            edits={"BRAND.md": [("| ai-refined | SRC-001 |", "| ai-refined | 见访谈 |")]},
        )

    def test_unknown_segment_schema_brand_id_and_missing_field(self) -> None:
        self.assert_error(
            "BRAND.md: unknown segment 'pet-food'",
            edits={"BRAND.md": [("segment: export-b2b", "segment: pet-food")]},
        )
        self.assert_error(
            "PROGRESS.md: unknown segment 'pet-food'",
            edits={"PROGRESS.md": [("segment: export-b2b", "segment: pet-food")]},
        )
        self.assert_error(
            "COMPANY.md: unknown schema 'company/v9'",
            edits={"COMPANY.md": [("schema: company-context/v1", "schema: company/v9")]},
        )
        self.assert_error(
            "MESSAGING.md: brand_id 'other-fictional' does not match BRAND.md 'sample-fictional'",
            edits={"MESSAGING.md": [("brand_id: sample-fictional", "brand_id: other-fictional")]},
        )
        self.assert_error(
            "SITE-BRIEF.md: missing required field 'primary_conversion'",
            edits={
                "SITE-BRIEF.md": [("primary_conversion: inquiry-form", 'primary_conversion: ""')]
            },
        )

    def test_unknown_and_generic_segments_are_accepted(self) -> None:
        for value in ("unknown", "generic"):
            result = self.check(
                edits={
                    "BRAND.md": [("segment: export-b2b", f"segment: {value}")],
                    "PROGRESS.md": [("segment: export-b2b", f"segment: {value}")],
                }
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_site_brief_without_website_module_warns(self) -> None:
        self.assert_warning(
            "SITE-BRIEF.md exists but the website module is not selected",
            edits={
                "PROGRESS.md": [
                    ("modules: [execution, website]", "modules: [execution]"),
                    ("| W1 | 网站目标与约束 | done", "| W1 | 网站目标与约束 | not-selected"),
                ]
            },
        )

    def test_reports_every_problem_in_one_run(self) -> None:
        result = self.check(
            edits={
                "BRAND.md": [("segment: export-b2b", "segment: pet-food")],
                "COMPANY.md": [("CLM-001", "CLM-777")],
            }
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown segment 'pet-food'", result.stdout)
        self.assertIn("COMPANY.md: unknown reference CLM-777", result.stdout)

    def test_decision_status_must_be_a_bare_known_value(self) -> None:
        # Found in the final review: a decorated or translated status slipped past
        # the "approved needs an approver and a date" check.
        for bad in ("已批准", "Approved", "`approved`", "approved（经操作者转述）", "agreed"):
            self.assert_error(
                f"BRAND.md: invalid decision_status '{bad}' on DEC-POSITIONING-001",
                edits={
                    "BRAND.md": [("| approved | fictional-owner | 2025-01-08 |", f"| {bad} | | |")]
                },
            )

    def test_v1_record_with_unknown_decision_status_only_warns(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            project = Path(temporary_root) / "legacy"
            project.mkdir()
            text = V1_BRAND_TEXT.replace("| approved | fictional-owner |", "| 已批准 | fictional-owner |")
            self.assertNotEqual(text, V1_BRAND_TEXT)
            (project / "BRAND.md").write_text(text, encoding="utf-8")
            result = run_script("check_brand_project.py", project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "- WARN: BRAND.md: invalid decision_status '已批准' on DEC-POSITIONING-001",
                result.stdout,
            )

    def test_duplicate_stage_rows_fail(self) -> None:
        # Found in the final review: the last duplicate row won and hid a skipped gate.
        self.assert_error(
            "PROGRESS.md: duplicate stage 4",
            edits={
                "PROGRESS.md": [
                    (
                        "| 4 | 诊断与定位 | done | | |\n",
                        "| 4 | 诊断与定位 | skipped: 客户赶时间 | | |\n| 4 | 诊断与定位 | done | | |\n",
                    )
                ]
            },
        )

    def test_only_the_stage_table_is_read(self) -> None:
        result = self.check(
            edits={
                "PROGRESS.md": [
                    (
                        "## 会话记录\n",
                        "## 会话记录\n\n| stage | status |\n|---|---|\n| 4 | skipped: 备注里的旧表 |\n",
                    )
                ]
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 warnings", result.stdout)

    def test_utf8_bom_is_accepted(self) -> None:
        def add_bom(project: Path) -> None:
            for name in ("BRAND.md", "PROGRESS.md", "COMPANY.md"):
                path = project / name
                path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())

        result = self.check(mutate=add_bom)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PROJECT CHECK PASSED: 5 files checked, 0 warnings", result.stdout)

    def test_non_utf8_file_is_reported_not_crashed(self) -> None:
        def to_gbk(name: str):
            def mutate(project: Path) -> None:
                path = project / name
                path.write_bytes(path.read_text(encoding="utf-8").encode("gbk"))

            return mutate

        for name in ("COMPANY.md", "BRAND.md"):
            result = self.check(mutate=to_gbk(name))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(f"- ERROR: {name}: not UTF-8", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_approved_record_requires_passed_gates(self) -> None:
        approved = [("record_status: working", "record_status: approved")]
        self.assert_error(
            "BRAND.md: record_status is 'approved' but gate stage 7 is 'deferred: 等客户回复'",
            edits={
                "BRAND.md": approved,
                "PROGRESS.md": [("| 7 | 汇总确认 | done", "| 7 | 汇总确认 | deferred: 等客户回复")],
            },
        )
        result = self.check(edits={"BRAND.md": approved})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_messaging_without_foundation_version_only_warns(self) -> None:
        # Older MESSAGING.md files leave this empty; that must not fail a legacy project.
        self.assert_warning(
            "MESSAGING.md: no foundation_version, cannot tell whether it is stale",
            edits={"MESSAGING.md": [("foundation_version: 0.3", 'foundation_version: ""')]},
        )

    def test_handoff_files_go_stale_when_messaging_moves_on(self) -> None:
        # Raised in PR review: MESSAGING.md can change while BRAND.md does not.
        newer_messaging = {
            "MESSAGING.md": [
                ("version: 0.1\nfoundation_version: 0.3", "version: 0.2\nfoundation_version: 0.3")
            ]
        }
        result = self.check(edits=newer_messaging)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in ("COMPANY.md", "SITE-BRIEF.md"):
            self.assertIn(
                f"- WARN: {name}: stale (generated from MESSAGING.md 0.1, current 0.2)",
                result.stdout,
            )

    def test_empty_messaging_version_is_not_stale(self) -> None:
        result = self.check(
            edits={
                "MESSAGING.md": [
                    ("version: 0.1\nfoundation_version: 0.3", "version: 0.2\nfoundation_version: 0.3")
                ],
                "COMPANY.md": [("messaging_version: 0.1", 'messaging_version: ""')],
                "SITE-BRIEF.md": [("messaging_version: 0.1", 'messaging_version: ""')],
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 warnings", result.stdout)

    def test_invalid_messaging_version_fails(self) -> None:
        self.assert_error(
            "COMPANY.md: invalid version 'latest'",
            edits={"COMPANY.md": [("messaging_version: 0.1", "messaging_version: latest")]},
        )

    def test_segment_must_match_between_brand_and_progress(self) -> None:
        # Raised in PR review: two different valid segments used to pass.
        self.assert_error(
            "PROGRESS.md: segment 'dtc-ecommerce' does not match BRAND.md 'export-b2b'",
            edits={"PROGRESS.md": [("segment: export-b2b", "segment: dtc-ecommerce")]},
        )
        # Before stage 0 settles the client type one side is still unknown; that is not a mismatch.
        result = self.check(edits={"PROGRESS.md": [("segment: export-b2b", "segment: unknown")]})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_record_status_must_be_a_known_value(self) -> None:
        # Raised in PR review: a decorated value skipped the "approved needs passed gates" rule.
        for bad in ("已批准", "Approved", "approved（客户已签）"):
            self.assert_error(
                f"BRAND.md: invalid record_status '{bad}'",
                edits={"BRAND.md": [("record_status: working", f"record_status: {bad}")]},
            )

    def test_v1_record_with_unknown_record_status_only_warns(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            project = Path(temporary_root) / "legacy"
            project.mkdir()
            text = V1_BRAND_TEXT.replace("record_status: working", "record_status: 工作稿")
            self.assertNotEqual(text, V1_BRAND_TEXT)
            (project / "BRAND.md").write_text(text, encoding="utf-8")
            result = run_script("check_brand_project.py", project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("- WARN: BRAND.md: invalid record_status '工作稿'", result.stdout)

    def test_rejects_a_path_that_is_not_a_directory(self) -> None:
        result = run_script("check_brand_project.py", Path(tempfile.gettempdir()) / "no-such-project-dir")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a directory", result.stderr)


NAME_TABLE = (
    "| 品牌或名称 | 语言 | 标准写法 | 可用简称 | 停用写法 | 依据 |\n"
    "|---|---|---|---|---|---|\n"
    "| 样本 | 中文 | {standard} | {short} | {retired} | DEC-POSITIONING-001 |\n"
)
RETIRED_WARNING = "- WARN: {name}: retired name spelling '{spelling}' (see the name table in MESSAGING.md)"


def with_name_table(standard: str = "样本实验室", short: str = "样本室", retired: str = "样本工坊"):
    """Edits that put a name-writing table (all names fictional) into MESSAGING.md."""
    table = NAME_TABLE.format(standard=standard, short=short, retired=retired)
    return {"MESSAGING.md": [("# Sample MESSAGING（虚构）\n", f"# Sample MESSAGING（虚构）\n\n{table}")]}


class NameConsistencyTests(unittest.TestCase):
    def check(self, edits):
        with tempfile.TemporaryDirectory() as temporary_root:
            project = make_project(Path(temporary_root) / "project", edits=edits)
            result = run_script("check_brand_project.py", project)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_brand_name_in_a_derived_file_must_match_brand_md(self) -> None:
        mismatch = {"COMPANY.md": [("brand_id: sample-fictional", "brand_id: sample-fictional\nbrand_name: Sample Co")]}
        self.assertIn(
            "- WARN: COMPANY.md: brand_name 'Sample Co' does not match BRAND.md 'Sample'",
            self.check(mismatch),
        )
        same = {"COMPANY.md": [("brand_id: sample-fictional", "brand_id: sample-fictional\nbrand_name: Sample")]}
        self.assertIn("0 warnings", self.check(same))

    def test_name_table_alone_raises_no_warning(self) -> None:
        # The table is the one place a retired spelling is allowed to appear.
        self.assertIn("0 warnings", self.check(with_name_table()))

    def test_retired_spelling_in_a_derived_file_warns(self) -> None:
        edits = with_name_table()
        edits["COMPANY.md"] = [("# Sample 速读（虚构）", "# Sample 速读（虚构）\n\n样本工坊是一家虚构企业。")]
        edits["MESSAGING.md"].append(("# Sample MESSAGING（虚构）", "# Sample MESSAGING（虚构）\n\n欢迎来到样本工坊。"))
        output = self.check(edits)
        for name in ("COMPANY.md", "MESSAGING.md"):
            self.assertIn(RETIRED_WARNING.format(name=name, spelling="样本工坊"), output)
        self.assertNotIn("SITE-BRIEF.md: retired", output)

    def test_brand_md_may_record_the_retired_spelling(self) -> None:
        # The decision that retires a spelling has to name it.
        edits = with_name_table()
        edits["BRAND.md"] = [("# Sample BRAND（虚构）", "# Sample BRAND（虚构）\n\n停用样本工坊这个写法。")]
        self.assertIn("0 warnings", self.check(edits))

    def test_retired_spelling_that_contains_a_short_name_is_still_flagged(self) -> None:
        edits = with_name_table(short="样本", retired="样本 温控")
        edits["SITE-BRIEF.md"] = [("# Sample 建站交接（虚构）", "# Sample 建站交接（虚构）\n\n样本 温控，以及样本。")]
        self.assertIn(RETIRED_WARNING.format(name="SITE-BRIEF.md", spelling="样本 温控"), self.check(edits))

    def test_standard_spelling_that_contains_a_retired_one_is_not_flagged(self) -> None:
        edits = with_name_table(standard="样本实验室", short="", retired="样本")
        edits["COMPANY.md"] = [("# Sample 速读（虚构）", "# Sample 速读（虚构）\n\n样本实验室是一家虚构企业。")]
        self.assertIn("0 warnings", self.check(edits))
        edits["COMPANY.md"] = [("# Sample 速读（虚构）", "# Sample 速读（虚构）\n\n样本实验室，也有人叫它样本。")]
        self.assertIn(RETIRED_WARNING.format(name="COMPANY.md", spelling="样本"), self.check(edits))

    def test_empty_markers_in_the_retired_cell_are_ignored(self) -> None:
        for marker in ("", "无", "—"):
            edits = with_name_table(retired=marker)
            edits["COMPANY.md"] = [("# Sample 速读（虚构）", "# Sample 速读（虚构）\n\n暂无其他写法 — 仅此一种。")]
            self.assertIn("0 warnings", self.check(edits), repr(marker))

    def test_spellings_are_split_on_the_list_comma_only(self) -> None:
        # A legal name such as "Sample Co., Ltd." contains an ordinary comma.
        edits = with_name_table(standard="Sample Co., Ltd.", short="", retired="Sample Inc、样本工坊")
        edits["COMPANY.md"] = [("# Sample 速读（虚构）", "# Sample 速读（虚构）\n\nSample Co., Ltd. 曾写作 Sample Inc。")]
        output = self.check(edits)
        self.assertIn(RETIRED_WARNING.format(name="COMPANY.md", spelling="Sample Inc"), output)
        self.assertIn("1 warnings", output)


if __name__ == "__main__":
    unittest.main()
