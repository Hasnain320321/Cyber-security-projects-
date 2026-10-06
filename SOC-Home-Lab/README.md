# SOC Home Lab

**Status:** Complete - first portfolio version

## Objective

The purpose of this project is to build a small Security Operations Centre style lab where endpoint and security events can be collected, monitored, detected, and investigated.

The project is designed to demonstrate practical skills relevant to junior SOC Analyst and Cyber Security Analyst roles.

## Current Architecture

```text
                 SOC HOME LAB

          +-----------------------+
          |   SIEM / Dashboard    |
          |        Wazuh          |
          +-----------+-----------+
                      ^
                      | Logs / alerts
                      |
          +-----------+-----------+
          |     Windows 10/11     |
          |                       |
          | Windows Event Logs    |
          | Sysmon (Active)       |
          | Wazuh Agent (Active)  |
          +-----------+-----------+
                      ^
                      |
             Controlled testing
                      |
          +-----------+-----------+
          |      Kali Linux       |
          |     Test machine      |
          +-----------------------+
```

The current lab uses the official Wazuh 4.14.8 appliance in Oracle VirtualBox. The Wazuh VM uses NAT for outbound internet access and a Host-Only adapter for isolated communication with the Windows host.

## What This Project Demonstrates

- Building an isolated cyber security lab
- Windows endpoint monitoring
- Windows Event Log analysis
- Sysmon telemetry
- SIEM ingestion and alerting
- Basic detection engineering
- Custom Wazuh rule creation
- Alert triage
- Incident investigation
- Process-to-network event correlation
- MITRE ATT&CK mapping
- Security report writing
- Benign-positive analysis
- Defensive recommendations

## Detection Scenarios

### 1. Failed Local Authentication

A controlled local sign-in failure was generated and investigated using Windows Security telemetry in Wazuh.

Investigation focused on:

- Account and host
- Event ID 4625
- Source and logon context
- Nearby successful authentication
- Number and pattern of attempts
- Wazuh rule and severity
- Final classification

### 2. PowerShell Process Spawning PowerShell

A safe PowerShell child process was deliberately generated and investigated using Sysmon Event ID 1 and Wazuh.

Investigation focused on:

- Process image
- Full command line
- Parent and child process relationship
- User
- PID and parent PID
- Integrity level
- Follow-on child-process activity
- MITRE ATT&CK T1059.001 - PowerShell

### 3. Custom PowerShell Test-NetConnection Detection

A controlled PowerShell connectivity test was generated against the lab Wazuh manager at `192.168.56.101:443`.

A custom Wazuh rule was created to detect process-creation events whose command line contains `Test-NetConnection`.

Investigation focused on:

- Custom Wazuh rule ID 100100
- Sysmon Event ID 1 process telemetry
- Full PowerShell command line
- User, PID, parent PID, and integrity level
- Sysmon Event ID 3 network telemetry
- Correlation using PID 15676
- Source and destination IP/port
- Network and child-process scope checks
- Evidence-based MITRE ATT&CK mapping
- Benign Positive classification

## Investigation Workflow

The workflow used during the investigations is:

```text
Validate
  |
  v
Identify
  |
  v
Correlate
  |
  v
Scope
  |
  v
Classify
```

The analyst validates the underlying telemetry, identifies the affected user/host/process, correlates related events, scopes the activity, and then classifies it based on the evidence.

## Repository Structure

```text
SOC-Home-Lab/
|
|-- README.md
|-- INTERVIEW-SUMMARY.md
|-- setup/
|   |-- lab-plan.md
|
|-- detections/
|   |-- 01-windows-failed-logon.md
|   |-- 02-powershell-process-spawn.md
|   |-- 03-powershell-test-netconnection.md
|   |-- detection-template.md
|
|-- investigations/
|   |-- 01-failed-local-authentication.md
|   |-- 02-powershell-process-spawn.md
|   |-- 03-test-netconnection-network-activity.md
|   |-- investigation-template.md
|
|-- screenshots/
|   |-- README.md
|   |-- 04 through 19 evidence screenshots
|
|-- notes/
    |-- learning-log.md
```

## Verified Progress Evidence

### Windows endpoint enrolled in Wazuh

The Windows host has been successfully enrolled as a Wazuh agent over the isolated Host-Only network.

- **Agent name:** `Windows-Host`
- **Endpoint IP:** `192.168.56.1`
- **Wazuh manager:** `192.168.56.101`
- **Agent version:** `4.14.8`
- **Status:** **Active**

This confirms that the Windows endpoint is registered with the Wazuh manager and the agent is actively communicating with the SIEM.

### Sysmon installed and generating events

Sysmon was installed on the Windows host and the `Microsoft-Windows-Sysmon/Operational` channel was verified. Sysmon **Event ID 1 (Process Create)** and **Event ID 3 (Network Connection)** telemetry were observed during the lab.

### Sysmon telemetry ingested by Wazuh

Wazuh Threat Hunting confirmed that Sysmon process-creation telemetry from `Windows-Host` is being ingested and is searchable.

This verifies the endpoint telemetry path:

**Windows host -> Sysmon -> Wazuh agent -> Wazuh manager/dashboard**

### Scenario 1 - Failed local authentication

A controlled local sign-in failure generated **Windows Event ID 4625**, which was ingested by Wazuh and matched **rule 60122** at **level 5**.

The failed event was correlated with a **Windows Event ID 4624** successful workstation unlock a few seconds later. The activity was classified as a **Benign Positive** because it was a single expected local failure followed by a successful unlock, with no evidence of repeated credential guessing or remote activity in the data reviewed.

- [Detection 01 - Windows Failed Logon](./detections/01-windows-failed-logon.md)
- [Investigation 01 - Failed Local Authentication](./investigations/01-failed-local-authentication.md)

### Scenario 2 - PowerShell process creation

A controlled PowerShell process was generated using:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process | Select-Object -First 5"
```

Sysmon Event ID 1 recorded the process and Wazuh raised **rule 92027** at **level 4**, describing a PowerShell process spawning another PowerShell instance.

The command line, process lineage, user, PID, parent PID, and integrity level were investigated. The activity was classified as a **Benign Positive**. MITRE ATT&CK **T1059.001 - PowerShell** was retained because the telemetry directly demonstrated PowerShell execution.

- [Detection 02 - PowerShell Process Spawn](./detections/02-powershell-process-spawn.md)
- [Investigation 02 - PowerShell Process Spawn](./investigations/02-powershell-process-spawn.md)

### Scenario 3 - Custom Test-NetConnection detection

A custom Wazuh rule was created in `local_rules.xml` to alert on Sysmon Event ID 1 process creation when the command line contains `Test-NetConnection`.

The controlled test launched:

```powershell
powershell.exe -NoProfile -Command "Test-NetConnection 192.168.56.101 -Port 443"
```

Wazuh raised custom **rule 100100** at **level 6**. The detected PowerShell process had PID `15676`.

Sysmon Event ID 3 telemetry for the same PID confirmed a TCP connection from `192.168.56.1:58463` to `192.168.56.101:443`. A 30-minute network scope query found one matching Event ID 3 record for PID `15676`, and a child-process query found no Event ID 1 events with `ParentProcessId = 15676` in the reviewed period.

The activity was classified as a **Benign Positive** because the detection was accurate but the activity was deliberately generated and expected in the controlled lab.

- [Detection 03 - PowerShell Test-NetConnection](./detections/03-powershell-test-netconnection.md)
- [Investigation 03 - Test-NetConnection Network Activity](./investigations/03-test-netconnection-network-activity.md)
- [Scenario evidence screenshots](./screenshots/README.md)

## Success Criteria

The first version of this project will be considered complete when:

- [x] Windows host is connected to the isolated lab network
- [x] Kali Linux can communicate with the Windows endpoint
- [x] Kali Linux can communicate with the Wazuh manager
- [x] Wazuh is operational
- [x] Wazuh agent is connected to Windows
- [x] Windows Event Logs are visible in the SIEM
- [x] Sysmon is installed and generating telemetry
- [x] At least three controlled security scenarios are generated
- [x] At least three detections are documented
- [x] At least two investigations are completed
- [x] MITRE ATT&CK techniques are mapped where supported by evidence
- [x] Screenshots and evidence are organised
- [x] Final lessons learned are written

## Final Project Notes

- [Learning log and lessons learned](./notes/learning-log.md)
- [Interview-ready project summary](./INTERVIEW-SUMMARY.md)
- [Screenshot evidence index](./screenshots/README.md)

Direct Kali-to-Windows communication was verified successfully with 4/4 ICMP replies and 0% packet loss. The first version of Project 1 is complete: three controlled scenarios, three detections, three investigations, organised evidence, lessons learned, troubleshooting notes, and an interview-ready summary.

## Safety and Scope

All testing in this project is limited to systems and virtual machines that I own or control. The lab is intended for defensive learning, monitoring, detection, and incident-response practice.
