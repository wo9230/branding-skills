# Contributing

Contributions should preserve the separation between reusable Skills and brand-specific data.

## Before opening a change

1. Keep examples and eval scenarios fictional and mark them as synthetic.
2. Do not add personal records, customer material, internal URLs, local absolute paths, or real configuration values.
3. Keep `BRAND.md` as the source record for generated messaging, handoff, and visual outputs.
4. Add or update behavior tests for script changes.
5. Keep every `SKILL.md` within 120 lines; move detail into `references/`.
6. When a Skill file and a script share a term (a stage id, a status value, a column name), change `scripts/brandlib.py`, the reference file, and the contract test together.
7. Run:

```bash
python3 scripts/verify_release.py .
python3 scripts/validate_skills.py .
python3 -m unittest discover -s tests -v
python3 scripts/check_brand_project.py examples/fictional-b2b
```

## Adding a segment pack

A segment pack adds the questions, proof types, and site pattern for one kind of client. Adding an industry takes one file and one table row.

1. Create `skills/brand-journey/references/segments/<id>.md`. Use lowercase letters, digits, and hyphens for the id. `generic` and `unknown` are reserved.
2. Give the file exactly eight level-two headings, in this order and with this wording: `## 1. 识别信号`, `## 2. 各阶段加问`, `## 3. 价格模块`, `## 4. 渠道模块`, `## 5. 证明与高风险说法`, `## 6. 网站交接模式`, `## 7. 表达注意`, `## 8. 问卷加问`.
3. Under section 8, add exactly three level-three headings in this order: `### 核心`, `### 落地`, `### 建站`. The project initializer assembles the client questionnaire from them.
4. Register the pack with one row in `skills/brand-journey/references/segments/INDEX.md`.
5. Do not write industry benchmark figures. Conversion rates, acquisition costs, and similar numbers may only come from a client's own data or from research with a source and date.
6. Run `python3 scripts/validate_skills.py .`; it checks the registry against the files and each pack's structure.

## Adding a behaviour scenario

Scenarios in `evals/` check that an agent with no background can do the right thing from the Skill files alone.

1. Add the scenario name to `EXPECTED_EVALS` in `tests/test_evals.py`.
2. Write `evals/<name>.md` in the format described in `evals/README.md`, using invented material only.
3. Run the scenario as that README describes and fix the Skill file, not the scenario, when a check fails.

## Pull requests

Describe the observable behavior changed, the tests run, and any compatibility impact. Do not attach private source material to an issue or pull request.
