# Investigation 01 — Controlled Failed-Login Burst

**Date:** 8 October 2026  
**Affected host:** `Windows-Host`  
**Tested accounts:** `SOC-Lab-Test`, `SOC-Lab-Test2` (mixed-account test)  
**Disposition:** Benign Positive (authorised lab test)

## Alert and scope

The test generated three deliberately failed Windows sign-ins and produced a custom Wazuh level-10 alert, rule `100101`, at **16:47:18** local dashboard time. The rule description indicated three failed logins against the same account within 60 seconds.

The earlier standalone Wazuh rule `60122` detects individual failures. It was used as the prerequisite for the custom correlation rule.

## Investigation workflow

### Validate
- Confirmed Windows Security Event ID `4625`.
- Verified failed-login `status: 0xC000006D`, `subStatus: 0xC000006A` (incorrect password).
- Verified Wazuh rule `100101` (level 10), `rule.frequency: 3`, and the `previous_output` field containing related event data.

### Identify
- Target account: `SOC-Lab-Test`, specifically created for authorised testing.
- Endpoint: `Windows-Host`.
- Event's recorded source IP: `127.0.0.1` (local loopback).
- Agent IP: `192.168.56.1` (agent endpoint; not the attacker/source IP field).
- Logon Type: `2`, local interactive login.

### Correlate
- Three closely spaced failures were intentionally generated in the lab.
- A custom pattern alert appeared after Wazuh Manager was restarted to load the new rule.
- Later, a single isolated failed login at **16:55:28** triggered `60122`; no new `100101` appeared in the reviewed time range.
- **Mixed-account test (17:18):** `60122` events at `17:18:01.232` and `17:18:03.330` were verified as targeting `SOC-Lab-Test`. The third `60122` event at `17:18:07.360` targeted `SOC-Lab-Test2`. All three were interactive (Type 2), source `127.0.0.1`, substatus `0xC000006A`, and occurred within about six seconds. A `rule.id:100101` search returned no results in the relevant 15-minute window.

### Scope
No external source or compromise was established by the reviewed local interactive login evidence. A network/RDP brute-force scenario was **not** tested. No successful compromised login or malicious post-authentication activity was demonstrated.

### Classify
**Benign Positive**: alerts correctly reflected the authorised test activity. For detection-quality assessment, the burst test is a true-positive match for the modelled behaviour, not a real-world confirmed attack.

## MITRE ATT&CK

**T1110 — Brute Force** is the mapping configured in the detection rule, reflecting repeated credential guesses. This mapping is not an assertion that an actual adversary was present.

## Lessons learned

1. Event ID `4625` indicates failure; the status/substatus explain why.
2. Logon Type 2 indicates local interactive sign-in; Type 3 network; Type 10 remote interactive.
3. A Wazuh alert's `rule.id` is different from Windows `data.win.system.eventID`.
4. Correlation thresholds help reduce noise, but legitimate password mistakes can generate the same pattern.
5. Verify positive and negative test results, not just that the service is running.

## Remaining tasks

- Commit labelled Wazuh screenshot evidence.
- Mixed-account 2+1 case tested; next test three consecutive failures for `SOC-Lab-Test2` and additional source-IP/timing edge cases.
- Review whether the rule threshold/source grouping should be tuned.
- Finalize interview-style narrative and project summary.

This report is deliberately limited to the evidence actually observed in the lab.
