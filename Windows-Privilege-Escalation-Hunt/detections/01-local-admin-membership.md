# Detection 01 — Unusual Local Administrators Group Membership Addition

**Status: Detection design only — not deployed or validated.**

## Hypothesis

Unexpected addition of a local or domain identity to the built-in Windows Administrators group may permit subsequent elevated access and justify SOC review. Legitimate software installers and administrators may perform this too.

- Event provider: `Microsoft-Windows-Security-Auditing`
- Windows Security event: `4732`
- High-value group: built-in Administrators SID ending in `-544`
- ATT&CK: [T1098.007](https://attack.mitre.org/techniques/T1098/007/) (Additional Local or Domain Groups)

## Fields to verify in actual Wazuh event

| Windows event information | Investigation question |
| --- | --- |
| `Member` (account SID, possibly account name) | Which account was added? |
| `Group` name and SID | Was the affected group actually Administrators? |
| `Subject` username/SID | Who made the change? |
| Computer/agent name | On which endpoint? |
| Event time | When did it happen? |
| Related process and logon events | Did the actor use an expected administration tool? |

Do **not** hardcode Wazuh JSON paths yet: obtain them from a real Event 4732 first, since flattened field names and parsers differ.

## Test matrix

| Test | Expected |
| --- | --- |
| Approved addition to Administrators (dedicated test identity) | Relevant raw Windows 4732; custom high-interest alert after detection rule is deployed |
| Removal from Administrators | Windows 4733 and confirmed rollback |
| Approved addition to nonprivileged group | Raw group-change telemetry but no *Administrators-specific* custom alert |
| Special-privileges logon alone (4672) | No alert claiming an account was newly added to Administrators |

**Threshold:** A single unexpected membership addition can be significant. Do **not** copy the three-in-60-seconds brute-force rule from Project 2.

## Rule development sequence

1. Check audit policy.
2. Verify that 4732 exists in Windows Event Viewer and Wazuh.
3. Identify the **actual** fields for target group SID/name, subject and member.
4. Select a new unused Wazuh custom rule ID that does not conflict with rule 100100 or 100101.
5. Test syntax, restart the manager and check service status.
6. Validate positive/negative tests, document exact observed outcomes, and retain rollback proof.

No XML rule has been created or deployed for this project yet.
