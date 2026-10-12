# Project 5 — Network PCAP Investigation

**Status:** IN PROGRESS — practical traffic analysis performed on 12 October 2026; written investigation drafted; evidence PNG upload and final review outstanding.

**Case:** PCAP-0051 — published SOC training exercise, *Download from Fake Software Site* (22 January 2025). This is a third-party historical training capture, **not a real-world incident personally handled by the analyst**.

## What this project demonstrates

- Examining a real training PCAP in Wireshark (39,427 packets; 145 IPv4 endpoints visible in statistics).
- Identifying a Windows endpoint using DHCP, DNS and Kerberos.
- Correlating HTTP request frames with responses and inspecting captured scripts **without executing them**.
- Documenting a two-stage script retrieval sequence and periodic HTTP polling, with packet-numbered evidence.
- Investigating an additional encrypted TLS 1.2 connection without making unsupported C2 claims.
- Preserving a locally calculated SHA-256 and documenting evidence limitations.

## Findings at a glance

| Item | Evidence-grounded finding |
| --- | --- |
| Client | `DESKTOP-L8C5GSJ` / `10.1.17.215` / MAC `00:0d:b7:26:4a:74` — DHCP frame 3 |
| Kerberos principal | `shutchenson` in realm `BLUEMOONTUESDAY` — AS-REQ frame 258; **not confirmed script executor** |
| Suspicious server | `5.252.153.241:80` — HTTP request/response traffic |
| First file response | GET `/api/file/get-file/264872` (5031), HTTP 200 (5033), 417-byte VBScript-style component |
| Second file response | GET `/api/file/get-file/29842.ps1` (5063), HTTP 200 (5071), 1,512-byte obfuscated PowerShell-like response |
| Subsequent activity | 10 visible GETs to `/1517096937` about 5.19 seconds apart, followed by HTTP 404s — **suspected automated polling** |
| Additional TLS | `10.1.17.215 → 45.125.66.32:2917`; TLS 1.2 with encrypted data, relationship to downloads **unconfirmed** |
| Assessment | **High-confidence suspicious multistage script retrieval; possible beaconing.** Host execution, impact and confirmed compromise are **not established**. |

## Evidence source and preservation

- **Training source:** https://malware-traffic-analysis.net/2025/01/22/index.html
- **Local file:** `/home/kali/Downloads/2025-01-22-traffic-analysis-exercise.pcap` (user's Kali VM)
- **SHA-256 (user-run command, screenshot reviewed):** `e59db1c07c6fdefafa0abdbca03248c341cdc36c09c34753204d3162802a3586`
- **Original file:** kept locally, not distributed here; the provider page's ~20.5 MB figure is for the ZIP, **not a verified extracted PCAP size**.
- **Evidence source:** real user Wireshark screenshots supplied during the investigation. These were visually reviewed, but **screenshots have not yet been uploaded to GitHub**.

## Project documents

- [Investigation report](./investigations/CASE-0051-INVESTIGATION-REPORT.md) — structured narrative, packet-level timeline, decisions and limitations.
- [Screenshot evidence index](./screenshots/README.md) — 11 curated screenshots, **upload pending**.
- Pending final QA: verify the evidence files, consider privacy of visible account names and dangerous URLs, and cross-check any claims against screenshots.

## Safety and scope

All work so far was static/read-only analysis of a third-party training PCAP in Kali Linux. No payload was executed, no suspicious destination was contacted as part of the analysis, and no production environment was investigated. **DNS/SNI queries, HTTP request intent and Kerberos principals must not be used to assert unobserved process execution or blame a particular user.**

## Remaining work

1. Add genuine screenshot files listed in the evidence index and verify image visibility and correspondence to reported packet numbers.
2. Perform final report/evidence consistency checks; note if the original fake-software landing page cannot be established from this capture.
3. Once evidence is complete, change status to Complete; then update the portfolio roadmap and prepare the interview guide, learning review and exactly 20 new flashcards (81–100) in the separate SOC study repository.
