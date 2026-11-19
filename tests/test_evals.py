from __future__ import annotations

import unittest

from helpers import REPO_ROOT

import brandlib


# Add a scenario name here first, then write evals/<name>.md.
EXPECTED_EVALS: tuple[str, ...] = ()
EVAL_HEADINGS = ("## 材料", "## 操作", "## 应当出现", "## 不应出现")


class EvalsStructureTests(unittest.TestCase):
    def test_expected_evals_exist_and_nothing_else(self) -> None:
        found = sorted(
            path.stem for path in (REPO_ROOT / "evals").glob("*.md") if path.name != "README.md"
        )
        self.assertEqual(found, sorted(EXPECTED_EVALS))

    def test_every_eval_is_well_formed(self) -> None:
        for stem in EXPECTED_EVALS:
            text = (REPO_ROOT / "evals" / f"{stem}.md").read_text(encoding="utf-8")
            fm = brandlib.parse_frontmatter(text)
            self.assertEqual(fm.get("eval"), stem)
            self.assertEqual(fm.get("fictional"), "true", stem)
            self.assertIn("skills", fm, stem)  # may be []: some scenarios give no Skill on purpose
            positions = [text.find(heading) for heading in EVAL_HEADINGS]
            self.assertTrue(min(positions) >= 0 and positions == sorted(positions), stem)


if __name__ == "__main__":
    unittest.main()
