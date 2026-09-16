# Scan Summary

Scan date: 2026-09-16

## Filesystem scanners

| Check | Version | Exit status | Recorded result | Report |
|---|---|---:|---|---|
| Gitleaks filesystem scan | 8.30.1 | 0 | 0 findings | `gitleaks-filesystem.json` |
| TruffleHog filesystem scan | 3.97.4 | 0 | 0 output records; tool summary reported 0 verified and 0 unverified findings | `trufflehog-filesystem.jsonl` |
| Credential-keyword scan | ripgrep | 1 | No matches; ripgrep uses exit status 1 when no line matches | `credential-keyword-scan.txt` |
| External private deny-list scan | ripgrep | 1 | No matches; ripgrep uses exit status 1 when no line matches | `private-deny-scan.txt` |

The external deny-list file was not copied into this repository. Empty text reports are retained as evidence that the corresponding command produced no matching lines.

These results describe the commands that were run against this filesystem snapshot. They do not replace review of the staged file list or the repository host's scanning and push-protection controls before publication.
