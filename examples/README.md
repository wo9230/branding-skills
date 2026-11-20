# Examples

Every example in this directory is synthetic and marked as fictional. Names, organizations, products, figures, and statements do not represent real entities or outcomes.

## fictional-b2b

A complete client project for an invented company, as it looks after the guided interview has run through every required stage and both optional modules.

| File | What it shows |
|---|---|
| `SOURCE-MATERIAL.md` | The raw input: an early self-description, interview excerpts including the owner's original vague wording, and three existing descriptions that disagree with each other |
| `PROGRESS.md` | The interview tracker: segment, selected modules, stage states, parked items, session log |
| `BRAND.md` | The single source of truth (`brand-foundation/v2`): facts with their status, the competition table, the list of public names, and the decision table with `formed_by` and `origin_ref` |
| `reports/2025-01-15-client-confirmation.md` | The plain-language report the client signs: original wording beside the suggested wording, with the reason for each change |
| `MESSAGING.md` | Website page copy, the standard descriptions (name spelling, fixed terms, one introduction in three lengths, which length each platform uses), and a Claim Map that says what may be published |
| `reports/2025-01-20-consistency-audit.md` | The consistency check: the existing descriptions side by side, each mismatch by type, what replaces each, and the owner's answers |
| `COMPANY.md` | The one-to-two-page context any agent reads first |
| `SITE-BRIEF.md` | The stack-agnostic site brief: the site's one job, page tree, page-by-page content by Copy ID, and gaps |
| `AGENTS.md` | The pointer file placed at the project root |

To follow one statement end to end, look for `DEC-POSITIONING-001`: the owner's original words are in `SOURCE-MATERIAL.md`, the refined wording and its approval are in `BRAND.md`, and the side-by-side comparison is in the confirmation report. `DEC-POSITIONING-002` is a refined draft the owner rejected.

To follow a name being standardized, look for `DEC-NAME-001`: three spellings appear in part three of `SOURCE-MATERIAL.md`, the audit report lays them side by side, `BRAND.md` records the owner's decision, and the name table in `MESSAGING.md` lists the standard, the allowed short form, and the retired spellings. This company has one brand, so there is no `DEC-ARCH` decision; `evals/18-multi-brand-architecture.md` covers a company with several.

Check the example, then copy it into a scratch directory:

```bash
python3 scripts/check_brand_project.py examples/fictional-b2b
```

```bash
python3 scripts/run_demo.py --output /tmp/branding-skills-demo
```
