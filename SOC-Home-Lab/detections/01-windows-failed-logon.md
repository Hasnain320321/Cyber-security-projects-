# Detection 01: Windows Failed Logon

## Purpose

Detect Windows authentication failures so that an analyst can identify invalid sign-in attempts and decide whether they are benign mistakes or part of suspicious credential activity.

## Threat / Behaviour

Failed logons are common and are not automatically malicious. They become more concerning when they are repeated, originate from unexpected sources, target multiple accounts, or are followed by other suspicious activity.

## Data Source

- Windows Security Log
- Wazuh

## Detection Logic

The lab validated Windows Security **Event ID 4625**, which represents a failed account logon.

Wazuh matched the event using:

- **Rule ID:** `60122`
- **Rule level:** `5`
- **Rule description:** `Logon Failure - Unknown user or bad password`

Threat Hunting validation filter:

```text
agent.name: Windows-Host
data.win.system.channel: Security
data.win.system.eventID: 4625
```

## Trigger Conditions

The detection fires when the monitored Windows endpoint records a Security Event ID 4625 that is ingested and matched by the relevant Wazuh rule.

## MITRE ATT&CK Mapping

No project-specific ATT&CK technique is assigned to the single benign failed-login test.

The Wazuh rule displayed an automatic mapping to T1531, but that technique did not match the observed behaviour and was therefore not adopted in the analysis.

## Validation

The detection was safely tested by entering one deliberately incorrect Windows Hello PIN on a Windows endpoint owned and controlled by the lab operator.

Windows generated Event ID 4625, and Wazuh ingested the event and raised rule 60122 at level 5.

## Expected Evidence

- **Host:** `Windows-Host`
- **Endpoint IP:** `192.168.56.1`
- **Source IP:** `127.0.0.1` for the controlled local test
- **Event ID:** `4625`
- **Logon type:** `2`
- **Wazuh rule ID:** `60122`
- **Wazuh level:** `5`

## False / Benign Positives

Legitimate causes can include:

- A user mistyping a password or PIN
- A user forgetting changed credentials
- Cached or stale credentials
- Misconfigured services or scheduled tasks

## Triage Steps

1. Validate the underlying Windows Event ID 4625.
2. Identify the affected host and account.
3. Check the source address and logon type.
4. Count the number of failures and determine the time window.
5. Look for successful logons immediately after the failures.
6. Review whether other accounts or hosts are involved.
7. Decide whether the activity is expected, suspicious, or malicious.
8. Escalate only when the evidence supports it.

## Response Recommendations

For an isolated expected failure, no action may be required.

For suspicious repeated failures, review the source, affected accounts, successful follow-on logons, and broader endpoint/network telemetry before considering credential reset, source blocking, endpoint isolation, or escalation.

## Result

- **Classification:** Benign Positive
- **Severity:** Low investigation severity / Wazuh level 5
- **Escalation required:** No

## Lessons Learned

A failed-logon alert is a starting point for investigation rather than proof of an attack. Context, frequency, source, logon type, and related successful authentications determine whether the activity should be escalated.
