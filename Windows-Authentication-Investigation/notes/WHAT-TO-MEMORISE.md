# Project 2 — What to Memorise and What to Understand

**Date:** 8 October 2026  
**Project:** Windows Authentication Investigation  
**Study plan:** Read these notes once, answer the flashcards without looking, and practise explaining one event in your own words. You do **not** need to memorise entire PowerShell commands, Wazuh filter syntax or every Windows Event ID.

## Priority 1 — Memorise These Core Facts

### 1. Windows event IDs and substatus

| Item | Meaning | How to recall |
| --- | --- | --- |
| Windows Event ID **4625** | Failed logon | 5 = failure in this learning pair |
| Windows Event ID **4624** | Successful logon | 4 = successful sign-in in this learning pair |
| **0xC000006A** | Wrong password | Explains *why* authentication failed |
| **0xC000006D** | Authentication failure | Overall unsuccessful authentication |
| Wazuh rule **60122** | Individual Windows login failure in this lab | First-level failure alert |
| Wazuh rule **60118** | Windows workstation logon success in this lab | Successful-login alert |
| Custom Wazuh rule **100101** | Correlates three failed logins for the same username within 60 seconds | Our own rule, alert level 10 |

Don't mix up `data.win.system.eventID` (Windows event) with `rule.id` (Wazuh alert rule).

### 2. The four logon types worth knowing

| Type | Meaning |
| --- | --- |
| **2** | Interactive / local Windows login |
| **3** | Network login, e.g. shared network resource |
| **7** | Unlock an existing Windows session |
| **10** | RemoteInteractive login, often Remote Desktop/RDP |

### 3. Your investigation checklist

**Account → Source IP → Logon Type → Number/timing of attempts → Device → What happened after login**

Ask yourself: *Who? Where from? How? How often? Which device? What next?*

### 4. Your detection-engineering rule

- Parent event: `60122` (individual failed login).
- Custom rule: `100101`, Level 10.
- `frequency=3`: count matching failure events.
- `timeframe=60`: within 60 seconds.
- `same_field=win.eventdata.targetUserName`: group by the same target username.
- MITRE ATT&CK `T1110`: brute force **detection mapping**; not proof an attacker was present.
- This three-attempt threshold is intentionally sensitive for **lab validation**, not a recommended production policy.

### 5. The four tests you completed

| Test | Expected outcome | What you saw |
| --- | --- | --- |
| 3 failures on SOC-Lab-Test | Correlation alert | Custom 100101 fired |
| 1 isolated failure | No correlation alert | 60122 only in reviewed window |
| 2 failures account 1 + 1 failure account 2 | No combined alert | 60122 events only; 100101 absent in reviewed window |
| 3 failures on SOC-Lab-Test2 | Correlation alert | Custom 100101 fired |

**Positive testing** proves the rule can alert when the intended pattern occurs. **Negative testing** checks that nonmatching behaviour does not raise the same alert.

### 6. SOC classifications

- **Benign Positive:** Correctly detected real activity that is authorised/harmless in context.
- **False Positive:** Detection incorrectly indicates the specified suspicious behaviour when it did not occur.
- **True Positive (detection validation):** Rule matches the actual targeted behaviour; this does not automatically imply a real criminal attack.
- **Undetermined:** Insufficient evidence; continue investigation or escalate appropriately.

A Level 10 or Level 15 alert is not proof of malicious activity.

## Priority 2 — Understand These Concepts (Do Not Rote-Memorise Everything)

### 7. Failed -> failed -> success timeline

On 8 October 2026 for **SOC-Lab-Test2**:
- **18:01:21:** Event 4625 failure.
- **18:01:26:** Event 4625 failure.
- **18:01:33:** Event 4624 success, Logon Type 2, event source IP `127.0.0.1`.

This was an **authorised local test**. Matching account and timeline are important, but do not by themselves prove account compromise.

### 8. Correlating with other alerts

Sysmon **Event ID 1** records process creation; **Event ID 3** records network connections. After a login, check processes, parent/child relationships, commands, network activity, user identity, session attribution and timing.

A CMD-related Wazuh alert appeared around 18:01:47 and an expanded process record showed **McAfee WebAdvisor BrowserHost.exe**. It was not conclusively attributed to the SOC-Lab-Test2 session. Temporal proximity does **not** prove causation.

### 9. Identifying the IP correctly

- `agent.ip = 192.168.56.1`: IP of the monitored Windows agent in the host-only lab.
- `data.win.eventdata.ipAddress = 127.0.0.1`: source recorded in the specific local sign-in event.
- A different source IP can be legitimate; investigate ownership, location and context instead of assuming attack.

### 10. When to escalate

Escalate according to policy when evidence suggests unauthorised activity, such as repeated attempts from unknown sources, unexpected successes, access to privileged accounts, unusual processes after login, lateral movement or confirmed user denial. Preserve evidence first. Do not lock accounts or reset passwords merely because a low-threshold lab detection fired.

## The Five Anchors to Recall at the Start of Every Lesson

1. **4625 fail, 4624 success.**
2. **Account / IP / logon type / attempts / device / after-login activity.**
3. **60122 single failure; 100101 repeated-failure rule.**
4. **Positive AND negative tests are needed.**
5. **An alert is not proof of compromise.**

## What You Do NOT Need to Memorise

- Full XML syntax for `local_rules.xml` (know what frequency, timeframe and same_field do).
- Every Wazuh field path (know how to locate `targetUserName`, event ID, source and rule ID).
- Large lists of Windows Event IDs not used in your projects.
- Long PowerShell commands or exact process hashes/PIDs.
- The full hexadecimal strings of all status codes: prioritise `0xC000006A` and their meaning; reference the others when needed.

## Daily 10-Minute Study Routine

1. **2 minutes:** Recite the five anchors without notes.
2. **5 minutes:** Answer the [combined Project 1 + Project 2 twenty-card deck](../../study/SOC-FLASHCARDS-PROJECTS-1-2.md).
3. **3 minutes:** Explain one real investigation out loud: detection, fields checked, correlation and final classification.

Don't just repeat a definition. Say **why** it matters for investigation. If you miss a card, review it and try again the next day.

## Short interview-ready answer

"I created Wazuh rule 100101 for repeated Windows failed logins, correlated by username within 60 seconds. I validated it using positive and negative tests against two test accounts. I also investigated two Event 4625 failures followed by an Event 4624 success, checking identity, IP and logon type. The events were authorised lab activity, so the outcome was benign; I documented the alert limitations and how I'd respond to a real case."

## Links

- [Project 2 interview guide](../INTERVIEW-SUMMARY.md)
- [Investigation 02](../investigations/02-failed-then-successful-login.md)
- [Response playbook](../response/01-authentication-alert-triage-playbook.md)
- [Combined 20-card deck](../../study/SOC-FLASHCARDS-PROJECTS-1-2.md)
