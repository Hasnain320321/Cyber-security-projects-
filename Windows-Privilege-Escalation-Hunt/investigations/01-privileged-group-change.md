# Investigation 01 — Local Administrators Membership Change

**Status: COMPLETE — core investigation, controlled tests, limited process/logon correlation, safe cleanup and 26 uploaded evidence screenshots, 10 October 2026.**

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

## Linked primary evidence

All captures can be found in the [complete screenshot index](../screenshots/README.md); the table below maps the strongest directly to observed conclusions.

| Conclusion | Verified supporting captures |
| --- | --- |
| Logging and baseline configured | [01 Security Group Management audit](../screenshots/01-audit-policy.png), [02 Wazuh agent collection](../screenshots/02-wazuh-collection.png), [03 admin baseline](../screenshots/03-admin-baseline.png), [04 disabled test identity](../screenshots/04-disabled-test-account.png) |
| Actual privileged-group addition occurred | [05 Wazuh subject/member/group](../screenshots/05-admin-4732-target-and-actor.png) + [05b Windows 4732](../screenshots/05b-admin-4732-event-id.png) |
| Initial admin privilege addition was rolled back | [06 Windows 4733](../screenshots/06-windows-4733-rollback.png) + [06b Wazuh 4733 details](../screenshots/06b-wazuh-4733-target-member.png) |
| Wazuh custom rule built and loaded | [07 XML creation](../screenshots/07-custom-rule-file-created.png), [07b manager active](../screenshots/07b-wazuh-manager-active.png) |
| Controlled positive test fired **100102 / level 13** | [08 positive field context](../screenshots/08-positive-event-fields.png), [08b Event 4732](../screenshots/08b-positive-event4732.png), [08c rule 100102 level 13](../screenshots/08c-positive-rule100102-level13.png) (three complementary views) |
| Rollback and disabled test account remained safe | [09 PowerShell check](../screenshots/09-safe-final-end-state.png) |
| Removal event **4733** did not trigger addition rule | [10 combined rule/event query no matches](../screenshots/10-negative-4733-no-custom-alert.png) + [10b Wazuh 4733 received](../screenshots/10b-negative-4733-seen-in-wazuh.png) |
| Ordinary group addition not mistaken for Administrators | [11 target group Event 4732](../screenshots/11-nonadmin-addition-event4732.png) + [12 Wazuh rule 60144/level 5](../screenshots/12-negative-rule60144.png) and [12b description](../screenshots/12b-negative-rule60144-description.png) |
| Ordinary test group removed | [13 PowerShell cleanup](../screenshots/13-temporary-group-cleanup.png), [13b deletion Event 4734](../screenshots/13b-temporary-group-deletion-event4734.png) |
| Logon/process context reviewed with limits | [14 no logon matches in selected window](../screenshots/14-logon-correlation-no-matches.png); [17 Sysmon elevated PowerShell launch](../screenshots/17-sysmon-powershell-correlated-2222.png), [16 Wazuh SSH session](../screenshots/16-sysmon-ssh-wazuh-2230.png) |
| Disposable test account removed after testing | [18 final safety checks and account deletion](../screenshots/18-final-test-account-deleted.png) |

**Interpretation:** No single crop proves the entire investigation; paired screenshots must be read together where field values are displayed at different scroll positions. These are screenshots of authorised lab activity, not a real intrusion.

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
- **Correlate:** Wazuh ingestion and the pair of 4732/4733 events are verified. A limited 4624/4672 query found no matches for the disabled test account in the checked time window; Sysmon Event 1 captured elevated PowerShell process creation near the event, but did not expose individual typed commands. These findings do not establish absence of other activity.
- **Scope:** No claim of broader investigation or absence of malicious activity beyond the limited controlled change. The account remained disabled and lost membership after the test; it was later deleted after safe checks.
- **Classify:** A **true-positive detection of a real administrative change**, but **benign/authorised lab activity**, not a demonstrated compromise.
- **Response:** Roll back elevated membership, verify actual account and group state, retain audit records and review approval + related activity for any unexpected real-world occurrence.

## Validation and safety

The main `hasna` account was confirmed enabled and in Administrators before testing. The built-in Administrator account was disabled. A dedicated disabled test account was used; its group membership was changed only briefly, with automatic rollback and an independent final check. The privileged test account was **not enabled**, and there is no evidence it ever logged on during this test. No production or third-party machine was targeted.

## Logon check: additional observed result

On 10 October 2026, a read-only PowerShell search of Windows Security events **4624 and 4672** during **22:15–22:50 local time** filtered messages for the disabled `SOC-PrivEsc-Test` username or SID. The script printed **"No matching test-account logons found in this time window."** This is a **negative search result for the specified records/window**, not independent proof that the account was never used, and query errors were configured to be silently ignored. A limited Sysmon Event 1 correlation is documented below; it supports actor/session context without proving which command changed membership.

## Sysmon process correlation

Read-only search of the Sysmon Operational log (Event ID **1**, 22:15–22:50 local time) produced relevant process-create records:

| Time (local) | Observation | Assessment |
| --- | --- | --- |
| **22:22:19** | `powershell.exe` launched by `explorer.exe`, actor `hasna`, **High** integrity, Logon ID `0x3FE50` | Approximately seconds before observed 4732 membership event, consistent with authorised elevated PowerShell session |
| **22:30:46** | `ssh.exe` launched from PowerShell, command line to `wazuh-user@192.168.56.101`, **High** integrity | Consistent with Wazuh server management during lab |
| **22:35:57** | Another elevated PowerShell created by Explorer, actor `hasna` | Additional shell context, not proof of group change |

**Evidence boundary:** Event 1 shows process creation and startup command line, not each PowerShell statement typed later. No claim is made that Sysmon independently captured `Add-LocalGroupMember`; Windows 4732 and Wazuh 100102 are the primary evidence for the group change. The process/logon context is corroborative, not conclusive.

## Gaps and recommended follow-up

- [x] All 26 original screenshots uploaded and indexed; key captures explicitly linked to corresponding findings
- [x] Document limited 4624/4672 search and Sysmon Event 1 process context with attribution limitations
- [x] After reviewing results, permanently removed the disabled lab account and verified it no longer existed
- [x] Document tuning/limitations: target Administrators SID -544 and event 4732 rather than all group changes; validate exclusions via 4733 and non-admin 4732

## Final cleanup evidence

After the controlled tests, an elevated PowerShell script checked the disposable account was still **disabled**, not in **Administrators**, and the normal test group no longer existed. The account was then deleted using `Remove-LocalUser`. A second lookup found no remaining account; the command printed **"CLEANUP VERIFIED: Temporary test account deleted."** The main `hasna` account was not removed or demoted. No Windows account-deletion event (4726) has been reviewed, so cleanup proof is limited to the PowerShell output.

## Lessons learned

The **same Event 4732** can describe both an ordinary group addition and an Administrators addition. Checking the **target group SID** prevents misclassification. A rule's alert severity is not equivalent to proof of malicious intent. Positive tests alone are not sufficient: the rollback and a distinct non-admin group negative test provide important assurance.
