# SOC Home Lab — Interview Summary

## 30-Second Version

I built a small SOC home lab using a Windows endpoint, Sysmon, a Wazuh 4.14.8 SIEM appliance, VirtualBox networking, and Kali Linux for lab expansion. I generated controlled security events, investigated them using a repeatable SOC workflow, and documented the evidence in GitHub.

I completed three scenarios: a failed Windows logon, suspicious-looking PowerShell process creation, and a custom Wazuh detection for PowerShell `Test-NetConnection` activity. I used Windows Security logs, Sysmon Event IDs 1 and 3, Wazuh alerts, process lineage, command lines, PIDs, and network fields to validate and correlate the activity.

The main lesson was that an alert is only the starting point. I learned to verify the underlying telemetry, scope the activity, and classify events based on evidence rather than assuming that a suspicious-looking alert is malicious.

## 60-Second Version

I built a SOC home lab using Wazuh, Sysmon, a monitored Windows endpoint, VirtualBox networking, and Kali Linux.

The Windows host sends Windows Event Logs and Sysmon telemetry into Wazuh. I verified the full telemetry path and then generated three controlled scenarios.

The first scenario was a failed local authentication event. I investigated Event ID 4625, correlated it with a later Event ID 4624 success, and classified it as a Benign Positive.

The second scenario generated a PowerShell child process. Sysmon Event ID 1 and Wazuh rule 92027 showed the process, command line, user, PID, parent PID, and integrity level. I scoped for follow-on child processes and retained MITRE ATT&CK T1059.001 because the evidence directly showed PowerShell execution.

For the third scenario I created my own Wazuh rule, rule 100100, to detect `Test-NetConnection` in a PowerShell process command line. I then correlated the Wazuh process alert with Sysmon Event ID 3 using the same PID, proving that the detected process made the expected TCP connection to the lab Wazuh server on port 443.

Across the project I used the workflow **Validate -> Identify -> Correlate -> Scope -> Classify** and documented the detections, investigations, screenshots, troubleshooting, and lessons learned in GitHub.

## Technical Architecture

```text
Windows endpoint
  |- Windows Security Event Logs
  |- Sysmon
  |- Wazuh Agent
          |
          | Host-Only network
          v
Wazuh 4.14.8 appliance
  |- Manager
  |- API
  |- Dashboard / Threat Hunting

Kali Linux VM
  |- Controlled lab/test system
```

Verified lab addresses:

- Windows endpoint: `192.168.56.1`
- Wazuh manager: `192.168.56.101`

## Scenario 1 — Failed Authentication

### What happened?

A controlled local sign-in failure was generated on the Windows endpoint.

### What telemetry did you use?

- Windows Event ID 4625 — failed logon
- Windows Event ID 4624 — successful logon/unlock
- Wazuh rule 60122

### What did you investigate?

- Account
- Device
- Source context
- Logon type
- Number of attempts
- Timeline
- Successful login after the failure

### Verdict

**Benign Positive.**

The authentication failure was real, but it was an expected local mistake followed by a successful unlock, with no evidence of repeated credential guessing or suspicious remote activity in the reviewed data.

## Scenario 2 — PowerShell Process Investigation

### What happened?

I generated:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process | Select-Object -First 5"
```

### What telemetry did you use?

- Sysmon Event ID 1 — Process Create
- Wazuh rule 92027 — `Powershell process spawned powershell instance`

### What did you investigate?

- Process image
- Full command line
- User
- PID
- Parent image
- Parent PID
- Integrity level
- Child-process scope

### Verdict

**Benign Positive.**

The alert correctly detected PowerShell spawning another PowerShell process, but the command was deliberately generated and harmless in the lab.

### MITRE

**T1059.001 — PowerShell**

The mapping was kept because PowerShell execution was directly supported by the telemetry.

## Scenario 3 — Custom Wazuh Detection

### What happened?

I created a custom Wazuh rule to detect PowerShell process creation when the command line contains `Test-NetConnection`.

The controlled trigger was:

```powershell
powershell.exe -NoProfile -Command "Test-NetConnection 192.168.56.101 -Port 443"
```

### Custom detection

- Rule ID: `100100`
- Level: `6`
- Description: `Custom detection: PowerShell Test-NetConnection executed`

### What telemetry did you use?

- Sysmon Event ID 1 — Process Create
- Sysmon Event ID 3 — Network Connection
- Wazuh custom alert

### What was the key correlation?

The Wazuh process alert showed PID `15676`.

I queried Sysmon Event ID 3 for the same PID and found:

- Source: `192.168.56.1:58463`
- Destination: `192.168.56.101:443`
- Protocol: TCP
- Initiated: true

That allowed me to prove that the exact PowerShell process detected by Wazuh generated the expected network connection.

### Scope

- One matching Event ID 3 network connection was found for PID `15676` in the 30-minute period reviewed.
- No child process creation from PID `15676` was found in the reviewed Sysmon Event ID 1 data.

### Verdict

**Benign Positive.**

The detection was correct, but the activity was intentionally generated in the controlled lab.

## Investigation Workflow

### Validate

Confirm the alert is backed by genuine underlying telemetry.

### Identify

Identify the relevant host, user, account/process, command line, PID, privilege level, source/destination, and timestamp.

### Correlate

Connect related events using fields such as PID, host, account, IP address, or time.

### Scope

Determine how far the activity went without claiming more than the reviewed data proves.

### Classify

Classify the event as:

- True Positive
- False Positive
- Benign Positive
- Undetermined

Then decide whether escalation is needed.

## Important Concepts I Can Explain

### Benign Positive vs False Positive

A **Benign Positive** means the detection correctly identified the activity, but the activity was expected or harmless.

A **False Positive** means the detection itself incorrectly identified the activity.

### Sysmon Event ID 1

**Process Creation.**

Useful investigation fields include:

- Image
- CommandLine
- ParentImage
- User
- PID
- Parent PID
- Integrity
- Time

### Sysmon Event ID 3

**Network Connection.**

Useful fields include:

- Process
- Source IP
- Destination IP
- Source port
- Destination port
- Protocol
- User
- Time

### High Integrity

High integrity means the process is running in an elevated context. It is important investigation context but does not prove maliciousness.

### MITRE ATT&CK

I only retain a MITRE ATT&CK technique when the observed evidence supports it.

For example, I retained **T1059.001 PowerShell** because the telemetry directly proved PowerShell execution. I did not label a single connection to port 443 as scanning or C2 because the evidence did not prove those behaviours.

## Troubleshooting Example

At one point the Wazuh dashboard reported that the API was down.

I checked the manager service and found a startup timeout. I reviewed the service logs, Wazuh logs, memory, and running processes. A stale startup lock contained PID `1962`, but the process no longer existed.

After confirming the lock was stale, it was removed and the Wazuh manager was started again successfully.

This taught me to troubleshoot from evidence rather than immediately reinstalling or rebuilding a system.

## What I Would Improve Next

- Validate direct Kali-to-Windows communication if needed for future offensive/defensive scenarios.
- Expand the lab with more network-focused testing and PCAP analysis.
- Add Sigma/KQL-style detection work.
- Add threat-intelligence and phishing investigations.
- Continue building detection engineering skills with explainable rules and clear false-positive analysis.

## GitHub Evidence

The project repository contains:

- Three detection write-ups
- Three investigation reports
- Numbered evidence screenshots
- Wazuh custom rule evidence
- Learning and troubleshooting notes
- MITRE ATT&CK mappings where supported
- Final project documentation
