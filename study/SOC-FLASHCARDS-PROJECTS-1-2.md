# SOC Daily Flashcards - Projects 1 and 2

**Total: 40 flashcards - 20 Project 1 (SOC Home Lab) + 20 Project 2 (Windows Authentication Investigation).**

**Updated:** 8 October 2026

These 40 questions are based on the work actually documented in the two GitHub projects. **Default when asking for SOC flashcards:** use the full 40-card deck; present Project 1 and Project 2 in separate sections. Quiz without revealing answers immediately when interactive testing is requested.

## Project 1 - SOC Home Lab (20 cards)

| # | Question | Answer |
| --- | --- | --- |
| 1 | What does a SIEM do, and which SIEM did you use? | Collects, correlates and helps investigate security logs and alerts. I used Wazuh. |
| 2 | What is the difference between the Wazuh agent and manager? | The agent sends Windows telemetry; the manager receives, analyses and alerts on it. |
| 3 | What does Sysmon Event ID 1 record? | Process creation, including executable, command line, user and parent-process details. |
| 4 | What does Sysmon Event ID 3 record? | Network connections, including process, source/destination IPs, ports and protocol. |
| 5 | Why investigate ParentImage and ParentProcessId? | To understand process ancestry and identify what launched the process. |
| 6 | What is a PID, and how did you use one? | Process ID. I matched a PowerShell process to its network event using the same PID. |
| 7 | What did custom Wazuh rule 100100 detect? | A PowerShell process whose command line contained Test-NetConnection. |
| 8 | What did your Test-NetConnection test establish? | Sysmon Event ID 3 linked the alerted PowerShell PID 15676 to a TCP connection to 192.168.56.101:443. |
| 9 | What is the five-step SOC investigation workflow? | Validate -> Identify -> Correlate -> Scope -> Classify. |
| 10 | Why was the PowerShell detection a Benign Positive? | It correctly alerted on activity intentionally generated in my authorised lab. |
| 11 | What were the three Project 1 investigation scenarios? | Failed local authentication; PowerShell spawning PowerShell; custom Test-NetConnection detection with network correlation. |
| 12 | What did Wazuh rule 92027 indicate in Project 1? | A PowerShell process spawned another PowerShell process; Sysmon Event ID 1 was examined. |
| 13 | What does a full process command line tell you? | What the process was instructed to execute; the executable name alone is not enough context. |
| 14 | What does an elevated or High integrity level mean? | The process runs with elevated privileges; elevation by itself does not mean malicious activity. |
| 15 | What does MITRE ATT&CK T1059.001 represent in your lab? | PowerShell execution. It was supported by the observed process telemetry. |
| 16 | What did you check after finding the PowerShell process? | Related network activity and child processes, scoped to the reviewed data and time window. |
| 17 | Why can't one TCP connection to port 443 prove scanning or C2? | One expected connection to a known lab destination does not establish repeated scanning or command-and-control behaviour. |
| 18 | What are the Windows host and Wazuh manager lab IPs? | Windows host 192.168.56.1; Wazuh manager 192.168.56.101 on the Host-Only network. |
| 19 | What is the difference between NAT and Host-Only networking here? | NAT provided outbound internet access; Host-Only allowed isolated communication between lab host and VM. |
| 20 | How did you approach the Wazuh 'API is down' issue? | Check service status, logs, process state and stale startup lock; fix only after verification, then confirm the manager is running. |

## Project 2 - Windows Authentication Investigation (20 cards)

| # | Question | Answer |
| --- | --- | --- |
| 21 | What is the difference between Windows Events 4625 and 4624? | 4625 = failed logon; 4624 = successful logon. |
| 22 | Which logon types did we learn? | 2 = local interactive; 3 = network; 7 = unlock; 10 = remote interactive/RDP. |
| 23 | What does substatus 0xC000006A mean? | Incorrect password; it helps explain a Windows 4625 failure. |
| 24 | What is your failed-login investigation checklist? | Account -> source IP -> logon type -> attempts/time -> device -> activity after login. |
| 25 | What does Wazuh rule 60122 represent in the lab? | An individual Windows failed-logon alert. |
| 26 | What does your custom Wazuh rule 100101 detect? | Three failed logins for the same targeted username within 60 seconds, based on individual 60122 matches. |
| 27 | What do frequency, timeframe and same_field each do? | Set the event threshold, time window and matching field (target username). |
| 28 | What did the mixed-account 2+1 test demonstrate? | Two failures for one account plus one for another produced no new 100101 alert in the inspected window. |
| 29 | Why correlate failed 4625 attempts with a 4624 success? | To investigate whether the same account successfully authenticated after failures and evaluate the context. |
| 30 | Does a high-severity alert or MITRE mapping prove compromise? | No. Investigate underlying activity, attribution, scope and whether testing was authorised. |
| 31 | What did Wazuh rule 60118 mean in your second investigation? | A Windows workstation logon-success alert associated with Event ID 4624 in this lab. |
| 32 | What does status 0xC000006D indicate? | Authentication failed; substatus can provide a more specific reason. |
| 33 | What is the difference between agent.ip and the logon event's ipAddress? | agent.ip is the monitored endpoint's IP; event ipAddress is the source recorded in that login event. |
| 34 | What does source IP 127.0.0.1 mean in these test events? | Local loopback, consistent with a login originating locally rather than an identified external source. |
| 35 | What were the four detection test outcomes? | 3 on account 1: alert; 1 isolated: no correlation; 2+1 split: no correlation; 3 on account 2: alert. |
| 36 | Why run a negative test as well as a positive test? | To verify the rule does not create unnecessary high-severity alerts for nonmatching behaviour. |
| 37 | What happened in Investigation 2's confirmed timeline? | SOC-Lab-Test2 failed at 18:01:21 and 18:01:26, then successfully logged in at 18:01:33. |
| 38 | Why was a separate Logon Type 7 event excluded? | It was an unlock for a different Microsoft account, not the same test identity and interactive session. |
| 39 | Why not attribute the nearby McAfee BrowserHost.exe alert to SOC-Lab-Test2? | Its process user/session connection to that successful login was not established; nearby timestamps are insufficient. |
| 40 | What would you recommend if an authentication incident were genuinely suspicious? | Preserve logs; confirm account/source/session; inspect post-login actions; escalate and apply approved containment if supported by evidence. |


## Suggested review method

1. Answer each question before looking at the answer.
2. Mark each card correct/incorrect, and score Project 1 out of 20 and Project 2 out of 20.
3. Repeat missed cards after the full deck and the next day.
4. Focus on **why** you investigate each field, rather than memorising long PowerShell commands, PIDs or entire XML syntax.

## Source documentation

- [Project 1 interview summary](../SOC-Home-Lab/INTERVIEW-SUMMARY.md)
- [Project 1 learning log](../SOC-Home-Lab/notes/learning-log.md)
- [Project 2 interview summary](../Windows-Authentication-Investigation/INTERVIEW-SUMMARY.md)
- [Project 2 memorisation notes](../Windows-Authentication-Investigation/notes/WHAT-TO-MEMORISE.md)

**Boundaries:** The four Project 2 rule tests were authorised local lab activity, not evidence of a real brute-force compromise. The Project 1 test TCP connection was expected, not evidence of scanning or C2.
