# Detection: [Detection Name]

## Purpose

Describe the behaviour this detection is intended to identify.

## Threat / Behaviour

Explain why the activity could be suspicious or malicious.

## Data Source

Examples:

- Windows Security Log
- Sysmon
- Wazuh
- Network telemetry

## Detection Logic

Document the query, rule, filter, threshold, or event IDs used.

```text
Add rule or query here
```

## Trigger Conditions

Explain exactly what must occur for the alert to fire.

## MITRE ATT&CK Mapping

- **Tactic:**
- **Technique:**
- **Technique ID:**

## Validation

Describe how the detection was safely tested in the lab.

## Expected Evidence

- Host:
- User:
- Source IP:
- Destination:
- Process:
- Event ID:
- Timestamp:

## False Positives

List legitimate behaviour that might trigger this detection.

## Triage Steps

1. Validate the alert.
2. Identify the affected host and user.
3. Review related events around the same time.
4. Look for follow-on activity.
5. Determine whether the activity is expected.
6. Classify the alert.

## Response Recommendations

Document what should happen if the alert is confirmed malicious.

## Result

- **Classification:** True Positive / False Positive / Benign Positive / Undetermined
- **Severity:**
- **Escalation required:** Yes / No

## Lessons Learned

What did this detection teach you?
