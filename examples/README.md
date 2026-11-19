# Examples

Every example in this directory is synthetic and marked as fictional. Names, organizations, products, figures, and statements do not represent real entities or outcomes.

## fictional-b2b

A complete client project for an invented company, as it looks after the guided interview has run through every required stage and both optional modules.

| File | What it shows |
|---|---|
| `SOURCE-MATERIAL.md` | The raw input: an early self-description and interview excerpts, including the owner's original vague wording |
| `PROGRESS.md` | The interview tracker: segment, selected modules, stage states, parked items, session log |
| `BRAND.md` | The single source of truth (`brand-foundation/v2`): facts with their status, the competition table, and the decision table with `formed_by` and `origin_ref` |
| `reports/2025-01-15-client-confirmation.md` | The plain-language report the client signs: original wording beside the suggested wording, with the reason for each change |
| `MESSAGING.md` | Website page copy with a Claim Map that says what may be published |
| `COMPANY.md` | The one-to-two-page context any agent reads first |
| `SITE-BRIEF.md` | The stack-agnostic site brief: the site's one job, page tree, page-by-page content by Copy ID, and gaps |
| `AGENTS.md` | The pointer file placed at the project root |

To follow one statement end to end, look for `DEC-POSITIONING-001`: the owner's original words are in `SOURCE-MATERIAL.md`, the refined wording and its approval are in `BRAND.md`, and the side-by-side comparison is in the confirmation report. `DEC-POSITIONING-002` is a refined draft the owner rejected.

Check the example, then copy it into a scratch directory:

```bash
python3 scripts/check_brand_project.py examples/fictional-b2b
```

```bash
python3 scripts/run_demo.py --output /tmp/branding-skills-demo
```
