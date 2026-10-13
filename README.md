# Cyber Security Portfolio

> A hands-on portfolio focused on SOC Analyst and Cyber Security Analyst skills: monitoring, detection, investigation, incident response, networking, endpoint telemetry, SIEM, and threat analysis.

## About This Portfolio

I am building this repository to document practical cyber security work rather than only listing tools on a CV. Each project shows the lab setup, detection logic, observed evidence, investigation reasoning, MITRE ATT&CK mapping, and recommended response. Authorised lab events are not presented as real attacks.

## Current Focus

**Project 1 — SOC Home Lab:** Complete, including three controlled scenarios, detections, investigations, and screenshots.

**Project 2 — Wazuh Brute-Force Detection & Authentication Investigation:** Complete. Built and tested custom rule `100101`, conducted four positive/negative tests, wrote two investigations and a response playbook, and curated 26 screenshots.

**Project 3 — Windows Privilege Escalation Hunt:** **Complete (10 October 2026)** — detection tests, limited log/process correlation, final cleanup and 26 evidence screenshots verified on GitHub. Created custom Wazuh rule `100102` (level 13) for Windows Security 4732 additions specifically to the built-in Administrators group. Confirmed alerts, 4733 rollback, and two negative tests including a normal-group 4732 that triggered built-in rule `60144`, not `100102`.

**Project 4 — Phishing Email Investigation:** **Complete (11 October 2026) — offline email-analysis lab.** Investigated a historical redacted banking-impersonation sample, built/tested a Python indicator extractor (4/4 tests), compared against a labelled synthetic benign email, reviewed headers and message content, and verified five user-captured evidence screenshots. No live compromise or site analysis claimed.

**Project 5 — Network PCAP Investigation:** **Complete (12 October 2026)** — offline analysis of a third-party training capture; correlated a VBScript downloader, an obfuscated PowerShell-like HTTP response and suspected ~5.2-second polling, identified the host and a Kerberos principal, documented a later TLS session, computed a PCAP SHA-256, and verified **11 genuine Wireshark screenshots**. Execution/compromise unproven.

**Project 6 — Vulnerability Assessment:** **Complete (13 October 2026) — authorised Vulnversity training lab with 11 original screenshots uploaded and verified against the prepared evidence ZIP.** Assessed an authorised TryHackMe Vulnversity machine, identified six open ports and a web upload form, confirmed a `.phtml` upload restriction bypass and safely validated server-side PHP execution using a harmless echo-only test. No real-world exploitation claimed.

## Portfolio Projects

| Project | Main skills | Status |
| --- | --- | --- |
| [SOC Home Lab](./SOC-Home-Lab/) | Wazuh, Windows Security logs, Sysmon, detection and triage | Complete |
| [Brute-Force Detection & Windows Authentication](./Windows-Authentication-Investigation/) | Rule 100101, Windows 4625/4624, validation, investigations | Complete |
| [Windows Privilege Escalation Hunt](./Windows-Privilege-Escalation-Hunt/) | 4732/4733, rule 100102, group SID targeting, positive/negative tests, [26 evidence screenshots](./Windows-Privilege-Escalation-Hunt/screenshots/README.md), T1098.007 | Complete |
| [Phishing Email Investigation](./Phishing-Email-Investigation/) | Historical redacted email, Python tool, 4/4 tests, source hash, benign control, [5 screenshots](./Phishing-Email-Investigation/screenshots/README.md), [report](./Phishing-Email-Investigation/investigations/FINAL-INVESTIGATION-REPORT.md) | Complete — scoped offline investigation |
| [Network PCAP Investigation](./Network-PCAP-Investigation/) | Wireshark, staged-download analysis, suspected beaconing, TLS, DHCP, Kerberos, [11 screenshots](./Network-PCAP-Investigation/screenshots/), [report](./Network-PCAP-Investigation/investigations/CASE-0051-INVESTIGATION-REPORT.md) | **Complete — scoped offline training case (12 Oct 2026)** |
| [Vulnerability Assessment](./Vulnerability-Assessment/) | Nmap, Gobuster, harmless PHP execution validation, [11 screenshots](./Vulnerability-Assessment/screenshots/README.md), [report](./Vulnerability-Assessment/investigations/VA-001-UPLOAD-VALIDATION-REPORT.md), remediation | **Complete — scoped authorised TryHackMe lab (13 Oct 2026)** |
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

**Portfolio status:** Projects **1–6 complete and documented**. Project 6's 11 original screenshot PNGs were byte-for-byte verified against the prepared ZIP; original native AttackBox scan files were not directly exported. **Project 7** Detection Engineering is planned. All work is on authorised labs or explicitly scoped offline training artifacts, not live incidents.
