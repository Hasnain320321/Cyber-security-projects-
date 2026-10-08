# Investigation 01 — Suspected Privileged Group Membership Change

**Status: Template / Not yet conducted.**

## Incident overview

- Detection date/time: *Pending*
- Agent and host: *Pending*
- Windows Event ID / Wazuh rule ID: *Pending*
- Group name and SID: *Pending*
- Account added: *Pending*
- Actor account: *Pending*
- Outcome: *Pending*

## SOC investigation steps

1. **Validate:** Is this Windows Security Event 4732? Was the high-value Administrators group changed?
2. **Identify:** Which member was added, and who initiated the action? Compare `Member`, `Subject`, `Group` and computer.
3. **Correlate:** Find relevant 4624 and 4672 logs plus process command line/parent lineage (when present).
4. **Scope:** Were additional group changes, account creations or suspicious logins observed? Avoid inferring uncollected activity.
5. **Classify:** Authorised change, suspicious, confirmed malicious or undetermined. Explain why.
6. **Respond:** Preserve evidence, escalate when needed, and recommend reversing unauthorised access through approved procedures.

## Evidence placeholders

- [ ] Audit policy screenshot
- [ ] Windows 4732 original event fields
- [ ] Wazuh 4732 query/event details
- [ ] New detection alert (if built)
- [ ] Group change actor and member
- [ ] Windows 4733 event and post-test membership check
- [ ] Negative test (nonprivileged group)
- [ ] Relevant post-change 4624/4672/Sysmon review

**Do not fill this template with hypothetical event outputs.** Only record what is actually observed.
