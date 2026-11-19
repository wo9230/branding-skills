from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import PACK_OK, make_segments, make_skill_tree, run_script, write

import brandlib


REPO_ROOT = Path(__file__).resolve().parents[1]
CREATE_SCRIPT = REPO_ROOT / "scripts" / "create_brand_project.py"
DEMO_SCRIPT = REPO_ROOT / "scripts" / "run_demo.py"
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "verify_release.py"
EXAMPLE = REPO_ROOT / "examples" / "fictional-b2b"
DEMO_FILES = (
    "SOURCE-MATERIAL.md",
    "AGENTS.md",
    "PROGRESS.md",
    "BRAND.md",
    "MESSAGING.md",
    "COMPANY.md",
    "SITE-BRIEF.md",
    "reports/2025-01-15-client-confirmation.md",
)


class CreateBrandProjectTests(unittest.TestCase):
    def test_creates_isolated_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "sample-brand"
            result = subprocess.run(
                [sys.executable, str(CREATE_SCRIPT), str(destination)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "README.md").is_file())
            self.assertTrue((destination / "intake" / "BRAND-WORKBOOK.md").is_file())
            self.assertTrue((destination / "sources").is_dir())
            self.assertTrue((destination / "reports").is_dir())
            self.assertTrue((destination / "output").is_dir())

    def test_rejects_destination_inside_repository(self) -> None:
        destination = REPO_ROOT / "sample-project-test"
        result = subprocess.run(
            [sys.executable, str(CREATE_SCRIPT), str(destination)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the branding-skills repository", result.stderr)
        self.assertFalse(destination.exists())

    def create(self, destination: Path, *args: str):
        return run_script("create_brand_project.py", destination, *args)

    def progress(self, destination: Path):
        text = (destination / "PROGRESS.md").read_text(encoding="utf-8")
        rows = {
            row["stage"]: row["status"]
            for row in brandlib.iter_table_rows(text, ["stage", "status"])
        }
        return brandlib.parse_frontmatter(text), rows

    def test_creates_journey_files_with_core_only_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "sample-brand"
            self.assertEqual(self.create(destination).returncode, 0)
            self.assertTrue((destination / "AGENTS.md").is_file())
            fm, rows = self.progress(destination)
            self.assertEqual(fm["segment"], "unknown")
            self.assertEqual(brandlib.parse_inline_list(fm["modules"]), [])
            self.assertEqual([rows[s] for s in ("E1", "E2", "W1")], ["not-selected"] * 3)
            questionnaire = (destination / "intake" / "CLIENT-QUESTIONNAIRE.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("<!-- part:core -->", questionnaire)
            self.assertNotIn("part:execution", questionnaire)
            self.assertNotIn("part:website", questionnaire)
            self.assertNotIn("<!-- segment:", questionnaire)
            readme = (destination / "README.md").read_text(encoding="utf-8")
            for token in ("PROGRESS.md", "AGENTS.md", "CLIENT-QUESTIONNAIRE.md", "$brand-journey"):
                self.assertIn(token, readme, token)

    def test_segment_and_modules_shape_progress_and_questionnaire(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "sample-brand"
            result = self.create(destination, "--segment", "export-b2b", "--modules", "execution")
            self.assertEqual(result.returncode, 0, result.stderr)
            fm, rows = self.progress(destination)
            self.assertEqual(fm["segment"], "export-b2b")
            self.assertEqual(brandlib.parse_inline_list(fm["modules"]), ["execution"])
            self.assertEqual(
                [rows[s] for s in ("E1", "E2", "W1")], ["pending", "pending", "not-selected"]
            )
            self.assertEqual(rows["4"], "pending")
            text = (destination / "intake" / "CLIENT-QUESTIONNAIRE.md").read_text(encoding="utf-8")
            order = [
                text.find(mark)
                for mark in (
                    "<!-- part:core -->",
                    "<!-- segment:export-b2b part:core -->",
                    "<!-- part:execution -->",
                    "<!-- segment:export-b2b part:execution -->",
                )
            ]
            self.assertTrue(min(order) >= 0 and order == sorted(order), order)
            self.assertNotIn("part:website", text)
            self.assertIn("你们的产品主要卖到哪些国家或地区？", text)
            self.assertNotIn("希望网站用哪些语言？", text)

    def test_generic_segment_adds_no_pack_questions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "sample-brand"
            result = self.create(
                destination, "--segment", "generic", "--modules", "website", "execution"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            fm, rows = self.progress(destination)
            self.assertEqual(fm["segment"], "generic")
            self.assertEqual(brandlib.parse_inline_list(fm["modules"]), ["execution", "website"])
            self.assertEqual([rows[s] for s in ("E1", "E2", "W1")], ["pending"] * 3)
            text = (destination / "intake" / "CLIENT-QUESTIONNAIRE.md").read_text(encoding="utf-8")
            self.assertLess(text.find("<!-- part:execution -->"), text.find("<!-- part:website -->"))
            self.assertNotIn("<!-- segment:", text)

    def test_rejects_unknown_segment_without_creating_anything(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "sample-brand"
            result = self.create(destination, "--segment", "pet-food")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown segment 'pet-food'", result.stderr)
            self.assertIn("domestic-b2b, dtc-ecommerce, export-b2b, generic", result.stderr)
            self.assertFalse(destination.exists())

    def test_rejects_unknown_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "sample-brand"
            result = self.create(destination, "--modules", "ads")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid choice", result.stderr)
            self.assertFalse(destination.exists())

    def test_creates_project_in_non_ascii_path_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "客户 项目" / "青岛 样例"
            result = self.create(destination, "--segment", "dtc-ecommerce", "--modules", "website")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "PROGRESS.md").is_file())
            text = (destination / "intake" / "CLIENT-QUESTIONNAIRE.md").read_text(encoding="utf-8")
            self.assertIn("<!-- segment:dtc-ecommerce part:website -->", text)


class DemoTests(unittest.TestCase):
    def test_creates_demo_from_synthetic_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "demo"
            result = subprocess.run(
                [
                    sys.executable,
                    str(DEMO_SCRIPT),
                    "--output",
                    str(destination),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DEMO PASSED", result.stdout)
            for name in DEMO_FILES:
                path = destination / name
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8").lower()
                self.assertTrue("fictional: true" in text or "虚构" in text)

    def test_rejects_nonempty_demo_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            destination = Path(temporary_root) / "demo"
            destination.mkdir()
            (destination / "existing.txt").write_text("keep", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(DEMO_SCRIPT),
                    "--output",
                    str(destination),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not empty", result.stderr)
            self.assertEqual(
                (destination / "existing.txt").read_text(encoding="utf-8"),
                "keep",
            )

    def test_example_passes_project_check_without_warnings(self) -> None:
        result = run_script("check_brand_project.py", EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("5 files checked, 0 warnings", result.stdout)

    def test_example_shows_a_refined_and_confirmed_statement(self) -> None:
        text = (EXAMPLE / "BRAND.md").read_text(encoding="utf-8")
        self.assertEqual(brandlib.parse_frontmatter(text)["schema"], "brand-foundation/v2")
        rows = list(brandlib.iter_table_rows(text, ["Decision ID", "formed_by", "origin_ref"]))
        refined = [
            row
            for row in rows
            if row["formed_by"] == "ai-refined" and row["decision_status"] == "approved"
        ]
        self.assertTrue(refined)
        self.assertTrue(all(row["origin_ref"] for row in refined))
        self.assertTrue(any(row["decision_status"] == "candidate" for row in rows))
        self.assertTrue(any(row["decision_status"] == "rejected" for row in rows))
        report = (EXAMPLE / "reports" / "2025-01-15-client-confirmation.md").read_text(encoding="utf-8")
        for token in ("您原来的说法", "建议的说法", "为什么这样改"):
            self.assertIn(token, report, token)

    def test_example_company_file_follows_the_contract(self) -> None:
        text = (EXAMPLE / "COMPANY.md").read_text(encoding="utf-8")
        headings = [line for line in text.splitlines() if line.startswith("## ")]
        self.assertEqual(len(headings), 12)
        self.assertLessEqual(len(text.splitlines()), 150)
        brief = (EXAMPLE / "SITE-BRIEF.md").read_text(encoding="utf-8")
        self.assertEqual(len([line for line in brief.splitlines() if line.startswith("## ")]), 9)

    def test_demo_fails_when_fixture_breaks_the_check(self) -> None:
        # run_demo must really run the self-check: hand it a broken copy of the example.
        with tempfile.TemporaryDirectory() as temporary_root:
            fixture = Path(temporary_root) / "fixture"
            shutil.copytree(EXAMPLE, fixture)
            brief = fixture / "SITE-BRIEF.md"
            brief.write_text(
                brief.read_text(encoding="utf-8") + "\n另见 COPY-999（虚构）。\n", encoding="utf-8"
            )
            result = run_script(
                "run_demo.py", "--output", Path(temporary_root) / "out", "--fixture", fixture
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown reference COPY-999", result.stdout)
            self.assertNotIn("DEMO PASSED", result.stdout)


class VerifyReleaseTests(unittest.TestCase):
    def test_current_release_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VERIFY_SCRIPT), str(REPO_ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_detects_private_path_in_external_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            fixture_root = Path(temporary_root)
            for skill_name in (
                "brand-foundation",
                "brand-expression",
                "brand-visual-board",
            ):
                skill_dir = fixture_root / "skills" / skill_name
                skill_dir.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text("---\nname: test\n---\n", encoding="utf-8")

            private_path = "/" + "Users/" + "example/private-file.md"
            (fixture_root / "leak.md").write_text(private_path, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(fixture_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("macOS absolute user path", result.stdout)

    def test_rejects_excluded_data_file_type(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            fixture_root = Path(temporary_root)
            for skill_name in (
                "brand-foundation",
                "brand-expression",
                "brand-visual-board",
            ):
                skill_dir = fixture_root / "skills" / skill_name
                skill_dir.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text("---\nname: test\n---\n", encoding="utf-8")

            (fixture_root / "sample.csv").write_text("name,value\nalpha,1\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(fixture_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("excluded file type", result.stdout)

    def test_requires_fictional_marker_in_evals(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            root = Path(temporary_root)
            write(root / "evals" / "README.md", "# Evals\n")
            write(root / "evals" / "01-sample.md", "# 场景\n没有标注\n")
            result = run_script("verify_release.py", root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("eval lacks fictional marker: evals/01-sample.md", result.stdout)
            self.assertNotIn("evals/README.md", result.stdout)


class ValidateSkillsTests(unittest.TestCase):
    def run_fixture(self, packs, index_rows=None, mutate=None):
        with tempfile.TemporaryDirectory() as temporary_root:
            root = make_skill_tree(Path(temporary_root))
            make_segments(root, packs, index_rows)
            if mutate:
                mutate(root)
            return run_script("validate_skills.py", root)

    def test_repository_passes_with_three_packs(self) -> None:
        result = run_script("validate_skills.py", REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("3 segment packs", result.stdout)

    def test_valid_fixture_passes(self) -> None:
        result = self.run_fixture({"export-b2b": PACK_OK})
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("1 segment packs", result.stdout)

    def test_rejects_missing_section(self) -> None:
        broken = PACK_OK.replace("## 5. 证明与高风险说法\n", "")
        self.assertNotEqual(broken, PACK_OK)
        result = self.run_fixture({"export-b2b": broken})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("export-b2b.md", result.stdout)
        self.assertIn("证明与高风险说法", result.stdout)

    def test_rejects_extra_level_two_heading(self) -> None:
        result = self.run_fixture({"export-b2b": PACK_OK + "\n## 9. 其他\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("export-b2b.md", result.stdout)

    def test_rejects_missing_questionnaire_group(self) -> None:
        broken = PACK_OK.replace("### 建站\n", "")
        self.assertNotEqual(broken, PACK_OK)
        result = self.run_fixture({"export-b2b": broken})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("section 8", result.stdout)

    def test_rejects_unregistered_pack(self) -> None:
        result = self.run_fixture(
            {"export-b2b": PACK_OK, "extra": PACK_OK},
            index_rows={"export-b2b": "export-b2b.md"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unregistered segment pack: extra.md", result.stdout)

    def test_rejects_registered_file_that_is_missing(self) -> None:
        result = self.run_fixture(
            {"export-b2b": PACK_OK},
            index_rows={"export-b2b": "export-b2b.md", "pets": "pets.md"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("segment file missing: pets.md", result.stdout)

    def test_rejects_reserved_segment_id(self) -> None:
        result = self.run_fixture({"generic": PACK_OK})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reserved segment id: generic", result.stdout)

    def test_rejects_segment_id_that_differs_from_file_name(self) -> None:
        result = self.run_fixture(
            {"export-b2b": PACK_OK}, index_rows={"overseas": "export-b2b.md"}
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("segment id must match file name: overseas", result.stdout)

    def test_rejects_missing_index(self) -> None:
        def mutate(root: Path) -> None:
            (root / "skills/brand-journey/references/segments/INDEX.md").unlink()

        result = self.run_fixture({"export-b2b": PACK_OK}, mutate=mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("segments index missing", result.stdout)

    def test_rejects_overlong_skill_file(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "brand-foundation" / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8") + "line\n" * 130, encoding="utf-8")

        result = self.run_fixture({"export-b2b": PACK_OK}, mutate=mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exceeds 120 lines", result.stdout)


if __name__ == "__main__":
    unittest.main()
