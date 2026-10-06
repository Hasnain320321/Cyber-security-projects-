# Screenshot Evidence

This folder stores screenshots used as evidence for the SOC Home Lab.

## Rules

- Do not upload passwords, tokens, API keys, private email addresses, or other sensitive information.
- Crop screenshots so the relevant evidence is easy to identify.
- Use clear filenames in chronological order.
- Refer to screenshots from the relevant investigation or detection document.

## Suggested Naming

```text
01-host-only-network.png
02-wazuh-ip-addresses.png
03-connectivity-test.png
04-wazuh-agent-active.png
05-sysmon-event.png
06-wazuh-sysmon-ingestion.png
07-failed-login-event-details.png
08-failed-login-wazuh-rule.png
09-powershell-command-details.png
10-powershell-rule-92027.png
11-powershell-no-child-processes.png
```

## Current Evidence

### 04 - Wazuh agent active

![Wazuh agent active](./04-wazuh-agent-active.png)

The Wazuh dashboard shows the `Windows-Host` endpoint at `192.168.56.1` running Wazuh agent version `4.14.8` with **Active** status. This confirms that the Windows endpoint has successfully enrolled with and is communicating with the Wazuh manager over the isolated lab network.

### 05 - Sysmon Event ID 1

![Sysmon Event ID 1](./05-sysmon-event.png)

Windows Event Viewer shows the `Microsoft-Windows-Sysmon/Operational` log generating **Event ID 1 (Process Create)** events. This confirms that Sysmon is installed correctly and producing endpoint telemetry locally.

### 06 - Wazuh Sysmon ingestion

![Wazuh Sysmon ingestion](./06-wazuh-sysmon-ingestion.png)

Wazuh Threat Hunting was filtered to `Windows-Host`, the `Microsoft-Windows-Sysmon/Operational` channel, and **Event ID 1**. The returned events confirm that Sysmon process-creation telemetry from the Windows host is being ingested and is searchable in Wazuh.

### 07 - Failed login event details

![Failed login event details](./07-failed-login-event-details.png)

Wazuh event details show Windows Security **Event ID 4625**, confirming that the monitored Windows endpoint recorded an account logon failure.

### 08 - Wazuh failed-login rule

![Wazuh failed-login rule](./08-failed-login-wazuh-rule.png)

Wazuh matched the failed-authentication event to **rule 60122** at **level 5**. This provides SIEM-side evidence that the Windows authentication failure was collected and detected.


### 09 - PowerShell command and process details

![PowerShell command and process details](./09-powershell-command-details.png)

Sysmon Event ID 1 records the controlled PowerShell process and its full command line, including `-NoProfile`, `-ExecutionPolicy Bypass`, and `Get-Process | Select-Object -First 5`. The event also records the PowerShell image, user context, process ID, parent process information, and high integrity level used during the lab test.

### 10 - Wazuh PowerShell rule 92027

![Wazuh PowerShell rule 92027](./10-powershell-rule-92027.png)

Wazuh matched the process-creation telemetry to **rule 92027** at **level 4**, with the description `Powershell process spawned powershell instance`. The alert is mapped to **MITRE ATT&CK T1059.001 - PowerShell** under the Execution tactic, which is supported by the observed telemetry.

### 11 - PowerShell scope check

![PowerShell scope check](./11-powershell-no-child-processes.png)

Wazuh was filtered to the monitored Windows host, the Sysmon Operational channel, **Event ID 1**, and `parentProcessId = 6880` over the last 24 hours. The query returned **No results match your search criteria**, providing evidence that no additional child-process creation for PID 6880 was found in the Wazuh data reviewed.
