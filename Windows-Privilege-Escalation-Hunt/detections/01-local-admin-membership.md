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

## Why the negative tests matter

Event ID 4732 alone includes ordinary local group membership additions. Filtering specifically for the built-in `Administrators` target SID and the **addition** event reduces irrelevant alerts. A group removal event 4733 should not be labelled a new administrator grant.

## Triage and limitations

1. Validate 4732 + target group SID `-544`, identify host/actor/member and exact time.
2. Ask whether the change was approved; verify identity and reason, do not infer malice solely from a level 13 alert.
3. Correlate nearby 4624, 4672, relevant Sysmon process telemetry **where available**.
4. If unauthorised: preserve evidence, escalate and follow approved least-privilege/rollback procedures.
5. Watch for localised group names, benign administrator workflows, domain principals and potentially missing collection.

**Known gaps:** final screenshot upload and cross-event logon/process correlation remain outstanding. This is not presented as a production deployment.
