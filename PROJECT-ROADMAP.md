# SOC / Cyber Security Analyst Portfolio Roadmap

This roadmap keeps the portfolio focused on the practical skills expected from junior SOC and cyber security analyst roles.

## Phase 1 — SOC Home Lab

**Status:** Complete — 3/3 controlled scenarios, 3 detections, 3 investigations, evidence, lessons learned, and Kali-to-Windows connectivity validation completed.

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

**Status:** **Complete (8 October 2026).** Custom Wazuh brute-force detection rule 100101 (three failed logins per account within 60 seconds) was tested in four controlled scenarios. Two Windows authentication investigations, 26 curated screenshots (19 for the first and seven for the second), an evidence timeline with documented limits, and response guidance are documented. Further remote/production rule tuning is optional future work.

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

**Status:** **Complete (10 October 2026).** Custom Wazuh rule 100102 (level 13) validated on actual Windows Event 4732 targeting Administrators, with Event 4733 rollback, non-administrator group negative test, limited logon and Sysmon process correlation, 26 curated screenshots and verified disposal of the temporary test account.

**Goal:** Hunt changes to the built-in local Administrators group; determine the actor, added account, authorisation and related process/logon context without mistaking all admin actions for attacks.

**Core events:** Windows Security 4732 (added to local group), 4733 (removed), 4672 (privileged logon context), 4624 (logon), Sysmon 1 (process creation). Target the privileged group identity rather than treating every group change as malicious.

**MITRE ATT&CK:** T1098.007 — Additional Local or Domain Groups (Persistence / Privilege Escalation).

**Delivered outcomes:** Read-only auditing checks; controlled positive + nonprivileged negative tests on an owned machine; automatic rollback and independent verification; deployed custom Wazuh rule 100102; investigation report; limited Sysmon/logon correlation; 26 linked screenshots; and confirmed disposal of the temporary test account. This was authorised lab activity, not a live compromise.

**Repository:** [Windows Privilege Escalation Hunt](./Windows-Privilege-Escalation-Hunt/) · [26 screenshots](./Windows-Privilege-Escalation-Hunt/screenshots/README.md).

The separate **Phase 3 — Phishing Email Investigation** was reopened and subsequently completed on 11 October 2026 as a scoped offline investigation. It remains distinct from the privilege escalation hunt.

## Phase 3 — Phishing Email Investigation

**Status:** **Complete (11 October 2026) for scoped offline lab investigation.** The introductory synthetic CASE-0041 was followed by a **redacted historical real-world banking-impersonation email (CASE-0042)**, local Python indicator extraction and 4/4 passing unit tests, a decoded MIME body inspection, and a **synthetic benign control (CASE-0043)** analysed with the same tool. Five genuine user-captured screenshots are linked and verified.

**Report and evidence:** [Project 4 README](./Phishing-Email-Investigation/) · [Consolidated findings](./Phishing-Email-Investigation/investigations/FINAL-INVESTIGATION-REPORT.md) · [Five evidence screenshots](./Phishing-Email-Investigation/screenshots/README.md) · [Python tool](./Phishing-Email-Investigation/tools/email_triage.py).

**Skills supported by evidence:**

- Email headers, sender domain comparison, reported SPF/DKIM/DMARC interpretation including `permerror`
- Read-only Python .eml parsing, test execution, SHA-256 hashing, safe defanging and URL-domain extraction
- HTML-link role analysis (CTA vs logo image vs unsubscribe) without clicking
- Evidence integrity and privacy-aware redaction
- Suspicious historical vs **constructed benign** sample reasoning; observed facts vs inference
- ATT&CK T1566.002 thematic mapping, report writing and recommended response

**Boundaries:** The source sample's mail path and destination are pre-redacted; no real authentication verification, live threat intelligence/redirect testing, production email quarantine, recipient impact or compromise was established. The tool is an extractor, not an autonomous malicious-email classifier.

## Phase 4 — Network PCAP Investigation

**Status:** **COMPLETE (12 October 2026) — scoped offline historical PCAP training investigation.** In Kali Wireshark, examined a published third-party [PCAP case](https://malware-traffic-analysis.net/2025/01/22/index.html), recorded local SHA-256, tied a VBScript-style response to an obfuscated PowerShell HTTP stage, documented ~5.19-second suspected polling, identified client/Kerberos context and investigated a later TLS 1.2 session. [Project 5 summary](./Network-PCAP-Investigation/) · [CASE-0051 report](./Network-PCAP-Investigation/investigations/CASE-0051-INVESTIGATION-REPORT.md) · [11 original uploaded and hash-verified evidence screenshots](./Network-PCAP-Investigation/screenshots/README.md). **No endpoint process execution, confirmed compromise, malware-family attribution or real-world incident handling is claimed.**

**Scenario:** Investigate suspicious network behaviour from a packet capture.

Skills demonstrated:

- Wireshark
- TCP/IP
- DNS / HTTP(S)
- Port and protocol analysis
- Filtering and traffic reconstruction
- Scan / brute-force / command-and-control indicators

## Phase 5 — Vulnerability Assessment

**Status:** **COMPLETE (13 October 2026) — scoped authorised TryHackMe Vulnversity lab.** Confirmed server-side processing of an inert `.phtml` test after an upload validation bypass. [Technical report](./Vulnerability-Assessment/investigations/VA-001-UPLOAD-VALIDATION-REPORT.md), [11 uploaded screenshots](./Vulnerability-Assessment/screenshots/README.md) hash-matched to the prepared ZIP, evidence transcriptions and separate interview/study materials complete. Native AttackBox scan files were not directly exported; no remediation retest was performed.

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
