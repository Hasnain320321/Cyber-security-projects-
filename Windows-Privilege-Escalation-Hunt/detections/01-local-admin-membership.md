# Detection 01 — Local Administrators Group Addition

**Status: Deployed and validated in the personal Wazuh lab, 10 October 2026.**

## Detection hypothesis

Adding an account to the built-in Windows Administrators group can enable subsequent elevated actions. Alert on **actual additions** rather than removals or changes to unprivileged groups. An alert requires triage; it does not by itself prove malicious activity.

- Windows provider: `Microsoft-Windows-Security-Auditing`
- Security Event ID: **4732** (group member added)
- Target group SID: **S-1-5-32-544** (built-in Administrators)
- Subject: `win.eventdata.subjectUserName`
- Member: `win.eventdata.memberSid`
- Group: `win.eventdata.targetUserName`, `win.eventdata.targetSid`
- Event ID field: `win.system.eventID`
- ATT&CK: **T1098.007**
- Baseline rule: Wazuh **60154**, level 12, "Administrators Group Changed"
- Custom rule: **100102**, level 13, tailored to **additions**

## Deployed rule

Path on manager: `/var/ossec/etc/rules/privilege_escalation_rules.xml`. See [copy of validated XML source](./privilege_escalation_rules.xml).

```xml
<group name="windows,privilege_escalation_hunt,">
  <rule id="100102" level="13">
    <if_sid>60154</if_sid>
    <field name="win.system.eventID" type="pcre2">^4732$</field>
    <field name="win.eventdata.targetSid" type="pcre2">^S-1-5-32-544$</field>
    <description>Local Administrators addition: $(win.eventdata.memberSid) by $(win.eventdata.subjectUserName)</description>
    <mitre>
      <id>T1098.007</id>
    </mitre>
  </rule>
</group>
```

The `wazuh-analysisd -t` configuration check succeeded and `wazuh-manager` restarted with status `active`. The **actual custom alert** (rule 100102, level 13) was verified in Wazuh on a new, controlled Event 4732.

## Evidence-backed tests

| Scenario | Expected | Observed | Verdict |
| --- | --- | --- | --- |
| **Positive:** disabled `SOC-PrivEsc-Test` temporarily added to Administrators | Event 4732, rule 100102 | Event 4732, target `-544`, account SID ending `-1005`, `rule.id=100102`, `rule.level=13`; event record ID `1466264` | **PASS** |
| **Negative A:** same test account removed from Administrators | Event 4733 but not 100102 | 4733 present in Wazuh; combined filter of 100102 and 4733 yielded no results | **PASS** |
| **Negative B:** account added to a normal temporary group | Event 4732 but not 100102 | 4732, `SOC-NonAdmin-Test` target SID ending `-1006`, **rule 60144 / level 5** | **PASS** |
| Cleanup | No remaining admin test membership or temp normal group | PowerShell confirmed removed; account remained disabled; group deletion was logged as 4734 | **PASS** |

**Important qualifier:** This is a lab-based test of three specifically observed scenarios, not proof the rule is perfect or tuned for every production environment.

## Screenshot-backed validation

The following pairs show **event context and Wazuh rule outcome together**. The cropped rule-ID image alone is not sufficient to validate the positive detection.

- **Positive:** [Event 4732 + Administrators target](../screenshots/08-positive-event-fields.png) · [Event ID confirmation](../screenshots/08b-positive-event4732.png) · [custom rule 100102 / level 13](../screenshots/08c-positive-rule100102-level13.png).
- **Negative — removal:** [no 100102+4733 matches](../screenshots/10-negative-4733-no-custom-alert.png) **and** [4733 events ingested](../screenshots/10b-negative-4733-seen-in-wazuh.png).
- **Negative — ordinary group:** [normal group + Event 4732](../screenshots/11-nonadmin-addition-event4732.png) · [rule 60144 / level 5](../screenshots/12-negative-rule60144.png) · [description](../screenshots/12b-negative-rule60144-description.png).
- **Safe testing:** [PowerShell rollback](../screenshots/09-safe-final-end-state.png) · [final account deletion](../screenshots/18-final-test-account-deleted.png).

[Browse all 26 evidence files by stage](../screenshots/README.md).

## Why the negative tests matter

Event ID 4732 alone includes ordinary local group membership additions. Filtering specifically for the built-in `Administrators` target SID and the **addition** event reduces irrelevant alerts. A group removal event 4733 should not be labelled a new administrator grant.

## Triage and limitations

1. Validate 4732 + target group SID `-544`, identify host/actor/member and exact time.
2. Ask whether the change was approved; verify identity and reason, do not infer malice solely from a level 13 alert.
3. Correlate nearby 4624, 4672, relevant Sysmon process telemetry **where available**.
4. If unauthorised: preserve evidence, escalate and follow approved least-privilege/rollback procedures.
5. Watch for localised group names, benign administrator workflows, domain principals and potentially missing collection.

**Scope limitation:** all 26 screenshots are in the project evidence folder. A limited 4624/4672 identity/time query found no matches and Sysmon Event 1 supplied process creation context; neither proves that no other activity occurred. These lab tests do not establish production detection accuracy or cover every administrator workflow.
