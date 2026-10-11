# Cyber Security Portfolio

> A hands-on portfolio focused on SOC Analyst and Cyber Security Analyst skills: monitoring, detection, investigation, incident response, networking, endpoint telemetry, SIEM, and threat analysis.

## About This Portfolio

I am building this repository to document practical cyber security work rather than only listing tools on a CV. Each project shows the lab setup, detection logic, observed evidence, investigation reasoning, MITRE ATT&CK mapping, and recommended response. Authorised lab events are not presented as real attacks.

## Current Focus

**Project 1 — SOC Home Lab:** Complete, including three controlled scenarios, detections, investigations, and screenshots.

**Project 2 — Wazuh Brute-Force Detection & Authentication Investigation:** Complete. Built and tested custom rule `100101`, conducted four positive/negative tests, wrote two investigations and a response playbook, and curated 26 screenshots.

**Project 3 — Windows Privilege Escalation Hunt:** **Complete (10 October 2026)** — detection tests, limited log/process correlation, final cleanup and 26 evidence screenshots verified on GitHub. Created custom Wazuh rule `100102` (level 13) for Windows Security 4732 additions specifically to the built-in Administrators group. Confirmed alerts, 4733 rollback, and two negative tests including a normal-group 4732 that triggered built-in rule `60144`, not `100102`.

**Project 4 — Phishing Email Investigation:** **Complete (11 October 2026) — offline email-analysis lab.** Investigated a historical redacted banking-impersonation sample, built/tested a Python indicator extractor (4/4 tests), compared against a labelled synthetic benign email, reviewed headers and message content, and verified five user-captured evidence screenshots. No live compromise or site analysis claimed.

## Portfolio Projects

| Project | Main skills | Status |
| --- | --- | --- |
| [SOC Home Lab](./SOC-Home-Lab/) | Wazuh, Windows Security logs, Sysmon, detection and triage | Complete |
| [Brute-Force Detection & Windows Authentication](./Windows-Authentication-Investigation/) | Rule 100101, Windows 4625/4624, validation, investigations | Complete |
| [Windows Privilege Escalation Hunt](./Windows-Privilege-Escalation-Hunt/) | 4732/4733, rule 100102, group SID targeting, positive/negative tests, [26 evidence screenshots](./Windows-Privilege-Escalation-Hunt/screenshots/README.md), T1098.007 | Complete |
| [Phishing Email Investigation](./Phishing-Email-Investigation/) | Historical redacted email, Python tool, 4/4 tests, source hash, benign control, [5 screenshots](./Phishing-Email-Investigation/screenshots/README.md), [report](./Phishing-Email-Investigation/investigations/FINAL-INVESTIGATION-REPORT.md) | Complete — scoped offline investigation |
| Network PCAP Investigation | Wireshark, TCP/IP, threat analysis | Planned |
| Vulnerability Assessment | Nmap, scanning, remediation | Planned |
| Detection Engineering | KQL/Sigma, alert tuning, MITRE ATT&CK | Planned |

See the full plan in [PROJECT-ROADMAP.md](./PROJECT-ROADMAP.md).

## Tools & Technologies

Wazuh, Windows Event Viewer, Sysmon, PowerShell, VirtualBox, Kali Linux, Linux CLI, Wireshark, Nmap, Burp Suite, Packet Tracer and MITRE ATT&CK.

Future learning may include Microsoft Sentinel, KQL, Sigma rules, threat intelligence tools and defensive automation.

## How Projects Are Documented

Objectives; lab setup; scenario; data sources; detection logic; test matrix; investigation; evidence; MITRE mapping; findings; response recommendations; legitimate activity/false-positive discussion; lessons learned; honest limitations.

## Important Note

All simulations and testing are undertaken only on authorised personally controlled systems. A security alert is an investigative lead, not automatic proof of malicious activity.

---

**Portfolio status:** Projects 1–4 complete and documented; Project 4 completed as an **offline historical-sample / synthetic-control exercise**, not a live incident. Network PCAP, vulnerability assessment and detection engineering are planned.
