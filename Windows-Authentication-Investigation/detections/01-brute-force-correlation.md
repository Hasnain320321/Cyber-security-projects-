# Detection 01 — Repeated Windows Failed Logins

**Date tested:** 8 October 2026  
**Status:** Four initial validation scenarios passed in the lab; additional tuning needed.

## Detection hypothesis

A short burst of failed Windows logons against the same account may indicate credential guessing. It can also result from legitimate user error, so the alert is **suspicious pattern evidence**, not proof of compromise.

## Telemetry and precursor

- Windows Security Event ID: `4625`
- Existing Wazuh rule: `60122` — individual failed logon
- Source: Windows endpoint security events ingested by Wazuh agent

## Custom rule as entered into the lab

Located inside `local_rules.xml` without replacing Project 1's custom rule `100100`.

```xml
<!-- Project 2: Windows brute-force detection -->
<group name="windows,authentication_failed,custom_detection,">
  <rule id="100101" level="10" frequency="3" timeframe="60">
    <if_matched_sid>60122</if_matched_sid>
    <same_field>win.eventdata.targetUserName</same_field>
    <description>Possible brute-force activity: 3 failed logins against the same account within 60 seconds</description>
    <mitre>
      <id>T1110</id>
    </mitre>
    <group>brute_force,authentication_failed,</group>
  </rule>
</group>
```

### Logic

- `if_matched_sid`: correlate preceding events matched by rule `60122`.
- `frequency="3"` and `timeframe="60"`: require a burst of matching events within 60 seconds.
- `same_field`: correlate the same targeted username.
- `level="10"`: surface the correlated pattern above the individual level-5 failures.
- `T1110`: intended MITRE ATT&CK mapping (Brute Force). No actual compromise is claimed.

**Lab threshold:** Three failures in 60 seconds is deliberately sensitive for testing and is not a general production recommendation.

## Validation performed

| Test | Input | Expected | Observed | Outcome |
| --- | --- | --- | --- | --- |
| Positive | Three wrong passwords against `SOC-Lab-Test` in quick succession | `100101` alert | Level-10 `100101` at 16:47:18 on 8 Oct 2026; `rule.frequency: 3`; earlier-event `previous_output` | Passed |
| Negative | One wrong password against same account after waiting beyond correlation window | Individual `60122` but no new `100101` | `60122` at 16:55:28; no new `100101` observed in reviewed window | Passed within observed window |
| Mixed accounts | Two incorrect passwords for `SOC-Lab-Test` and one for `SOC-Lab-Test2`, all within seconds | Three `60122` events; no `100101` | `60122` at 17:18:01.232 and 17:18:03.330 (account 1), and at 17:18:07.360 (account 2); no new `100101` in reviewed window | Passed within observed window |
| Second-account positive | Three wrong passwords against `SOC-Lab-Test2` | New `100101` alert associated with second account | Level-10 `100101` at 17:30:13.110 on 8 Oct 2026; expanded `4625` event contained `targetUserName: SOC-Lab-Test2` | Passed |

The Wazuh manager restarted successfully and was reported `active (running)` prior to live testing.

## False-positive and coverage considerations

- A legitimate employee mistyping a password three times can trigger a benign alert.
- Username grouping does not ensure that all attempts came from the same IP.
- Interactive local logons (Type 2) do not validate detection coverage for network logons (Type 3) or RDP (Type 10).
- Mixed-username case (2+1) and independent three-failure second-account test were completed; still test account case variations, timing boundaries, bursts beyond the threshold, lockout behaviour and successful logons (4624).
- Alert severity must not substitute for incident severity or verification.

## Suggested analyst response

Confirm the target username, source, originating device, logon type, counts and time distribution; correlate with successful logins and follow-on account activity. Escalate only when evidence supports an unauthorised attempt or compromise; otherwise document benign findings.

## Evidence — direct links to screenshots

All screenshots are committed under this project's [19-image evidence index](../screenshots/README.md).

| Purpose | Evidence |
| --- | --- |
| Rule configuration | [Custom XML rule 100101](../screenshots/04-custom-rule-100101.png) |
| Manager status after restart | [Wazuh service active](../screenshots/05-manager-active.png) |
| Initial telemetry | [Three individual 60122 events](../screenshots/03-three-individual-failures.png) |
| First positive test | [Level-10 100101 alert](../screenshots/06-positive-100101-alert.png), [correlation details](../screenshots/07-positive-alert-details.png), [T1110 mapping](../screenshots/07a-positive-mitre-mapping.png) |
| Single-failure negative | [Individual 60122 alert](../screenshots/08-negative-60122-alert.png), [target account](../screenshots/09-negative-test-account.png) |
| Mixed-username negative | [Three individual failures](../screenshots/10-mixed-account-three-failures.png), [first username](../screenshots/11-mixed-account-user-one-first.png), [second account](../screenshots/12-mixed-account-user-two.png), [no new 100101](../screenshots/13-mixed-account-no-correlation.png) |
| Second-account positive | [Fresh 100101 alert](../screenshots/14-second-account-positive-alert.png), [target username](../screenshots/15-second-account-alert-user.png) |

![Custom rule 100101 generates a high-severity correlated alert for the controlled positive test](../screenshots/06-positive-100101-alert.png)

The visual results confirm how the rule behaved in these four lab scenarios. They do not prove production readiness or actual malicious activity.
