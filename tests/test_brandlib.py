from __future__ import annotations

import unittest

from helpers import REPO_ROOT  # noqa: F401  importing helpers puts scripts/ on sys.path

import brandlib


class BrandlibTests(unittest.TestCase):
    def test_parse_frontmatter_handles_crlf_and_quotes(self) -> None:
        text = (
            '---\r\nschema: "brand-foundation/v2"\r\nversion: 0.10\r\n'
            "modules: [execution, website]\r\nowner: ''\r\n---\r\n# body\r\n"
        )
        fm = brandlib.parse_frontmatter(text)
        self.assertEqual(fm["schema"], "brand-foundation/v2")
        self.assertEqual(fm["version"], "0.10")
        self.assertEqual(fm["owner"], "")
        self.assertEqual(brandlib.parse_inline_list(fm["modules"]), ["execution", "website"])
        self.assertEqual(brandlib.parse_inline_list("[]"), [])
        self.assertEqual(brandlib.parse_frontmatter("# no frontmatter\n"), {})

    def test_parse_frontmatter_drops_trailing_comments_on_plain_values(self) -> None:
        fm = brandlib.parse_frontmatter('---\npace: focused   # focused | batch\ncolor: "#fff"\n---\n')
        self.assertEqual(fm["pace"], "focused")
        self.assertEqual(fm["color"], "#fff")

    def test_parse_frontmatter_ignores_a_utf8_bom(self) -> None:
        fm = brandlib.parse_frontmatter("\ufeff---\nschema: x/v1\n---\n# body\n")
        self.assertEqual(fm.get("schema"), "x/v1")

    def test_decision_status_vocabulary(self) -> None:
        self.assertEqual(
            brandlib.DECISION_STATUSES, ("candidate", "approved", "rejected", "superseded")
        )

    def test_version_tuple_orders_numerically(self) -> None:
        self.assertGreater(brandlib.version_tuple("0.10"), brandlib.version_tuple("0.9"))
        self.assertEqual(brandlib.version_tuple("1"), (1,))
        with self.assertRaises(ValueError):
            brandlib.version_tuple("draft")

    def test_iter_table_rows_selects_tables_by_header(self) -> None:
        text = (
            "| Decision ID | choice | decision_status |\n|---|---|---|\n"
            "| DEC-PRICE-001 | 报价分 A\\|B 两档 | approved |\n| DEC-PRICE-002 | 只有两格 |\n\n"
            "| Claim ID | 主张 |\n|---|---|\n| CLM-001 | x |\n"
        )
        rows = list(brandlib.iter_table_rows(text, ["Decision ID", "decision_status"]))
        self.assertEqual([r["Decision ID"] for r in rows], ["DEC-PRICE-001", "DEC-PRICE-002"])
        self.assertEqual(rows[0]["choice"], "报价分 A|B 两档")
        self.assertEqual(rows[1]["decision_status"], "")

    def test_stage_status_vocabulary(self) -> None:
        for ok in (
            "pending",
            "in-progress",
            "awaiting-evidence",
            "done",
            "not-selected",
            "deferred: 等客户报价单",
            "skipped: 客户取消",
        ):
            self.assertTrue(brandlib.is_valid_stage_status(ok), ok)
        for bad in ("", "deferred", "deferred: ", "skipped", "complete"):
            self.assertFalse(brandlib.is_valid_stage_status(bad), bad)

    def test_find_ids_works_next_to_chinese_text(self) -> None:
        text = "见DEC-POSITIONING-001、CLM-002与COPY-010，另见SRC-003。DEC-X-1 不算。"
        self.assertEqual(
            brandlib.find_ids(text),
            {"DEC-POSITIONING-001", "CLM-002", "COPY-010", "SRC-003"},
        )


if __name__ == "__main__":
    unittest.main()
