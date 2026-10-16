# DE-007 — Encoded PowerShell detection validation

**Date:** 16 October 2026. **Disposition:** authorised lab / benign positive. **Project status:** complete for the documented scope.

## Question

Can a custom Wazuh rule identify the two tested encoded-command forms in a PowerShell-to-PowerShell process chain, while preserving ordinary command execution as a nonmatch?

## Evidence and reasoning

The baseline event established that Windows-Host process telemetry reached Wazuh. The executable and parent were Windows PowerShell, and the command line included PROJECT7_BASELINE. Sysmon Event ID 1 and process context were inspected.

An initial full-switch encoded test appeared under built-in 92057, level 12. Refining the custom rule as a child of that installed rule produced 100107 at level 12. An ordinary command control remained under 92027 at level 4.

Testing -enc then revealed a custom coverage gap. Its process event was present, but the final alert was generic nested-PowerShell rule 92027 at level 4. The final change allowed either 92027 or 92057 as parent and matched either enc or EncodedCommand as the switch token. A new -enc test produced 100107 at 22:41:18 BST. Full-switch regression produced 100107 at 22:43:05; the final ordinary control produced 92027 at 22:43:13.

## Classification

The positives are **benign positives**: the rule correctly identified the intended encoded-command behaviour, generated with permission and a harmless Write-Output payload. An alert level of 12 and ATT&CK T1059.001 describe detection priority and technique context, not proven attacker intent. The negative test is a nonmatch for the custom encoded-command detection; it may still appropriately appear as a different generic alert.

## Findings

1. Collection worked for the reviewed tests.
2. The final custom rule matched the two tested switches in the observed ancestry.
3. A meaningful tuning gap was found and retested, rather than assuming that one successful test proved coverage.
4. The collected ordinary-command control did not match the final custom rule.
5. Coverage remains dependent on the installed parent rules and command-line visibility.

## Impact and response

No unauthorised execution, persistence, data theft, external connection or host compromise was demonstrated. No containment was needed for the authorised test. For an unexpected real alert, preserve telemetry and follow the [triage playbook](../playbooks/POWERSHELL-TRIAGE.md); response depends on decoded content, authorisation and corroborating activity.

## Evidence integrity and limits

[Fourteen original PNG screenshots](../screenshots/README.md) were selected from the session, renamed descriptively without altering image bytes, and fingerprinted with SHA-256 and Git blob hashes. Navigation-only images and redundant interim views were excluded. Earlier configuration screenshots are explicitly historical, not the final deployed XML. The final-rule screenshot is an editor view with the bottom cropped; runtime alerts support deployment. Native event logs were not exported. The final XML file is a transcription of the displayed configuration and tested changes, not a downloaded manager file.

The final command-detail images do not carry event IDs or timestamps in their crops; association with the matching overview rows follows the guided row-opening sequence. No universal detection coverage, production precision, arbitrary parent support or PowerShell 7 validation is claimed.

## Lessons learned

Validate collection before debugging detection logic. Inspect installed parent rules. Test alternative syntax. Keep severity deliberate. Treat a missing custom alert differently from a missing event. Repeat both positive and negative checks after tuning, and document the exact boundary of the result.
