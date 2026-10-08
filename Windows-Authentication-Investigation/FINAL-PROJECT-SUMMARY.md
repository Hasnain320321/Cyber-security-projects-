# Project 2 — Final Portfolio Summary

**Project:** Windows Authentication Investigation and Brute-Force Detection with Wazuh  
**Status:** Complete — 8 October 2026  
**Scope:** Home lab; authorised local tests, not a simulated remote adversary or production deployment.

## Objective

Build and validate a Wazuh rule to detect bursts of Windows authentication failures, investigate identity-related alerts, and explain how an SOC analyst distinguishes potentially hostile behaviour from legitimate user activity.

## Lab implementation

- Wazuh Manager 4.14.8 VM in VirtualBox and active Wazuh agent on `Windows-Host`
- Local non-administrator test users: `SOC-Lab-Test`, `SOC-Lab-Test2`
- Windows Security log events `4625` / `4624` and supporting Sysmon process telemetry
- Individual Wazuh failure rule `60122`, success rule `60118`
- Custom Wazuh XML correlation rule `100101`: `frequency=3`, `timeframe=60`, username grouping, level 10, mapped to ATT&CK **T1110**

## Practical outcomes

| Workstream | Verified outcome |
| --- | --- |
| Detection engineering | Rule 100101 saved, manager restarted and alert generated |
| Positive test 1 | Three failed logins for first test account -> correlated level-10 alert |
| Negative test 1 | One wrong password -> individual `60122`, no new correlated alert in reviewed window |
| Negative test 2 | 2+1 failures split across accounts -> no correlated alert in reviewed window |
| Positive test 2 | Three failures for second test account -> new correlated level-10 alert |
| Authentication investigation | Two `4625` failures for `SOC-Lab-Test2` at 18:01:21/26 followed by `4624` success at 18:01:33 for the same account; Logon Type 2 |
| Post-login triage | Nearby shell-related alerts were reviewed; McAfee WebAdvisor BrowserHost.exe appears in expanded telemetry, but the alerted process was **not proven to be initiated by the logged-in test account** |
| Reporting | Two investigations, detection design, response playbook, learning points, interview summary and evidence index |

## Evidence

- [All 26 curated screenshots — 19 from Investigation 01 and 7 from Investigation 02](./screenshots/README.md)
- [Investigation 01](./investigations/01-controlled-login-attempts.md)
- [Investigation 02](./investigations/02-failed-then-successful-login.md) and [transcribed timeline](./evidence/02-authentication-timeline.md)
- [Custom rule XML and validation table](./detections/01-brute-force-correlation.md)
- [Triage and response playbook](./response/01-authentication-alert-triage-playbook.md)
- [Expanded interview summary, including a 60-second explanation and 12 interview questions](./INTERVIEW-SUMMARY.md)
- [Project 2 memorisation notes](./notes/WHAT-TO-MEMORISE.md)
- [Combined 40-card revision deck: 20 per project](../study/SOC-FLASHCARDS-PROJECTS-1-2.md)
- [Investigation 02 screenshot audit and missing-image checklist](./evidence/INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md)
- [Learning review: five anchors and 20 flashcards](./notes/LEARNING-REVIEW.md)

**Evidence boundary:** GitHub now hosts **26 curated images: 19 from Investigation 01 and 7 from Investigation 02**. The second investigation also includes a textual reconstruction of the observed timeline. Its cropped failure-alert image does not display the username filter, and the McAfee BrowserHost.exe detail image has not been uploaded. These limitations are explicitly recorded rather than presenting the screenshots as complete forensic logs.

## Conclusion

The project successfully demonstrates entry-level SOC skills in Windows log analysis, Wazuh alert triage, rule authoring, event correlation, controlled testing and benign activity classification. The repeated failures were deliberately generated, and the failed-then-successful sequence was performed by the authorised lab user. No real-world compromise was demonstrated.

## Limitations and optional future improvements

- Correlation threshold is low for production and can fire for an employee mistyping a password.
- Tests were local interactive logons (Type 2); network/RDP attacks and distributed sources were not validated.
- Usernames were used for grouping; source-IP independence, window boundaries, and lockouts deserve additional testing.
- Uploading the missing `25-mcafee-webadvisor-process-details.png` and an uncropped failure-query screenshot showing the `targetUserName` filter would strengthen proof of Investigation 02, but these are outside the completed project scope.
- Expand follow-on process/user correlation and adopt an incident ticket format for a future iteration.

This project is **Complete**. Its local lab detection is not presented as production-ready.
