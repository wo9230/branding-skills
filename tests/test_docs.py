from __future__ import annotations

import json
import unittest

from helpers import REPO_ROOT, repo_text  # noqa: F401

from validate_skills import SKILL_NAMES


class DocsAndPackagingTests(unittest.TestCase):
    def test_readme_covers_the_new_workflow(self) -> None:
        text = repo_text("README.md")
        for token in (
            *SKILL_NAMES,
            "必选",
            "可选",
            "PROGRESS.md",
            "COMPANY.md",
            "SITE-BRIEF.md",
            "check_brand_project.py",
            "--segment",
            "--modules",
            "Claude Code",
            "Codex",
            "致谢",
        ):
            self.assertIn(token, text, token)

    def test_readme_installs_in_codex_and_shares_one_rules_file(self) -> None:
        readme = repo_text("README.md")
        for token in (
            "codex plugin marketplace add wo9230/branding-skills",
            "codex plugin add branding-skills@branding-skills",
            "@AGENTS.md",
        ):
            self.assertIn(token, readme, token)

    def test_readme_says_what_blocks_agents_md_and_where_the_import_goes(self) -> None:
        readme = repo_text("README.md")
        for token in (
            "`.claude/CLAUDE.md`",
            "`CLAUDE.local.md`",
            "`~/.claude/CLAUDE.md`",
            "和 `AGENTS.md` 同一个目录",
        ):
            self.assertIn(token, readme, token)
        self.assertNotIn("在那份 `CLAUDE.md` 里加一行", readme)

    def test_contributing_explains_how_to_add_a_segment_pack(self) -> None:
        text = repo_text("CONTRIBUTING.md")
        for token in ("segments/INDEX.md", "validate_skills.py", "check_brand_project.py", "evals/"):
            self.assertIn(token, text, token)

    def test_scope_architecture_and_changelog_are_current(self) -> None:
        self.assertIn("Five", repo_text("OSS-SCOPE.md"))
        architecture = repo_text("docs/ARCHITECTURE.md")
        for name in SKILL_NAMES:
            self.assertIn(name, architecture, name)
        self.assertIn("0.2.0", repo_text("CHANGELOG.md"))

    def test_docs_do_not_overstate(self) -> None:
        # Corrections from the final review.
        readme = repo_text("README.md")
        self.assertIn("`brand-journey` 需要和 `brand-foundation` 一起安装", readme)
        self.assertIn("--modules execution,website", readme)
        self.assertNotIn("--modules execution website", readme)
        changelog = repo_text("CHANGELOG.md")
        self.assertNotIn("hard rules are unchanged", changelog)
        self.assertIn("one was extended", changelog)
        self.assertIn("Reports are dated snapshots", repo_text("docs/ARCHITECTURE.md"))

    def test_plugin_manifest_is_valid_json(self) -> None:
        manifest = json.loads(repo_text(".claude-plugin/plugin.json"))
        self.assertEqual(manifest["name"], "branding-skills")
        self.assertEqual(manifest["version"], "0.2.0")
        self.assertGreaterEqual(len(manifest["description"]), 40)
        marketplace = json.loads(repo_text(".claude-plugin/marketplace.json"))
        self.assertEqual(marketplace["plugins"][0]["name"], "branding-skills")


if __name__ == "__main__":
    unittest.main()
