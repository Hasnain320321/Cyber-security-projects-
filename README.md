# Cyber Security Portfolio

> A hands-on portfolio focused on SOC Analyst and Cyber Security Analyst skills: monitoring, detection, investigation, incident response, networking, endpoint telemetry, SIEM, and threat analysis.

## About This Portfolio

I am building this repository to document practical cyber security work rather than only listing tools on a CV. Each project will show the problem, lab setup, evidence, investigation process, findings, MITRE ATT&CK mapping, and recommended response.

My target roles are:

- SOC Analyst / SOC Analyst Tier 1
- Cyber Security Analyst
- Junior Security Analyst
- Security Operations Analyst

## Current Focus

The first major project is a **SOC Home Lab** using a Windows endpoint, Kali Linux, Sysmon, Wazuh, and VirtualBox networking. Three controlled scenarios are now documented: failed authentication, PowerShell process investigation, and a custom Wazuh detection for PowerShell `Test-NetConnection` activity. The project includes three detection write-ups, three investigation reports, evidence screenshots, troubleshooting notes, and an interview-ready summary.

## Portfolio Projects

| Project | Main Skills | Status |
| --- | --- | --- |
| [SOC Home Lab](./SOC-Home-Lab/) | Wazuh SIEM, Windows logs, Sysmon, custom detection engineering, alert triage, event correlation, MITRE ATT&CK | Complete |
| Windows Authentication Investigation | Event logs, brute-force analysis, account activity | Planned |
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

**Portfolio status:** actively being built. Project 1 (SOC Home Lab) is complete; the remaining roadmap projects are planned/in progress.
