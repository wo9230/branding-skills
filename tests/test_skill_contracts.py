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


JOURNEY = "skills/brand-journey/"


class JourneyContractTests(unittest.TestCase):
    def test_stage_map_covers_every_stage(self) -> None:
        text = repo_text(JOURNEY + "references/stage-map.md")
        for stage in brandlib.REQUIRED_STAGES:
            self.assertIn(f"## 阶段 {stage}：{brandlib.STAGE_NAMES[stage]}", text)
        for stages in brandlib.MODULE_STAGES.values():
            for stage in stages:
                self.assertIn(f"## 模块 {stage}：{brandlib.STAGE_NAMES[stage]}", text)
        for token in ("execution", "website", "必答", "加深", "做到什么算完", "增量确认"):
            self.assertIn(token, text, token)

    def test_progress_template_matches_vocabulary(self) -> None:
        text = repo_text(JOURNEY + "assets/PROGRESS-TEMPLATE.md")
        fm = brandlib.parse_frontmatter(text)
        self.assertEqual(fm["schema"], "brand-journey-progress/v1")
        self.assertEqual(fm["segment"], "unknown")
        self.assertEqual(brandlib.parse_inline_list(fm["modules"]), [])
        rows = {row["stage"]: row for row in brandlib.iter_table_rows(text, ["stage", "status"])}
        optional = [stage for stages in brandlib.MODULE_STAGES.values() for stage in stages]
        self.assertEqual(set(rows), set(brandlib.REQUIRED_STAGES) | set(optional))
        for stage in brandlib.REQUIRED_STAGES:
            self.assertEqual(rows[stage]["status"], "pending")
            self.assertEqual(rows[stage]["name"], brandlib.STAGE_NAMES[stage])
        for stage in optional:
            self.assertEqual(rows[stage]["status"], "not-selected")
            self.assertEqual(rows[stage]["name"], brandlib.STAGE_NAMES[stage])
        for heading in ("## 关键决策", "## 稍后处理清单", "## 会话记录"):
            self.assertIn(heading, text)

    def test_output_contract_lists_every_status_and_report_path(self) -> None:
        text = repo_text(JOURNEY + "references/output-contracts.md")
        for token in (
            *brandlib.STAGE_STATUSES,
            "deferred: ",
            "skipped: ",
            "brand-journey-progress/v1",
            "reports/YYYY-MM-DD-client-confirmation.md",
            "保留原来的说法",
        ):
            self.assertIn(token, text, token)

    def test_anti_drift_has_progress_lines_and_twelve_rules(self) -> None:
        text = repo_text(JOURNEY + "references/anti-drift.md")
        for line in (
            "阶段 3/7 · 竞争与替代 · 第 2/5 问",
            "落地 E1 · 产品与价格 · 第 1/4 问",
            "建站 W1 · 网站目标与约束 · 第 1/5 问",
        ):
            self.assertIn(line, text)
        numbered = [line for line in text.splitlines() if line[:1].isdigit() and ". **" in line[:8]]
        self.assertEqual(len(numbered), 12)

    def test_questionnaire_has_three_parts_in_order(self) -> None:
        text = repo_text(JOURNEY + "assets/CLIENT-QUESTIONNAIRE.md")
        marks = [text.find(f"<!-- part:{part} -->") for part in brandlib.PART_LABELS]
        self.assertTrue(min(marks) > 0 and marks == sorted(marks), marks)

    def test_skill_entry_names_its_collaborators(self) -> None:
        text = repo_text(JOURNEY + "SKILL.md")
        for token in (
            "$brand-foundation",
            "$brand-expression",
            "$brand-visual-board",
            "$brand-handoff",
            "PROGRESS.md",
            "references/stage-map.md",
            "references/anti-drift.md",
            "references/conduct-modes.md",
            "references/output-contracts.md",
            "references/segments/INDEX.md",
        ):
            self.assertIn(token, text, token)


HANDOFF = "skills/brand-handoff/"


class HandoffContractTests(unittest.TestCase):
    def level_two(self, text: str) -> list[str]:
        return [line for line in text.splitlines() if line.startswith("## ")]

    def test_company_template(self) -> None:
        text = repo_text(HANDOFF + "assets/COMPANY-TEMPLATE.md")
        fm = brandlib.parse_frontmatter(text)
        self.assertIn(fm["schema"], brandlib.SCHEMAS["COMPANY.md"])
        for key in ("brand_id", "foundation_version", "messaging_version", "generated"):
            self.assertIn(key, fm)
        headings = self.level_two(text)
        self.assertEqual(len(headings), 12)
        self.assertEqual(headings[0], "## 1. 一句话")
        self.assertEqual(headings[5], "## 6. 产品、价格、渠道、推广")
        self.assertEqual(headings[9], "## 10. 网站目标与主转化")
        self.assertEqual(headings[11], "## 12. 细节去哪里读")

    def test_site_brief_template(self) -> None:
        text = repo_text(HANDOFF + "assets/SITE-BRIEF-TEMPLATE.md")
        fm = brandlib.parse_frontmatter(text)
        self.assertIn(fm["schema"], brandlib.SCHEMAS["SITE-BRIEF.md"])
        self.assertEqual(fm["brief_status"], "concept")
        for key in ("brand_id", "foundation_version", "language", "primary_conversion", "platform"):
            self.assertIn(key, fm)
        headings = self.level_two(text)
        self.assertEqual(len(headings), 9)
        self.assertEqual(headings[0], "## 1. 网站的任务")
        self.assertEqual(headings[8], "## 9. 给建站 AI 的要求")

    def test_agents_template_points_the_way(self) -> None:
        text = repo_text(HANDOFF + "assets/AGENTS-TEMPLATE.md")
        for token in ("COMPANY.md", "BRAND.md", "SITE-BRIEF.md", "output/DESIGN.md"):
            self.assertIn(token, text, token)
        snippet = repo_text(HANDOFF + "assets/AGENTS-SNIPPET.md")
        for token in ("COMPANY.md", "BRAND.md", "SITE-BRIEF.md"):
            self.assertIn(token, snippet, token)

    def test_references_carry_the_rules(self) -> None:
        company = repo_text(HANDOFF + "references/company-context.md")
        for token in ("150", "本次未做", "访谈未完成", "[候选决策]", "foundation_version"):
            self.assertIn(token, company, token)
        brief = repo_text(HANDOFF + "references/site-brief-method.md")
        for token in ("概念，未批准", "待表达", "Copy ID", "网站交接模式"):
            self.assertIn(token, brief, token)
        contract = repo_text(HANDOFF + "references/output-contracts.md")
        for token in ("company-context/v1", "site-brief/v1", "concept | working | approved"):
            self.assertIn(token, contract, token)

    def test_skill_entry(self) -> None:
        text = repo_text(HANDOFF + "SKILL.md")
        for token in (
            "COMPANY.md",
            "SITE-BRIEF.md",
            "AGENTS.md",
            "$brand-journey",
            "$brand-foundation",
            "references/company-context.md",
            "references/site-brief-method.md",
            "references/output-contracts.md",
        ):
            self.assertIn(token, text, token)


if __name__ == "__main__":
    unittest.main()
