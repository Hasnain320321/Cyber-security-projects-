# Phishing Email Investigation — Project 4

**Status: COMPLETE — 11 October 2026 (scoped offline SOC analysis of one historical redacted phishing-style email, plus a synthetic benign control).**

## What this project demonstrates

I performed a local, read-only Python/PowerShell email investigation on a Windows laptop. I evaluated a **real-world historical but redacted and defanged** DBS/POSB impersonation sample (CASE-0042) and compared its indicators with a **deliberately synthetic benign** library confirmation (CASE-0043). I built and executed a standard-library Python email triage script, ran four passing unit tests, extracted email header information and URLs, examined message content, calculated a SHA-256 sample hash, compared the control, documented a defensible conclusion, and preserved five genuine local screenshots.

**Conclusion:** CASE-0042 was assessed as **likely bank-impersonation phishing**, based on sender-brand mismatch, the banking-token action request, and a third-party button URL. Its true redirect destination and any credential theft remain **unverified**. CASE-0043 is benign **by construction**, not a real legitimate email that was independently authenticated.

## Evidence and reports

- [**Consolidated investigation report**](./investigations/FINAL-INVESTIGATION-REPORT.md) — source, SHA-256, methods, headers, URL roles, analysis, control comparison, ATT&CK mapping, limitations, and recommendations.
- [**Five verified practical evidence screenshots**](./screenshots/README.md) — original user-run local tests, sample listing, privacy-cropped Case 0042 triage output, decoded email body, and benign-case analysis.
- [**Evidence manifest**](./evidence/SCREENSHOT-UPLOAD-MANIFEST.md) — screenshot hashes and explicit description of the crop.
- [CASE-0042 technical triage](./investigations/CASE-0042-INITIAL-TRIAGE.md) · [Public sample provenance](./investigations/CASE-0042-SOURCE-AND-PLAN.md)
- [CASE-0043 benign-control comparison](./investigations/CASE-0043-BENIGN-COMPARISON.md)
- [Offline Python indicator extractor](./tools/email_triage.py) · [Four unit tests](./tests/test_email_triage.py) · [Tool usage notes](./tools/README.md)
- [Synthetic control fixture](./samples/CASE-0043-benign-control.eml); the historical CASE-0042 message remains in the [attributed public source corpus](./investigations/CASE-0042-SOURCE-AND-PLAN.md), not republished in this repository.

## Practical exercises completed

| Exercise | Verified outcome |
| --- | --- |
| Windows Python setup | Python 3.15.0 used from PowerShell |
| Tool unit tests | **4/4 passed** on user's laptop |
| CASE-0042 file analysis | **13,049 bytes**; SHA-256 `004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735`; JSON output saved locally |
| CASE-0042 email inspection | From domain `substackss.firebaseapp.com`; header-reported SPF pass, DKIM pass, DMARC permerror |
| CASE-0042 content and links | Banking token update pretext; HTML button points initially to `email.notify.thinkific.com`; logo from `www.dbs.com.sg`; unsubscribe to `bing.com` |
| CASE-0043 synthetic control | **1,363 bytes**; matching example From/Reply-To/Return-Path domains; SPF pass, DKIM none, DMARC pass **as simulated header claims** |
| Portfolio evidence | **5/5 actual screenshots** committed and checked against case descriptions; 01–03 also matched source screenshot Git blob hashes |

## Background — introductory synthetic case

The initial exercise, [CASE-0041](./investigations/CASE-0041-phishing-analysis.md), used a fully synthetic university-support email to practise header inspection, defanged links and reported authentication results. Its [source](./samples/CASE-0041-training-email.eml), [evidence](./evidence/CASE-0041-evidence.md), and [SOC response playbook](./response/PHISHING-TRIAGE-PLAYBOOK.md) are preserved as training materials; it is **not** the main real-world case or a genuine compromise.

## Evidence quality and limits

- CASE-0042 came from a public **pre-redacted** dataset, so original Received/Return-Path chain and original live URLs are unavailable. The header's SPF/DKIM/DMARC results were **read**, not independently authenticated.
- CASE-0043 is **synthetic**, with reserved `.example` addresses and simulated authentication results; the comparison does not establish accuracy statistics for an email classifier.
- The Python helper extracts indicators; **it does not classify emails as malicious or benign**.
- No malicious link was opened, redirect resolved, attachment executed, victim click observed, credentials stolen, mailbox searched, email quarantined or production incident handled.
- A privacy-cropped screenshot excludes an opaque tracking-style URL path. The [manifest](./evidence/SCREENSHOT-UPLOAD-MANIFEST.md) documents exactly what was cropped; no result values were invented.
- **Status COMPLETE means the scoped offline lab investigation and evidence review are complete**, not that a live phishing campaign was discovered or responded to.

[Return to portfolio](../README.md) · [Roadmap](../PROJECT-ROADMAP.md)
