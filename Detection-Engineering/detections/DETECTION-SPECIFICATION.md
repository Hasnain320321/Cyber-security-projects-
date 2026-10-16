# Detection specification — DE-007

## Hypothesis and data

Within nested Windows PowerShell process creation, an encoded-command switch warrants review because it obscures the visible script text. Legitimate automation can use the same feature. This rule identifies syntax and ancestry, not malicious intent.

Required input: Sysmon Event ID 1 collected by the Windows Wazuh agent, with image, commandLine and parentImage. The final parent rules provide the narrower process-creation context. Wazuh dashboard fields have a data. prefix (data.win.eventdata.commandLine); XML decoder fields use win.eventdata.commandLine.

## Rule contract

- ID **100107**; level **12**; same severity as the observed encoded-command built-in parent.
- if_sid **92027,92057**: eligible when either installed parent matches the same event; this is not a temporal correlation or a requirement for two prior alerts.
- Image suffix: powershell.exe or pwsh.exe, case insensitive.
- Command line: whitespace/start, hyphen, exactly enc or EncodedCommand, whitespace/end. Case insensitive.
- MITRE **T1059.001**, Execution. No additional evasion mapping is claimed merely because Base64 was used.
- Final executable rule: [powershell_encoded_command.xml](powershell_encoded_command.xml).

## Observed tuning sequence

| Revision | Change | Observed outcome |
| --- | --- | --- |
| Initial | sysmon_event1 parent group, full switch only, level 7 | Custom rule did not win; full-switch event appeared under 92057 / 12 |
| Full-switch refinement | Child of 92057; retain full-switch match; level 12 | 100107 matched full-switch test at 22:26:29; ordinary control remained 92027 / 4 |
| Coverage test | Ran same harmless encoded text with -enc | Event reached Wazuh but showed generic 92027 / 4; custom version missed it |
| Final | Parent IDs 92027 and 92057; match enc or EncodedCommand | -enc produced 100107 / 12; full-switch and negative regression checks passed |

The installed 92057 XML itself uses sysmon_event1, so that group name was valid. A mismatch between final alert groups and the original dependency group was not a valid root-cause explanation. The observations demonstrate a rule hierarchy/selection interaction; no exhaustive engine trace was captured to prove its internals. Adjusting the command-line regex alone would not address an event that remained on the 92027 branch.

## Deployment and rollback

The existing local_rules.xml was backed up outside the loaded rules directory to /var/ossec/etc/local_rules.before-project7.xml. Proposed ID 100107 was searched in /var/ossec/etc/rules/ and no match appeared. The Project 7 group was appended while preserving existing rules. Configuration checking used sudo /var/ossec/bin/wazuh-analysisd -t; initial validation returned without visible errors. The manager was restarted and shown active; later live alerts confirm the final rule loaded. There is no separate captured final validation exit-code record.

For a future deployment, validate the XML against the installed rules, confirm no duplicate ID, test matching and nonmatching events, then restart the manager and check health. To remove this lab rule, remove only its Project 7 group, validate and restart; avoid blindly restoring an old entire file after unrelated rule changes.

## False positives and tuning policy

Approved deployment scripts and administration may legitimately use encoded PowerShell. Review the decoded text, parent chain, user, expected task and surrounding telemetry. No production allowlist or alert-rate tuning was implemented. If later justified, make exceptions narrow, documented, owned and time-bounded; avoid blanket exclusions for PowerShell, administrators or an entire endpoint.

## Known limits

Two switch tokens are covered by the custom expression, not every PowerShell abbreviation. Parent rules constrain scope; an executable regex alone cannot widen inherited parent conditions. No measured detection rate or false-positive rate is available from three final lab checks. A nonmatching event is evidence for that control only, not proof that all normal PowerShell is excluded.

## References

- [Wazuh rules syntax](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html)
- [Wazuh custom rules](https://documentation.wazuh.com/current/user-manual/ruleset/rules/custom.html)
- [Wazuh analysisd validation](https://documentation.wazuh.com/current/user-manual/reference/daemons/wazuh-analysisd.html)
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [MITRE ATT&CK T1059.001](https://attack.mitre.org/techniques/T1059/001/)
