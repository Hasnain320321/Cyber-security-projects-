# Analyst playbook — encoded PowerShell alert

## 1. Validate

Confirm endpoint, timestamp, rule ID, Sysmon Event ID 1 and exact command line. Check whether the event is an approved lab/deployment task. Preserve the original command line and event identifiers before investigating.

## 2. Identify

Review image, parentImage, parentCommandLine, user, integrity level, ProcessGuid and ParentProcessGuid. Prefer process GUIDs when correlating over time; PIDs can be reused. An elevated process is context, not proof of abuse.

## 3. Decode safely

Extract only the Base64 argument and decode it as UTF-16LE text in an isolated analysis workflow. Do not invoke the decoded content or pipe it to Invoke-Expression. Base64 is an encoding, not encryption. Malformed or unexpectedly layered content needs further analysis. In this lab the known payload was Write-Output 'PROJECT7_ENCODED_TEST'.

## 4. Correlate and scope

Review nearby child-process, file, network, authentication, EDR and available PowerShell script-block events. Query related ProcessGuid/user/host and a justified time window. These are recommended next steps; they were not all performed in this project. Search across endpoints if real incident evidence warrants it.

## 5. Classify

Document observed facts separately from inference. Known approved test with matching behaviour = benign positive. An unexpected encoded command is an investigation lead. Determine whether it is authorised administration, a rule false positive, suspicious unconfirmed activity or a corroborated malicious incident.

## 6. Respond and tune

For the known lab test, record the evidence and close without containment. For corroborated unauthorised activity, preserve evidence, escalate and apply the organisation's approved endpoint containment and account response procedures. Do not isolate systems solely because Base64 appears. Consider scoped exceptions only with a verified business reason; track ownership and expiry and rerun detection/control tests after changes.
