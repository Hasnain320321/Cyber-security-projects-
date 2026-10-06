# Investigation 03: PowerShell Test-NetConnection Network Activity

## Executive Summary

A controlled network-connectivity test was generated on the monitored Windows endpoint to practise custom detection engineering and SOC investigation.

The test launched a new PowerShell process with the command:

```powershell
powershell.exe -NoProfile -Command "Test-NetConnection 192.168.56.101 -Port 443"
```

A custom Wazuh rule, ID `100100` at level `6`, detected the Sysmon Event ID 1 process-creation event because the command line contained `Test-NetConnection`.

The detected PowerShell process had PID `15676`. Local Sysmon Event ID 3 telemetry was then reviewed for that same PID and confirmed that it initiated a TCP connection from `192.168.56.1` to the lab Wazuh manager at `192.168.56.101:443`.

A 30-minute scope query found one Sysmon Event ID 3 network connection for PID `15676`. A separate Sysmon Event ID 1 scope query for `ParentProcessId: 15676` returned no matching child-process creation events in the reviewed time window.

The activity was classified as a **Benign Positive**. The custom detection correctly identified the activity it was designed to detect, but the PowerShell command and network connection were intentionally generated in the controlled lab and no suspicious follow-on activity was found in the checks performed.

## Alert Details

- **Alert name:** Custom detection: PowerShell Test-NetConnection executed
- **Date:** 6 October 2026
- **Wazuh alert timestamp:** approximately 23:48:46 local
- **Affected host:** `Windows-Host` / `LAPTOP-C7OPSS6H`
- **Endpoint IP:** `192.168.56.1`
- **User:** `LAPTOP-C7OPSS6H\\hasna`
- **Sysmon process event:** Event ID `1`
- **Wazuh rule ID:** `100100`
- **Wazuh rule level:** `6`
- **Integrity level:** `High`
- **Process ID:** `15676`
- **Parent process ID:** `12640`

## Initial Hypothesis

`Test-NetConnection` is a legitimate PowerShell diagnostic command, but unexpected connectivity testing can deserve investigation.

The initial task was to determine:

- What process executed the command?
- Which user executed it?
- What launched the process?
- Which destination and port were tested?
- Did the detected process actually generate the expected network connection?
- Did the process make additional network connections or launch child processes?
- Was the activity expected or suspicious?

## Data Sources Reviewed

- [x] Sysmon Event ID 1 - Process Create
- [x] Sysmon Event ID 3 - Network Connection
- [x] Wazuh / SIEM
- [ ] Windows Security authentication logs
- [ ] Packet capture
- [ ] Other

## Investigation Timeline

| Time | Event | Evidence | Analyst interpretation |
| --- | --- | --- | --- |
| ~23:48 local | New PowerShell process created | Sysmon Event ID 1; PID 15676 | Process execution requiring context |
| ~23:48 local | Custom Wazuh alert fired | Rule 100100, level 6 | Command line matched `Test-NetConnection` |
| ~23:48 local | Network connection generated | Sysmon Event ID 3; PID 15676 | Same process initiated TCP connection to 192.168.56.101:443 |
| Investigation | Network scope check | Count = 1 for Event ID 3 and PID 15676 in reviewed 30-minute window | Only one matching network event found in reviewed data |
| Investigation | Child-process scope check | No Event ID 1 results with ParentProcessId 15676 in reviewed 30-minute window | No child process creation found in reviewed data |

## Investigation Steps

### 1. Validate the alert

The Wazuh alert was validated against the underlying Sysmon Event ID 1 telemetry.

The alert showed:

- **Rule ID:** `100100`
- **Rule level:** `6`
- **Description:** `Custom detection: PowerShell Test-NetConnection executed`
- **Agent:** `Windows-Host`

This confirmed that the custom rule fired on real endpoint telemetry rather than producing an unsupported alert.

### 2. Identify the affected asset and process

The event occurred on `Windows-Host` (`LAPTOP-C7OPSS6H`) at `192.168.56.1`.

Relevant process evidence:

- **Image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Command line:** `powershell.exe -NoProfile -Command "Test-NetConnection 192.168.56.101 -Port 443"`
- **User:** `LAPTOP-C7OPSS6H\\hasna`
- **Integrity level:** `High`
- **PID:** `15676`
- **Parent image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Parent PID:** `12640`

The high integrity level was treated as elevated execution context, not as proof of malicious activity.

### 3. Correlate process activity with network telemetry

Sysmon Event ID 3 was queried locally for PID `15676`.

The matching network event showed:

- **Process:** `powershell.exe`
- **Process ID:** `15676`
- **User:** `LAPTOP-C7OPSS6H\\hasna`
- **Protocol:** `TCP`
- **Initiated:** `true`
- **Source IP:** `192.168.56.1`
- **Source port:** `58463`
- **Destination IP:** `192.168.56.101`
- **Destination port:** `443`
- **Destination port name:** `https`

This proved that the same PowerShell PID detected by Wazuh generated the expected network connection.

### 4. Determine scope

Two scope checks were performed.

#### Network scope

A 30-minute query counted Sysmon Event ID 3 records for PID `15676`.

**Result:** `Count = 1`.

The supported conclusion is:

> One Sysmon Event ID 3 network connection was found for PID 15676 in the 30-minute period reviewed.

This does not prove that the process could never have performed other activity outside the reviewed data or time window.

#### Child-process scope

A 30-minute Sysmon Event ID 1 query searched for:

`ParentProcessId: 15676`

The query returned no matching events.

The supported conclusion is:

> No child process creation from PID 15676 was found in the Sysmon data reviewed.

### 5. Classify the incident

**Benign Positive.**

The custom rule accurately detected a real `Test-NetConnection` command, so the alert was not a False Positive.

The activity was intentionally generated in the lab, the destination was the controlled Wazuh manager, the command tested a single TCP port, the network telemetry matched the expected behaviour, and no child process creation was found in the reviewed scope.

## Indicators / Relevant Artefacts

| Type | Value | Notes |
| --- | --- | --- |
| Host | `LAPTOP-C7OPSS6H` | Monitored Windows endpoint |
| Endpoint IP | `192.168.56.1` | Source host |
| Process | `powershell.exe` | Detected process |
| PID | `15676` | Correlated across Event ID 1 and Event ID 3 |
| Parent process | `powershell.exe` | Existing PowerShell session |
| Parent PID | `12640` | Parent process reported by Sysmon |
| Destination IP | `192.168.56.101` | Lab Wazuh manager |
| Destination port | `443` | TCP |
| Event ID | `1` | Sysmon process creation |
| Event ID | `3` | Sysmon network connection |
| Wazuh rule | `100100` | Custom detection |
| Wazuh level | `6` | Custom alert severity |

## MITRE ATT&CK Mapping

- **Tactic:** Execution
- **Technique:** PowerShell
- **Technique ID:** T1059.001

This mapping is retained because the evidence directly demonstrates PowerShell execution.

No network-scanning or command-and-control mapping was added. The observed evidence was a single controlled connection to one internal lab destination and one port, which is insufficient to claim scanning or C2 behaviour.

## Findings

The custom detection worked as intended and generated a visible Wazuh alert when a new PowerShell process executed `Test-NetConnection`.

The process evidence established the exact command, user, process lineage, integrity level, and PID.

Sysmon Event ID 3 then independently confirmed that PID `15676` initiated the expected TCP connection to `192.168.56.101:443`.

The network scope check found one matching connection for the PID in the reviewed 30-minute period, and the child-process scope check found no matching child-process creation events.

## Recommended Response

For this controlled lab event, no remediation or escalation is required.

In a real SOC environment, an analyst should review:

- Whether the user was expected to perform connectivity testing
- The destination reputation and ownership
- Whether multiple destinations or ports were tested
- Process ancestry
- Privilege level
- Related PowerShell activity
- Child processes
- Nearby authentication and endpoint events

Escalation should be based on the combined evidence and business context rather than the presence of `Test-NetConnection` alone.

## Final Verdict

- **Classification:** Benign Positive
- **Investigation severity:** Low
- **Wazuh alert level:** 6
- **Confidence:** High
- **Escalation:** No

## Evidence

Evidence reviewed during the lab includes:

- [Screenshot 12 - Initial Test-NetConnection success](../screenshots/12-test-netconnection-success.png)
- [Screenshot 13 - Custom Wazuh rule 100100 alert](../screenshots/13-custom-test-netconnection-alert.png)
- [Screenshot 14 - PowerShell process and command-line details](../screenshots/14-custom-rule-process-details.png)
- [Screenshot 15 - Custom rule evidence](../screenshots/15-custom-rule-evidence.png)
- [Screenshot 16 - Sysmon Event ID 3 PID correlation](../screenshots/16-event3-pid-correlation.png)
- [Screenshot 17 - Network scope count](../screenshots/17-network-scope-count.png)
- [Screenshot 18 - No child process creation found](../screenshots/18-no-child-processes-found.png)

## Lessons Learned

This investigation demonstrated the full analyst workflow:

**Validate -> Identify -> Correlate -> Scope -> Classify**

It also reinforced several important SOC concepts:

- Sysmon Event ID 1 records process creation.
- Sysmon Event ID 3 records network connections.
- Process IDs can be used to correlate process and network telemetry.
- A custom detection can be technically correct while the underlying activity is benign.
- High integrity means elevated execution context, not automatic maliciousness.
- Scope conclusions must stay inside the evidence and time window actually reviewed.
