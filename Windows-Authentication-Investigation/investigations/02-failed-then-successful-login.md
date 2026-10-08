# Investigation 02 — Failed Logins Followed by Successful Authentication

**Date:** 8 October 2026  
**System:** Windows endpoint monitored by Wazuh (agent: `Windows-Host`)  
**Account under review:** `SOC-Lab-Test2` (authorised test account)  
**Disposition:** **Benign Positive — controlled sign-in sequence.** No compromise established by reviewed evidence.

## Objective

Correlate Windows failed-logon events (4625) with a later successful authentication (4624), confirm the identity and logon context, check nearby process alerts without assuming they belong to the same user, and document an evidence-based SOC disposition.

## Investigated authentication timeline

| Dashboard local time, 8 Oct 2026 | Windows Event ID | Wazuh rule | Account and observed result |
| --- | --- | --- | --- |
| 18:01:21.619 | `4625` | `60122` | Failed login; filtering by `targetUserName = SOC-Lab-Test2` returned this event |
| 18:01:26.110 | `4625` | `60122` | Failed login; same filtered account |
| 18:01:33.061 | `4624` | `60118` | Successful login; expanded event confirmed `SOC-Lab-Test2`, Logon Type 2, source `127.0.0.1` |
| 18:01:47.591 / 18:01:47.626 | Sysmon process-creation alerts | `92052` / `92032` | Command-shell-related rule descriptions; later inspected process fields showed **McAfee WebAdvisor BrowserHost.exe**, but user/session correlation was not established |
| 18:01:48.480 | `4625` | `60122` | Separate failure with `msedgewebview2.exe` in process field; target username was **not present in reviewed fields** |

The two failed logins and success were established by querying the same target username in Wazuh. Times shown are dashboard-local. These are the **observed** events, not a claim that all Windows authentication or process events were exhaustively collected.

## Validate

- Windows Security Event ID `4625` indicates a failed sign-in; Wazuh matched `60122`.
- Windows Security Event ID `4624` indicates successful authentication; Wazuh matched `60118`.
- Expanded successful event at 18:01:33 confirmed `targetUserName: SOC-Lab-Test2`, `logonType: 2` (interactive), and `ipAddress: 127.0.0.1` (local loopback).
- Target-name-filtered query confirmed exactly the two displayed failures before the successful event in that searched window.
- The broader view also contained unrelated authentication activity, so event timestamps alone were not used as an identity match.

## Identify and correlate

The first two failures targeted the same authorised test account and were followed about 7 seconds after the second failure by a successful *local interactive* logon. The test was performed deliberately in the lab by the account owner. The source-field value was local loopback; the Wazuh agent IP (`192.168.56.1`) is **not** a remote attacker IP.

A separate `4624` event involving a Microsoft-account session had Logon Type 7 (unlock) and **did not** match the test account, so it was excluded from the incident timeline.

## Scope of post-login activity

Two command-shell-related alerts appeared roughly 14 seconds after the success. One expanded alert displayed:

- Process image: `C:\Program Files\McAfee\WebAdvisor\BrowserHost.exe`
- Company/description in telemetry: `McAfee, LLC` / `McAfee WebAdvisor (browser proxy)`
- Command line: referenced the browser extension and a parent-window argument
- Integrity level: Medium

The user identified McAfee WebAdvisor as legitimate installed software. The telemetry **suggests** browser-security activity but does not independently verify the file's digital signature, identify the parent process, or show that `SOC-Lab-Test2` executed it. Therefore, this process alert is **not attributed to the test account or classified as malicious**.

An application compatibility rule `92058` appeared at 18:00:33, **before** the confirmed test-account logon, and was not attributed to that account. The `18:01:48` `4625` associated with Microsoft Edge WebView2 is also treated as a separate event because its **target account was not established**.

## Classification

**Benign Positive** for the controlled 4625 -> 4625 -> 4624 authentication sequence: Wazuh correctly observed the events, and their legitimate lab origin is known. This is **not** evidence of a successful real-world brute-force compromise.

**Scope limitation:** No exhaustive post-authentication process, network, file-access or persistence investigation was performed. The surrounding process alerts were reviewed for context only and remain *not conclusively attributed* to the sign-in. A different outcome might be warranted with evidence of remote origin, anomalous 4624s or suspicious post-login commands.

## SOC recommendation for a real incident

Confirm account and source for each failure and success, correlate Logon Type and session timing, inspect follow-on process/network activity, and consult the account owner or system operator. If unauthorised access is substantiated, follow incident response procedures (contain the account/session, rotate credentials, revoke sessions, retain logs, and escalate). Do not treat an automatic severity level or MITRE mapping as proof.

See the [response and triage playbook](../response/01-authentication-alert-triage-playbook.md), [time-based evidence transcription](../evidence/02-authentication-timeline.md), and [visual evidence index](../screenshots/README.md).

## Evidence provenance

Seven relevant original screenshot excerpts from this investigation are now available in the [Project 2 evidence index](../screenshots/README.md):

- [16 — Initial failed-login overview](../screenshots/16-failed-logins-overview.png) and [20 — the two failed attempts](../screenshots/20-two-failures-targeted-account.png)
- [17 — Successful login at 18:01:33](../screenshots/17-test-account-success-list.png), [18 — local source and Type 2](../screenshots/18-success-logon-type-and-ip.png), and [19 — SOC-Lab-Test2 target username](../screenshots/19-success-target-username.png)
- [21 — separate later WebView2-linked failure](../screenshots/21-separate-webview-failure-process.png)
- [24 — nearby process alert list](../screenshots/24-nearby-sysmon-process-alerts.png)

The PNG showing the McAfee WebAdvisor `BrowserHost.exe` command line was **not included in the GitHub upload**. That detail was observed in a screenshot supplied during the live conversation and described here, but must not be represented as an uploaded exhibit.

**Limits of image evidence:** The filtered query linked failures to `SOC-Lab-Test2` during investigation, but screenshot 20 crops out the username/filter chips. The screenshots are excerpts, not a full exported log. The other event's target username and the process alerts' user/session attribution were not established. Two low-value cropped images were removed during curation. See the [audit manifest](../evidence/INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md).

## Key lessons

1. `4625` means failure; `4624` means success.
2. Correlate by account, time, source and logon type — timestamps alone are insufficient.
3. Logon Type 7 means **unlock**; Logon Type 2 means **local interactive login**.
4. An alert after a sign-in is not necessarily **caused** by that user's session.
5. The meaning of an alert depends on evidence and context, not only its level or description.
