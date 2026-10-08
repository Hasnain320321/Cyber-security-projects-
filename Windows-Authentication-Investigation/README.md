# Project 2 — Windows Authentication Investigation

**Status:** In progress — initial detection and controlled positive/negative tests completed on 8 October 2026.

## Objective

Investigate repeated Windows authentication failures using Wazuh, create and validate a custom rule for a suspicious failure pattern, distinguish authorised testing from an attack, and document defensive recommendations.

This is a separate portfolio project from [Project 1 — SOC Home Lab](../SOC-Home-Lab/).

## Lab and data sources

- Wazuh 4.14.8 manager in VirtualBox and a Windows endpoint with active Wazuh agent (`Windows-Host`)
- Windows Security Event ID **4625** (failed logon)
- Existing Wazuh rule **60122** (individual login failure)
- Dedicated local, non-administrator test account **SOC-Lab-Test**
- Wazuh custom rule **100101**, stored in `local_rules.xml`
- Host-only lab network; `192.168.56.1` is the Wazuh agent's IP address, not necessarily the authentication source

## Completed exercises

1. Reviewed an earlier isolated failed logon to establish baseline telemetry.
2. Created the dedicated `SOC-Lab-Test` account.
3. Generated three deliberately incorrect interactive local logins; Wazuh recorded three level-5 `60122` alerts.
4. Added and saved custom Wazuh rule `100101` to correlate three matching failures within 60 seconds, grouped by targeted username.
5. Restarted Wazuh Manager and confirmed the service was active.
6. **Positive test:** custom rule `100101` generated a level-10 alert at **2026-10-08 16:47:18** (dashboard local time). The expanded record showed `rule.frequency: 3` and `previous_output`.
7. **Negative test:** one later failed logon at **2026-10-08 16:55:28** produced a `60122` alert for `SOC-Lab-Test`, with no new `100101` alert observed in the inspected event window.

## Key evidence

- `targetUserName: SOC-Lab-Test`
- `data.win.system.eventID: 4625`
- `data.win.eventdata.logonType: 2` (interactive logon)
- `data.win.eventdata.ipAddress: 127.0.0.1` (local loopback source for the observed event)
- `status: 0xC000006D`; `subStatus: 0xC000006A` (incorrect password)
- Custom rule `100101`, level 10, mapped to MITRE ATT&CK **T1110 — Brute Force**

## Interpretation and limitations

The rule correctly detected the controlled repeated-failure pattern and did not fire on the single-failure negative test observed. This is **initial lab validation**, not proof of a production-ready detection.

Because the activity was authorised, its operational classification is **Benign Positive**; as a rule-validation test, it demonstrated a true-positive match for the intentionally generated pattern. The MITRE T1110 label reflects the detection's intended behaviour, **not proof that a real attacker was present**.

**Current limitations / follow-up tests:**

- Three mistyped passwords by a real employee could also trigger the rule.
- Matching on username alone can combine attempts from different source IPs; investigate source separately.
- Test mixed accounts, boundary timing, repeated bursts and real remote authentication telemetry before production use.
- Verify alert counts, time windows and Wazuh correlation behaviour under additional scenarios.
- Save and label screenshots from the lab in the evidence folder. Screenshots are **not yet uploaded** in this project folder.

## Documentation

- [Detection design and test](./detections/01-brute-force-correlation.md)
- [SOC investigation report](./investigations/01-controlled-login-attempts.md)
- [Evidence checklist](./screenshots/README.md)

## Analyst approach

Validate -> Identify -> Correlate -> Scope -> Classify.

In a genuine incident, review account identity, source IP/device, logon type, failure count/time distribution, related successful logins (4624), and actions after any success before escalating or containing.
