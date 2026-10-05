# Investigation 01: Failed Local Authentication

## Executive Summary

A controlled failed Windows sign-in was generated on the monitored Windows endpoint to validate authentication monitoring and practise Tier 1 SOC triage. Windows recorded Security Event ID 4625 and Wazuh raised rule 60122 at level 5 with the description `Logon Failure - Unknown user or bad password`.

The failed sign-in was followed approximately four seconds later by Windows Security Event ID 4624 showing a successful workstation unlock. The failed event originated locally from `127.0.0.1`, used interactive logon type 2, and the event substatus `0xc0000380` was consistent with the deliberately incorrect PIN used during the test.

The activity was therefore classified as a **Benign Positive**. The detection correctly identified a real authentication failure, but the surrounding context showed no evidence of malicious activity or a brute-force attempt.

## Alert Details

- **Alert name:** Logon Failure - Unknown user or bad password
- **Date:** 5 October 2026
- **Failed-event time:** approximately 20:23:27 local time
- **Affected host:** `Windows-Host` / `LAPTOP-C7OPSS6H`
- **Endpoint IP:** `192.168.56.1`
- **Source IP:** `127.0.0.1`
- **Windows Event ID:** `4625`
- **Wazuh rule ID:** `60122`
- **Wazuh rule level:** `5`
- **Logon type:** `2` - interactive/local sign-in
- **Authentication package:** `Negotiate`
- **Logon process:** `User32`
- **Process:** `C:\\Windows\\System32\\svchost.exe`
- **Status:** `0xc000006d`
- **Substatus:** `0xc0000380`

## Initial Hypothesis

A failed interactive sign-in could represent a legitimate user entering an incorrect credential, a misconfiguration, or suspicious credential-access activity. The alert required context before deciding whether escalation was necessary.

## Data Sources Reviewed

- [x] Windows Security Logs
- [x] Wazuh / SIEM
- [ ] Sysmon
- [ ] Network telemetry
- [ ] Other

## Investigation Timeline

| Time | Event | Evidence | Analyst interpretation |
| --- | --- | --- | --- |
| ~20:23:27 | Failed local sign-in | Windows Event ID 4625; Wazuh rule 60122, level 5 | Real authentication failure requiring triage |
| ~20:23:30 | Successful workstation unlock | Windows Event ID 4624; logon type 7 | Successful legitimate unlock shortly after the failed attempt |

The two events occurred only a few seconds apart.

## Investigation Steps

### 1. Validate the alert

The Wazuh alert was validated against the underlying Windows Security event. Event ID 4625 was present in the local Windows Security log and in Wazuh, confirming that the alert was based on genuine endpoint telemetry.

### 2. Identify the affected asset

The event occurred on `Windows-Host` (`LAPTOP-C7OPSS6H`) at `192.168.56.1`. The source address was `127.0.0.1`, indicating the attempt originated locally on the same endpoint rather than from a remote host.

### 3. Review related activity

A Windows Event ID 4624 was observed approximately four seconds after the failed event. The successful event used logon type 7, which represents a workstation unlock. This matched the controlled test sequence: one incorrect PIN followed by a correct sign-in.

### 4. Determine scope

Only one controlled failed authentication was generated. No repeated failures, remote source addresses, or wider signs of credential attack were observed during this test.

### 5. Classify the incident

**Benign Positive.**

The alert correctly detected a real failed authentication event, so it was not a false detection. However, the event was expected and deliberately generated as part of the lab.

## Indicators / Relevant Artefacts

| Type | Value | Notes |
| --- | --- | --- |
| Host | `LAPTOP-C7OPSS6H` | Monitored Windows endpoint |
| Endpoint IP | `192.168.56.1` | Wazuh agent IP |
| Source IP | `127.0.0.1` | Localhost; activity originated on the endpoint |
| Event ID | `4625` | Failed logon |
| Related Event ID | `4624` | Successful logon / workstation unlock |
| Process | `C:\\Windows\\System32\\svchost.exe` | Recorded in failed-event telemetry |

## MITRE ATT&CK Mapping

No project-specific MITRE ATT&CK technique is assigned to this single benign failed sign-in.

Wazuh automatically associated the alert with **T1531 - Account Access Removal**, but the observed behaviour did not involve removing or inhibiting account access, so that mapping was not adopted for this investigation. A future repeated credential-guessing scenario would be evaluated separately for techniques such as brute force only if the evidence supports that behaviour.

## Findings

The alert was caused by one deliberately incorrect Windows sign-in attempt. The event was local, interactive, and immediately followed by a successful workstation unlock. There was no evidence of repeated password guessing, a remote source, lateral movement, or other malicious follow-on activity.

## Recommended Response

For this controlled lab event, no remediation or escalation is required.

In a real SOC environment, an analyst should compare the event with surrounding authentication activity, check for repeated failures, review source addresses and affected accounts, and escalate if the pattern suggests credential guessing or unauthorised access.

## Final Verdict

- **Classification:** Benign Positive
- **Investigation severity:** Low
- **Wazuh alert level:** 5
- **Confidence:** High
- **Escalation:** No

## Evidence

Evidence captured during the lab includes:

- Windows Event Viewer showing Security Event ID 4625.
- Wazuh Threat Hunting showing rule 60122, level 5, for the failed authentication.
- Wazuh event details showing local source `127.0.0.1`, logon type 2, status/substatus values, and the Windows Security channel.
- A related Windows Event ID 4624 showing a successful workstation unlock shortly afterwards.

Screenshots containing account email information should be redacted before being committed to a public repository.

## Lessons Learned

This investigation demonstrated that an alert should not be treated as malicious solely because a SIEM triggered. The underlying Windows event, source, logon type, timing, related activity, and user context all need to be correlated before deciding whether escalation is necessary.

It also demonstrated the difference between a **false positive** and a **benign positive**: the detection was technically correct, but the activity itself was expected and harmless.
