# SOC / Cyber Security Analyst Portfolio Roadmap

This roadmap keeps the portfolio focused on the practical skills expected from junior SOC and cyber security analyst roles.

## Phase 1 — SOC Home Lab

**Status:** Complete — 3/3 controlled scenarios, 3 detections, 3 investigations, evidence, lessons learned, interview summary, and Kali-to-Windows connectivity validation completed.

**Goal:** Build a small security monitoring environment and prove that endpoint activity can be collected, detected, and investigated.

### Core components

- Kali Linux — controlled attack/test machine
- Windows 10/11 VM — monitored endpoint
- Ubuntu/Linux VM — SIEM/server where required
- Sysmon — enhanced Windows telemetry
- Wazuh — initial SIEM platform
- VirtualBox or another hypervisor

### Evidence to produce

- Lab architecture diagram
- Windows logging screenshots
- Sysmon configuration evidence
- Wazuh agent connected to Windows
- SIEM dashboard showing events
- At least three security detections — **completed**
- At least two full incident investigations — **completed (three written)**
- MITRE ATT&CK mappings — **completed where evidence supports them**
- Final project summary — **completed**

## Phase 2 — Wazuh Brute-Force Detection & Windows Authentication Investigation

**Status:** **Complete (8 October 2026).** Custom Wazuh brute-force detection rule 100101 (three failed logins per account within 60 seconds) was tested in four controlled scenarios. Two Windows authentication investigations, 26 curated screenshots (19 for the first and seven for the second), an evidence timeline with documented limits, response guidance and interview summary are documented. Further remote/production rule tuning is optional future work.

**Evidence and reports:** [Windows Authentication Investigation](./Windows-Authentication-Investigation/) · [Final summary](./Windows-Authentication-Investigation/FINAL-PROJECT-SUMMARY.md)

**Scenario:** Multiple failed Windows logins, followed by investigation of the source and account activity.

Skills demonstrated:

- Windows Security Event Logs
- Event IDs such as 4624 and 4625
- Authentication analysis
- Timeline building
- True-positive / false-positive classification
- Escalation and remediation recommendations

## Supplemental Hunt — Windows Privilege Escalation (new, separate)

**Status:** In progress — documentation/setup only; no new lab events or detection results yet.

**Goal:** Hunt changes to the built-in local Administrators group; determine the actor, added account, authorisation and related process/logon context without mistaking all admin actions for attacks.

**Core events:** Windows Security 4732 (added to local group), 4733 (removed), 4672 (privileged logon context), 4624 (logon), Sysmon 1 (process creation). Target the privileged group identity rather than treating every group change as malicious.

**MITRE ATT&CK:** T1098.007 — Additional Local or Domain Groups (Persistence / Privilege Escalation).

**Planned outcomes:** Read-only auditing check; controlled positive + nonprivileged negative test on a machine owned by the learner; reversible membership change; custom Wazuh detection; rollback proof; investigation report, curated screenshots and interview notes. The tests are **not yet completed**.

**Repository:** [Windows Privilege Escalation Hunt](./Windows-Privilege-Escalation-Hunt/).

The existing **Phase 3 — Phishing Email Investigation** remains planned for later; this supplemental project does not erase or renumber it.

## Phase 3 — Phishing Email Investigation

**Scenario:** Analyse a suspicious email and decide whether it is benign, suspicious, or malicious.

Skills demonstrated:

- Email headers
- SPF / DKIM / DMARC concepts
- URL and domain analysis
- Hash and IOC analysis
- Threat intelligence
- MITRE ATT&CK mapping
- Incident report writing

## Phase 4 — Network PCAP Investigation

**Scenario:** Investigate suspicious network behaviour from a packet capture.

Skills demonstrated:

- Wireshark
- TCP/IP
- DNS / HTTP(S)
- Port and protocol analysis
- Filtering and traffic reconstruction
- Scan / brute-force / command-and-control indicators

## Phase 5 — Vulnerability Assessment

**Scenario:** Assess a deliberately vulnerable lab machine and create a prioritised remediation report.

Skills demonstrated:

- Nmap
- Vulnerability scanning
- Exposure analysis
- Severity and risk
- Evidence collection
- Remediation recommendations

## Phase 6 — Detection Engineering

**Goal:** Build simple but explainable detection logic.

Example detections:

- Repeated failed logins
- Suspicious PowerShell activity
- New administrator account creation
- Unusual outbound connections
- Port scanning
- Suspicious process execution

Each detection should document:

- What behaviour it detects
- Why the behaviour matters
- Required telemetry
- Query or rule
- MITRE ATT&CK mapping
- Expected false positives
- Investigation steps
- Recommended response

## Skills Priority

### High priority

- Networking fundamentals
- Windows and Linux fundamentals
- Security logs
- SIEM
- Alert triage
- Incident investigation
- Wireshark / PCAP analysis
- EDR concepts

### Medium priority

- MITRE ATT&CK
- Threat intelligence
- Microsoft Sentinel
- Microsoft Defender
- Active Directory / Entra ID fundamentals
- PowerShell
- Python
- Vulnerability management

### Later development

- Cloud security fundamentals
- KQL
- Sigma
- Detection engineering
- Automation

## Target Outcome

The finished portfolio should allow a recruiter or interviewer to open GitHub and see direct evidence that I can:

- Read security telemetry
- Recognise suspicious behaviour
- Investigate alerts
- Explain what happened
- Distinguish a true positive from a false positive
- Map behaviour to MITRE ATT&CK
- Recommend containment and remediation
- Document findings clearly
