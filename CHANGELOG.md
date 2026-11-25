# Changelog

## Unreleased

### Added

- `brand-foundation`: brand architecture for a company that uses more than one public name. `BRAND.md` gains an optional name inventory; the method lists the four usual relationships between brands, with one master brand as the default candidate; and there are two optional decision prefixes, `DEC-ARCH` for how the names relate and `DEC-NAME` for the standard spelling of each. The owner chooses, and the Skill coins no names.
- `brand-expression`: standard descriptions in `MESSAGING.md`: how each name is written, one category term, the figures that may be public, one introduction in three lengths, and which length each platform uses. Platform length limits are looked up when needed, not stored.
- `brand-expression`: a read-only consistency check that lays a company's existing descriptions side by side, lists each mismatch by type, and writes `reports/YYYY-MM-DD-consistency-audit.md`. Facts that contradict each other are listed for the owner, never resolved by the Skill.
- `brand-journey`: stage 0 notes every public name and existing description it reads, stage 1 lists the names, stage 4 settles how they relate when there is more than one, stage 6 fixes the standard spelling, and the consistency check is offered after stage 7. No stage is added, and the per-stage question caps still hold.
- `scripts/check_brand_project.py`: two warnings, for a `brand_name` that differs between files and for a retired name spelling found in a derived file.
- Two behaviour scenarios: a company with several brands, and platform descriptions that contradict each other.

### Changed

- README: Codex installs this repository as a plugin from the same manifest Claude Code uses (`codex plugin marketplace add`, then `codex plugin add`). Checked on Codex CLI 0.166.0, along with the copy-into-`~/.codex/skills` route.
- `brand-handoff`: one `AGENTS.md` serves both Codex and Claude Code. When a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in the project or above it stops Claude Code from reading `AGENTS.md`, the Skill tells the user and offers a `CLAUDE.md` beside the project's `AGENTS.md` holding an `@AGENTS.md` line, instead of writing a second rules file.
- `brand-handoff`: `COMPANY.md` quotes the standard one-line description word for word, the `AGENTS.md` template and snippet tell agents to keep the standard wording, and `SITE-BRIEF.md` carries the organization details a site gives to search engines.
- The fictional example moves to version 0.3 and shows a name being standardized after a consistency check.

### Compatibility

- Records and `MESSAGING.md` files without the new content are unaffected: both schemas are unchanged, and the new checks only warn.

## 0.2.0 — 2026-11-19

### Added

- `brand-journey`: a guided client interview with eight required stages, two gates, and two optional modules (execution: product, price, channel, promotion; website: site goal and constraints). Progress is kept in `PROGRESS.md`, so an interview can be resumed from the recorded next question.
- Segment packs for export B2B, domestic B2B, and DTC e-commerce, selected from the client's material and confirmed by the operator. A registry and validator make a new industry one file and one table row.
- Refine-then-confirm method in `brand-foundation`: the client's own wording is kept as a source, the weak points are named, at most three refined versions are offered from registered facts only, and nothing is final until the named approver confirms it.
- Strategy and execution method in `brand-foundation`: diagnosis, guiding policy, positioning elements, product, price, channel, and promotion decisions.
- `brand-handoff`: `COMPANY.md`, a one-to-two-page company context any agent can read first; `AGENTS.md`, a pointer file; and `SITE-BRIEF.md`, a stack-agnostic site brief produced when the website module was done.
- `scripts/check_brand_project.py`: a read-only check for derived files that are stale against `BRAND.md` or `MESSAGING.md`, references to missing ids, forbidden progress states, a segment that differs between `BRAND.md` and `PROGRESS.md`, unknown status values, and approvals without an approver or date.
- Client questionnaire and client confirmation report templates in plain language.
- Seventeen behaviour scenarios in `evals/`, written with synthetic material.
- Claude Code plugin manifest and marketplace file.

### Changed

- `BRAND.md` moves to `schema: brand-foundation/v2`: `segment` and `operator` in the frontmatter, a competition and alternatives table, diagnosis and guiding policy, seven new decision prefixes, and two decision-table columns (`formed_by`, `origin_ref`). Claim and source id formats are now stated explicitly (`CLM-001`, `SRC-001`).
- `brand-expression` gains a website page copy route keyed by Copy ID.
- `brand-visual-board` can emit `output/DESIGN.md` in committed mode.
- `scripts/create_brand_project.py` creates `PROGRESS.md`, `AGENTS.md`, and an assembled client questionnaire, and accepts `--segment` and `--modules` (comma-separated, repeatable).
- `scripts/run_demo.py` copies the extended example and runs the project check on it.
- The fictional example is now a complete client package.

### Compatibility

- `brand-foundation/v1` records remain readable and pass the project check unchanged. A record is upgraded only when a task must write v2 fields.
- The three original Skills can still be used on their own. Their hard rules are kept: in `brand-foundation` one was extended (recording the owner's product, price, channel, and promotion decisions is foundation work when the task asks for it) and one was added (a refined statement stays a candidate until the named approver confirms it).
- New `BRAND.md` records are written as v2, and `brand-foundation` now offers refined wording beside the owner's original when used on its own.
- `scripts/validate_skills.py` now also validates segment packs and limits each `SKILL.md` to 120 lines.
