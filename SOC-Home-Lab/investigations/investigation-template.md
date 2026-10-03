# Incident Investigation: [Incident Name]

## Executive Summary

Write a short summary of what triggered the investigation, what was found, and the final verdict.

## Alert Details

- **Alert name:**
- **Date / time:**
- **Affected host:**
- **User:**
- **Source IP:**
- **Destination IP:**
- **Severity:**

## Initial Hypothesis

What could this activity represent?

## Data Sources Reviewed

- [ ] Windows Security Logs
- [ ] Sysmon
- [ ] Wazuh / SIEM
- [ ] Network telemetry
- [ ] Other:

## Investigation Timeline

| Time | Event | Evidence | Analyst interpretation |
| --- | --- | --- | --- |
| | | | |

## Investigation Steps

### 1. Validate the alert

Explain why the alert fired and whether the underlying telemetry is valid.

### 2. Identify the affected asset

Record the host, user, IP address, and relevant process information.

### 3. Review related activity

Look before and after the alert for connected events.

### 4. Determine scope

Was one account or host involved, or were there other affected systems?

### 5. Classify the incident

State whether the activity is:

- True Positive
- False Positive
- Benign Positive
- Undetermined

## Indicators of Compromise / Indicators

| Type | Value | Notes |
| --- | --- | --- |
| IP | | |
| Domain | | |
| Hash | | |
| Account | | |
| Process | | |

## MITRE ATT&CK Mapping

- **Tactic:**
- **Technique:**
- **Technique ID:**

## Findings

Describe what happened using evidence rather than assumptions.

## Recommended Response

Examples:

- Reset affected credentials
- Isolate endpoint
- Block malicious indicator
- Review additional logs
- Escalate to Tier 2 / Incident Response
- Patch or harden the affected system

Only include actions relevant to the actual investigation.

## Final Verdict

- **Classification:**
- **Severity:**
- **Confidence:**
- **Escalation:** Yes / No

## Evidence

Add links to screenshots or other evidence stored in the repository.

## Lessons Learned

Explain what you learned and what you would improve next time.
