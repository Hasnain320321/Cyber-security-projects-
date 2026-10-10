# Windows Privilege Escalation Hunt — Wazuh + Sysmon

**Status: Planned — lab preparation and documentation created; no new hunt executed yet.**

## Objective

Investigate suspicious changes to local administrator privileges using Windows Security events and Wazuh. Distinguish authorised administration from unauthorised privilege escalation, corroborate process and logon activity where available, and document a defensible SOC analyst conclusion.

This project is **separate** from the completed [SOC Home Lab](../SOC-Home-Lab/) and [Wazuh Brute-Force Detection](../Windows-Authentication-Investigation/) projects. It uses the existing lab as infrastructure but will contain its own evidence and investigation reports.

## Main hypothesis

A new member of the built-in local Administrators group may indicate an unexpected privilege change. This is a **hunt lead, not automatically an attack**. Check the added account, who made the change, change approval, source host, session and follow-on actions.

MITRE ATT&CK mapping: **T1098.007 — Account Manipulation: Additional Local or Domain Groups** (tactics: Persistence, Privilege Escalation). Authoritative reference: https://attack.mitre.org/techniques/T1098/007/

## Data sources and event IDs

| Source | Event | Significance |
| --- | --- | --- |
| Windows Security | **4732** | Member added to security-enabled local group (core test) |
| Windows Security | **4733** | Member removed from security-enabled local group (rollback evidence) |
| Windows Security | **4735** | Local security group changed; may accompany membership changes |
| Windows Security | **4672** | Special privileges assigned to new logon; context only, not proof of escalation |
| Windows Security | **4624** | Successful logon; correlate account, type, session and time |
| Sysmon Operational | **1** | Process creation; command line, user and parent process when collected |

**Important:** Local built-in Administrators group SID typically ends **-544**; compare the event's actual `targetSid`/group name (localisation can affect the displayed name). Event 4732 alone does not mean the member has already exercised elevated privileges.

Microsoft 4732 documentation: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732

## Planned controlled lab scenarios

1. **Baseline:** Confirm relevant Windows Security auditing is enabled, log ingestion reaches Wazuh, and capture ordinary known admin/security-group activity where available.
2. **Positive test — privileged group change:** In an **isolated, authorised test environment**, temporarily add a dedicated, non-sensitive test account to the local Administrators group using an administrator account, record the Security 4732 event, investigate it, and **remove the account immediately** to capture event 4733. Do not perform this on a work/school-owned endpoint.
3. **Detection:** Create and validate a separate Wazuh custom detection for additions to the built-in Administrators group, only after observing the true event field names. Never modify Project 1 rule 100100 or Project 2 rule 100101.
4. **Negative / tuning test:** Examine a change to a **non-privileged local group** or another approved event and ensure it is not misclassified as an Administrators-group escalation.
5. **Investigation:** Attribute the actor and added member, check related 4624/4672 and Sysmon process activity (if collected), establish authorisation and outcome.
6. **Reporting:** Screenshots, detection write-up, incident narrative, response recommendations, and MITRE mapping.

## Safety and rollback

- **Start read-only.** First check Windows audit policy; do not change group membership yet.
- Use a disposable Windows VM for privilege-change testing if one is available; otherwise, discuss risks of using the personally owned Windows test host before changing it.
- Confirm the baseline group membership and a working **second** local admin path before any change. Never demote the only administrator.
- Change **only a dedicated test account** in a machine you own/control; no remote exploitation or persistence is necessary.
- Remove the test account from the privileged group immediately after collecting evidence and independently confirm restoration.
- Do not claim real compromise from authorised administrative actions.

## Investigation workflow

**Validate -> Identify -> Correlate -> Scope -> Classify -> Recommend Response**

Check: **Who was added? Which privileged group? Who performed the change? When? Where? Was it authorised? What happened afterwards?**

## Repository structure

- [Detection plan](./detections/01-local-admin-membership.md) — hypothesis, fields and test matrix.
- [Investigation template](./investigations/01-privileged-group-change.md) — fill in only after observing actual events.
- [Screenshot evidence checklist](./screenshots/README.md) — placeholder list, no evidence uploaded yet.

## Status checklist

- [x] Repo project structure and learning objectives established.
- [ ] Verify audit policy and Wazuh event ingestion.
- [ ] Capture approved positive/negative group-change events.
- [ ] Build and test Wazuh rule using observed event fields.
- [ ] Verify rollback/administrators membership restoration.
- [ ] Investigate and classify actual generated events.
- [ ] Add screenshots and completed investigation write-up.

**Status will be changed to Complete only after testing and evidence are verified.**
