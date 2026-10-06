# SOC Home Lab Learning Log

This log records the main work completed, problems encountered, troubleshooting performed, and lessons learned while building Project 1.

## 4 October 2026 — Wazuh Manager and Windows Agent

### Work Completed

- Imported the official Wazuh 4.14.8 appliance into VirtualBox.
- Configured the Wazuh VM with NAT for internet access and a Host-Only adapter for isolated lab communication.
- Verified the Wazuh host-only IP as `192.168.56.101`.
- Verified the Windows host IP as `192.168.56.1`.
- Confirmed successful connectivity from Windows to Wazuh.
- Installed and enrolled the Wazuh agent on the real Windows host.
- Confirmed the agent appeared as `Windows-Host` with **Active** status.

### Problems Encountered

The initial Wazuh import was blocked by insufficient storage.

### Troubleshooting and Resolution

Storage was cleaned up, enough free space was created, and the Wazuh OVA was imported successfully.

### What I Learned

- A SIEM lab depends on basic networking and system resources before any detection work can begin.
- NAT and Host-Only networking serve different purposes: internet access versus isolated host-to-VM communication.
- An active Wazuh agent confirms communication with the manager, but does not by itself prove every desired log source is being collected.

---

## 5 October 2026 — Sysmon and Scenario 1

### Work Completed

- Installed Sysmon on the Windows host.
- Verified the `Microsoft-Windows-Sysmon/Operational` log.
- Confirmed Sysmon Event ID 1 process telemetry locally and in Wazuh.
- Generated a controlled failed local authentication event.
- Investigated Windows Event ID 4625 in Wazuh.
- Correlated the failure with a later successful Windows Event ID 4624.
- Reviewed account, host, source, logon context, number of attempts, and timeline.
- Documented Detection 01 and Investigation 01.

### Classification

**Benign Positive.**

The authentication failure was real, but it was an expected local mistake followed by a successful unlock. The reviewed data did not show repeated credential guessing or suspicious remote activity.

### What I Learned

For a failed-login alert, the important questions are:

- Which account?
- Which device?
- Which source IP or source context?
- What logon type?
- How many attempts?
- When did they occur?
- Was there a successful login immediately afterwards?

I also learned the difference between:

- **Benign Positive:** the detection is correct, but the activity is harmless or expected.
- **False Positive:** the detection itself is wrong.

---

## 6 October 2026 — Scenario 2: PowerShell Process Investigation

### Work Completed

Generated the controlled command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process | Select-Object -First 5"
```

Sysmon Event ID 1 recorded the process creation and Wazuh raised:

- **Rule ID:** `92027`
- **Level:** `4`
- **Description:** `Powershell process spawned powershell instance`

The investigation reviewed:

- Image
- Full command line
- User
- Process ID
- Parent process
- Parent process ID
- Integrity level
- Time

The child PowerShell process had PID `6880` and parent PID `1296`.

A scope search for Sysmon Event ID 1 events with `parentProcessId = 6880` returned no results in the Wazuh data reviewed.

### Classification

**Benign Positive.**

The alert accurately detected PowerShell spawning PowerShell, but the activity was deliberately generated in the lab and the command only enumerated running processes.

### MITRE ATT&CK

**T1059.001 — PowerShell** was retained because the telemetry directly proved PowerShell execution.

### What I Learned

- Sysmon Event ID 1 means **Process Creation**.
- For process investigations, check **Image, CommandLine, ParentImage, User, PID/Parent PID, Integrity, and Time**.
- The executable name alone is not enough; the full command line explains what the process actually did.
- Parent-child process relationships provide important context.
- `High` integrity means elevated execution context, not automatic maliciousness.
- A SIEM description that sounds suspicious is not proof of compromise.
- MITRE ATT&CK mappings should only be retained when supported by the evidence.

---

## 6-7 October 2026 — Scenario 3: Custom Detection and Network Correlation

### Work Completed

First generated a controlled connection using:

```powershell
Test-NetConnection 192.168.56.101 -Port 443
```

Local Sysmon telemetry confirmed **Event ID 3 — Network Connection**.

A custom Wazuh rule was then created in `/var/ossec/etc/rules/local_rules.xml` to detect Sysmon Event ID 1 process creation where the command line contains `Test-NetConnection`.

The test was triggered with:

```powershell
powershell.exe -NoProfile -Command "Test-NetConnection 192.168.56.101 -Port 443"
```

Wazuh generated:

- **Rule ID:** `100100`
- **Level:** `6`
- **Description:** `Custom detection: PowerShell Test-NetConnection executed`

The detected process had:

- **PID:** `15676`
- **Parent PID:** `12640`
- **Integrity:** `High`
- **User:** `LAPTOP-C7OPSS6H\\hasna`

Sysmon Event ID 3 for PID `15676` showed:

- **Source:** `192.168.56.1:58463`
- **Destination:** `192.168.56.101:443`
- **Protocol:** TCP
- **Initiated:** true

The same PID was used to correlate the process event with the network event.

### Scope

A 30-minute Event ID 3 query for PID `15676` returned:

`Count = 1`

A 30-minute Event ID 1 query for `ParentProcessId: 15676` returned no matching child-process events.

### Classification

**Benign Positive.**

The custom rule correctly detected the intended command, but the activity was deliberately generated against the lab Wazuh manager and matched the expected behaviour.

### MITRE ATT&CK

**T1059.001 — PowerShell** was retained because PowerShell execution was directly shown.

No scanning or command-and-control technique was added because a single controlled connection to one destination and port did not prove either behaviour.

### What I Learned

- Sysmon Event ID 3 means **Network Connection**.
- Useful Event ID 3 fields include process, source IP, destination IP, source/destination port, user, protocol, and time.
- A process ID can be used to correlate process execution with network activity.
- Detection engineering means turning useful telemetry into an alert with explainable logic.
- A custom rule can be technically correct while the underlying activity is still benign.
- A single network connection is not enough evidence to call activity scanning or C2.
- Scope statements must stay within the time window and data actually reviewed.

---

## Wazuh Startup Troubleshooting — 6 October 2026

### Problem Encountered

The Wazuh dashboard reported:

- `API is down`
- Authorization-token/API connection errors

The `wazuh-manager` systemd service showed:

- `Active: failed`
- `Result: timeout`

### Troubleshooting

The following checks were performed:

- Reviewed `systemctl status wazuh-manager`.
- Reviewed journal logs.
- Reviewed `/var/ossec/logs/ossec.log`.
- Checked available memory.
- Checked for active Wazuh processes.
- Found a stale `/var/ossec/var/start-script-lock` directory containing PID `1962`.
- Confirmed PID `1962` was no longer running.

### Resolution

The stale startup lock was removed and the Wazuh manager was started again.

Final status:

`Active: active (running)`

### What I Learned

Troubleshooting should follow evidence rather than immediately reinstalling software:

**Symptom -> service status -> logs -> process state -> stale state/lock -> controlled fix -> verify service**

---

## Investigation Workflow Learned

The five-step workflow used throughout the project is:

**Validate -> Identify -> Correlate -> Scope -> Classify**

### Validate

Confirm the alert is backed by genuine telemetry.

### Identify

Determine the host, user, process/account, command line, PID, source/destination, privilege level, and time that matter to the alert.

### Correlate

Look for related events before and after the alert and connect telemetry using fields such as PID, account, host, or timestamp.

### Scope

Determine how far the activity went, while keeping conclusions limited to the data and time window actually reviewed.

### Classify

Decide whether the event is a True Positive, False Positive, Benign Positive, or still Undetermined, and whether escalation is required.

---

## Final Lessons Learned

The biggest lesson from Project 1 is that a SOC analyst should not decide whether activity is malicious from the alert name alone.

The underlying evidence matters more than the label. Authentication events need authentication context. Process alerts need command-line and process-lineage context. Network activity needs source, destination, port, process, and behavioural context.

Sysmon significantly improves endpoint visibility by providing detailed process and network telemetry. Wazuh then provides centralised alerting and investigation, while custom rules can turn specific telemetry into detections.

I also learned that documentation must distinguish what the evidence proves from what I assume. Statements such as **"no child process creation was found in the reviewed data"** are more accurate than broad claims such as **"nothing else happened."**

Three controlled scenarios were completed, three detections were documented, and three investigations were written with evidence and final classifications.


---

## 7 October 2026 — Final Kali-to-Windows Connectivity Validation

### Work Completed

The final lab-network check tested direct connectivity from the Kali Linux VM to the monitored Windows host:

```bash
ping -c 4 192.168.56.1
```

The first test returned 100% packet loss. The issue was the Windows host firewall, not the VirtualBox route.

A narrowly scoped Windows firewall rule was used to allow inbound ICMPv4 echo requests only on the Host-Only lab interface and only from the `192.168.56.0/24` lab subnet.

The test was repeated and returned:

- 4 packets transmitted
- 4 packets received
- 0% packet loss

### What I Learned

- A failed ping does not automatically mean the network path is broken; an endpoint firewall may be dropping ICMP.
- Firewall changes should be scoped to the required interface, protocol, and lab subnet instead of disabling protection broadly.
- Network connectivity should be verified with evidence rather than assumed.

### Project 1 Completion

With Kali-to-Windows communication verified, the first version of the SOC Home Lab is complete.
