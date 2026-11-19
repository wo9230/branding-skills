"""Contract tests: the Skill reference files use the vocabulary the scripts enforce."""

from __future__ import annotations

import unittest

from helpers import REPO_ROOT, repo_text  # noqa: F401

import brandlib


FOUNDATION = "skills/brand-foundation/"


class FoundationV2ContractTests(unittest.TestCase):
    def test_output_contract_defines_v2(self) -> None:
        text = repo_text(FOUNDATION + "references/output-contracts.md")
        for token in (
            "schema: brand-foundation/v2",
            "brand-foundation/v1",
            "segment: unknown",
            'operator: ""',
            "[本次未做]",
            "来源与查询日期",
            *brandlib.NEW_DECISION_PREFIXES,
        ):
            self.assertIn(token, text, token)

    def test_strategy_reference_has_all_modules(self) -> None:
        text = repo_text(FOUNDATION + "references/strategy-and-execution.md")
        for heading in (
            "## 诊断",
            "## 方针",
            "## 定位五要素",
            "## 产品",
            "## 价格",
            "## 渠道",
            "## 推广",
            "## 不做什么",
        ):
            self.assertIn(heading, text, heading)
        self.assertIn("最多三个", text)

    def test_routing_has_new_families(self) -> None:
        text = repo_text(FOUNDATION + "references/interview-routing.md")
        for family in ("| 竞争 |", "| 诊断 |", "| 价格 |", "| 渠道 |", "| 推广 |"):
            self.assertIn(family, text, family)

    def test_workbook_targets_v2_and_marks_optional_parts(self) -> None:
        text = repo_text(FOUNDATION + "assets/BRAND-WORKBOOK.md")
        fm = brandlib.parse_frontmatter(text)
        self.assertEqual(fm["target_schema"], "brand-foundation/v2")
        self.assertIn("segment", fm)
        self.assertIn("operator", fm)
        self.assertGreaterEqual(text.count("选做"), 3)

    def test_skill_entry_points_to_new_reference(self) -> None:
        text = repo_text(FOUNDATION + "SKILL.md")
        self.assertIn("references/strategy-and-execution.md", text)
        self.assertLessEqual(len(text.splitlines()), 120)


if __name__ == "__main__":
    unittest.main()
