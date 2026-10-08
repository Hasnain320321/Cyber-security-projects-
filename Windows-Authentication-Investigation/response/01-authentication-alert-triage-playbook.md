# Windows Authentication Alert — SOC Triage & Response Playbook

**Scope:** Windows Event ID 4625 (failed logon), Event ID 4624 (successful logon), Wazuh rule 60122 (individual failure) and lab rule 100101 (correlated failures). This is a **defensive decision guide**, not a claim that containment was performed in the lab.

## 1. Validate the alert

- Confirm event provider and type. Do not confuse Windows `data.win.system.eventID` with Wazuh `rule.id`.
- Record host, username, source IP, Logon Type, accurate time, status/substatus, and Wazuh severity.
- Differentiate `agent.ip` (where the monitoring agent lives) from the source address inside the Windows logon event.
- Investigate errors caused by service accounts, scheduled tasks, stale credentials or legitimate typing mistakes.

## 2. Scope the authentication pattern

1. How many failures? Over what window? Is the rate unusual for this account and host?
2. Are they targeting one username or many? Are all attempts from the same source?
3. Are any **4624** successes present near the failures? Do the account, source, host and Logon Type actually match?
4. Which account was targeted: local, domain, administrator, service, or high-value identity?
5. What happened **after** any success (new processes, PowerShell or CMD, privileged logons, lateral connections, file changes)?
6. Could the source be an owned virtual machine, internal proxy, loopback or legitimate endpoint?

### Quick event guide

| Event / code | Meaning |
| --- | --- |
| Windows 4625 | Failed authentication |
| Windows 4624 | Successful authentication |
| Status `0xC000006D` | Authentication failed |
| Substatus `0xC000006A` | Wrong password |
| Logon Type 2 | Interactive (local) |
| Logon Type 3 | Network |
| Logon Type 7 | Unlock |
| Logon Type 10 | RemoteInteractive (often RDP) |
| Wazuh 60122 | Individual failed login alert |
| Wazuh 100101 | Three correlated failures within 60 seconds for one username (sensitive lab rule) |

## 3. Classify on evidence

- **Expected / Benign Positive:** Detection correctly describes real activity that was authorised, such as a documented test or user password mistake.
- **Suspicious / Needs escalation:** Unknown source or account, repeated high-rate guesses, unexpected success, or concerning follow-on execution.
- **Confirmed unauthorised activity:** Evidence of account misuse or compromise, supported by relevant logs, owner confirmation or additional corroboration.
- **False Positive:** Detection did not correctly match the actual behaviour or event type — don't confuse this with a genuine but harmless authentication pattern.

**A Wazuh rule level or MITRE tag is not a compromise verdict.**

## 4. Recommended response if malicious activity is supported

Follow approved organisational procedures and coordinate with the incident lead. Depending on circumstances:

1. Preserve raw log evidence and timestamps, plus relevant alerts and endpoint telemetry.
2. Escalate suspected credential attacks or unexpected successful authentications.
3. Confirm identity-owner actions and consider a credential reset and token/session revocation.
4. Apply targeted containment, access blocks, MFA enforcement or conditional access updates after assessing business impact.
5. Examine any post-login persistence or lateral movement indicators.
6. Document the outcome and update detections to reduce repeat noise.

**Do not lock out accounts, delete data or block sources solely because a low-threshold lab rule fired.**

## 5. Tuning considerations

Our lab threshold of `frequency=3` and `timeframe=60` is intentionally low. For production, baseline account type, legitimate mistakes and environment; consider source address, rate, distinct targeted usernames, successful logons, privileged identities, lockout signals, and exclusions with documented justification. Test both positive and negative cases after rule changes.

## Applied lab outcome

Two controlled investigative scenarios were documented:
- [Investigation 01: four detection validation tests](../investigations/01-controlled-login-attempts.md)
- [Investigation 02: two failed logins followed by success](../investigations/02-failed-then-successful-login.md)

No account compromise was established in the reviewed authorised test.
