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
07-failed-login-alert.png
08-investigation-search.png
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
