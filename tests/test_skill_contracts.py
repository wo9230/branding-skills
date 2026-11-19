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

    def test_output_contract_pins_id_formats_and_register_headers(self) -> None:
        # Found in dry run 01: without these, a model invents ids such as "C-001".
        text = repo_text(FOUNDATION + "references/output-contracts.md")
        for token in ("CLM-001", "SRC-001", "| Source ID |", "| Claim ID |", "不占行"):
            self.assertIn(token, text, token)
        for example in ("CLM-001", "SRC-001", "DEC-POSITIONING-001"):
            self.assertEqual(brandlib.find_ids(example), {example})

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


class RefinementContractTests(unittest.TestCase):
    def test_refinement_reference_is_complete(self) -> None:
        text = repo_text(FOUNDATION + "references/refinement.md")
        for heading in (
            "## 两类内容",
            "## 品牌表述包含什么",
            "## 六步",
            "## 质量标准",
            "## 边界",
            "## 记录方式",
        ):
            self.assertIn(heading, text, heading)
        for standard in ("具体", "可区分", "有取舍", "有依据", "不夸大", "听得懂", "说得出口"):
            self.assertIn(standard, text, standard)
        for token in (
            "最多三个",
            "两轮",
            "采用",
            "修改",
            "保留原话",
            "暂缓",
            "待补证据",
            *brandlib.FORMED_BY,
        ):
            self.assertIn(token, text, token)

    def test_decision_table_has_refinement_columns(self) -> None:
        header = (
            "| Decision ID | choice | decision_status | owner | date | reason | scope "
            "| formed_by | origin_ref |"
        )
        contract = repo_text(FOUNDATION + "references/output-contracts.md")
        self.assertIn(header, contract)
        self.assertIn("AI 的保留意见", contract)
        self.assertIn("formed_by", repo_text(FOUNDATION + "assets/BRAND-WORKBOOK.md"))

    def test_skill_entry_points_to_refinement(self) -> None:
        self.assertIn("references/refinement.md", repo_text(FOUNDATION + "SKILL.md"))


SEGMENTS = "skills/brand-journey/references/segments/"


class SegmentPackContractTests(unittest.TestCase):
    def test_index_registers_the_three_first_packs(self) -> None:
        self.assertEqual(
            brandlib.read_segment_index(REPO_ROOT),
            {
                "export-b2b": "export-b2b.md",
                "domestic-b2b": "domestic-b2b.md",
                "dtc-ecommerce": "dtc-ecommerce.md",
            },
        )

    def test_packs_cover_the_spec_difference_table(self) -> None:
        required = {
            "export-b2b.md": ("询盘", "起订量", "交期", "贸易条款", "样品", "展会", "认证", "出口"),
            "domestic-b2b.md": ("线索", "方案报价", "账期", "招投标", "资质", "标杆案例"),
            "dtc-ecommerce.md": ("下单", "促销", "运费", "退换", "质保", "达人", "复购", "评价"),
        }
        for name, words in required.items():
            text = repo_text(SEGMENTS + name)
            for word in words:
                self.assertIn(word, text, f"{name}: {word}")
            self.assertLessEqual(len(text.splitlines()), 160, name)
            self.assertNotRegex(text, r"\d+(\.\d+)?\s*%", name)  # no benchmark figures


if __name__ == "__main__":
    unittest.main()
