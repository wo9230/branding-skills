from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import PACK_OK, make_segments, make_skill_tree, run_script, write


REPO_ROOT = Path(__file__).resolve().parents[1]
CREATE_SCRIPT = REPO_ROOT / "scripts" / "create_brand_project.py"
DEMO_SCRIPT = REPO_ROOT / "scripts" / "run_demo.py"
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "verify_release.py"


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
            for name in ("SOURCE-MATERIAL.md", "BRAND.md", "MESSAGING.md"):
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
