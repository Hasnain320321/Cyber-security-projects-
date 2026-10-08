# Project 2 — Evidence Screenshots

**Status:** Screenshot files not yet committed. This is the planned evidence checklist, not a claim that images are present in the repository.

When capturing screenshots from the test, keep timestamps and rule IDs visible, and avoid exposing passwords or other unnecessary personal information.

| Proposed filename | Evidence required |
| --- | --- |
| `01-wazuh-agent-running.png` | Active Wazuh manager/agent status |
| `02-test-account-created.png` | `SOC-Lab-Test` local account |
| `03-single-failed-logon-fields.png` | `4625`, target username, logon type, source and substatus |
| `04-custom-rule-100101.png` | New XML rule below existing Project 1 rule |
| `05-manager-active.png` | Wazuh manager running after restart |
| `06-positive-100101-alert.png` | 8 Oct 2026 16:47:18 level-10 alert |
| `07-positive-alert-details.png` | Rule `100101`, frequency 3 and MITRE T1110 |
| `08-negative-60122-alert.png` | 8 Oct 2026 16:55:28 `60122` alert |
| `09-negative-test-account.png` | `targetUserName: SOC-Lab-Test` on isolated failed logon |

## Interpretation

The positive test confirms the intended alert was generated. The negative test did not generate a fresh custom alert in the observed window. This does not replace additional production-quality tests.

Related documents: [Detection](../detections/01-brute-force-correlation.md) · [Investigation](../investigations/01-controlled-login-attempts.md).
