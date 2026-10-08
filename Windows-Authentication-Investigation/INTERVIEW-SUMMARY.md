# Project 2 — Interview Summary

## 30-second explanation

I built and validated a custom Wazuh rule for repeated Windows authentication failures using Windows Security Event ID 4625 and a same-username three-event threshold within 60 seconds. I tested it against two local standard-user accounts with two positive and two negative scenarios. I then investigated two failed logins followed by a successful Event ID 4624 login for the same account, checking source, Logon Type and nearby process alerts. All activity was authorised in my lab; I documented the evidence, limitations and recommended SOC response.

## What I actually built

- Test accounts: `SOC-Lab-Test` and `SOC-Lab-Test2`.
- Data source: Windows Security log events ingested by the Wazuh agent (`Windows-Host`).
- Parent detection: `60122` (failed logon).
- Custom rule: `100101`, Level 10, `frequency=3`, `timeframe=60`, `same_field=win.eventdata.targetUserName`.
- ATT&CK mapping: T1110 — Brute Force (detection mapping, not proof of an actual attacker).

## Tests completed on 8 October 2026

| Scenario | Expected | Observed |
| --- | --- | --- |
| Three wrong passwords for account 1 | `100101` | Alert at 16:47:18; level 10 and `rule.frequency: 3` |
| One wrong password for account 1 | Only `60122` | `60122` at 16:55:28, no new `100101` seen |
| Two wrong passwords for account 1 + one for account 2 | `60122` events only | Three `60122` events at 17:18:01/:03/:07; no `100101` seen |
| Three wrong passwords for account 2 | `100101` | Alert at 17:30:13; expanded event target `SOC-Lab-Test2` |

## Investigation 02 — Failed followed by successful login

Two 4625 events at 18:01:21 and 18:01:26 targeted `SOC-Lab-Test2`; a 4624 at 18:01:33 successfully logged the same account in using Logon Type 2. A separate Microsoft-account Logon Type 7 unlock was excluded. McAfee WebAdvisor BrowserHost.exe appeared in process-alert telemetry around 18:01:47, but we did not establish that the test-account session initiated it; no compromise was concluded. See [Investigation 02](./investigations/02-failed-then-successful-login.md).

## How I investigated

**Validate -> Identify -> Correlate -> Scope -> Classify**

1. Validated Windows Event ID 4625 and status/substatus; `0xC000006A` indicated a bad password.
2. Identified the affected user, endpoint and logon type.
3. Distinguished the authentication-event source IP `127.0.0.1` from Wazuh agent IP `192.168.56.1`.
4. Correlated the failures by time and target username.
5. Classified the intentionally created alerts as **Benign Positives** operationally, while recognising that the positive scenarios were successful detection tests.

## What I'd do during a real incident

Check the attempted usernames, originating IP and device, logon types, event timeline, any successful logins (4624), account lockouts and follow-on activity. Assess whether attempts are expected, automated, external or potentially compromised. Escalate and recommend containment such as credential reset or session revocation if the evidence establishes risk.

## Limitations I would mention

- The test involved local interactive logons (Type 2), not a real remote attacker.
- The threshold is deliberately low and may flag ordinary typing errors.
- The rule groups usernames, not necessarily source IP addresses.
- Boundary-window behaviour, account case differences, lockout handling, RDP/network logons and repeat bursts were not fully tested.
- A Wazuh Level 10 alert is a signal to investigate; it is not confirmation of compromise.
- All 19 evidence screenshots have been committed within Project 2 and grouped in the [visual evidence index](./screenshots/README.md).

## Response and practical outcome

See the [SOC triage/response playbook](./response/01-authentication-alert-triage-playbook.md) and [final portfolio summary](./FINAL-PROJECT-SUMMARY.md). I did not perform real-world containment; the report recommends actions that would be appropriate if malicious activity were substantiated.

## Visual proof for interviews

- [Detection rule 100101](./screenshots/04-custom-rule-100101.png)
- [Positive alert for first test account](./screenshots/06-positive-100101-alert.png)
- [Mixed-account negative test](./screenshots/13-mixed-account-no-correlation.png)
- [Positive alert for second test account](./screenshots/14-second-account-positive-alert.png)
- [Complete 19-image evidence index for Investigation 01](./screenshots/README.md)
- [Investigation 02 transcribed event timeline](./evidence/02-authentication-timeline.md) (original PNGs not in repository)

## Likely interview questions

**Why have both positive and negative tests?**  
Positive testing checks that suspicious patterns trigger; negative testing checks that ordinary events do not generate needless higher-severity alerts.

**What is a benign positive?**  
A correctly detected event or pattern that turns out to be expected or harmless in context.

**What is the difference between Event ID 4625 and Wazuh rule 100101?**  
4625 is a Windows failed-logon event. 100101 is custom Wazuh logic correlating multiple failed-logon events.

**Why use a same-username field?**  
To avoid combining unrelated account failures into a single three-failure threshold.

**Does T1110 prove an attack?**  
No. It describes the behaviour the detection is designed to identify.
