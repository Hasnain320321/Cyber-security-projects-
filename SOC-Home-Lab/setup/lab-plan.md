# SOC Home Lab — Build and Completion Record

## Final Lab Design

| System | Purpose | Current state |
| --- | --- | --- |
| Windows 10/11 host | Monitored endpoint | Active |
| Wazuh 4.14.8 appliance | SIEM / event collection / alerting | Active |
| Kali Linux VM | Controlled test machine for later lab expansion | Present |

## Networking

The lab uses Oracle VirtualBox.

The Wazuh VM has:

- NAT for outbound internet access.
- A Host-Only adapter for isolated communication with the Windows host.

Verified host-only addresses:

- **Windows host:** `192.168.56.1`
- **Wazuh manager:** `192.168.56.101`

Windows-to-Wazuh connectivity was verified successfully.

Kali-to-Wazuh communication was verified earlier in the build. Kali-to-Windows communication was also verified successfully: `ping -c 4 192.168.56.1` returned 4/4 replies with 0% packet loss after a narrowly scoped Windows firewall rule allowed ICMP echo on the Host-Only lab interface/subnet.

## Windows Endpoint

The original plan used a dedicated Windows VM, but the working lab uses the real Windows host as the monitored endpoint.

Completed tasks:

- [x] Windows endpoint available
- [x] Host-only networking configured
- [x] Windows Event Logs reviewed
- [x] Sysmon installed
- [x] Wazuh agent installed
- [x] Endpoint appears in Wazuh as `Windows-Host`
- [x] Wazuh agent status verified as Active

## Telemetry Verification

Completed:

- [x] Wazuh agent online
- [x] Windows hostname identified
- [x] Endpoint IP identified
- [x] Windows Security events visible in Wazuh
- [x] Sysmon Event ID 1 generated locally
- [x] Sysmon Event ID 1 searchable in Wazuh
- [x] Sysmon Event ID 3 generated locally
- [x] Custom Wazuh detection rule validated

The verified telemetry path is:

```text
Windows activity
      |
      v
Windows Event Logs / Sysmon
      |
      v
Wazuh agent
      |
      v
Wazuh manager
      |
      v
Wazuh Threat Hunting / alerts
```

## Controlled Test Scenarios

### Scenario 1 — Failed Local Authentication

- [x] Generated controlled authentication failure
- [x] Investigated Windows Event ID 4625
- [x] Correlated nearby Event ID 4624 success
- [x] Documented Detection 01
- [x] Documented Investigation 01
- [x] Classified as Benign Positive

### Scenario 2 — PowerShell Process Spawn

- [x] Generated safe PowerShell child process
- [x] Investigated Sysmon Event ID 1
- [x] Reviewed command line and process lineage
- [x] Scoped for child-process activity
- [x] Documented Detection 02
- [x] Documented Investigation 02
- [x] Mapped T1059.001 where supported
- [x] Classified as Benign Positive

### Scenario 3 — Custom Test-NetConnection Detection

The original draft plan mentioned network scanning from Kali. The completed third scenario was changed to a safer and more useful detection-engineering exercise using a controlled PowerShell connectivity test.

- [x] Generated `Test-NetConnection` activity
- [x] Verified Sysmon Event ID 3 locally
- [x] Created custom Wazuh rule 100100
- [x] Triggered and validated the custom alert
- [x] Investigated Sysmon Event ID 1 process telemetry
- [x] Correlated PID 15676 with Sysmon Event ID 3
- [x] Scoped network activity in a 30-minute window
- [x] Scoped for child-process creation
- [x] Documented Detection 03
- [x] Documented Investigation 03
- [x] Classified as Benign Positive

## Documentation and Evidence

Completed:

- [x] Three detection write-ups
- [x] Three investigation write-ups
- [x] Screenshots organised and captioned
- [x] Main SOC Home Lab README updated
- [x] Learning log and troubleshooting notes written
- [x] Evidence-based MITRE ATT&CK mapping used
- [x] Interview-ready project summary created

## Completion Checklist

- [x] Hypervisor confirmed
- [x] Lab networking configured
- [x] Wazuh installed and operational
- [x] Wazuh agent installed
- [x] Sysmon installed
- [x] Normal telemetry confirmed
- [x] Failed-login scenario completed
- [x] PowerShell scenario completed
- [x] Custom network-related detection scenario completed
- [x] Three detections documented
- [x] Three investigations documented
- [x] Evidence organised
- [x] Lessons learned written
- [x] Kali Linux can communicate directly with the Windows endpoint

## Evidence Naming Convention

The evidence folder currently uses numbered filenames from `04` through `19`, with each screenshot documented in `screenshots/README.md`.

## Safety

All testing is limited to systems and virtual machines owned or controlled by the lab operator. The scenarios are designed for defensive monitoring, detection, investigation, and SOC practice.
