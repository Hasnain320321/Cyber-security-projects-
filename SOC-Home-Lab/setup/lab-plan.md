# SOC Home Lab — Build Plan

## Stage 1 — Confirm Host Capacity

Before assigning resources, record the host system:

- CPU:
- RAM:
- Free storage:
- Hypervisor:
- Kali installation type: bare metal / VM / other

Resource allocations will be chosen after confirming these values.

## Stage 2 — Create the Lab Network

The environment should be isolated from unrelated systems.

Planned systems:

| System | Purpose |
| --- | --- |
| Kali Linux | Controlled security testing |
| Windows 10/11 | Monitored endpoint |
| Wazuh server | SIEM / event collection |

The exact virtual-network mode will be documented once the hypervisor is confirmed.

## Stage 3 — Prepare Windows Endpoint

Tasks:

- Create Windows VM
- Apply normal updates
- Create a dedicated lab user
- Verify networking
- Enable / review Windows Event Logs
- Install Sysmon
- Install Wazuh agent
- Confirm endpoint appears in Wazuh

## Stage 4 — Verify Telemetry

Before generating attack-like behaviour, confirm normal telemetry first.

Evidence to capture:

- Wazuh agent online
- Windows hostname
- Endpoint IP address
- Windows Event Logs arriving
- Sysmon events arriving
- Dashboard / event search

## Stage 5 — Controlled Test Scenarios

Only after logging is confirmed:

1. Failed login activity
2. Network scanning from Kali
3. Safe suspicious-looking PowerShell activity

Each scenario should be followed by a documented investigation.

## Stage 6 — Documentation

For every major step:

- Explain what was configured
- Save commands used
- Save screenshots
- Record problems encountered
- Explain how the problem was resolved
- Avoid including passwords, API keys, tokens, or personal information

## Evidence Naming Convention

Use descriptive filenames, for example:

```text
01-wazuh-agent-connected.png
02-windows-event-log.png
03-sysmon-events.png
04-failed-login-alert.png
05-investigation-timeline.png
```

## Completion Checklist

- [ ] Host specifications recorded
- [ ] Hypervisor confirmed
- [ ] Windows VM created
- [ ] Lab networking configured
- [ ] Wazuh installed
- [ ] Wazuh agent installed
- [ ] Sysmon installed
- [ ] Normal events confirmed
- [ ] Failed-login scenario completed
- [ ] Network-scan scenario completed
- [ ] PowerShell scenario completed
- [ ] Investigations documented
