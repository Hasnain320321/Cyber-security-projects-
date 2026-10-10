# Investigation 01 — Local Administrators Membership Change

**Status: Core investigation and controlled detection tests performed, 10 October 2026. Evidence file upload and further logon/process correlation pending.**

## Executive summary

A Wazuh alert for a Windows Administrators group membership change was investigated on a personal lab endpoint. The analyst intentionally added a **disabled** dedicated test account `SOC-PrivEsc-Test` to the built-in local Administrators group and immediately removed it. Windows and Wazuh confirmed the addition (**4732**), removal (**4733**) and unchanged safe end state. Subsequently, new custom Wazuh detection **100102, level 13**, correctly alerted on a second controlled addition. Negative tests confirmed that the addition rule did **not** match group removals (4733) or addition to a non-administrator local group (4732 under rule 60144).

**Disposition: Authorised benign lab activity; technically true positive for the membership-change detection. No observed evidence of attacker compromise.**

## Key timeline (10 October 2026; Windows/Wazuh UI local display times)

| Sequence | Evidence |
| --- | --- |
| Baseline | Security Group Management auditing = Success; Windows Security log enabled; Wazuh agent running with Security eventchannel collection |
| Initial controlled admin addition | 4732 in Wazuh, built-in rule **60154 / level 12**, record **1466196**, Administrators SID **S-1-5-32-544** |
| Initial rollback | 4733 recorded locally and in Wazuh, record **1466198**, member SID ending **-1005**, group **Administrators** |
| Custom rule deployment | Rule **100102 / level 13**, child of 60154 and restricted to Event 4732 + target SID `S-1-5-32-544`; configuration validation passed; manager active after restart |
| Post-deployment positive test | Wazuh 4732, record **1466264**, group Administrators, member SID ending `-1005`; **rule 100102 / level 13 verified** |
| Post-deployment rollback | PowerShell reported removal; independent membership check found test account absent; account remained disabled |
| Negative A | Wazuh displayed 4733 removal alerts; rule 100102 + event 4733 combined search returned no matches |
| Negative B | Test account added to temporary `SOC-NonAdmin-Test` group; 4732 in Wazuh, group SID ending `-1006`; **rule 60144 / level 5**, not 100102 |
| Cleanup | Temporary non-admin group deletion logged as **4734**, record **1466318**; account remained disabled |

## Observable event details

| Investigation field | Verified finding |
| --- | --- |
| Wazuh agent | `Windows-Host` |
| Windows event channel | Security |
| Windows event provider | Microsoft-Windows-Security-Auditing |
| Subject / actor | `hasna` |
| Member | Test account `SOC-PrivEsc-Test` identified via its local-user SID ending `-1005` |
| Privileged target group | Built-in `Administrators`, SID `S-1-5-32-544` |
| Normal-group negative test | `SOC-NonAdmin-Test`, SID ending `-1006` |
| Initial built-in Wazuh rule | `60154`, "Administrators Group Changed", level 12 |
| New custom Wazuh rule | `100102`, level 13 |
| Normal group event's Wazuh rule | `60144`, level 5 |

## Investigation reasoning

- **Validate:** Event 4732 showed a real local security-group membership addition. The target SID `-544` established that the target was Administrators, distinguishing it from the `-1006` normal-group negative case.
- **Identify:** `subjectUserName` is **who made the change**, whereas `memberSid` is **the account added**. The test account SID was resolved with PowerShell `Get-LocalUser`.
- **Authorisation:** Changes were deliberately initiated as a documented lab test by the owner of the endpoint.
- **Correlate:** Wazuh ingestion and the pair of 4732/4733 events are verified. **A structured review of 4624/4672 and Sysmon process events has not yet been completed**; none is claimed as collected or exculpatory.
- **Scope:** No claim of broader investigation or absence of malicious activity beyond the limited controlled change. The account remained disabled and lost membership after the test.
- **Classify:** A **true-positive detection of a real administrative change**, but **benign/authorised lab activity**, not a demonstrated compromise.
- **Response:** Roll back elevated membership, verify actual account and group state, retain audit records and review approval + related activity for any unexpected real-world occurrence.

## Validation and safety

The main `hasna` account was confirmed enabled and in Administrators before testing. The built-in Administrator account was disabled. A dedicated disabled test account was used; its group membership was changed only briefly, with automatic rollback and an independent final check. The privileged test account was **not enabled**, and there is no evidence it ever logged on during this test. No production or third-party machine was targeted.

## Logon check: additional observed result

On 10 October 2026, a read-only PowerShell search of Windows Security events **4624 and 4672** during **22:15–22:50 local time** filtered messages for the disabled `SOC-PrivEsc-Test` username or SID. The script printed **"No matching test-account logons found in this time window."** This is a **negative search result for the specified records/window**, not independent proof that the account was never used, and query errors were configured to be silently ignored. Sysmon Event 1/process correlation has not yet been conducted.

## Gaps and recommended follow-up

- [ ] Upload carefully reviewed screenshot PNGs; preserve unaltered event fields and visible rule IDs where possible
- [ ] Query relevant Windows 4624 and 4672 activity around the test, and Sysmon Event 1 if present; document what is and is not attributable
- [ ] Decide whether to remove the disabled lab account after evidence gathering (do not silently delete it)
- [ ] Write a short detection tuning/reflection conclusion after the follow-up

## Lessons learned

The **same Event 4732** can describe both an ordinary group addition and an Administrators addition. Checking the **target group SID** prevents misclassification. A rule's alert severity is not equivalent to proof of malicious intent. Positive tests alone are not sufficient: the rollback and a distinct non-admin group negative test provide important assurance.
