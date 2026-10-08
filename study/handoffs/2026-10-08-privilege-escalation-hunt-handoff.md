# SOC Portfolio Handoff - Privilege Escalation Hunt Added

**Date:** 8 October 2026  
**Repository:** https://github.com/Hasnain320321/Cyber-security-projects-  
**Use:** Resume the next lab session without losing progress. This handoff was checked against the live GitHub project documents on 8 October 2026.

## Portfolio status

| Workstream | Status | What is verified |
| --- | --- | --- |
| Project 1: SOC Home Lab | **Complete** | Wazuh/Sysmon lab, three controlled scenarios, detections, investigations and interview summary |
| Project 2: Wazuh Brute-Force Detection and Authentication Investigation | **Complete** | Custom rule 100101, four validation scenarios, two investigations, response guide, interview summary and 26 curated GitHub screenshots |
| New standalone supplemental project: Windows Privilege Escalation Hunt | **Planned / setup ready** | GitHub structure and detection/investigation/evidence templates created; no test events or new detections yet |
| Phishing Email Investigation (original roadmap Phase 3) | **Planned** | Deferred by user; not replaced or renamed by the new hunt |

### Project 1 - retained as Complete

- Wazuh 4.14.8 manager with Windows agent and Sysmon; isolated host-only lab network.
- Windows host agent IP: `192.168.56.1`; Wazuh manager: `192.168.56.101`.
- Three documented SOC scenarios, including PowerShell process creation and Test-NetConnection detection `100100`.
- Files in `SOC-Home-Lab/` remain independent from the new project.

### Project 2 - retained as Complete

- Windows failed sign-in `4625`, successful sign-in `4624`.
- Custom Wazuh rule `100101`: 3 matching failed logins against the same username within 60 seconds (intentionally low lab threshold).
- Four controlled validation scenarios: two positive and two negative.
- Separate investigation: two failures for `SOC-Lab-Test2` at 18:01:21 and 18:01:26 followed by an authorised local Type 2 success at 18:01:33.
- **26 curated screenshots on GitHub:** 19 for Investigation 01 and 7 for Investigation 02.
- Known optional evidence gap: `25-mcafee-webadvisor-process-details.png` not uploaded; the account filter is not visible in the cropped failure-row screenshot. These limitations are documented, and the case is not presented as a real attacker compromise.
- Daily review: **40 flashcards total**, 20 SOC Home Lab + 20 Project 2, at `study/SOC-FLASHCARDS-PROJECTS-1-2.md`.

## New project - Windows Privilege Escalation Hunt

**Project folder:** [Windows-Privilege-Escalation-Hunt](../../Windows-Privilege-Escalation-Hunt/)

**Goal:** Hunt for unexpected membership changes in the local Windows Administrators group and explain whether the activity is approved administration or a potential escalation attempt.

**Primary data sources:**

| Event | Meaning |
| --- | --- |
| Windows Security `4732` | Member added to a security-enabled local group |
| Windows Security `4733` | Member removed from a security-enabled local group |
| Windows Security `4735` | Security-enabled local group changed (supplemental context) |
| Windows Security `4672` | Special privileges assigned to a new logon; does not by itself prove a change |
| Windows Security `4624` | Successful login to correlate |
| Sysmon `1` | Process creation evidence when captured |

**Privilege-target check:** The built-in Administrators group typically has a SID ending `-544`. Confirm the actual group identity in collected telemetry before writing a custom rule.

**MITRE ATT&CK:** `T1098.007` - Additional Local or Domain Groups.

**New project files verified on GitHub:**

- `Windows-Privilege-Escalation-Hunt/README.md` - project scope, safety, steps and status.
- `detections/01-local-admin-membership.md` - detection hypothesis, rule planning and positive/negative test matrix.
- `investigations/01-privileged-group-change.md` - unfilled investigation template (NOT a completed case).
- `screenshots/README.md` - planned evidence checklist (zero collected screenshots).
- `notes/INTERVIEW-PREP.md` - concepts and anticipated interview questions (NOT completed answers).

**Important:** No privilege membership changes, 4732/4733 evidence, custom rule, positive/negative tests, screenshots or final privilege-escalation investigation have been performed yet. Never label this project Complete on the current evidence.

## Resume from exactly this step

On the Windows lab machine, in **PowerShell as Administrator**, run this **read-only** command:

```powershell
auditpol /get /subcategory:"Security Group Management"
```

Send a **screenshot of the output**. We will explain Success/Failure/No Auditing, decide whether any audit policy change is needed, and verify that relevant Security logs can reach Wazuh.

**Do not add an account to Administrators, change audit settings, or create a new detection rule yet.**

## Future planned lab sequence

1. Inspect Windows audit-policy setting (above) and Wazuh telemetry readiness.
2. Prefer an owned/disposable Windows VM for group membership change testing. If using the actual Windows host, agree safety and recovery plan first.
3. Record baseline Administrators group membership and confirm a second, working administrator route; avoid changing the only administrator.
4. Perform a controlled, reversible test-account addition in a machine you own/control; capture Event 4732, who acted (Subject), added account (Member), actual group SID and timestamp.
5. Remove the test user and verify restoration; capture Event 4733.
6. Develop a **new, independent** Wazuh rule for Administrators-group additions only after examining actual ingested event fields. Preserve existing rule 100100 and 100101.
7. Run negative validation using an approved nonprivileged group change; check for false positives.
8. Investigate related 4624, 4672 and Sysmon 1 events where available, then write case findings, evidence index, defensive recommendations and interview summary.

## Five knowledge anchors for the next session

1. **SIEM = Security Information and Event Management**; Wazuh collects and correlates endpoint/security logs.
2. **Agent sends telemetry; manager processes and correlates it.**
3. **4732 = group member added; 4733 = group member removed.**
4. **Subject = account performing the change; Member = account being added/removed; Group = target group.**
5. **4672 privileged logon does NOT automatically prove privilege escalation.** Alert -> validate -> identify -> correlate -> scope -> classify.

## Guardrails

- All privilege-change testing must remain on systems owned/controlled by the learner.
- Maintain clear Project 1, Project 2 and Privilege Escalation Hunt folders; do not move old evidence.
- Preserve honest evidence boundaries; no invented screenshots, rules or completed tests.
- Phishing Email Investigation remains planned for later when the user requests it.

## Links

- [Portfolio](../../README.md)
- [Project roadmap](../../PROJECT-ROADMAP.md)
- [Privilege Escalation Hunt](../../Windows-Privilege-Escalation-Hunt/README.md)
- [Privilege Hunt detection plan](../../Windows-Privilege-Escalation-Hunt/detections/01-local-admin-membership.md)
- [SOC 40-card deck](../SOC-FLASHCARDS-PROJECTS-1-2.md)
