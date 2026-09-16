# Architecture

## Components

```text
Source material
      │
      ▼
brand-foundation ──────▶ BRAND.md
                             │
                             ▼
brand-expression ──────▶ MESSAGING.md
                             │
                             ▼
brand-visual-board ────▶ Visual outputs
```

### brand-foundation

Separates facts, evidence, decisions, hypotheses, conflicts, and unknowns. Its primary output is `BRAND.md`.

### brand-expression

Transforms an existing `BRAND.md` into positioning, message hierarchy, voice guidance, and channel-ready drafts without creating new facts.

### brand-visual-board

Transforms the approved foundation and messaging into comparable visual directions, design variables, and a browser-ready brand board.

## Data boundary

Installed Skills contain methods and blank assets. Brand-specific material belongs in a separate project directory created with `scripts/create_brand_project.py`.

Derived files may reference `BRAND.md`, but they do not replace it as the source record.

## Runtime

The repository has no service process, database, or network requirement. Python helper scripts use the standard library.
