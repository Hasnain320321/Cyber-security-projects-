# Project 2 — Final Portfolio Summary

**Project:** Windows Authentication Investigation and Brute-Force Detection with Wazuh  
**Portfolio version:** 1.0 — completed 8 October 2026  
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

- [All 19 uploaded screenshots from the initial detection-testing investigation](./screenshots/README.md)
- [Investigation 01](./investigations/01-controlled-login-attempts.md)
- [Investigation 02](./investigations/02-failed-then-successful-login.md) and [transcribed timeline](./evidence/02-authentication-timeline.md)
- [Custom rule XML and validation table](./detections/01-brute-force-correlation.md)
- [Triage and response playbook](./response/01-authentication-alert-triage-playbook.md)
- [Interview summary](./INTERVIEW-SUMMARY.md)
- [Learning review: five anchors and 20 flashcards](./notes/LEARNING-REVIEW.md)

**Evidence boundary:** All 19 screenshots in GitHub belong to the first investigation. The second investigation's screenshots were reviewed in the session but are currently represented in the repository only by a clearly-labelled reconstructed timeline and write-up.

## Conclusion

The project successfully demonstrates entry-level SOC skills in Windows log analysis, Wazuh alert triage, rule authoring, event correlation, controlled testing and benign activity classification. The repeated failures were deliberately generated, and the failed-then-successful sequence was performed by the authorised lab user. No real-world compromise was demonstrated.

## Limitations and future improvements (not required for v1.0)

- Correlation threshold is low for production and can fire for an employee mistyping a password.
- Tests were local interactive logons (Type 2); network/RDP attacks and distributed sources were not validated.
- Usernames were used for grouping; source-IP independence, window boundaries, and lockouts deserve additional testing.
- Supplemental original PNG evidence for the second investigation would strengthen the portfolio.
- Expand follow-on process/user correlation and adopt an incident ticket format for a future iteration.

This is a **completed first portfolio version**, not a claim that the detection is production-ready.
