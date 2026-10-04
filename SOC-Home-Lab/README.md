# SOC Home Lab

**Status:** In progress

## Objective

The purpose of this project is to build a small Security Operations Centre style lab where endpoint and security events can be collected, monitored, detected, and investigated.

The project is designed to demonstrate practical skills relevant to junior SOC Analyst and Cyber Security Analyst roles.

## Planned Architecture

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
          | Sysmon                |
          | Wazuh Agent           |
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

An Ubuntu/Linux VM may be used for the Wazuh server depending on the final lab configuration.

## What This Project Will Demonstrate

- Building an isolated cyber security lab
- Windows endpoint monitoring
- Windows Event Log analysis
- Sysmon telemetry
- SIEM ingestion and alerting
- Basic detection engineering
- Alert triage
- Incident investigation
- MITRE ATT&CK mapping
- Security report writing
- False-positive analysis
- Defensive recommendations

## Planned Detection Scenarios

### 1. Failed Login / Brute-Force Activity

Generate repeated failed login events against a lab account and investigate:

- Username
- Source
- Timestamp
- Number of attempts
- Successful logins after failures
- Event IDs
- Severity
- Recommended response

### 2. Suspicious PowerShell Activity

Generate safe PowerShell activity in the lab and identify the related telemetry.

Investigation will focus on:

- Parent and child processes
- Command line
- User
- Timestamp
- Sysmon events
- Reason the activity may be suspicious
- Possible legitimate explanations

### 3. Network Scanning

Use Kali Linux against the lab Windows machine to generate controlled scan activity.

Investigation will focus on:

- Source IP
- Destination IP
- Ports
- Scan pattern
- SIEM alerts
- Endpoint/network evidence
- MITRE ATT&CK mapping

## Investigation Workflow

For each incident:

```text
Alert
  |
  v
Validate telemetry
  |
  v
Identify user / host / source
  |
  v
Build timeline
  |
  v
Check related events
  |
  v
Classify true positive / false positive
  |
  v
Map to MITRE ATT&CK
  |
  v
Recommend response
  |
  v
Document evidence
```

## Repository Structure

```text
SOC-Home-Lab/
|
|-- README.md
|-- setup/
|   |-- lab-plan.md
|
|-- detections/
|   |-- detection-template.md
|
|-- investigations/
|   |-- investigation-template.md
|
|-- screenshots/
|   |-- README.md
|
|-- notes/
    |-- learning-log.md
```

Additional files will be added as the lab is built.

## Verified Progress Evidence

### Windows endpoint enrolled in Wazuh

The Windows host has been successfully enrolled as a Wazuh agent over the isolated Host-Only network.

- **Agent name:** `Windows-Host`
- **Endpoint IP:** `192.168.56.1`
- **Wazuh manager:** `192.168.56.101`
- **Agent version:** `4.14.8`
- **Status:** **Active**

This confirms that the Windows endpoint is registered with the Wazuh manager and the agent is actively communicating with the SIEM. Sysmon installation and telemetry validation are the next steps.

## Success Criteria

The first version of this project will be considered complete when:

- [ ] Windows VM is running
- [ ] Kali Linux can communicate with the lab endpoint
- [ ] Wazuh is operational
- [x] Wazuh agent is connected to Windows
- [ ] Windows Event Logs are visible in the SIEM
- [ ] Sysmon is installed and generating telemetry
- [ ] At least three controlled security scenarios are generated
- [ ] At least three detections are documented
- [ ] At least two investigations are completed
- [ ] MITRE ATT&CK techniques are mapped
- [ ] Screenshots and evidence are organised
- [ ] Final lessons learned are written

## Safety and Scope

All testing in this project is limited to systems and virtual machines that I own or control. The lab is intended for defensive learning, monitoring, detection, and incident-response practice.
