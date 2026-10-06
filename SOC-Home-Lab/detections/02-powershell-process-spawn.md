# Detection 02: PowerShell Process Spawned PowerShell

## Purpose

Detect PowerShell process creation where a PowerShell process spawns another PowerShell instance so that an analyst can review the command line, parent process, user context, privilege level, and follow-on activity.

## Threat / Behaviour

PowerShell is a legitimate administration tool, but it is also commonly used for execution and post-exploitation activity. A PowerShell process launching another PowerShell instance is not automatically malicious and must be investigated in context.

## Data Source

- Sysmon
- Wazuh

## Detection Logic

The lab validated Sysmon **Event ID 1**, which records process creation.

Wazuh matched the event using:

- **Rule ID:** `92027`
- **Rule level:** `4`
- **Rule description:** `Powershell process spawned powershell instance`

Threat Hunting validation filters used during investigation included:

```text
data.win.system.eventID: 1
data.win.eventdata.commandLine: Get-Process
```

## Trigger Conditions

The detection fires when Sysmon records a PowerShell process creation that matches the Wazuh rule for a PowerShell process spawning another PowerShell instance.

## MITRE ATT&CK Mapping

- **Tactic:** Execution
- **Technique:** PowerShell
- **Technique ID:** T1059.001

This mapping is retained because the observed telemetry directly showed PowerShell execution.

## Validation

The detection was safely tested on the monitored Windows endpoint by deliberately running:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process | Select-Object -First 5"
```

The command only enumerated the first five running processes. Sysmon recorded the child PowerShell process as Event ID 1 and Wazuh raised rule 92027.

## Expected Evidence

- **Host:** `Windows-Host` / `LAPTOP-C7OPSS6H`
- **Endpoint IP:** `192.168.56.1`
- **User:** `LAPTOP-C7OPSS6H\\hasna`
- **Process:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Parent process:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Child PID:** `6880`
- **Parent PID:** `1296`
- **Integrity level:** `High`
- **Event ID:** `1`
- **Wazuh rule ID:** `92027`
- **Wazuh level:** `4`

## False / Benign Positives

Legitimate causes can include:

- Administrative PowerShell usage
- Automation or scripts
- Security tooling
- Troubleshooting commands
- Controlled lab testing

## Triage Steps

1. Validate the Sysmon Event ID 1 process-creation event.
2. Identify the host, user, image, command line, and integrity level.
3. Review the parent image and parent command line.
4. Check whether the PowerShell process spawned additional child processes.
5. Review nearby events for related suspicious behaviour.
6. Compare the activity with expected user or administrative behaviour.
7. Classify the alert based on evidence.

## Response Recommendations

For expected administrative or lab activity, no remediation may be required.

If the command line, parent process, user context, or follow-on behaviour is suspicious, review additional endpoint telemetry and consider escalation, isolation, credential review, or containment only when supported by evidence.

## Result

- **Classification:** Benign Positive
- **Severity:** Low investigation severity / Wazuh level 4
- **Escalation required:** No

## Lessons Learned

A PowerShell alert is a starting point for investigation rather than proof of compromise. The command line, process lineage, user context, privilege level, and follow-on activity are required to decide whether the event is benign or malicious.
