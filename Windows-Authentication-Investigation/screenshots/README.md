# Project 2 — Wazuh Evidence Index

**Status:** All **19 PNG screenshots uploaded to this directory** and verified against the Project 2 GitHub upload commit of 8 October 2026. Every image belongs to `Windows-Authentication-Investigation/screenshots/`; **Project 1 (`SOC-Home-Lab/`) is unchanged**.

These 19 screenshots support **Investigation 01** (custom brute-force detection tests). The additional Investigation 02 evidence is [listed separately as pending upload](../evidence/INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md); do not interpret its checklist as confirmation those ten PNGs exist in GitHub. They are stored together in one dedicated evidence folder, but organised **by investigation phase below**. The detection and investigation reports link directly to the relevant images so reviewers do not need to browse them in filename order.

## 1. Lab setup and rule configuration (4 images)

| Evidence | What it demonstrates |
| --- | --- |
| [01 — Wazuh agent running](./01-wazuh-agent-running.png) | Windows agent visible in Wazuh |
| [02 — Test account created](./02-test-account-created.png) | Dedicated local `SOC-Lab-Test` account |
| [04 — Custom Wazuh rule](./04-custom-rule-100101.png) | XML logic for rule `100101`, added without replacing the Project 1 rule |
| [05 — Wazuh Manager running](./05-manager-active.png) | Service active after the rules were loaded |

## 2. Initial failed-logon analysis and positive test (6 images)

| Evidence | What it demonstrates |
| --- | --- |
| [03 — Three individual failures](./03-three-individual-failures.png) | Three level-5 `60122` alerts |
| [03a — Target username and 4625](./03a-target-username-event4625.png) | Windows Security Event ID `4625` and targeted test account |
| [03b — Source and logon type](./03b-source-and-logontype.png) | Loopback source `127.0.0.1` and local interactive Logon Type 2 |
| [06 — Correlated Level 10 alert](./06-positive-100101-alert.png) | `100101` triggered at 16:47:18 |
| [07 — Correlation details](./07-positive-alert-details.png) | Frequency and `previous_output` evidence |
| [07a — MITRE mapping](./07a-positive-mitre-mapping.png) | T1110 mapping on the custom rule; **not evidence of a real attacker** |

**Representative positive-test alert:**

![Wazuh rule 100101 generated for the controlled three-failure test](./06-positive-100101-alert.png)

## 3. Isolated single-failure negative test (2 images)

| Evidence | What it demonstrates |
| --- | --- |
| [08 — Single 60122 failure](./08-negative-60122-alert.png) | One ordinary failed login at 16:55:28, without a new correlation alert in the reviewed window |
| [09 — Single failure target account](./09-negative-test-account.png) | Target account `SOC-Lab-Test` |

## 4. Mixed-account negative test, two-plus-one (5 images)

| Evidence | What it demonstrates |
| --- | --- |
| [10 — Three 60122 failures](./10-mixed-account-three-failures.png) | Events at 17:18:01, 17:18:03 and 17:18:07 |
| [11 — Account 1, first failure](./11-mixed-account-user-one-first.png) | First event targeted `SOC-Lab-Test` |
| [11a — Account 1, second failure](./11a-mixed-account-user-one-second.png) | Second event targeted `SOC-Lab-Test` |
| [12 — Account 2, one failure](./12-mixed-account-user-two.png) | Third event targeted `SOC-Lab-Test2` |
| [13 — No new correlation alert](./13-mixed-account-no-correlation.png) | `100101` query returned no results in the test window |

**Representative negative-test search:**

![No rule 100101 alert observed for the mixed-account two-plus-one test](./13-mixed-account-no-correlation.png)

## 5. Independent positive test on second account (2 images)

| Evidence | What it demonstrates |
| --- | --- |
| [14 — Second account rule 100101](./14-second-account-positive-alert.png) | New level-10 correlated alert at 17:30:13 |
| [15 — Second account identified](./15-second-account-alert-user.png) | Expanded `4625` event targeted `SOC-Lab-Test2` |

**Representative second-account positive test:**

![Custom rule 100101 triggered again for a different test account](./14-second-account-positive-alert.png)

## How to interpret the evidence

Four controlled validation scenarios were completed on 8 October 2026: **two positive tests** against separate accounts, **one isolated negative**, and **one mixed-account 2+1 negative**. These demonstrate initial rule behaviour in the local lab, not production readiness or a real compromise.

- [Detection design and validation](../detections/01-brute-force-correlation.md)
- [Investigation 01 — detection validation](../investigations/01-controlled-login-attempts.md)
- [Investigation 02 — failed-to-successful login](../investigations/02-failed-then-successful-login.md), with [textual evidence timeline](../evidence/02-authentication-timeline.md) (separate screenshots not yet uploaded)
- [Project 2 overview](../README.md)
- [Interview summary](../INTERVIEW-SUMMARY.md)
- [Project 2 memory notes](../notes/WHAT-TO-MEMORISE.md)
- [Combined Project 1 + 2 20-card review](../../study/SOC-FLASHCARDS-PROJECTS-1-2.md)

**Privacy note:** The repository is public. Screenshots show lab host/account identifiers; review public images periodically for sensitive information. No passwords should be included.
