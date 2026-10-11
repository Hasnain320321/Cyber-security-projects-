# CASE-0043 — Benign Email Control and CASE-0042 Comparison

**Status:** Local offline control analysis **performed** on 11 October 2026; user-provided PowerShell screenshots reviewed. [CASE-0043 terminal screenshot](../screenshots/05-case0043-benign-control.png) committed and verified on GitHub.  
**Sample:** [CASE-0043-benign-control.eml](../samples/CASE-0043-benign-control.eml), a **deliberately synthetic** benign control authored for this training project. `.example` is reserved for examples.  
**Environment:** Windows laptop, Python 3.15.0, PowerShell, [email_triage.py](../tools/email_triage.py).

## User-run commands and evidence

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Hasnain320321/Cyber-security-projects-/main/Phishing-Email-Investigation/samples/CASE-0043-benign-control.eml" -OutFile ".\samples\CASE-0043-benign-control.eml"
python tools\email_triage.py samples\CASE-0043-benign-control.eml --output output\CASE-0043.json
```

The user shared screenshots demonstrating the file download command, the offline analysis command, the successful message `Saved read-only triage results: output\CASE-0043.json`, and JSON output. The user-captured PowerShell evidence is now archived as [05-case0043-benign-control.png](../screenshots/05-case0043-benign-control.png) in the screenshot folder.

## Observed tool output

| Key | Value |
| --- | --- |
| Tool version | 1.0 |
| Source file | `CASE-0043-benign-control.eml` |
| SHA-256 | `221d438532587cb14cfce20202da72a4863270fd823527087ff9ea2b0cbd3fbb` |
| Size | 1,363 bytes |
| Subject | `Study room booking confirmation for 14 October` |
| Date header | `Sun, 11 Oct 2026 17:30:00 +0100` (synthetic, not independently corroborated) |
| From domain | `training.example` |
| Reply-To domain | `training.example` |
| Return-Path domain | `training.example` |
| Received headers | 1 (synthetic) |
| Reported SPF | `pass` |
| Reported DKIM | `none` |
| Reported DMARC | `pass` |
| Extracted URL domain | `portal.training.example` |
| Attachment metadata | None |

The sample has **simulated** email-authentication claims; SPF/DMARC were **not verified by DNS or cryptographic checks**. DKIM being absent does not prove a message is suspicious. The existence of one Received header also does not establish a real relay.

## Case 0042 vs CASE-0043

| Field | Case 0042: redacted historical banking-impersonation sample | Case 0043: synthetic benign control |
| --- | --- | --- |
| Identity/content | Claims DBS/POSB; asks to update a banking digital token to avoid service interruption | A previously requested study-room booking, no urgent account-authentication demand |
| Sender domain | `substackss.firebaseapp.com`, distinct from bank's claimed identity | `training.example`, consistent with Reply-To and Return-Path |
| Header-reported SPF | pass | pass (simulated) |
| Header-reported DKIM | pass | none (simulated) |
| Header-reported DMARC | permerror | pass (simulated) |
| URL domains | Three; includes a third-party call-to-action link | One; reserved example library portal |
| Attachments | None detected | None detected |
| Assessment | **Suspicious, likely phishing**, provisional; redirect destination and impact not established | **Benign by construction**; not an independently verified real email |
| Distinct methodological limitation | Historical message's routing headers were redacted by source corpus | Fictional headers and domain provide controlled parser test, not mail provenance |

## Analyst reasoning

The main distinction is **intent inferred from content and context**, not just SPF/DKIM/DMARC result strings or URL counts. The banking sample mixes financial-account pressure with a sender domain not visibly tied to DBS/POSB and a third-party digital-token update button. The control simply confirms a pre-arranged room booking without requesting credentials, urgent verification or redirection to banking login; it uses consistent `.example` identities.

The Python script **extracts indicators only** and performs **no autonomous malicious/benign classification**. This comparison demonstrates the analyst interpreting extracted evidence, not measured phishing-detector accuracy or a true-negative rate. Nothing here proves account compromise, identifies a threat actor, or verifies a live landing page.

## Follow-up before project completion

- **Completed:** Screenshot of the user-run Case 0043 output uploaded and verified as [05-case0043-benign-control.png](../screenshots/05-case0043-benign-control.png).
- Upload earlier local unit-test and Case 0042 summary evidence screenshots, cropping/removing the long tracking URL path.
- Review both samples together and complete a final investigation report with explicit evidence, confidence, source limitations and recommendations.
- Project 4 remains **IN PROGRESS** until the evidence review is complete.
