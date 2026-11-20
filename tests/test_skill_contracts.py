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

    def test_one_agents_file_serves_claude_code_and_codex(self) -> None:
        contract = repo_text(HANDOFF + "references/output-contracts.md")
        for token in ("Codex", "Claude Code", "@AGENTS.md"):
            self.assertIn(token, contract, token)

    def test_claude_md_import_sits_beside_the_project_agents_file(self) -> None:
        contract = repo_text(HANDOFF + "references/output-contracts.md")
        for token in (
            "`.claude/CLAUDE.md`",
            "`CLAUDE.local.md`",
            "`~/.claude/CLAUDE.md`",
            "和 `AGENTS.md` 同一个目录",
            "不写进上级目录的文件",
        ):
            self.assertIn(token, contract, token)
        self.assertNotIn("在那份 `CLAUDE.md` 里加一行", contract)
        entry = repo_text(HANDOFF + "SKILL.md")
        for token in ("`.claude/CLAUDE.md`", "`CLAUDE.local.md`", "beside the project's `AGENTS.md`"):
            self.assertIn(token, entry, token)


if __name__ == "__main__":
    unittest.main()


class ExpressionAndVisualContractTests(unittest.TestCase):
    def test_expression_covers_website_page_copy(self) -> None:
        text = repo_text("skills/brand-expression/references/offer-and-channel-copy.md")
        for token in ("## 网站页面文案", "Copy ID", "SITE-BRIEF.md", "segment", "export-b2b"):
            self.assertIn(token, text, token)
        entry = repo_text("skills/brand-expression/SKILL.md")
        self.assertIn("Website page copy", entry)
        self.assertLessEqual(len(entry.splitlines()), 120)

    def test_visual_board_can_emit_design_md(self) -> None:
        contract = repo_text("skills/brand-visual-board/references/output-contracts.md")
        for token in (
            "## `output/DESIGN.md`",
            "committed",
            "查阅日期",
            "google-labs-code/design.md",
        ):
            self.assertIn(token, contract, token)
        self.assertIn("output/DESIGN.md", repo_text("skills/brand-visual-board/SKILL.md"))


class ReviewFixContractTests(unittest.TestCase):
    """Text rules added after the final whole-branch review."""

    def test_version_rule_is_stated_where_versions_are_written_and_read(self) -> None:
        contract = repo_text(FOUNDATION + "references/output-contracts.md")
        for token in ("按数字比较", '"0.10"'):
            self.assertIn(token, contract, token)
        for path in (HANDOFF + "assets/AGENTS-TEMPLATE.md", HANDOFF + "assets/AGENTS-SNIPPET.md"):
            self.assertIn("按数字比较", repo_text(path), path)

    def test_decision_status_values_and_relay_note_location(self) -> None:
        contract = repo_text(FOUNDATION + "references/output-contracts.md")
        for status in brandlib.DECISION_STATUSES:
            self.assertIn(f"`{status}`", contract, status)
        for path in (JOURNEY + "references/conduct-modes.md", JOURNEY + "references/output-contracts.md"):
            text = repo_text(path)
            self.assertIn("经操作者转述", text, path)
            self.assertIn("变更记录", text, path)

    def test_decision_row_cells_hold_bare_values(self) -> None:
        # Found in the end-to-end walkthrough: notes such as "经操作者转述" were written
        # into the owner cell, and two sources were listed in origin_ref.
        contract = repo_text(FOUNDATION + "references/output-contracts.md")
        for token in ("只写审批人", "用顿号隔开", "不写进"):
            self.assertIn(token, contract, token)

    def test_working_version_at_the_gate_has_a_recorded_form(self) -> None:
        text = repo_text(JOURNEY + "references/stage-map.md")
        for token in ("接受为工作版本", "保持 `candidate`"):
            self.assertIn(token, text, token)

    def test_secondary_segment_pack_survives_a_resume(self) -> None:
        self.assertIn("第二细分包：", repo_text(JOURNEY + "references/segments/INDEX.md"))

    def test_partial_approval_scope_rule(self) -> None:
        text = repo_text(JOURNEY + "references/output-contracts.md")
        for token in ("approval_scope", "暂缓的事项"):
            self.assertIn(token, text, token)

    def test_client_report_template_matches_its_contract(self) -> None:
        template = repo_text(JOURNEY + "assets/CLIENT-REPORT-TEMPLATE.md")
        contract = repo_text(JOURNEY + "references/output-contracts.md")
        sections = [line for line in template.splitlines() if line.startswith("## ")]
        self.assertEqual(len(sections), 6)
        for token in ("保留意见", "这些内容从哪里来"):
            self.assertIn(token, template, token)
            self.assertIn(token, contract, token)


EXPRESSION = "skills/brand-expression/"


def table_header(columns: tuple[str, ...]) -> str:
    return "| " + " | ".join(columns) + " |"


class BrandArchitectureContractTests(unittest.TestCase):
    def test_architecture_reference_is_complete(self) -> None:
        text = repo_text(FOUNDATION + "references/brand-architecture.md")
        for heading in (
            "## 什么时候用",
            "## 列名称清单",
            "## 品牌，还是只是名称",
            "## 四种关系",
            "## 默认与分开的理由",
            "## 怎么提候选",
            "## 证明与承诺的边界",
            "## 标准写法",
            "## 一个品牌一份档案",
            "## 不做什么",
        ):
            self.assertIn(heading, text, heading)
        for token in (
            "单一主品牌",
            "主品牌带子品牌",
            "背书品牌",
            "各自独立",
            "最多三个",
            "DEC-ARCH",
            "DEC-NAME",
            table_header(brandlib.NAME_INVENTORY_HEADERS),
        ):
            self.assertIn(token, text, token)

    def test_new_prefixes_are_shared_vocabulary(self) -> None:
        for prefix in ("DEC-ARCH", "DEC-NAME"):
            self.assertIn(prefix, brandlib.NEW_DECISION_PREFIXES)
            self.assertNotIn(prefix, brandlib.STATEMENT_PREFIXES)
            self.assertEqual(brandlib.find_ids(f"{prefix}-001"), {f"{prefix}-001"})

    def test_output_contract_registers_the_name_inventory(self) -> None:
        text = repo_text(FOUNDATION + "references/output-contracts.md")
        for token in (
            "对外名称清单",
            table_header(brandlib.NAME_INVENTORY_HEADERS),
            "可选内容",
            "brand-architecture.md",
        ):
            self.assertIn(token, text, token)

    def test_entry_routing_and_workbook_reach_the_reference(self) -> None:
        entry = repo_text(FOUNDATION + "SKILL.md")
        self.assertIn("references/brand-architecture.md", entry)
        self.assertLessEqual(len(entry.splitlines()), 120)
        self.assertIn(
            "brand-architecture.md", repo_text(FOUNDATION + "references/scenario-branches.md")
        )
        self.assertIn("| 名称与架构 |", repo_text(FOUNDATION + "references/interview-routing.md"))
        self.assertIn("对外用着哪些名称", repo_text(FOUNDATION + "assets/BRAND-WORKBOOK.md"))


AUDIT_REPORT = "reports/YYYY-MM-DD-consistency-audit.md"


class ConsistentDescriptionsContractTests(unittest.TestCase):
    def test_reference_covers_standard_descriptions_and_the_audit(self) -> None:
        text = repo_text(EXPRESSION + "references/consistent-descriptions.md")
        for heading in (
            "## 标准说法包含什么",
            "## 三档介绍",
            "## 不能变和可以变",
            "## 平台对照表",
            "## 给网站用的机构信息",
            "## 一致性体检",
            "## 不做什么",
        ):
            self.assertIn(heading, text, heading)
        for token in (
            "一句话",
            "短介绍",
            "标准介绍",
            "查询日期",
            "未检查",
            "alternateName",
            "sameAs",
            "DEC-NAME",
            "DEC-ARCH",
            AUDIT_REPORT,
            table_header(brandlib.NAME_WRITING_HEADERS),
        ):
            self.assertIn(token, text, token)

    def test_reference_names_every_kind_of_mismatch(self) -> None:
        text = repo_text(EXPRESSION + "references/consistent-descriptions.md")
        for kind in (
            "名称写法不同",
            "数字或事实对不上",
            "品类说法不同",
            "品牌关系说不清",
            "内容过期",
            "说了不能说的话",
        ):
            self.assertIn(kind, text, kind)

    def test_messaging_template_has_the_standard_section(self) -> None:
        text = repo_text(EXPRESSION + "assets/MESSAGING-TEMPLATE.md")
        for token in (
            "## 标准说法",
            "### 名称写法",
            "### 固定用词",
            "### 三档介绍",
            "### 平台对照",
            table_header(brandlib.NAME_WRITING_HEADERS),
        ):
            self.assertIn(token, text, token)
        self.assertLess(text.find("## 标准说法"), text.find("## Claim Map"))

    def test_contract_and_entry_point_to_the_reference(self) -> None:
        contract = repo_text(EXPRESSION + "references/output-contracts.md")
        for token in ("标准说法", AUDIT_REPORT, "consistent-descriptions.md"):
            self.assertIn(token, contract, token)
        entry = repo_text(EXPRESSION + "SKILL.md")
        self.assertIn("references/consistent-descriptions.md", entry)
        self.assertLessEqual(len(entry.splitlines()), 120)
        self.assertIn(
            "consistent-descriptions.md",
            repo_text(EXPRESSION + "references/offer-and-channel-copy.md"),
        )


def must_answer_counts(stage_map: str) -> dict[str, int]:
    """Count the bullets under every bold "必答" label, per stage section of the stage map."""
    counts: dict[str, int] = {}
    stage = ""
    counting = False
    for line in stage_map.splitlines():
        if line.startswith("## "):
            head = line[3:].split("：", 1)[0]
            stage = head.split(" ", 1)[1] if head.startswith(("阶段 ", "模块 ")) else ""
            counting = False
        elif line.startswith("**"):
            counting = "必答" in line
        elif counting and stage and line.startswith("- "):
            counts[stage] = counts.get(stage, 0) + 1
    return counts


def pack_must_answer_counts(pack: str) -> dict[str, int]:
    """Count the "- 必答：" bullets a segment pack adds to each stage."""
    counts: dict[str, int] = {}
    stage = ""
    for line in pack.splitlines():
        if line.startswith("### 阶段 "):
            stage = line.split(" ")[2]
        elif line.startswith("#"):
            stage = ""
        elif stage and line.startswith("- 必答："):
            counts[stage] = counts.get(stage, 0) + 1
    return counts


class ConsistencyWiringContractTests(unittest.TestCase):
    def test_stage_map_places_names_architecture_and_the_audit(self) -> None:
        text = repo_text(JOURNEY + "references/stage-map.md")
        for token in (
            "对外名称清单",
            "DEC-ARCH",
            "DEC-NAME",
            "一致性体检",
            "references/brand-architecture.md",
        ):
            self.assertIn(token, text, token)

    def test_must_answer_caps_still_hold_with_every_pack(self) -> None:
        core = must_answer_counts(repo_text(JOURNEY + "references/stage-map.md"))
        self.assertEqual(core["0"], 4)
        self.assertEqual(core["6"], 4)
        for file_name in brandlib.read_segment_index(REPO_ROOT).values():
            added = pack_must_answer_counts(repo_text(SEGMENTS + file_name))
            for stage, count in core.items():
                cap = 4 if stage == "0" else 5
                self.assertLessEqual(count + added.get(stage, 0), cap, f"{file_name} stage {stage}")

    def test_questionnaire_asks_for_names_and_existing_descriptions(self) -> None:
        text = repo_text(JOURNEY + "assets/CLIENT-QUESTIONNAIRE.md")
        core = text.split("<!-- part:core -->", 1)[1].split("<!-- part:execution -->", 1)[0]
        for token in ("对外用着哪些名字", "现在各处是怎么介绍"):
            self.assertIn(token, core, token)

    def test_journey_entry_and_contract_mention_the_new_work(self) -> None:
        entry = repo_text(JOURNEY + "SKILL.md")
        for token in ("brand architecture", "consistency check", "references/brand-architecture.md"):
            self.assertIn(token, entry, token)
        self.assertLessEqual(len(entry.splitlines()), 120)
        contract = repo_text(JOURNEY + "references/output-contracts.md")
        for token in ("一致性体检", AUDIT_REPORT, "DEC-ARCH", "DEC-NAME"):
            self.assertIn(token, contract, token)

    def test_segment_packs_mention_the_name_inventory(self) -> None:
        for file_name in brandlib.read_segment_index(REPO_ROOT).values():
            self.assertIn("名称清单", repo_text(SEGMENTS + file_name), file_name)

    def test_handoff_files_carry_the_standard_descriptions(self) -> None:
        for path in (
            "references/company-context.md",
            "assets/COMPANY-TEMPLATE.md",
            "assets/AGENTS-TEMPLATE.md",
            "assets/AGENTS-SNIPPET.md",
        ):
            self.assertIn("标准说法", repo_text(HANDOFF + path), path)
        self.assertIn("DEC-ARCH", repo_text(HANDOFF + "references/company-context.md"))
        for path in ("references/site-brief-method.md", "assets/SITE-BRIEF-TEMPLATE.md"):
            self.assertIn("机构信息", repo_text(HANDOFF + path), path)
        self.assertIn("standard descriptions", repo_text(HANDOFF + "SKILL.md"))
