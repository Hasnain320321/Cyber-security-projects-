# Project 3 — Interview Preparation and Memory Anchors

**Based on the authorised Windows Privilege Escalation Hunt tests completed 10 October 2026.**

## Short interview explanation

"In my personal Wazuh SOC lab I investigated Windows local-group changes. I checked Windows Security Group Management auditing and Wazuh log ingestion, then used a disabled test account to simulate an addition to the built-in Administrators group. I verified Event 4732 with the actor, member SID and target group SID, and confirmed rollback with Event 4733. I implemented custom Wazuh rule 100102, child of built-in rule 60154, to alert only on Event 4732 targeting the built-in Administrators SID S-1-5-32-544. The new rule generated a level 13 alert for the controlled positive test. My negative tests showed removals (4733) were not classified as additions, while an addition to a non-admin group (4732) was instead handled by built-in rule 60144, level 5. The alert was a true positive for a real group change, but the activity was an authorised lab test, not a compromise."

## Five memory anchors

1. **SIEM workflow:** Windows Security log → Wazuh agent → Wazuh manager/rules → analyst triage.
2. **4732 / 4733:** Member added / member removed from security-enabled local group; **4734** is group deletion.
3. **Subject / Member / Group:** Who performed it / which identity changed / what group changed.
4. **Administrators SID ends -544:** A 4732 event without confirming the target group can be an ordinary group change.
5. **Alert ≠ attack:** An accurate detection can represent an authorised change; check approval and follow-on evidence.

## Questions to practise

1. Why doesn't Event ID 4732 alone prove administrator escalation?
2. What's the distinction between `subjectUserName` and `memberSid`?
3. Which identifier reliably distinguishes the built-in Administrators group from a newly created test group?
4. What would you correlate with Event 4732 before escalating? (4624 logon, 4672 privileged logon, Sysmon process telemetry when present, change approval.)
5. Why are negative tests necessary for detection engineering?
6. What did rule 100102 add beyond built-in Wazuh rule 60154?
7. Why was the detected event a true positive but the activity classified as benign?
8. How did you restore and verify safe group membership after the test?

## Technical quick reference

| Concept | Verified lab result |
| --- | --- |
| Main custom rule | 100102, level 13 |
| Parent built-in rule | 60154, level 12 |
| Windows 4732 addition | Positive when target SID is S-1-5-32-544 |
| Windows 4733 removal | Excluded from custom addition rule |
| Non-admin 4732 test | Rule 60144, level 5 |
| MITRE ATT&CK | T1098.007 |
| Test account | SOC-PrivEsc-Test, disabled throughout |
| Remaining work | Screenshots in repo, logon/process correlation and final housekeeping |

These are **project-specific notes**, not a replacement for the existing 40 flashcards from Projects 1 and 2. Add Project 3 cards only when reviewing this completed material in a later study session.
