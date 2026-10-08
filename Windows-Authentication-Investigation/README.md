# Project 2 — Windows Authentication Investigation

**Status:** **Complete — first portfolio version (8 October 2026).** Four correlation-rule tests and a separate failed-to-successful authentication investigation documented. Advanced detection tuning is future work.

## Objective

Investigate repeated Windows authentication failures using Wazuh, create and validate a custom rule for a suspicious failure pattern, distinguish authorised testing from an attack, and document defensive recommendations.

This is a separate portfolio project from [Project 1 — SOC Home Lab](../SOC-Home-Lab/).

## Lab and data sources

- Wazuh 4.14.8 manager in VirtualBox and a Windows endpoint with active Wazuh agent (`Windows-Host`)
- Windows Security Event ID **4625** (failed logon)
- Existing Wazuh rule **60122** (individual login failure)
- Two dedicated local, non-administrator test accounts **SOC-Lab-Test** and **SOC-Lab-Test2**
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
8. **Mixed-account test:** at **17:18:01.232** and **17:18:03.330**, two rule `60122` events had target `SOC-Lab-Test`; at **17:18:07.360**, a third rule `60122` event had target `SOC-Lab-Test2`. No new `100101` alert appeared in the test window. This supports username-specific correlation.
9. **Second-account positive test:** a level-10 `100101` alert appeared at **17:30:13.110**. The expanded alert showed Windows Event ID `4625`, `targetUserName: SOC-Lab-Test2`, and incorrect-password substatus `0xC000006A`, confirming that the custom rule can fire on another account independently.
10. **Investigation 02:** two `4625` failures for `SOC-Lab-Test2` at 18:01:21 and 18:01:26 were correlated with a `4624` successful interactive login at 18:01:33. Nearby command-shell-related alerts were reviewed but not conclusively attributed to this session. The sign-in was an authorised local test.

## Key evidence

- `targetUserName: SOC-Lab-Test`
- `data.win.system.eventID: 4625`
- `data.win.eventdata.logonType: 2` (interactive logon)
- `data.win.eventdata.ipAddress: 127.0.0.1` (local loopback source for the observed event)
- `status: 0xC000006D`; `subStatus: 0xC000006A` (incorrect password)
- Custom rule `100101`, level 10, mapped to MITRE ATT&CK **T1110 — Brute Force**

## Evidence at a glance

**26 curated PNGs** are on GitHub: 19 from Investigation 01 and seven supporting Investigation 02. All are linked in the [Project 2 visual evidence index](./screenshots/README.md). A [reconstructed timeline](./evidence/02-authentication-timeline.md) explains which observations each image supports and where screenshots alone are incomplete. Two low-value cropped fragments were removed; image 25 (McAfee BrowserHost.exe process details) was not uploaded. See the [audit manifest](./evidence/INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md).

| Scenario | Direct evidence | Outcome |
| --- | --- | --- |
| Lab setup and custom rule | [Wazuh XML](./screenshots/04-custom-rule-100101.png) · [Manager status](./screenshots/05-manager-active.png) | Rule deployed |
| First-account positive | [Alert](./screenshots/06-positive-100101-alert.png) · [Details](./screenshots/07-positive-alert-details.png) | Passed |
| Single-failure negative | [Failure alert](./screenshots/08-negative-60122-alert.png) · [Username](./screenshots/09-negative-test-account.png) | Passed in reviewed window |
| Mixed-account negative (2+1) | [Individual failures](./screenshots/10-mixed-account-three-failures.png) · [No correlated alert](./screenshots/13-mixed-account-no-correlation.png) | Passed in reviewed window |
| Second-account positive | [Alert](./screenshots/14-second-account-positive-alert.png) · [Username](./screenshots/15-second-account-alert-user.png) | Passed |
| Failed → successful authentication | [Two failed-login rows](./screenshots/20-two-failures-targeted-account.png) · [Success](./screenshots/17-test-account-success-list.png) · [Target account](./screenshots/19-success-target-username.png) · [Investigation 02](./investigations/02-failed-then-successful-login.md) | Authorised sequence documented; source-event crops are not complete exports |

![Custom Wazuh rule 100101 successfully detected a controlled burst of failures](./screenshots/06-positive-100101-alert.png)

## Interpretation and limitations

The rule correctly detected the controlled repeated-failure pattern, did not fire on the single-failure negative test observed, and did not combine two failures for one test account with one failure for a different test account. This is **initial lab validation**, not proof of a production-ready detection.

Because the activity was authorised, its operational classification is **Benign Positive**; as a rule-validation test, it demonstrated a true-positive match for the intentionally generated pattern. The MITRE T1110 label reflects the detection's intended behaviour, **not proof that a real attacker was present**.

**Scope limitations and optional future improvements:**

- Three mistyped passwords by a real employee could also trigger the rule.
- Matching on username alone can combine attempts from different source IPs; investigate source separately.
- Both account-specific positive tests and the mixed-account 2+1 case are complete; timing-boundary, repeated-burst and real remote authentication telemetry tests remain outside the current test scope.
- Verify alert counts, time windows and Wazuh correlation behaviour under additional scenarios.
- All **26 retained evidence screenshots** are uploaded and grouped by investigation and scenario in the [evidence index](./screenshots/README.md). The McAfee process-detail image remains missing.

## Documentation

- [Detection design and test](./detections/01-brute-force-correlation.md)
- [Investigation 01 — controlled failure detection](./investigations/01-controlled-login-attempts.md)
- [Investigation 02 — failed then successful login](./investigations/02-failed-then-successful-login.md)
- [Investigation 02 evidence timeline (transcribed)](./evidence/02-authentication-timeline.md)
- [SOC triage and response playbook](./response/01-authentication-alert-triage-playbook.md)
- [Final project summary](./FINAL-PROJECT-SUMMARY.md)
- [Evidence index — 26 curated screenshots](./screenshots/README.md)
- [Interview summary](./INTERVIEW-SUMMARY.md)
- [Project 2 essential memorisation notes](./notes/WHAT-TO-MEMORISE.md)
- [Combined Project 1 + Project 2 daily 40 flashcards](../study/SOC-FLASHCARDS-PROJECTS-1-2.md)
- [Project 2-only learning review](./notes/LEARNING-REVIEW.md)
- [Investigation 02 image-by-image audit and missing-image checklist](./evidence/INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md)

## Analyst approach

Validate -> Identify -> Correlate -> Scope -> Classify.

In a genuine incident, review account identity, source IP/device, logon type, failure count/time distribution, related successful logins (4624), and actions after any success before escalating or containing.

**First-version completion note:** Core planned local authentication detection, validation, investigation and reporting are complete. This status does **not** certify production readiness or comprehensive post-login forensic coverage.
