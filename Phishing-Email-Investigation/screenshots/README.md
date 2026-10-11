# Project 4 — Practical Evidence Index

**Verification status: 5/5 screenshots uploaded and checked on 11 October 2026.** All five were captured from the user's real local Windows PowerShell/Python investigation or tests, not created as fictional terminal output. GitHub file presence and names verified; images 01–03 also matched the local prepared versions by **Git blob SHA** (exact Git object hashes).

| Evidence | What it demonstrates | GitHub |
| --- | --- | --- |
| [01 — Unit tests](./01-python-unit-tests-passed.png) | `python -m unittest discover -s tests -v` — four passing tests on Windows | Verified |
| [02 — Sample file list](./02-case0042-sample-list.png) | `Get-ChildItem .\samples` — CASE-0041 and real-world CASE-0042 samples present | Verified |
| [03 — Case 0042 triage summary](./03-case0042-triage-summary.png) | Executed extractor command; source SHA-256, sender identity, and reported SPF/DKIM/DMARC result | Verified — **crop documented** |
| [04 — Decoded body](./04-case0042-decoded-body.png) | Local MIME/plaintext extraction of DBS/POSB token-update pretext | Verified |
| [05 — Benign comparison](./05-case0043-benign-control.png) | Local CASE-0043 parser output, synthetic control with no attachments and a reserved example link | Verified |

## Integrity and transparency

- **01 and 02:** Original user-supplied screenshots, unedited.
- **03:** Original user PowerShell screenshot cropped vertically to its top 600 px, showing genuine results while excluding an opaque token-like URL path. Cropping is disclosed; no screen output changed or recreated.
- **04 and 05:** User-captured files uploaded as project evidence.
- [Screenshot file hashes and crop disclosure](../evidence/SCREENSHOT-UPLOAD-MANIFEST.md)
- [Consolidated investigation report](../investigations/FINAL-INVESTIGATION-REPORT.md)

These screenshots prove **local lab procedures**, not a successful live attack or a production SOC investigation. The report cites source provenance and does not assert actual credential theft, validated phishing redirect or malicious infrastructure.
