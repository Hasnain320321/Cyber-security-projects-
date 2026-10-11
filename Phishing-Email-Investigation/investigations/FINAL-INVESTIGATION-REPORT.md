# Project 4 — Final Investigation Report: CASE-0042 with CASE-0043 Control

**Report prepared:** 11 October 2026  
**Project status:** **COMPLETE — scoped offline lab investigation, five screenshots and evidence QA verified on 11 October 2026.** Historical public redacted sample analysed locally; no real-world compromise inferred.  
**Analyst work:** Local Windows PowerShell and Python investigation, supported by guided review.  
**Classification:** **Likely phishing / bank impersonation (moderate-to-high confidence based on preserved content and sender/link mismatch)**. Confidence in any *actual credential theft or redirect destination* is **not established**.  
**Incident scope:** Historical, redacted public corpus message — **not a live organisational alert or confirmed intrusion**.

## Executive summary

The analyst investigated a historical redacted email that claims to come from DBS/POSB and asks a recipient to update a supposedly invalid digital-banking token. The visible sender is `"DBS/POSB." <noreply@substackss.firebaseapp.com>`, rather than a verified DBS/POSB domain. The preserved HTML email places an **Update Your DBS Digital Token** button on a long third-party `email.notify.thinkific.com` URL, not an established bank login page. The full redirect destination was **not opened or observed**.

Email headers **report** SPF `pass`, DKIM `pass`, and DMARC `permerror`. These values were extracted from the source; they were not independently recomputed. The case illustrates why authentication checks alone do not determine whether a bank-branded email is safe.

The analyst also ran the same offline extraction tool on CASE-0043, an intentionally synthetic routine library-booking email used as a benign control. The second exercise supports **analyst interpretation of differences**, not a measured phishing-classifier detection rate.

## 1. Evidence origin and integrity

| Field | CASE-0042 |
| --- | --- |
| Corpus | [cw-l/email-corpus](https://github.com/cw-l/email-corpus), real-world messages redacted/defanged by its maintainer |
| Pinned source | [Commit `220ba996e76d0a1ef27e0598c958b3cd1d141388`](https://github.com/cw-l/email-corpus/commit/220ba996e76d0a1ef27e0598c958b3cd1d141388) |
| Sample | `submissions/b037056b02c300ba/1.0.0/emails/004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735.eml` |
| User's local filename | `CASE-0042-real-redacted.eml` |
| User-run reported SHA-256 | `004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735` |
| User-run reported size | 13,049 bytes |
| Processing | Python 3.15.0, `tools/email_triage.py` v1.0, read-only; no network visits or attachment execution |

The hash matches the public dataset file's hash-like name; it identifies the user-analysed sample but **cannot authenticate the email's claimed bank sender**. The corpus is not a full forensic acquisition: notably, routing data and original live URLs are redacted.

## 2. Procedures performed

1. Ran `python -m unittest discover -s tests -v` on Windows: **4 tests, 4 passed**, as evidenced by the user-captured terminal screenshot.
2. Listed `samples/` and confirmed the historical .eml and the separate synthetic primer were present.
3. Executed `python tools\email_triage.py samples\CASE-0042-real-redacted.eml --output output\CASE-0042.json`; the script saved structured output and printed its fields.
4. Examined reported authentication fields, sender domain, URL hostnames, file hash, and source limitations.
5. Used a local Python MIME parser to display the decoded `text/plain` body; captured a screenshot of the actual banking-token language.
6. Reviewed the public sample's HTML source to distinguish **logo resource**, **button destination**, and **unsubscribe destination**.
7. Downloaded the deliberately synthetic CASE-0043 safe library confirmation message and analysed it with the same script on the Windows laptop.
8. Recorded observed facts, security interpretation, remaining unknowns and recommended SOC response. **No live link was opened; no quarantine or production containment was performed.**

## 3. Technical findings: CASE-0042

| Attribute | Recorded observation | Interpretation |
| --- | --- | --- |
| Subject | `Account Notice: Digital Token Update Needed` | Security-update/account-access pretext |
| Date header | `Thu, 12 Feb 2026 05:15:59 +0000` | Preserved message claim; not independently corroborated |
| From | `"DBS/POSB." <noreply@substackss.firebaseapp.com>` | Bank-branded display name with a visibly different mail domain |
| Reported SPF | `pass` | An authentication outcome for the relevant sending identity, **not proof of DBS authorisation** |
| Reported DKIM | `pass`, `header.d=firebaseapp.com` | Signature result as recorded in the received sample, **not independently verified** |
| Reported DMARC | `permerror` | A **permanent evaluation error**, not interchangeable with `fail` |
| Received / Return-Path | 0 Received headers, no Return-Path domain in parsed redacted file | Delivery chain **cannot be reconstructed** from this dataset |
| Attachments | No attachment metadata extracted | No payload/attachment analysis was performed |
| Message body | Says the digital authentication token is invalid, banking services may be affected, asks for update, and says to wait up to 12 hours afterward | Uses service-disruption concern and a digital-token action request; reason for 12-hour statement unknown |

### URL and HTML roles

| Extracted hostname | Observed role | Important limitation |
| --- | --- | --- |
| `email.notify.thinkific.com` | **HTML href target** for the “Update Your DBS Digital Token” button | Long path intentionally omitted from public report; no redirect was followed or final landing page verified |
| `www.dbs.com.sg` | Image reference for DBS-branded logo | A genuine brand image **does not** prove the message is legitimate |
| `bing.com` | “Unsubscribe” hyperlink | Being a common destination does not authenticate the email |

These are **observed links**, not automatically confirmed malicious IOCs. Do not block third-party services wholesale on the strength of a single unvalidated sample.

### Red flags supporting a phishing assessment

- Bank identity is asserted by a display name and message copy, but the visible sender domain is not shown to be authorised by DBS/POSB.
- The recipient is told their digital banking access may be affected and is urged to update a token.
- The actionable button links to a third-party notification/tracking hostname; its actual redirect and destination were not validated.
- Branding/logo and support-signature language lend credibility without providing assurance.

**Threat hypothesis:** A banking-impersonation lure attempting to move the reader to an attacker-selected workflow, potentially credential or token harvesting. **That is an inference, not an observed collection page or stolen credential.**

## 4. Control exercise: CASE-0043

**Origin:** [`samples/CASE-0043-benign-control.eml`](../samples/CASE-0043-benign-control.eml), created specifically as a **synthetic benign fixture**, not an independently sourced real legitimate email. It confirms a previously requested study room booking and says no action is necessary.

The user downloaded it and ran the same Python script locally. Its output showed:

| Field | Observed control result |
| --- | --- |
| File size | 1,363 bytes |
| SHA-256 | `221d438532587cb14cfce20202da72a4863270fd823527087ff9ea2b0cbd3fbb` |
| From / Reply-To / Return-Path domains | `training.example` for each |
| Received header count | 1, **synthetic** |
| SPF / DKIM / DMARC | `pass` / `none` / `pass`, all **simulated header claims** |
| Link | `portal.training.example`, reserved example domain |
| Attachments | None reported |
| Scenario classification | Benign **by construction** |

**Comparison:** Both emails contain hyperlinks and SPF `pass` appears in both source headers. The difference that matters most is the **content and identity/URL context**: Case 0042 requests a sensitive banking-token update from an unverified sender domain; Case 0043 is a routine no-action training booking confirmation with matched example-domain addresses.

**Interpretive limit:** The script is an offline **extractor**, not a malicious/benign classifier. Two labelled examples cannot establish true-positive/false-positive rates or production detection accuracy.

## 5. Evidence register and screenshot integrity

| ID | Evidence | Verified in GitHub? |
| --- | --- | --- |
| 01 | [Windows Python unittest: four tests `OK`](../screenshots/01-python-unit-tests-passed.png) | **Uploaded and verified** |
| 02 | [Local samples folder listing](../screenshots/02-case0042-sample-list.png): confirms sample files and size | **Uploaded and verified** |
| 03 | [CASE-0042 script output](../screenshots/03-case0042-triage-summary.png): SHA-256, sender, reported auth | **Uploaded and verified** — privacy-cropped to omit opaque URL path |
| 04 | [Decoded CASE-0042 message body](../screenshots/04-case0042-decoded-body.png) | **Uploaded and verified** |
| 05 | [CASE-0043 benign control terminal output](../screenshots/05-case0043-benign-control.png) | **Uploaded and verified** |

All five genuine user-captured screenshots are now committed in the repository, and 01–03 matched the prepared originals by Git blob SHA. Cropping the Case 0042 terminal screenshot to omit a long tracking-style link is a **privacy redaction by omission, not synthetic evidence**. The GitHub [screenshot index](../screenshots/README.md) records upload status. The public repository intentionally does not contain the unredacted `CASE-0042.json` with its long path.

## 6. Outcome, confidence, and unknowns

**Triage outcome:** **Likely phishing / DBS-POSB impersonation**, moderate-to-high confidence from sender-brand mismatch, message content, and button context.  
**Observed impact:** **None established.** This was historical offline sample analysis, not a user-incident response.  
**Attribution:** Unknown.  
**Verified destination:** Unknown; the button's first visible hostname is `email.notify.thinkific.com`, and redirects were **not** tested.  
**Mail authentication:** Only recorded header claims were examined.  
**ATT&CK reference:** **T1566.002 — Phishing: Spearphishing Link**, *scenario-level alignment only*. No real breach or later-stage ATT&CK activity was observed.

**Important reporting discipline:** Avoid claiming confirmed credentials stolen, an exposed real customer, a malicious Thinkific service, active command-and-control, validated relay IP, or production blocking/containment.

## 7. Recommended actions if encountered in a real SOC

1. Preserve the full original message, trusted gateway traces, recipients, delivery IDs, and evidence timestamps.
2. Independently assess the claimed bank sender and authentication outcomes using **trusted** receiving-infrastructure records; investigate DMARC permerror rather than treating it as a simple fail.
3. Safely investigate the button's effective destination in an approved isolated workflow; do **not** browse an unknown link on a normal workstation or submit credentials.
4. Search mail logs for other recipients and review available proxy/DNS/identity telemetry for clicks, login anomalies or post-click activity.
5. If validated as malicious, follow approved quarantine/purge, security awareness and incident-escalation processes.
6. If credential exposure or unauthorised access is **confirmed**, coordinate credential resets, session revocation and scope review as appropriate.
7. Record false-positive alternatives and document which systems, dates and searches were actually checked.

**These are recommendations only, not response activities performed in this lab.**

## 8. Skills demonstrated, limitations and next improvement

**Demonstrated:** Local Python script execution; repeatable unit tests; offline .eml parsing and SHA-256 evidence integrity; MIME/body inspection; extracted sender and authentication fields; safe URL extraction; identifying HTML CTA vs image and unsubscribe links; a benign-control comparison; evidence-focused report writing.

**Not demonstrated:** Live email-gateway operations; independently verified SPF/DKIM/DMARC; live redirect/page analysis; real threat-intelligence validation; user impact investigation; quarantine or credential compromise.

**Project quality checkpoint:** **Passed for the defined offline scope.** Five user-captured screenshots are uploaded and verified, links are indexed, the local script ran successfully, the benign synthetic comparison was completed, and limitations are documented. This does **not** establish live phishing campaign detection, real credential compromise, or verified phishing-page behaviour.
