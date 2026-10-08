# Project 2 — Learning Review and SOC Flashcards

**Project:** Windows Authentication Investigation with Wazuh  
**Date:** 8 October 2026  
**Study goal:** Explain the workflow from memory rather than memorising every filter or command.

## Five memory anchors

1. **4625 = failed login; 4624 = successful login.** Know the outcome before drawing a conclusion.
2. **Account → source → logon type → attempts → device → activity after login.** This is the investigation checklist.
3. **Rule 60122 detects individual failures; rule 100101 correlates a same-account burst.** The lab detection used three failures within 60 seconds.
4. **Positive and negative tests both matter.** We tested three failures against each account, a single failure, and a 2+1 cross-account mixture.
5. **Alert ≠ compromise.** A level or MITRE mapping starts an investigation; attribution and post-login evidence determine the conclusion.

## Twenty daily recall cards

| # | Question | Answer |
| --- | --- | --- |
| 1 | What is Windows Event ID 4625? | Failed logon. |
| 2 | What is Windows Event ID 4624? | Successful logon. |
| 3 | What does substatus 0xC000006A mean? | Incorrect password. |
| 4 | What does status 0xC000006D indicate? | Authentication failure. |
| 5 | What does Logon Type 2 mean? | Local interactive login. |
| 6 | What does Logon Type 3 mean? | Network logon. |
| 7 | What does Logon Type 7 mean? | Unlock an existing workstation session. |
| 8 | What does Logon Type 10 mean? | RemoteInteractive, commonly RDP. |
| 9 | What does 127.0.0.1 indicate? | Local loopback address. |
| 10 | What is the difference between agent.ip and ipAddress? | Agent IP is the monitored host address; the event source IP is where the logon was recorded as originating. |
| 11 | What does Wazuh rule 60122 detect in this lab? | An individual failed login. |
| 12 | What does custom Wazuh rule 100101 detect? | Correlated failed logins against the same account in a short interval. |
| 13 | What is the lab frequency threshold? | 3 matching failures. |
| 14 | What is the lab timeframe? | 60 seconds. |
| 15 | What does same_field do? | Correlates matching values of a chosen event field, here target username. |
| 16 | What is a positive detection test? | Generate intended suspicious-pattern behaviour and verify it alerts. |
| 17 | What is a negative detection test? | Generate ordinary/nonmatching behaviour and verify it does not create the same correlation alert. |
| 18 | What does benign positive mean? | Real correctly detected activity that is expected or harmless in the investigation context. |
| 19 | Why correlate 4625 with 4624? | To check whether a failed-sign-in pattern was followed by successful authentication of the same account and context. |
| 20 | Why investigate processes after a successful login? | Unexpected activity may add evidence of misuse, but nearby alerts must be attributed to the right user/session before conclusions. |

## Two practice interview prompts

**Prompt 1:** Describe the four tests you performed for Wazuh rule 100101 and why each mattered.

**Prompt 2:** Explain the 18:01:21 → 18:01:26 → 18:01:33 event sequence and why the nearby McAfee alert alone did not prove compromise.

## Answer framework

**Validate → Identify → Correlate → Scope → Classify → Recommend response.**

Refer to the [Project 2 overview](../README.md) and [final summary](../FINAL-PROJECT-SUMMARY.md). This review is a study aid and does not claim that the student has memorised every item yet.
