# Windows Privilege Escalation Hunt — Wazuh + Windows Security

**Status: Detection and controlled tests validated (10 October 2026). Evidence upload and additional log correlation are pending.**

## Objective

Investigate membership changes to the built-in Windows **Administrators** group, create a focused SIEM detection, distinguish authorised lab activity from potential compromise, and demonstrate careful rollback and negative testing.

This is a standalone portfolio project using the existing Wazuh + Sysmon lab infrastructure from Project 1, but **not** reusing its investigation evidence. Project 2's brute-force rule remains separate.

## Key result

A disabled local test account, `SOC-PrivEsc-Test`, was temporarily added to the Administrators group and promptly removed on a personally controlled Windows host. Windows Security Event **4732** was observed in Wazuh and custom rule **100102 (level 13)** triggered. Rollback Event **4733** was observed; the test account remained disabled and was not left in the Administrators group. A separate local non-admin-group addition produced Event **4732** under existing Wazuh rule **60144 (level 5)**, **not** custom rule 100102.

**Verdict:** True-positive detection of the targeted *membership-change event*, with **authorised benign lab activity**; **not** evidence of compromise, active exploitation, or that the disabled test account ever logged in with elevated permissions.

## Environment / data sources

- Windows personal test host, Wazuh agent `Windows-Host`; Wazuh Manager 4.14.8 lab
- Windows Security log auditing: **Security Group Management = Success**
- Windows Security eventchannel collection enabled in the Wazuh agent, service confirmed running
- Wazuh Manager rule check and restart succeeded; service returned `active`
- Relevant Windows events: **4732** group member added, **4733** member removed, **4734** group deleted, optionally **4624** successful logon and **4672** special privileges assigned at logon
- Sysmon Event 1 can provide process context when present; **no Sysmon/process correlation is claimed yet**

## Observed rule logic

- Existing built-in Wazuh rule **60154** reports Administrators group changed, level 12
- Added independent **custom rule 100102** in `/var/ossec/etc/rules/privilege_escalation_rules.xml`
- Child of rule `60154`, restricted to Windows `win.system.eventID = 4732` **and** `win.eventdata.targetSid = S-1-5-32-544`
- Severity **level 13**, ATT&CK **T1098.007 (Additional Local or Domain Groups)**
- Previous custom rules **100100** and **100101** were verified present and were not altered
- See [rule source](./detections/privilege_escalation_rules.xml) and [test matrix](./detections/01-local-admin-membership.md)

## Completed controlled scenarios

| Test | Verified observation | Meaning |
| --- | --- | --- |
| Baseline auditing/ingestion | Enabled audit policy, active Windows Security log, Wazuh agent running and event reception | Suitable telemetry |
| Initial admin group addition | Security **4732**, target `Administrators` SID `S-1-5-32-544`, subject `hasna`, test account SID ending `-1005`; built-in rule 60154 observed | Detectable privileged-group change |
| Initial rollback | Security **4733**, same member/group; Windows log and Wazuh confirmed | Successful removal |
| Post-rule positive test | New **4732** (record **1466264**); custom rule **100102**, level **13** | **Positive test passed** |
| Admin removal negative | Wazuh **4733** observed; combined filter `rule.id:100102` + `eventID:4733` returned no matches | **Removal exclusion passed** |
| Normal-group negative | `SOC-PrivEsc-Test` added to temporary `SOC-NonAdmin-Test` group; **4732**, target SID ending `-1006`, Wazuh **60144**, level **5** | **Non-admin exclusion passed** |
| Non-admin cleanup | **4734** logged for temporary group deletion (record **1466318**) | Cleanup observed |

The positive-test script printed successful removal and an independent group-membership check showed the test account absent from Administrators. `SOC-PrivEsc-Test` remained **disabled** throughout the tests.

## Logon correlation check (10 October 2026)

A read-only Windows PowerShell query searched Security Event IDs **4624** (successful logon) and **4672** (special privileges assigned) from **22:15–22:50 local time**, filtering event messages for the disabled `SOC-PrivEsc-Test` username or SID. **No matching test-account records were returned.** This supports the limited finding that no such matches were observed **in that time window**; it does not prove that no account logon ever occurred or rule out logging/query limitations. A Sysmon Event 1 process review remains outstanding.

## Investigation / response reasoning

For a real alert: confirm group SID `-544`; identify the **subject** (actor), **member** (newly added identity), **target group**, host and time; check change approval and correlate relevant 4624/4672, Sysmon process activity and any other suspicious changes where data exists. If unauthorised, preserve logs, escalate through incident procedures, remove unexpected membership safely and examine follow-on activity.

ATT&CK: [T1098.007 — Account Manipulation: Additional Local or Domain Groups](https://attack.mitre.org/techniques/T1098/007/). A 4732 event is a detection lead, **not proof of attacker intent**.

See the [investigation report](./investigations/01-privileged-group-change.md).

## Safety and limitations

- Testing used a dedicated **disabled** account on a personally controlled Windows host.
- Before changes, the Administrators membership and account state were examined; the test never modified the `hasna` membership.
- Existing built-in Administrator account was disabled; the main `hasna` account was enabled and an Administrators group member. No claim of an independently tested backup-admin login.
- The test account was removed immediately after each privileged addition, with post-test membership validation.
- An authorised change can be a true positive for the *rule* without being a malicious incident.
- **Not yet verified:** full follow-on 4624/4672/Sysmon correlation, final screenshot files hosted in this repository, disposal of the disabled test account.
- Do not claim production deployment or real attacker activity.

## Repository files

- [Detection logic and test matrix](./detections/01-local-admin-membership.md)
- [Reproducible custom Wazuh rule source](./detections/privilege_escalation_rules.xml)
- [Investigation and verdict](./investigations/01-privileged-group-change.md)
- [Evidence checklist](./screenshots/README.md)
- [Interview preparation](./notes/INTERVIEW-PREP.md)

## Completion checklist

- [x] Audit policy, Windows Security log, Wazuh agent/ingestion verified
- [x] Approved group-change test executed
- [x] Events 4732/4733 confirmed in Windows/Wazuh
- [x] Custom rule 100102 deployed and its level 13 alert verified
- [x] Admin-removal and non-admin-group negative cases passed
- [x] Test account confirmed disabled; privileged membership removed; temporary normal group deleted
- [x] Investigation write-up based on observed results
- [ ] Upload curated, reviewed screenshots to this project's `screenshots/` folder
- [ ] Review pertinent logon/process context (and document evidence limitations)
- [ ] Verify final housekeeping; then mark fully **Complete**

**Current status: Tests validated; evidence and correlation pending.**
