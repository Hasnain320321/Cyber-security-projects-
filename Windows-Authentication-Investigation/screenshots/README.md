# Project 2 — Evidence Screenshots

**Status:** 19 original screenshots prepared in an upload-ready ZIP archive. The PNG files have **not yet been committed** to GitHub. This README is the evidence manifest, not proof of image upload.

All files belong under `Windows-Authentication-Investigation/screenshots/`. **Do not touch `SOC-Home-Lab/` (Project 1).**

| Filename in evidence archive | What it proves |
| --- | --- |
| `01-wazuh-agent-running.png` | Wazuh agent active in dashboard |
| `02-test-account-created.png` | Dedicated local account `SOC-Lab-Test` |
| `03-three-individual-failures.png` | Three individual 60122 events |
| `03a-target-username-event4625.png` | Windows Event 4625 and target account |
| `03b-source-and-logontype.png` | Event's loopback source and Logon Type 2 |
| `04-custom-rule-100101.png` | New XML correlation rule below existing rules |
| `05-manager-active.png` | Wazuh manager service active after restart |
| `06-positive-100101-alert.png` | Initial positive test: rule 100101 alert |
| `07-positive-alert-details.png` | Level 10 correlation, frequency and previous output |
| `07a-positive-mitre-mapping.png` | Rule's MITRE T1110 mapping |
| `08-negative-60122-alert.png` | Isolated failed login, rule 60122 |
| `09-negative-test-account.png` | Isolated event targeted `SOC-Lab-Test` |
| `10-mixed-account-three-failures.png` | Three 60122 events from mixed-account test |
| `11-mixed-account-user-one-first.png` | First failure targeted `SOC-Lab-Test` |
| `11a-mixed-account-user-one-second.png` | Second failure targeted `SOC-Lab-Test` |
| `12-mixed-account-user-two.png` | Third failure targeted `SOC-Lab-Test2` |
| `13-mixed-account-no-correlation.png` | No new custom 100101 alert during 2+1 mix |
| `14-second-account-positive-alert.png` | Custom 100101 alert for second account test |
| `15-second-account-alert-user.png` | Expanded custom alert targets `SOC-Lab-Test2` |

## Interpretation

Four validation scenarios were completed on 8 October 2026: two positive tests, one isolated negative and one mixed-account negative. Screenshots should be interpreted together with the [detection write-up](../detections/01-brute-force-correlation.md) and [investigation](../investigations/01-controlled-login-attempts.md).

**The images are currently in the separately prepared evidence archive, not this GitHub directory.** Upload the images to this exact directory, then verify they render. Before committing to a public repository, review screenshots for any personal usernames, machine names or other information you do not wish to publish.
