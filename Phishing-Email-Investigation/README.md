# Phishing Email Investigation — Project 4

**Status: IN PROGRESS — evidence upgrade (reopened 11 October 2026).** The introductory synthetic case is documented; a sourced real-world sample has now been analysed offline on the user's Windows laptop; three additional screenshots, a benign comparison and the final report remain pending.

## Evidence rebuild (in progress)

The initial synthetic CASE-0041 was **not** sufficient as a stand-alone hands-on portfolio project. We reopened this project instead of overstating completion.

- [CASE-0042 source provenance and practical evidence plan](./investigations/CASE-0042-SOURCE-AND-PLAN.md) — selected redacted real-world banking impersonation sample, now initially investigated on the user's laptop (evidence still incomplete).
- [Python offline email triage helper](./tools/email_triage.py) — read-only header/URL/hash extraction, no requests or attachment execution.
- [Four initial unit tests](./tests/test_email_triage.py) — passed in the assistant's isolated development container **and independently re-run on the user's Windows laptop (4/4 passed)**.
- [Reproducible synthetic test output](./evidence/CASE-0041-tool-output.json) — tool-generated output from the supplied safe training .eml. This is **assistant-executed proof of tool functionality**, not a real-world phishing investigation.
- [CASE-0042 verified initial laptop analysis](./investigations/CASE-0042-INITIAL-TRIAGE.md) — four local Python unit tests passed, the public sample was hashed and parsed, authentication headers and three URL hostnames were extracted, and the decoded message body was reviewed on the user's laptop; privacy-safe findings recorded.
- Real-world case [decoded-body PNG](./screenshots/04-case0042-decoded-body.png): **uploaded and verified**. Three other planned PNGs, benign comparison and final report: **PENDING**.

The portfolio should only be marked complete once the actual real-world sample analysis, genuine screenshots, meaningful controls, final report and evidence review are done.

## Overview

Conducted a guided SOC-style investigation of a **deliberately synthetic** university IT-support phishing email (case `CASE-0041`). Opened the training `.eml` safely as text, examined sender identities, authentication-result claims, the `Received` sequence, the defanged link, and social-engineering content. Classified the sample as a **phishing simulation** and documented response recommendations. No real phishing site was visited, no malware executed, and no real user compromise established.

**Verdict:** High-confidence phishing-pattern **training example**, consistent with an account-verification credential-harvesting lure. This is **not** a confirmed real-world incident.

## Evidence and case files

- [Investigation report](./investigations/CASE-0041-phishing-analysis.md) — analysis, timeline, findings, MITRE mapping, limitations and verdict.
- [Original synthetic email](./samples/CASE-0041-training-email.eml) — safe `.example` / documentation-only IP addresses; inspect in a text editor, not by following links.
- [Header and IOC evidence](./evidence/CASE-0041-evidence.md) — extracted strings with observed vs inferred distinctions.
- [Suggested SOC response](./response/PHISHING-TRIAGE-PLAYBOOK.md) — steps for a real environment, explicitly **not performed** on this training case.

## Skills demonstrated

- Email header triage: `From`, `Reply-To`, `Return-Path`, `Received`, `Message-ID`
- Interpreting **reported** SPF fail, DKIM none and DMARC fail
- Defanging and extracting indicators without visiting unknown links
- UTC timestamp normalization and basic message timeline
- Distinguishing facts, suspected attacker objective and unknown impact
- Phishing verdict, ATT&CK T1566.002 mapping and proportionate SOC response guidance

## Boundaries

- All domains use the reserved `.example` namespace; IPs `192.0.2.45` and `198.51.100.26` are documentation address ranges. Real DNS, WHOIS, web reputation, click telemetry and authentication validation are **not possible or meaningful** for this case.
- Header values (including authentication results and relay path) are **simulated input**, not independently validated mail-server logs.
- There was **no** real email-gateway quarantine, user-impact hunt, credential reset, Wazuh email detection, malware analysis, or live incident response.
- The uploaded `.eml` and text evidence extracts form the GitHub evidence; the screenshot viewed during the guided session has **not** been added to GitHub.

## Further practice

Repeat this workflow using a permitted, appropriately sanitised real email sample or an isolated phishing-training dataset if available. Never upload private recipient information or live malicious links to a public repository.

See the portfolio [home page](../README.md) and [roadmap](../PROJECT-ROADMAP.md).
