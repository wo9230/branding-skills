# Contributing

Contributions should preserve the separation between reusable Skills and brand-specific data.

## Before opening a change

1. Keep examples fictional and mark them as synthetic.
2. Do not add personal records, customer material, internal URLs, local absolute paths, or real configuration values.
3. Keep `BRAND.md` as the source record for generated messaging and visual outputs.
4. Add or update behavior tests for script changes.
5. Run:

```bash
python3 scripts/verify_release.py .
python3 scripts/validate_skills.py .
python3 -m unittest discover -s tests -v
```

## Pull requests

Describe the observable behavior changed, the tests run, and any compatibility impact. Do not attach private source material to an issue or pull request.
