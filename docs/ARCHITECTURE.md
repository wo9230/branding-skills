# Architecture

## Components

```text
Source material
      │
      ▼
brand-journey ─────────▶ PROGRESS.md, client confirmation report
      │  calls
      ▼
brand-foundation ──────▶ BRAND.md  (single source of truth)
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
brand-expression     brand-visual-board     brand-handoff
   MESSAGING.md        Visual outputs,      COMPANY.md, AGENTS.md,
                       output/DESIGN.md     SITE-BRIEF.md
```

### brand-journey

Owns the process of a client interview: eight required stages with two gates, two optional modules (execution, website), segment packs, progress tracking, and how to talk with the client. It defines no method of its own. At each stage it calls `brand-foundation` and writes through that Skill's record contract. Its own outputs are `PROGRESS.md`, which holds process state only, and the client confirmation report.

Segment packs live in `skills/brand-journey/references/segments/`. Each pack is one file with eight fixed sections, registered in `INDEX.md`.

### brand-foundation

Separates facts, evidence, decisions, hypotheses, conflicts, and unknowns. Its primary output is `BRAND.md` (`brand-foundation/v2`; v1 records remain readable). It also holds the methods the journey relies on: strategy and execution decisions, and the refine-then-confirm procedure that turns a client's own wording into a statement the client has approved.

### brand-expression

Transforms an existing `BRAND.md` into positioning, message hierarchy, voice guidance, channel-ready drafts, and website page copy without creating new facts. Every load-bearing line is registered with a Copy ID in `MESSAGING.md`.

### brand-visual-board

Transforms the approved foundation and messaging into comparable visual directions, design variables, and a browser-ready brand board. In committed mode it can also emit `output/DESIGN.md` for site-building agents.

### brand-handoff

Derives the files other agents read: `COMPANY.md`, a one-to-two-page company context; `AGENTS.md`, a pointer file for the project root; and `SITE-BRIEF.md`, a stack-agnostic site brief produced only when the website module was done. It adds no fact and makes no decision.

## Data boundary

Installed Skills contain methods and blank assets. Brand-specific material belongs in a separate project directory created with `scripts/create_brand_project.py`.

- `BRAND.md` is the only source of truth for facts and decisions.
- `PROGRESS.md` records process only: selected modules, stage states, the next question, parked items.
- `MESSAGING.md`, `COMPANY.md`, `SITE-BRIEF.md`, and visual outputs are derived. Each records the `BRAND.md` version it was built from and never replaces it. Versions are dotted integers compared numerically, so `0.10` is newer than `0.9`.
- Reports are dated snapshots. They carry a date rather than a version and are never read back as a source of truth.
- A candidate, hypothesis, or unknown keeps its label in every derived file.

`scripts/check_brand_project.py` reads a project and reports derived files that are stale, references to ids that do not exist, progress states the journey forbids, and approvals without an approver or date. It never writes.

## Shared vocabulary

Stage ids, status values, module names, and column names are defined once in `scripts/brandlib.py`. Contract tests in `tests/test_skill_contracts.py` check that the Skill reference files use the same tokens the scripts enforce.

## Runtime

The repository has no service process, database, or network requirement. Python helper scripts use the standard library. Behaviour scenarios in `evals/` are run by hand or by an agent and are not part of CI.
