# CASE-0042 — Public redacted real-world phishing sample (planned practical investigation)

**Status:** INITIAL LOCAL TRIAGE VERIFIED ON USER LAPTOP (11 October 2026); full investigation and screenshot upload pending. Training CASE-0041 is archived as an introductory synthetic exercise, not substituted for this case.

## Source

- Corpus: [cw-l/email-corpus](https://github.com/cw-l/email-corpus) — contributor-redacted and URL-defanged **real-world** emails.
- Repository commit pinned: [220ba996e76d0a1ef27e0598c958b3cd1d141388](https://github.com/cw-l/email-corpus/commit/220ba996e76d0a1ef27e0598c958b3cd1d141388).
- Sample path: `submissions/b037056b02c300ba/1.0.0/emails/004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735.eml`.
- [Read sample on GitHub](https://github.com/cw-l/email-corpus/blob/220ba996e76d0a1ef27e0598c958b3cd1d141388/submissions/b037056b02c300ba/1.0.0/emails/004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735.eml)
- Corpus licensing: MIT, subject to repository's notice and contributor privacy statement. Do not republish raw data to the portfolio without another PII review.

## Initial sample-selection observations (not a completed investigation)

The public sample describes a **DBS/POSB banking-token account notice**. Its visible From is `"DBS/POSB." <noreply@substackss.firebaseapp.com>`. An `Authentication-Results` header reports `spf=pass`, `dkim=pass`, and `dmarc=permerror`. These are **header claims, not independently verified results**. Passing SPF/DKIM may authenticate an attacker-controlled domain; it does not make the banking claim genuine.

**Dataset limitation:** The corpus maintainer strips `Received` and `Return-Path` headers and defangs URLs. We **cannot** claim to independently trace the delivery route, reconstruct all envelope sender data, or confirm a live malicious destination from this sample.

## User practical exercise (first steps completed; subsequent steps pending)

1. **Done on user laptop.** Download the sample via GitHub **Raw**; save exactly as `CASE-0042-real-redacted.eml` locally. **Do not double-click/open in a mail client or click any content links.**
2. **Done on user laptop, screenshots seen.** Extract the [local triage kit](../tools/) and use Windows Terminal/PowerShell to run `python tools/email_triage.py samples/CASE-0042-real-redacted.eml --output output/CASE-0042.json`.
3. **Terminal results shared in chat, not yet committed as PNGs.** Capture authentic screenshots of the local terminal, exact file SHA-256, JSON summary and manual header observations. Note that the case source originally lived outside the portfolio.
4. Record observed sender, reported authentication (including permerror), suspicious message content and link domains. Independently inspect recipient-safe artefacts; do not resolve, refang or browse live URLs.
5. Compare to the synthetic CASE-0041 and eventually a sourced legitimate/benign control case.
6. Produce a defensible verdict with **observed vs inferred vs unknown**, and justify it. No live incident response or credential theft can be claimed without telemetry.

## Initial verified findings

See [CASE-0042 initial hands-on triage](./CASE-0042-INITIAL-TRIAGE.md) for actual test output, SHA-256, header claims, URL roles, limitations, and the evidence upload backlog.

## Evidence to add

- `evidence/CASE-0042-output.json` from the executed script **after PII and link-token checks**.
- Actual user screenshots only (PNG), documenting command, file hash and results; label them as personal lab evidence.
- Final investigation report after results are verified, not in advance.

## Safety

Source messages are for offline study only. Defanging reduces accidental clicking but does not guarantee that every artefact is harmless. Do not run or open attachments. If samples contain residual personal information, redact before publishing.
