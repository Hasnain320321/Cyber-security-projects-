# CASE-0041 — Evidence and IOC register

**Source:** [Synthetic email file](../samples/CASE-0041-training-email.eml), inspected as plaintext in the guided session on 11 October 2026. The email includes an explicit `X-Lab-Notice` declaring synthetic provenance. This is a **textual extraction** from the attached source, not proof of a real threat.

## Email identities

| Field | Value |
| --- | --- |
| Display name | `MMU IT Support` |
| From address | `alerts@it-support.example` |
| Reply-To address | `helpdesk@campus-support.example` |
| Return-Path | `bounce@mailer-notify.example` |
| Recipient | `student@training.example` |
| Message-ID | `<case0041.20261009@mailer-notify.example>` |

## Routing and authentication claims

| Indicator | Recorded in training source |
| --- | --- |
| First purported submitting host | `workstation.mailer-notify.example` at `198.51.100.26` |
| Next relay | `relay.mailer-notify.example` at `192.0.2.45` |
| Recipient mail exchanger | `mx.training.example` |
| Reported SPF | `fail` for `mailer-notify.example` |
| Reported DKIM | `none` |
| Reported DMARC | `fail` for `it-support.example` |
| Sender Date (UTC) | `2026-10-09 13:11:30Z` |
| Relay Received (UTC) | `2026-10-09 13:11:48Z` |
| Final Received (UTC) | `2026-10-09 13:12:08Z` |

## Defanged URL indicator

`hxxps://account-review[.]example/verify`

**Analysis:** Distinct from the claimed support sender domain; context and urgent verification wording are consistent with a credential-phishing pretext. **Do not treat as a live IOC for blocklists:** `.example` and both IPs are reserved examples.

## Suspicious wording (short excerpts)

- `verify your account within 2 hours` — urgency.
- `Failure to verify will lock your university email` — threatened consequence.
- `Do not contact the IT desk` — discourages trusted verification.

## Evidence quality and boundaries

**Observed in source:** All strings, reported authentication values and timestamps above.  
**Inference:** Phishing-style credential-verification objective.  
**Not measured:** Mail-server validation, real sender reputation, actual recipients, clicks, credential submission, compromise or containment.  
**Missing GitHub artefact:** The user displayed a screenshot of Notepad during the session, but the PNG has **not** been uploaded to this repository. The raw sample and this transcript-derived extraction supply the current documented evidence.

**No live URLs were clicked or attachments executed.**
