# SOC / Cyber Security Analyst Portfolio Roadmap

This roadmap keeps the portfolio focused on the practical skills expected from junior SOC and cyber security analyst roles.

## Phase 1 — SOC Home Lab

**Status:** Near complete — 3/3 controlled scenarios, 3 detections, 3 investigations, evidence, lessons learned, and interview summary completed. Direct Kali-to-Windows connectivity remains an optional final validation.

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

## Phase 2 — Windows Authentication Investigation

**Scenario:** Multiple failed Windows logins, followed by investigation of the source and account activity.

Skills demonstrated:

- Windows Security Event Logs
- Event IDs such as 4624 and 4625
- Authentication analysis
- Timeline building
- True-positive / false-positive classification
- Escalation and remediation recommendations

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
