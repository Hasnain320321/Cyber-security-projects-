# SOC Daily Flashcards — Project 1 + Project 2

**Deck size: 20** (10 Project 1 + 10 Project 2)  
**Date added:** 8 October 2026  
**Format:** Read a question, answer aloud before revealing/looking at the answer, then mark correct or review.

When you ask for **SOC flashcards**, use this **20-card mixed deck** as the current core review set. Future project topics can rotate into the deck while keeping 20 questions per review session. Learn from your actual GitHub lab work rather than memorising unrelated definitions.

## Project 1 — SOC Home Lab (10 cards)

| # | Question | Answer |
| --- | --- | --- |
| 1 | What does a SIEM do, and which SIEM did you use? | Collects, correlates and helps investigate security logs and alerts. I used Wazuh. |
| 2 | What is the difference between the Wazuh agent and the Wazuh manager? | Agent collects/sends Windows telemetry; manager receives, analyses and produces alerts. |
| 3 | What does Sysmon Event ID 1 record? | Process creation, including image, command line, user and parent process information. |
| 4 | What does Sysmon Event ID 3 record? | Network connection telemetry including process, source/destination IP and ports. |
| 5 | Why look at ParentImage and ParentProcessId? | To understand which process spawned another and assess process lineage. |
| 6 | What does PID stand for, and how did you use it? | Process ID. I matched the PowerShell PID between process-creation and network connection events. |
| 7 | What did custom Wazuh rule 100100 look for? | PowerShell command lines containing Test-NetConnection in the controlled lab. |
| 8 | What did Test-NetConnection prove in your lab? | The detected PowerShell process (PID 15676) made an expected TCP connection to Wazuh 192.168.56.101:443, confirmed by Sysmon Event ID 3. |
| 9 | What is the Project 1 investigation workflow? | Validate -> Identify -> Correlate -> Scope -> Classify. |
| 10 | Why was the PowerShell test a benign positive? | The detection accurately observed activity I deliberately generated in the authorised lab. |

## Project 2 — Windows Authentication Investigation (10 cards)

| # | Question | Answer |
| --- | --- | --- |
| 11 | What is the difference between Windows Events 4625 and 4624? | 4625 = failed logon; 4624 = successful logon. |
| 12 | Which logon types did we learn? | 2 = local interactive; 3 = network; 7 = unlock; 10 = remote interactive/RDP. |
| 13 | What does 0xC000006A mean? | Incorrect password: explains a 4625 failure. |
| 14 | What is the checklist for a failed-login investigation? | Account -> source IP -> logon type -> attempts/timing -> device -> post-login activity. |
| 15 | What does Wazuh rule 60122 represent in our lab? | One failed Windows logon alert. |
| 16 | What does your rule 100101 detect? | Repeated 60122 failures against the same target username, configured for three within 60 seconds. |
| 17 | What do frequency, timeframe and same_field each do? | Required count, time window and matching username grouping. |
| 18 | What did the mixed-account test prove? | Two failures for account one + one for account two did not generate a new correlation alert in the inspected window. |
| 19 | Why correlate failed 4625 attempts with a 4624 success? | To see whether the same account eventually authenticated, then assess source, context and activity after login. |
| 20 | Does a high-severity alert or MITRE mapping prove compromise? | No. Validate evidence and scope; the authorised lab tests were benign positives. |

## How to review

1. Answer all 20 aloud, without reading the answer column.
2. Score yourself out of 20.
3. Write down only the questions you missed.
4. Repeat the missed questions the next day, mixed into the 20-card session.
5. Once these feel easy, include application questions about event correlation, process lineage, false positives and escalation.

## Mini scenario questions for deeper understanding

These are **optional**, not part of the daily 20-card count:

- Three failed logins occur for two different accounts in a 2+1 pattern. Should rule 100101 trigger? Why?
- A 4624 Logon Type 7 shows a Microsoft account unlock. Should you attribute it to a different account's 4625 failures?
- A CMD-related alert appears 14 seconds after a successful login, but the process username is not confirmed. What conclusion can you safely draw?
- Sysmon Event ID 1 shows PowerShell; Event ID 3 shows a TCP connection by the same PID. What does that correlation establish?

**Source files:** [Project 1 interview summary](../SOC-Home-Lab/INTERVIEW-SUMMARY.md) · [Project 2 interview summary](../Windows-Authentication-Investigation/INTERVIEW-SUMMARY.md) · [Project 2 learning review](../Windows-Authentication-Investigation/notes/LEARNING-REVIEW.md).
