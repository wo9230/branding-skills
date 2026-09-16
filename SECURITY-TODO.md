# Security TODO

## Before first remote publication

- [x] Review the final Git-add candidate file list with a dry run.
- [x] Run the filesystem credential scans recorded in `security-reports/`.
- [x] Run the private deny-list scan from a file stored outside this repository.
- [ ] Enable GitHub credential scanning and push protection. On 2026-09-16, GitHub returned HTTP 422 because this feature was unavailable for the private repository under its current plan. Do not push until the repository becomes eligible or the owner explicitly changes this publication gate.
- [x] Configure this local repository with a non-private commit identity.

## Credential rotation

No credential rotation entries are currently recorded for this extracted repository.

If a credential is ever found in an earlier source or external copy, record only its type and location here, rotate it before publication, and do not include the value.
