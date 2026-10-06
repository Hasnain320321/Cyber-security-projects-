# Investigation 02: PowerShell Process Spawning PowerShell

## Executive Summary

A controlled PowerShell command was generated on the monitored Windows endpoint to validate Sysmon process telemetry and practise Tier 1 SOC investigation. Sysmon recorded a process-creation event and Wazuh raised rule 92027 at level 4 with the description `Powershell process spawned powershell instance`.

The child process was `powershell.exe` with PID `6880`. Its command line used `-NoProfile` and `-ExecutionPolicy Bypass` to run `Get-Process | Select-Object -First 5`. The parent image was another PowerShell instance with PID `1296`, matching the fact that the test command was executed from an existing PowerShell session.

A scope query for Sysmon Event ID 1 events with `parentProcessId = 6880` returned no results in Wazuh, so no additional child process creation was found for the test PowerShell process in the data reviewed.

The activity was classified as a **Benign Positive**. The detection correctly identified real PowerShell process behaviour, but the command was deliberately generated in the lab and no malicious follow-on activity was found in the checks performed.

## Alert Details

- **Alert name:** Powershell process spawned powershell instance
- **Date:** 6 October 2026
- **Wazuh local timestamp:** approximately 15:51:37
- **Sysmon UTC time:** `2026-10-06 14:51:38.617`
- **Affected host:** `Windows-Host` / `LAPTOP-C7OPSS6H`
- **Endpoint IP:** `192.168.56.1`
- **User:** `LAPTOP-C7OPSS6H\\hasna`
- **Sysmon Event ID:** `1`
- **Wazuh rule ID:** `92027`
- **Wazuh rule level:** `4`
- **Integrity level:** `High`
- **Process ID:** `6880`
- **Parent process ID:** `1296`

## Initial Hypothesis

PowerShell spawning another PowerShell process can be legitimate administrative activity or suspicious execution. The command line, parent process, user context, privilege level, and follow-on activity needed to be reviewed before deciding whether escalation was necessary.

## Data Sources Reviewed

- [x] Sysmon
- [x] Wazuh / SIEM
- [ ] Windows Security Logs
- [ ] Network telemetry
- [ ] Other

## Investigation Timeline

| Time | Event | Evidence | Analyst interpretation |
| --- | --- | --- | --- |
| ~15:51 local | Child PowerShell process created | Sysmon Event ID 1; PID 6880 | Real process creation requiring context |
| ~15:51 local | Wazuh detection fired | Rule 92027, level 4 | PowerShell spawned from PowerShell |
| Investigation | Child-process scope check | `parentProcessId = 6880` returned no results | No additional child process creation found in reviewed Wazuh data |

## Investigation Steps

### 1. Validate the alert

The alert was validated against Sysmon Event ID 1 telemetry in Wazuh. The underlying process-creation event was present and contained the expected PowerShell executable and command line.

### 2. Identify the affected asset

The event occurred on `Windows-Host` (`LAPTOP-C7OPSS6H`) at `192.168.56.1`.

Relevant process evidence:

- **Image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Command line:** `powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process | Select-Object -First 5"`
- **User:** `LAPTOP-C7OPSS6H\\hasna`
- **Integrity level:** `High`
- **PID:** `6880`

### 3. Review related activity

Sysmon showed that the parent image was another PowerShell instance:

- **Parent image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Parent PID:** `1296`

This was consistent with how the lab operator executed the command: from an existing PowerShell session.

### 4. Determine scope

A Wazuh search for Sysmon Event ID 1 with `data.win.eventdata.parentProcessId = 6880` returned no results.

This supports the limited conclusion that no additional child process creation was found for PID 6880 in the Wazuh data reviewed. It does not prove that no other activity occurred anywhere on the endpoint.

### 5. Classify the incident

**Benign Positive.**

The detection correctly identified a real PowerShell-to-PowerShell process relationship, so it was not a False Positive. The activity was deliberately generated in the lab, the command only enumerated running processes, and no suspicious child process creation was found in the scope check.

## Indicators / Relevant Artefacts

| Type | Value | Notes |
| --- | --- | --- |
| Host | `LAPTOP-C7OPSS6H` | Monitored Windows endpoint |
| Endpoint IP | `192.168.56.1` | Wazuh agent IP |
| Process | `powershell.exe` | Child process |
| Child PID | `6880` | Test PowerShell process |
| Parent process | `powershell.exe` | Existing PowerShell session |
| Parent PID | `1296` | Parent process reported by Sysmon |
| Event ID | `1` | Sysmon process creation |
| Wazuh rule | `92027` | PowerShell spawned PowerShell |

## MITRE ATT&CK Mapping

- **Tactic:** Execution
- **Technique:** PowerShell
- **Technique ID:** T1059.001

Unlike the unsupported mapping seen in Investigation 01, this mapping is retained because PowerShell execution is directly demonstrated by the telemetry.

## Findings

The event was caused by a deliberately generated PowerShell command in the lab. Sysmon captured the process image, full command line, user, privilege level, process ID, and parent process information. Wazuh correctly detected the PowerShell-to-PowerShell process relationship.

The investigation found no evidence in the reviewed Wazuh process-creation data that PID 6880 launched additional child processes.

## Recommended Response

For this controlled lab event, no remediation or escalation is required.

In a real SOC environment, an analyst should examine the full command line, process ancestry, user context, integrity level, network activity, script content, and follow-on processes before deciding whether PowerShell activity is malicious.

## Final Verdict

- **Classification:** Benign Positive
- **Investigation severity:** Low
- **Wazuh alert level:** 4
- **Confidence:** High
- **Escalation:** No

## Evidence

Evidence reviewed during the lab includes:

- Sysmon Event ID 1 showing the child PowerShell process.
- Full command line containing `-NoProfile`, `-ExecutionPolicy Bypass`, and `Get-Process | Select-Object -First 5`.
- Parent image and parent PID showing PowerShell PID 1296 spawning PowerShell PID 6880.
- Wazuh rule 92027, level 4, mapped to T1059.001 PowerShell.
- Scope query showing no Sysmon Event ID 1 results with `parentProcessId = 6880`.

Clean screenshots will be linked here after they are committed to the repository.

## Lessons Learned

This investigation demonstrated how Sysmon Event ID 1 can reconstruct process execution using the image, command line, user, integrity level, process ID, and parent process fields.

It also reinforced the difference between a **Benign Positive** and a **False Positive**: the alert was technically correct, but the activity was expected and harmless in the lab context.
