# Project 3 — Verified Screenshot Evidence

**Status: Complete.** All **26 original PNG screenshots** have been committed to this folder and checked against the evidence index on 10 October 2026. The folder contains **Project 3 only**; Projects 1 and 2 retain separate evidence folders.

The filenames follow the order of the lab investigation. Companion filenames such as `05b`, `08b` and `08c` capture **different fields of the same event**, not separate incidents. Both screenshots may be necessary to validate a claim because the Wazuh event view is scrollable.

**Quick links:** [Investigation](../investigations/01-privileged-group-change.md) · [Detection tests](../detections/01-local-admin-membership.md) · [Rule XML](../detections/privilege_escalation_rules.xml) · [Project README](../README.md)

## Evidence by investigation stage

### 1. Baseline and safe setup

| Actual screenshot | Evidence shown |
| --- | --- |
| [`01-audit-policy.png`](./01-audit-policy.png) | Security Group Management auditing set to Success |
| [`02-wazuh-collection.png`](./02-wazuh-collection.png) | Running Wazuh agent and Security eventchannel collection configuration |
| [`03-admin-baseline.png`](./03-admin-baseline.png) | Original Administrators group membership before testing |
| [`04-disabled-test-account.png`](./04-disabled-test-account.png) | Dedicated account created; Enabled = False |

### 2. Initial administrator change and rollback

| Actual screenshot | Evidence shown |
| --- | --- |
| [`05-admin-4732-target-and-actor.png`](./05-admin-4732-target-and-actor.png) | Wazuh 4732 event: actor, member SID, Administrators target SID -544 |
| [`05b-admin-4732-event-id.png`](./05b-admin-4732-event-id.png) | Companion capture confirming Event 4732 and event message |
| [`06-windows-4733-rollback.png`](./06-windows-4733-rollback.png) | Windows Security Event 4733 showing removal |
| [`06b-wazuh-4733-target-member.png`](./06b-wazuh-4733-target-member.png) | Wazuh 4733 details linking removal to the same account/group |

### 3. Custom detection deployment

| Actual screenshot | Evidence shown |
| --- | --- |
| [`07-custom-rule-file-created.png`](./07-custom-rule-file-created.png) | Project 3 Wazuh rule created and configuration tested |
| [`07b-wazuh-manager-active.png`](./07b-wazuh-manager-active.png) | Manager successfully restarted; service active |

### 4. Positive test of custom rule 100102

| Actual screenshot | Evidence shown |
| --- | --- |
| [`08-positive-event-fields.png`](./08-positive-event-fields.png) | New 4732 member/target/actor context in Wazuh |
| [`08b-positive-event4732.png`](./08b-positive-event4732.png) | Companion capture confirming Windows Event ID 4732 |
| [`08c-positive-rule100102-level13.png`](./08c-positive-rule100102-level13.png) | Same positive test reported by custom rule 100102, level 13 |
| [`09-safe-final-end-state.png`](./09-safe-final-end-state.png) | Immediate rollback, test account disabled and no admin membership |

### 5. Negative test: removal must not trigger an addition rule

| Actual screenshot | Evidence shown |
| --- | --- |
| [`10-negative-4733-no-custom-alert.png`](./10-negative-4733-no-custom-alert.png) | Combined rule 100102 + Event 4733 search returned no matching alerts |
| [`10b-negative-4733-seen-in-wazuh.png`](./10b-negative-4733-seen-in-wazuh.png) | Separate 4733 query shows removals were ingested, not absent |

### 6. Negative test: ordinary local group

| Actual screenshot | Evidence shown |
| --- | --- |
| [`11-nonadmin-addition-event4732.png`](./11-nonadmin-addition-event4732.png) | 4732 for SOC-NonAdmin-Test; target SID is not the built-in Administrators SID |
| [`12-negative-rule60144.png`](./12-negative-rule60144.png) | Wazuh rule 60144, level 5, instead of custom rule 100102 |
| [`12b-negative-rule60144-description.png`](./12b-negative-rule60144-description.png) | Companion description for the ordinary group change |
| [`13-temporary-group-cleanup.png`](./13-temporary-group-cleanup.png) | Non-admin test group removed; test account stayed disabled |
| [`13b-temporary-group-deletion-event4734.png`](./13b-temporary-group-deletion-event4734.png) | Windows Security Event 4734 confirms temporary group deletion |

### 7. Event correlation and final cleanup

| Actual screenshot | Evidence shown |
| --- | --- |
| [`14-logon-correlation-no-matches.png`](./14-logon-correlation-no-matches.png) | 4624/4672 query found no test-account matches in the limited lab window |
| [`15-sysmon-powershell-high-2235.png`](./15-sysmon-powershell-high-2235.png) | Additional elevated PowerShell process creation at 22:35:57 |
| [`16-sysmon-ssh-wazuh-2230.png`](./16-sysmon-ssh-wazuh-2230.png) | SSH to lab Wazuh VM launched from PowerShell at 22:30:46 |
| [`17-sysmon-powershell-correlated-2222.png`](./17-sysmon-powershell-correlated-2222.png) | Elevated PowerShell started at 22:22:19, just before initial admin-change event |
| [`18-final-test-account-deleted.png`](./18-final-test-account-deleted.png) | Verified group safety, deleted disabled test account and confirmed absence |

## Evidence interpretation and quality checks

- **Positive rule result requires related captures.** Use [08-positive-event-fields](./08-positive-event-fields.png), [08b-positive-event4732](./08b-positive-event4732.png) and [08c-positive-rule100102-level13](./08c-positive-rule100102-level13.png) **together**. The tiny rule-ID crop alone does not prove the targeted group or event ID.
- **Removal negative test requires both views.** [10](./10-negative-4733-no-custom-alert.png) proves the combined filter had no results; [10b](./10b-negative-4733-seen-in-wazuh.png) proves removal events were actually received. Absence of an alert alone is not sufficient to prove correct collection.
- **Ordinary-group negative test requires two views.** [11](./11-nonadmin-addition-event4732.png) confirms the non-admin group and Event 4732; [12](./12-negative-rule60144.png) confirms built-in rule 60144/level 5. [12b](./12b-negative-rule60144-description.png) provides the message.
- **Sysmon correlation is contextual.** [17](./17-sysmon-powershell-correlated-2222.png) documents nearby PowerShell process creation; it does not independently prove which later interactive command changed membership.
- **No logon matches is a scoped result.** [14](./14-logon-correlation-no-matches.png) is a query of 4624/4672 within a limited window; it does not prove the account never logged in.
- **Final cleanup is distinct from membership rollback.** [18](./18-final-test-account-deleted.png) documents the disposal of the temporary account after the test.
- **Original captures preserved.** No screenshot has been fabricated, cropped further, renamed or altered as part of this GitHub organisation audit. Each of the 26 PNG files has nonzero size; filenames match this index.

## Public repository note

This repository is public. Original lab screenshots contain a local Windows username/hostname, internal `192.168.56.x` addresses and account SIDs. These support the investigation but are visible to visitors. They are **not passwords or credentials**. Consider whether you want to publish redacted copies in future; do not change forensic fields or make edited copies look like untouched evidence.

## Completeness

- [x] 26/26 expected PNG files in `Windows-Privilege-Escalation-Hunt/screenshots/`
- [x] All files indexed by exact filename with direct GitHub links
- [x] Baseline, positive, negative, correlation, and cleanup stages clearly separated
- [x] Every screenshot retained because it adds a field, validation step, or supporting context
- [x] Project 1 and Project 2 screenshot folders untouched
