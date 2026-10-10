# Windows Privilege Escalation Hunt — Wazuh + Windows Security

**Status: COMPLETE — controlled detection tests, investigation, rollback, Sysmon correlation, final cleanup and 26 verified screenshots (10 October 2026).**

## Objective

Investigate membership changes to the built-in Windows **Administrators** group, create a focused SIEM detection, distinguish authorised lab activity from potential compromise, and demonstrate careful rollback and negative testing.

This is a standalone portfolio project using the existing Wazuh + Sysmon lab infrastructure from Project 1, but **not** reusing its investigation evidence. Project 2's brute-force rule remains separate.

## Key result

A dedicated disabled local test account, `SOC-PrivEsc-Test`, was temporarily added to the Administrators group and promptly removed on a personally controlled Windows host. Windows Security Event **4732** was observed in Wazuh and custom rule **100102 (level 13)** triggered. Rollback Event **4733** was observed; the test account remained disabled and was not left in the Administrators group. A separate local non-admin-group addition produced Event **4732** under existing Wazuh rule **60144 (level 5)**, **not** custom rule 100102.

**Verdict:** True-positive detection of the targeted *membership-change event*, with **authorised benign lab activity**; **not** evidence of compromise, active exploitation, or that the disabled test account ever logged in with elevated permissions.

## Environment / data sources

- Windows personal test host, Wazuh agent `Windows-Host`; Wazuh Manager 4.14.8 lab
- Windows Security log auditing: **Security Group Management = Success**
- Windows Security eventchannel collection enabled in the Wazuh agent, service confirmed running
- Wazuh Manager rule check and restart succeeded; service returned `active`
- Relevant Windows events: **4732** group member added, **4733** member removed, **4734** group deleted, optionally **4624** successful logon and **4672** special privileges assigned at logon
- Sysmon Event 1 provided limited PowerShell process context during the tested time window; this is **not** proof of the exact group-change command.

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

A read-only Windows PowerShell query searched Security Event IDs **4624** (successful logon) and **4672** (special privileges assigned) from **22:15–22:50 local time**, filtering event messages for the disabled `SOC-PrivEsc-Test` username or SID. **No matching test-account records were returned.** This supports the limited finding that no such matches were observed **in that time window**; it does not prove that no account logon ever occurred or rule out logging/query limitations. A limited Sysmon Event 1 review found relevant elevated PowerShell process creation, described separately below; process creation alone does not record commands later typed in that shell.

## Sysmon process correlation (10 October 2026)

A read-only query of `Microsoft-Windows-Sysmon/Operational` Event ID **1** for 22:15–22:50 (local time) returned, among others:

- **22:22:19**: `powershell.exe` created by `explorer.exe`, user `hasna`, **High** integrity, Logon ID **0x3FE50**. This precedes the controlled **4732** group addition by seconds, and is consistent with the actor/session.
- **22:30:46**: `ssh.exe` spawned by `powershell.exe`, user `hasna`, High integrity, command line connects to the lab Wazuh VM at `192.168.56.101`; consistent with authorised lab management.
- **22:35:57**: another `powershell.exe` process started by Explorer, user `hasna`, High integrity.

The Sysmon events corroborate process/session context but **do not prove that the individual `Add-LocalGroupMember` command was executed inside any particular PowerShell process**: the Sysmon Event 1 command line is the shell executable invocation, not every command typed after startup.

## Investigation / response reasoning

For a real alert: confirm group SID `-544`; identify the **subject** (actor), **member** (newly added identity), **target group**, host and time; check change approval and correlate relevant 4624/4672, Sysmon process activity and any other suspicious changes where data exists. If unauthorised, preserve logs, escalate through incident procedures, remove unexpected membership safely and examine follow-on activity.

ATT&CK: [T1098.007 — Account Manipulation: Additional Local or Domain Groups](https://attack.mitre.org/techniques/T1098/007/). A 4732 event is a detection lead, **not proof of attacker intent**.

See the [investigation report](./investigations/01-privileged-group-change.md).

## Safety and limitations

- Testing used a dedicated **disabled** account on a personally controlled Windows host.
- Before changes, the Administrators membership and account state were examined; the test never modified the `hasna` membership.
- Existing built-in Administrator account was disabled; the main `hasna` account was enabled and an Administrators group member. No claim of an independently tested backup-admin login.
- The test account was removed immediately after each privileged addition, with post-test membership validation. After the investigation, the disposable test account itself was deleted, with a subsequent existence check confirming no account found.
- An authorised change can be a true positive for the *rule* without being a malicious incident.
- **Limitations:** negative 4624/4672 search was restricted to 22:15–22:50 and suppressed query errors; Sysmon Event 1 establishes process creation/context rather than the exact typed command; all supporting screenshots are retained in the public repository. The disabled test account was subsequently deleted.
- Do not claim production deployment or real attacker activity.

## Verified screenshot evidence

All **26 original PNG screenshots** are stored under [Project 3 / screenshots](./screenshots/), with a [fully linked evidence index](./screenshots/README.md). Every uploaded screenshot was verified against the local original by Git blob SHA-1; the **26 files match byte-for-byte, all PNGs open correctly, and none are exact duplicates**.

The strongest recruiter-facing evidence is:

| Investigation step | Linked screenshots |
| --- | --- |
| Audit, Wazuh collection and baseline | [01 audit policy](./screenshots/01-audit-policy.png), [02 Wazuh collection](./screenshots/02-wazuh-collection.png), [03 admin baseline](./screenshots/03-admin-baseline.png) |
| Windows admin group change | [05 target/actor](./screenshots/05-admin-4732-target-and-actor.png), [05b Event 4732](./screenshots/05b-admin-4732-event-id.png) |
| Initial rollback | [06 Windows 4733](./screenshots/06-windows-4733-rollback.png), [06b Wazuh 4733](./screenshots/06b-wazuh-4733-target-member.png) |
| Custom rule 100102 | [07 rule created](./screenshots/07-custom-rule-file-created.png), [08c level-13 alert](./screenshots/08c-positive-rule100102-level13.png) (read alongside [08 event fields](./screenshots/08-positive-event-fields.png) and [08b Event 4732](./screenshots/08b-positive-event4732.png)) |
| Negative tests | [10 no false removal alert](./screenshots/10-negative-4733-no-custom-alert.png), [10b 4733 received](./screenshots/10b-negative-4733-seen-in-wazuh.png), [11 non-admin Event 4732](./screenshots/11-nonadmin-addition-event4732.png), [12 rule 60144](./screenshots/12-negative-rule60144.png) |
| Correlation and cleanup | [17 Sysmon PowerShell](./screenshots/17-sysmon-powershell-correlated-2222.png), [14 scoped logon search](./screenshots/14-logon-correlation-no-matches.png), [18 final account deletion](./screenshots/18-final-test-account-deleted.png) |

Other companion and support screenshots remain available in the full index, not discarded.

## Repository files

- [Detection logic and test matrix](./detections/01-local-admin-membership.md)
- [Reproducible custom Wazuh rule source](./detections/privilege_escalation_rules.xml)
- [Investigation and verdict](./investigations/01-privileged-group-change.md)
- [26 verified screenshots — organised evidence index](./screenshots/README.md)
- [Project 3 interview guide and revision notes](https://github.com/Hasnain320321/SOC-Interview-and-Study-Notes/tree/main/Project-03-Privilege-Escalation-Hunt)
- [Cumulative SOC flashcards (60 cards)](https://github.com/Hasnain320321/SOC-Interview-and-Study-Notes/blob/main/Flashcards/SOC-MASTER-FLASHCARDS.md)

## Final cleanup (10 October 2026)

After completing the event investigations, the operator verified that `SOC-PrivEsc-Test` remained disabled and absent from Administrators, and that `SOC-NonAdmin-Test` no longer existed. They then ran `Remove-LocalUser -Name 'SOC-PrivEsc-Test'` and verified that `Get-LocalUser` no longer found the account. The PowerShell output printed **"CLEANUP VERIFIED: Temporary test account deleted."**. No claim is made that Event 4726 was checked in Wazuh.

## Completion checklist

- [x] Audit policy, Windows Security log, Wazuh agent/ingestion verified
- [x] Approved group-change test executed
- [x] Events 4732/4733 confirmed in Windows/Wazuh
- [x] Custom rule 100102 deployed and its level 13 alert verified
- [x] Admin-removal and non-admin-group negative cases passed
- [x] Test account confirmed disabled; privileged membership removed; temporary normal group deleted
- [x] Investigation write-up based on observed results
- [x] All 26 curated PNG screenshots verified in this project's `screenshots/` folder and indexed by investigation stage
- [x] Review limited 4624/4672 and Sysmon Event 1 context; document limitations
- [x] Final housekeeping: verified non-admin group gone, test account not enabled or in Administrators, and deleted temporary account; checked it no longer exists

**Final status: COMPLETE (10 October 2026).** The authorised lab evidence, custom rule, positive and negative test results, contextual Sysmon review, independent rollback and final account deletion are documented. Public screenshots retain their original lab-local identifiers.
