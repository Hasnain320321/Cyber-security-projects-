# CASE-0042 — Real-World Redacted Email: Initial Hands-On Triage

**Status:** In progress; local analysis, unit tests and decoded plaintext-body review confirmed by user screenshots on 11 October 2026.  
**Source:** [cw-l/email-corpus](https://github.com/cw-l/email-corpus) at commit `220ba996e76d0a1ef27e0598c958b3cd1d141388`, file `submissions/b037056b02c300ba/1.0.0/emails/004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735.eml`.  
**Environment:** User's Windows laptop, Python 3.15.0, PowerShell, offline `email_triage.py`.

## Executed on the user's laptop

- `python -m unittest discover -s tests -v`: screenshot showed **four tests passed / OK**.
- `Get-ChildItem .\samples`: confirmed `CASE-0041-synthetic.eml` (1,540 bytes) and `CASE-0042-real-redacted.eml` (**13,049 bytes**).
- `python tools\email_triage.py samples\CASE-0042-real-redacted.eml --output output\CASE-0042.json`: output saved to `output\CASE-0042.json`; console JSON displayed in user screenshots.
- The tool reported **SHA-256 `004f4a14e51ffd35a513984d464d59341d8440c65ebab3a5f3da620431c4b735`**, matching the corpus sample filename. This helps identify the analysed bytes; it does not prove the claimed sender's authenticity.

## Observed analysis output

| Field | Value |
| --- | --- |
| Subject | `Account Notice: Digital Token Update Needed` |
| Claimed Date header | `Thu, 12 Feb 2026 05:15:59 +0000` |
| From domain | `substackss.firebaseapp.com` |
| Reply-To domains | None extracted |
| Return-Path domains | None extracted |
| Received count | `0` — corpus was redacted |
| SPF (reported) | `pass` |
| DKIM (reported) | `pass` |
| DMARC (reported) | `permerror` — **not equivalent to fail** |
| Extracted URL hostnames | `bing.com`, `email.notify.thinkific.com`, `www.dbs.com.sg` |
| Attachments metadata | Empty list |

These results are **user-run program output**, not independently verified SPF/DKIM/DMARC validation. The corpus omits Received/Return-Path records; their absence does not mean the original email lacked routing hops.

## What the URL hostnames actually do

Source review of the publicly available redacted email shows:

- `www.dbs.com.sg` appears as a **remote DBS logo image** reference in HTML. A legitimate image URL can be embedded in a fraudulent email.
- `email.notify.thinkific.com` is the **clickable HTML button destination** for **"Update Your DBS Digital Token"**. Its long path is omitted from these public notes; it may contain a tracking identifier. We did **not** follow redirects or establish its eventual destination.
- `bing.com` appears as the **"Unsubscribe" link**. Its presence is not validation of the message's identity.

An extracted URL is an investigation lead, **not automatically a malicious IOC**.

## Body and risk indicators

**Direct local evidence:** The user executed a read-only Python email-parser command against `samples/CASE-0042-real-redacted.eml`, then supplied a screenshot of its decoded `text/plain` message body. The screenshot confirms the following statements in the email:

- The sender claims a DBS/POSB **authentication token is no longer valid**.
- Banking services, including card-related transactions, **may be temporarily affected**.
- The recipient is asked to **update the DBS Digital Token** for uninterrupted banking access.
- The message says to wait **up to 12 hours after the update** before accessing the account. The purpose of this unusual delay is **unknown**.
- The text includes general DBS/POSB customer-service-hotline references, a purported support-team signature, and an automated-notification signoff.

**Observed vs inferred:** Those are words visible in the preserved message, **not independently verified bank instructions**. The message does not explicitly ask the user to type their password in its plaintext body. Credential collection, any web-form contents, sender motive, or actual downstream impact remain **unverified**.

The preserved email uses a **DBS/POSB banking identity**, claims the customer's **authentication token is no longer valid**, warns banking services may be disrupted, and urges an update. The visible From domain `substackss.firebaseapp.com` does not match the claimed bank identity. SPF and DKIM reportedly passing only support authentication of the relevant sending identities, **not** the banking claim. The `dmarc=permerror` header shows an evaluation problem, not a simple negative outcome.

**Provisional assessment:** This is *suspicious banking impersonation consistent with phishing*. The specific click-through destination, credential collection, user impact and any actual compromise remain **unverified**. The decoded text body has now been reviewed, but classification remains provisional pending the benign comparison, source/context checks and final evidence review.

## Evidence still outstanding

1. The authentic screenshot of locally decoded `text/plain` message body **has been seen in this conversation (11 October 2026), but the PNG still needs to be added to GitHub**. Suggested name: `04-case0042-decoded-body.png`.
2. Actual screenshots shown in conversation, after privacy inspection, should be committed under `screenshots/`. **These PNGs have NOT yet been uploaded to GitHub.**
3. Do **not** upload the raw JSON without first removing long tracking-link paths and checking for identifiers; a public, hostname-only summary is sufficient for now.
4. A benign comparison sample and outcome, plus final investigation, limitations and defensible SOC verdict.

This is **offline analysis of a historical, pre-redacted dataset**; no live phishing site was clicked, no attachment executed, no real mailbox surveyed, and no production containment performed.
