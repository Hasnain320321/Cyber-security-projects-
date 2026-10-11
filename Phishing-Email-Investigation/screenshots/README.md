# Project 4 — User-Captured Practical Evidence

**Status: 1 screenshot uploaded and verified; 3 other screenshots pending.** This folder is prepared for genuine user-captured evidence from the local Windows/Python investigation. Screenshots seen in chat count as GitHub evidence only when their actual PNG has been committed and reviewed.

## Planned screenshot set

| Intended filename | Actual work shown | GitHub upload |
| --- | --- | --- |
| `01-python-unit-tests-passed.png` | PowerShell `python -m unittest discover -s tests -v`, 4/4 OK | Pending |
| `02-case0042-sample-list.png` | `Get-ChildItem .\samples` with two sample filenames and file sizes | Pending |
| `03-case0042-triage-summary.png` | `email_triage.py` output, sample SHA-256, subject, reported authentication statuses and hostname list | Pending |
| [`04-case0042-decoded-body.png`](./04-case0042-decoded-body.png) | Local decoding of the real-world email's plain-text body | **Uploaded and verified** (11 October 2026) |

## Privacy and quality guidance

- Submit **only genuine screenshots** of commands performed in the user's own lab.
- Crop out unnecessary personal information. Check for actual recipient addresses, tracking tokens, live links and account identifiers before publication.
- Prefer screenshots of distinct evidence, not duplicates; the raw long Thinkific tracking path can be omitted/cropped.
- No screenshot here demonstrates an observed click, verified malicious landing page, or compromised account.
- Refer to [initial hands-on triage](../investigations/CASE-0042-INITIAL-TRIAGE.md) for verified recorded findings.

**Do not change status to uploaded until the actual PNG exists in this folder.**
