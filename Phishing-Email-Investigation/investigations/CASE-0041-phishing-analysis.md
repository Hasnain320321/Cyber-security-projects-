# CASE-0041 — Synthetic University IT Phishing Email

**Analysed:** 11 October 2026  
**Case type:** Guided offline email-header and content investigation  
**Sample message date:** 9 October 2026  
**Source:** Training email supplied for Project 4 and viewed as raw text by the analyst  
**Scope:** One fully synthetic `.eml`, no live mailbox, gateway or endpoint telemetry  
**Disposition:** **Phishing simulation / training case — complete**  
**Confidence:** High that sample is deliberately constructed to imitate phishing; no assertion of an actual attack

## Executive summary

The sample masquerades as university IT support and asks a student to verify an account within two hours to prevent suspension. The purported support identities and verification link use different domains; the message tells the recipient not to contact the IT desk. Its synthetic `Authentication-Results` reports `spf=fail`, `dkim=none`, and `dmarc=fail`. These combined indicators support classification as a **phishing-style credential-verification lure** in this controlled training scenario.

No clicking, credential entry, compromised account, malicious payload or real sending infrastructure was observed.

## Evidence and methodology

1. Preserved the supplied training email as `../samples/CASE-0041-training-email.eml`.
2. Viewed the raw source text in Notepad; did **not** execute attachments or open the verification link.
3. Extracted routing, identity, authentication and message-body indicators from the source.
4. Normalised the `Date` header to UTC and ordered the claimed `Received` timestamps.
5. Documented observed facts separately from possible intent, and assessed a defensible simulated-case verdict.
6. Wrote proposed SOC escalation and containment guidance; did not carry out real containment.

Full evidence index: [CASE-0041 evidence](../evidence/CASE-0041-evidence.md).

## Source headers and identifiers

| Header | Observed value | Why it matters |
| --- | --- | --- |
| From | `"MMU IT Support" <alerts@it-support.example>` | Claimed identity / visible author address, not verified provenance |
| Reply-To | `"Account Verification" <helpdesk@campus-support.example>` | Response redirects to a different domain |
| Return-Path | `bounce@mailer-notify.example` | Distinct bounce/envelope-related domain |
| To | `student@training.example` | Synthetic recipient |
| Subject | `ACTION REQUIRED: Your university account will be disabled in 2 hours` | Urgency and threatened account loss |
| Message-ID | `<case0041.20261009@mailer-notify.example>` | Identifier for deduplication / tracing |
| Content-Type | `text/plain; charset="us-ascii"` | Text-only message; no attachment in this sample |
| Lab notice | `Synthetic training email. All domains and IP addresses are reserved examples.` | Explicit simulation provenance |

## Authentication and source trust

The **training header claims**: `spf=fail smtp.mailfrom=mailer-notify.example`, `dkim=none`, `dmarc=fail header.from=it-support.example`. These are not checks that the investigator independently re-ran. SPF relates to the envelope/mail-from domain and permitted sending servers, DKIM to validated cryptographic message signatures, and DMARC to alignment of applicable authentication with the visible From domain. Failure is significant context but **alone does not prove phishing**; successful authentication would not prove safety either.

The visible `From`, `Reply-To`, bounce identity, and linked domain differ. Legitimate systems can also use multiple domains, so identity mismatch is a warning sign requiring context, not standalone proof.

## Timeline (claimed by synthetic headers)

| UTC on 9 Oct 2026 | Event | Source |
| --- | --- | --- |
| 13:11:30 | Sender's declared message Date (`14:11:30 +0100`) | Date header, sender supplied |
| 13:11:48 | `workstation.mailer-notify.example` (`198.51.100.26`) to `relay.mailer-notify.example`, id `CASE-0040` | Lower Received header |
| 13:12:08 | `relay.mailer-notify.example` (`192.0.2.45`) to `mx.training.example`, id `CASE-0041` | Upper Received header |

This shows only the **route represented in the exercise email**; it does not establish an externally validated originating IP. In live triage, trust is assessed starting with headers added by the organization's mail infrastructure, then checking upstream claims.

## Link and behavioural analysis

- Defanged URL: `hxxps://account-review[.]example/verify`
- Domain: `account-review.example`; path: `/verify`
- Lure: a claimed unusual account login, looming two-hour suspension, and a demand for immediate verification.
- Additional concern: `Do not contact the IT desk about this automated verification request.` discourages checking through trusted channels.
- **Plausible objective (inference):** prompt the student to submit credentials to an imitation verification page.
- **Not established:** content of any website, landing page functionality, a credential collection form, clicks, successful authentication, or malicious domain reputation. `.example` is a reserved training suffix.

## Analysis: evidence vs inference

**Directly observed in sample:** wording, address strings, link, header fields and reported failures.  
**Supported interpretation:** phishing-themed social engineering, especially urgency, university-IT impersonation and suppression of independent verification.  
**Not supported:** real threat actor attribution, exfiltration, successful phishing, malware execution, or user compromise.

**MITRE ATT&CK:** T1566.002 — Phishing: Spearphishing Link. This is a **scenario-level thematic mapping** because the sample delivers a verification hyperlink; no actual intrusion technique was observed in production telemetry.

## Verdict and disposition

**Classify as: Synthetic phishing simulation (high confidence).**  
**Suspected objective:** credential harvesting, unverified because landing-page contents were not examined.  
**Known impact:** none established.  
**Investigation outcome:** closed for this one-email training case; not an active incident.

## Recommended response in a real enterprise

1. Preserve the original message and record trusted mail gateway trace details.
2. Quarantine/purge verified malicious copies using approved processes; search for similar messages and affected recipients.
3. Verify destinations and reputation in a safe analysis environment, **never by directly browsing live suspect links on an analyst workstation**.
4. Investigate web proxy, DNS, EDR, mail-gateway and identity-provider logs for clicks, credential entry or sign-in abnormalities.
5. If compromise is substantiated, escalate, reset credentials/revoke sessions as appropriate, review MFA, and examine post-login activity.
6. Document scope, affected users, indicators, false-positive considerations and notification/closure rationale.

These are recommendations **not executed** in the exercise.

## Limitations

Single purpose-built sample; reserved examples cannot provide meaningful reputation results. No actual mailbox, public DNS, real website, clicked-link artefacts, sender system logs, malware attachment, live SPF/DKIM/DMARC validation, or confirmed end-user interaction. All routing/authentication data are simulated. The raw-email screenshot shown during guided review has not been uploaded to GitHub; the uploaded source email and evidence extracts are verifiable text artefacts.

## Reflection

The core analytical skill is separating **what the message shows** from **what the attacker may want** and **what happened to a real user**. A plausible malicious lure is not proof of credential theft. In a live case, the next decisive sources would be trusted mail logs and user/identity telemetry.
