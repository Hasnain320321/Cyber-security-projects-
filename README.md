# Cyber Security Portfolio

> A hands-on portfolio focused on SOC Analyst and Cyber Security Analyst skills: monitoring, detection, investigation, incident response, networking, endpoint telemetry, SIEM, and threat analysis.

## About This Portfolio

I am building this repository to document practical cyber security work rather than only listing tools on a CV. Each project will show the problem, lab setup, evidence, investigation process, findings, MITRE ATT&CK mapping, and recommended response.

## Current Focus

**Project 1 — SOC Home Lab** is complete, including three controlled scenarios, three detection write-ups, three investigation reports, and screenshots.

**Project 2 — Wazuh Brute-Force Detection & Authentication Investigation** is **Complete**. The project built and validated Wazuh brute-force detection rule `100101` (three failures against the same account within 60 seconds) using four controlled positive/negative scenarios across two accounts and investigated Event ID 4625 failures followed by an Event ID 4624 successful login. It includes two investigation reports, 26 curated screenshots (19 from the first investigation and seven from the second), an evidence timeline with limitations, and a response playbook. Detection tuning for remote/production use remains optional future work.

**New — Windows Privilege Escalation Hunt** has been added as a separate upcoming investigation. Its GitHub plan, detection hypothesis, and evidence checklist are ready. **No privilege-change tests have been run yet.**

## Portfolio Projects

| Project | Main Skills | Status |
| --- | --- | --- |
| [SOC Home Lab](./SOC-Home-Lab/) | Wazuh SIEM, Windows logs, Sysmon, custom detection engineering, alert triage, event correlation, MITRE ATT&CK | Complete |
| [Brute-Force Detection & Windows Authentication](./Windows-Authentication-Investigation/) | Wazuh rule 100101: 3 failed logins / 60s per account; 4 validation tests; Windows 4625/4624 investigation; SOC response playbook | Complete |
| [Windows Privilege Escalation Hunt](./Windows-Privilege-Escalation-Hunt/) | Windows Event 4732/4733, privileged group changes, Wazuh detection, account/session correlation, MITRE T1098.007 | In progress — setup only |
| Phishing Email Investigation | Email headers, IOCs, threat intelligence, incident reporting | Planned |
| Network PCAP Investigation | Wireshark, TCP/IP, packet analysis, network threats | Planned |
| Vulnerability Assessment | Nmap, scanning, risk prioritisation, remediation | Planned |
| Detection Engineering | KQL/Sigma, detection logic, false positives, MITRE ATT&CK | Planned |

See the full plan in [PROJECT-ROADMAP.md](./PROJECT-ROADMAP.md).

## Tools & Technologies

Tools I am using or developing experience with include:

- Kali Linux
- Wireshark
- Nmap
- Burp Suite
- Linux command line
- Windows Event Viewer
- Sysmon
- Wazuh / SIEM tooling
- VirtualBox / virtual machines
- Packet Tracer
- MITRE ATT&CK

As the portfolio develops, I will add Microsoft Sentinel, KQL, Sigma rules, threat intelligence tooling, and basic PowerShell/Python automation.

## How Projects Are Documented

Each project will aim to include:

1. **Objective** — what the project demonstrates.
2. **Architecture / Lab Setup** — systems and tools used.
3. **Scenario** — the security event or incident being investigated.
4. **Data Sources** — logs, PCAPs, endpoint telemetry, alerts, etc.
5. **Detection** — how suspicious activity was identified.
6. **Investigation** — the steps taken to understand the event.
7. **Evidence** — screenshots, queries, filters, and relevant output.
8. **MITRE ATT&CK Mapping** — relevant tactics and techniques.
9. **Findings** — what happened and why it matters.
10. **Response / Remediation** — what a SOC analyst should do next.
11. **False Positives** — legitimate activity that could trigger the same alert.
12. **Lessons Learned** — what I improved through the project.

## Important Note

All attack simulations and testing documented here are performed only in systems and lab environments that I own or control. This repository is for defensive cyber security learning and portfolio evidence.

---

**Portfolio status:** Projects 1 and 2 are Complete. The Windows Privilege Escalation Hunt is in preparation; Phishing Email Investigation and the other future projects remain planned.
