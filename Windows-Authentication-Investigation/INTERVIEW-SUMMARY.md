# Project 2 — Interview-Ready Summary

**Project:** Windows Authentication Investigation and Wazuh Brute-Force Detection  
**Status:** Complete — first portfolio version (8 October 2026)  
**Boundary:** Authorised local test activity; no actual compromise or remote attack was demonstrated.

## 30-Second Version

I built and validated a custom Wazuh detection for repeated Windows authentication failures. I used Windows Security Event ID 4625 as input, Wazuh rule 60122 as the individual-failure match, and wrote rule 100101 to correlate three failures against the same username within 60 seconds. I tested two positive scenarios and two negative scenarios using two local test accounts. I then correlated two failed sign-ins with a successful Event ID 4624 sign-in and examined adjacent process alerts. I documented my findings, screenshots, limitations, and a response playbook in GitHub.

## 60-Second Version

My lab runs Wazuh 4.14.8 in VirtualBox and monitors a Windows endpoint using the Wazuh agent. Sysmon provides process telemetry.

First I created two local standard-user test accounts, SOC-Lab-Test and SOC-Lab-Test2. I studied 4625 failures and created Wazuh rule 100101 in local_rules.xml. It looks for multiple events matching Wazuh rule 60122, within 60 seconds, grouped by the target username. I confirmed the manager restarted successfully and the custom rule generated a level-10 alert.

I validated the logic four ways: three failures for account one triggered it; one isolated failure did not; two failures for account one plus one for account two did not; and three failures for account two triggered it. That showed why positive and negative testing both matter.

In a second investigation, I found two 4625 failures for SOC-Lab-Test2 at 18:01:21 and 18:01:26, followed by a 4624 success at 18:01:33 for the same account. It was a local interactive login (Type 2) from the loopback address in the event. I checked nearby CMD-related alerts but did not assume they were created by that user; one expanded event showed McAfee WebAdvisor BrowserHost.exe. Since the sign-in was an authorised lab test, I classified the authentication activity as a benign positive and documented what would be checked in a real incident.

My workflow was **Validate -> Identify -> Correlate -> Scope -> Classify -> Recommend response**.

## Technical Architecture

```text
Windows endpoint (Windows-Host; lab IP 192.168.56.1)
  |-- Security Event Log: 4625 / 4624
  |-- Sysmon: Event ID 1 (process creation)
  |-- Wazuh Agent
             |
             | Host-only lab network
             v
Wazuh 4.14.8 VM (192.168.56.101)
  |-- Manager and correlation rules
  |-- Wazuh Threat Hunting / alert dashboard
  |-- local_rules.xml: custom rule 100101
```

The lab infrastructure was established in Project 1; **Project 2 is a separate authentication-analysis/detection project**. The agent IP is not automatically the logon event's source IP.

## Scenario 1 — Detection Engineering: Brute-Force-Like Failure Pattern

### What problem did you try to solve?

Individual failed logins are common. I wanted a more meaningful alert when several failures were aimed at one account within a short interval, without incorrectly combining failures from other accounts.

### What telemetry did you use?

- Windows Security Event ID `4625` for failed logon.
- Wazuh rule `60122` for an individual authentication failure.
- Targeted account field `win.eventdata.targetUserName`.
- Source and session details: IP, Logon Type, substatus, device, timestamps.

### How did you write the detection?

I added custom rule `100101` under `local_rules.xml`, preserving Project 1's separate PowerShell rule `100100`.

```xml
<group name="windows,authentication_failed,custom_detection,">
  <rule id="100101" level="10" frequency="3" timeframe="60">
    <if_matched_sid>60122</if_matched_sid>
    <same_field>win.eventdata.targetUserName</same_field>
    <description>Possible brute-force activity: 3 failed logins against the same account within 60 seconds</description>
    <mitre><id>T1110</id></mitre>
    <group>brute_force,authentication_failed,</group>
  </rule>
</group>
```

### How did you test it?

| Scenario | Expected | Observed |
| --- | --- | --- |
| Three wrong passwords against SOC-Lab-Test | Level-10 custom alert | Rule 100101 at 16:47:18 |
| One isolated wrong password | Individual rule 60122, not custom alert | Rule 60122 at 16:55:28; no new 100101 in inspected window |
| Two failures for account one + one for account two | No custom alert | Three 60122 events, no new 100101 in inspected window |
| Three failures for SOC-Lab-Test2 | Custom alert should work for another username | Rule 100101 at 17:30:13; account two confirmed |

### Verdict and ATT&CK

The detections correctly reflected deliberately generated account failures. **Benign Positive** as SOC disposition. As rule testing, the positive cases confirmed the behaviour could be detected. MITRE ATT&CK **T1110 (Brute Force)** describes the detection hypothesis; it does **not** establish malicious intent.

Evidence: [XML rule](./screenshots/04-custom-rule-100101.png), [first positive alert](./screenshots/06-positive-100101-alert.png), [mixed-account negative](./screenshots/13-mixed-account-no-correlation.png), [second-account positive](./screenshots/14-second-account-positive-alert.png), and the [full 26-image evidence index](./screenshots/README.md).

## Scenario 2 — Failed Logins Followed by Successful Login

### What happened?

The account `SOC-Lab-Test2` had:

- **18:01:21** — Windows Event ID 4625, failure.
- **18:01:26** — Windows Event ID 4625, failure.
- **18:01:33** — Windows Event ID 4624, success.

The events were filtered by targeted username, rather than linked merely because of adjacent timestamps.

### What did you verify?

The successful event matched `SOC-Lab-Test2`, Logon Type `2` (interactive), source IP `127.0.0.1` (loopback) and Wazuh rule `60118`. We separately excluded a Microsoft-account Logon Type `7` event, which represented a workstation unlock for a different identity.

### What happened after the sign-in?

The nearby Wazuh alerts included rules `92052` and `92032` around 18:01:47, with command-shell-related descriptions. The expanded process fields showed McAfee WebAdvisor's `BrowserHost.exe`. **We did not prove that the test-account session started that process** and did not treat it as proof of attacker activity. Another 4625 event at 18:01:48 referenced Edge WebView2; its target account was not established in the reviewed screenshot fields.

### Verdict

**Benign Positive for the controlled authentication sequence**, without evidence of a real compromise. The neighbouring process alerts were treated as separate context with attribution limits, rather than overclaimed as malicious or fully exonerated.

Evidence: [Investigation 02 write-up](./investigations/02-failed-then-successful-login.md), [two observed failure alerts](./screenshots/20-two-failures-targeted-account.png), [success alert](./screenshots/17-test-account-success-list.png), [local Type 2 context](./screenshots/18-success-logon-type-and-ip.png), [target username](./screenshots/19-success-target-username.png), and the [timeline](./evidence/02-authentication-timeline.md). **Seven Investigation 02 PNGs are on GitHub**; McAfee process-detail image 25 remains missing. The cropped failure list alone does not prove username without the query context.

## Investigation Workflow I Can Explain

1. **Validate:** Check original Windows Event ID, Wazuh rule, severity, time and status/substatus.
2. **Identify:** Account, source IP vs agent IP, logon type, device and user.
3. **Correlate:** Match account and session context across events, then inspect the chronological sequence.
4. **Scope:** Review how many attempts, successful logins, adjacent process/network events, and exclusions.
5. **Classify:** Benign Positive, True Positive, False Positive or Undetermined according to observed evidence and context.
6. **Recommend response:** Preserve evidence and escalate/contain only when appropriate.

## Common Interview Questions and Model Answers

### 1. What is the difference between Event ID 4625 and Wazuh rule 60122?

4625 is the Windows Security Event ID for a failed logon. 60122 is the Wazuh detection rule that matched and raised an alert for it in this lab.

### 2. What is different about your custom rule 100101?

It correlates repeated individual failures against the **same target username** within the configured 60-second interval, instead of giving each failed event a separate higher-severity classification.

### 3. Why did you test more than one account?

To check that the rule follows the targeted username field, rather than accidentally being limited to one named account.

### 4. Why test 2 failures on one account plus 1 on another?

The rule should not combine the three failures across different accounts. Our test produced three individual 60122 alerts but no new 100101 alert in the reviewed period.

### 5. Why is one failed login important as a negative test?

A single mistyped password is common. Triggering the higher-severity alert for every one-off mistake would increase analyst noise and alert fatigue.

### 6. Does three failed logins and a later success mean compromise?

No. Confirm account, source, device, logon type, timings and post-login actions; the user may have mistyped their password and then authenticated legitimately.

### 7. What is a benign positive versus a false positive?

Benign positive: real correctly detected behaviour that was authorised or harmless in context. False positive: the detection incorrectly identified behaviour or misfired.

### 8. What does Logon Type 7 mean?

Unlocking an existing Windows session. It should not automatically be counted as the same kind of fresh logon as Type 2.

### 9. What does substatus 0xC000006A mean?

Incorrect password. Event ID 4625 tells us login failed; the substatus helps explain why.

### 10. Why did you examine Sysmon alerts around the successful login?

An attacker might execute tools after gaining access, but events merely occurring near a login do **not** prove the same user created them. Process user/session and parent process evidence would be needed.

### 11. Why does T1110 appear on a benign positive?

T1110 is the ATT&CK label for brute-force-like behaviour. It reflects the rule's detection logic, not a confirmed hostile operator.

### 12. What would you change for a real organisation?

Baseline normal sign-in failures, tune thresholds, assess source IP and identity scope, look for successful authentication after failures and privileged accounts, investigate lockouts, and test remote/network scenarios. Never assume a three-failure threshold is production-ready.

## Response, Evidence and Limitations

- [Defensive response and escalation playbook](./response/01-authentication-alert-triage-playbook.md)
- [Detection design and four tests](./detections/01-brute-force-correlation.md)
- [Investigation 01](./investigations/01-controlled-login-attempts.md)
- [Investigation 02](./investigations/02-failed-then-successful-login.md)
- [Project 2 evidence index (26 retained PNGs)](./screenshots/README.md)
- [Project 2 final summary](./FINAL-PROJECT-SUMMARY.md)

**Limits:** Testing used local interactive logons, not network/RDP brute-force; threshold deliberately low; session attribution for nearby process alerts incomplete; Seven Investigation 02 images uploaded; McAfee process-detail image missing; the cropped failure rows omit the username filter. Interview claims must stay within these bounds.

## 5 Points to Remember in an Interview

- I configured and tested a custom Wazuh correlation rule.
- I tested the same rule against two different accounts.
- I used both positive and negative tests.
- I correlated Windows logon failures and a subsequent success by username.
- I investigated nearby alerts but did not equate alert severity or temporal proximity with proof of compromise.
