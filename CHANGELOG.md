# Changelog

## 0.2.0 — 2026-11-19

### Added

- `brand-journey`: a guided client interview with eight required stages, two gates, and two optional modules (execution: product, price, channel, promotion; website: site goal and constraints). Progress is kept in `PROGRESS.md`, so an interview can be resumed from the recorded next question.
- Segment packs for export B2B, domestic B2B, and DTC e-commerce, selected from the client's material and confirmed by the operator. A registry and validator make a new industry one file and one table row.
- Refine-then-confirm method in `brand-foundation`: the client's own wording is kept as a source, the weak points are named, at most three refined versions are offered from registered facts only, and nothing is final until the named approver confirms it.
- Strategy and execution method in `brand-foundation`: diagnosis, guiding policy, positioning elements, product, price, channel, and promotion decisions.
- `brand-handoff`: `COMPANY.md`, a one-to-two-page company context any agent can read first; `AGENTS.md`, a pointer file; and `SITE-BRIEF.md`, a stack-agnostic site brief produced when the website module was done.
- `scripts/check_brand_project.py`: a read-only check for stale derived files, references to missing ids, forbidden progress states, and approvals without an approver or date.
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
