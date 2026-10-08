# Investigation 02 — Reconstructed Evidence Timeline

**Evidence type:** Manual transcription of screenshots reviewed during the 8 October 2026 lab session; **not** an original Wazuh export or independently captured raw log.  
**Scope:** Project 2 only. **Seven Investigation 02 screenshot excerpts are committed to GitHub** under the [evidence index](../screenshots/README.md). These are excerpts, not a complete event export.

## Confirmed account correlation

| Local dashboard time | Account | Windows Event ID | Wazuh rule | Basis |
| --- | --- | --- | --- | --- |
| 2026-10-08 18:01:21.619 | `SOC-Lab-Test2` | `4625` | `60122` | Username + Event ID filters on Wazuh Events returned event |
| 2026-10-08 18:01:26.110 | `SOC-Lab-Test2` | `4625` | `60122` | Same filtered query |
| 2026-10-08 18:01:33.061 | `SOC-Lab-Test2` | `4624` | `60118` | Expanded event: target username, Logon Type 2 and `127.0.0.1` |
| 2026-10-08 18:01:47.591 / .626 | Unverified | Sysmon process alert(s) | `92052`, `92032` | Alert list; expanded process fields show McAfee WebAdvisor BrowserHost.exe, but account correlation not established |
| 2026-10-08 18:01:48.480 | Target account not established | `4625` | `60122` | Expanded event includes `msedgewebview2.exe` process, no target username in submitted screenshots |

## Other observed alerts (not attributed to test account)

- `18:00:33.688`: Wazuh rule `92058`, application compatibility database launched; **before** the successful test-account logon.
- `18:01:41.070`: a Windows `4624` event for the user's main Microsoft-account session with Logon Type `7` (unlock), **not** `SOC-Lab-Test2`.

## Interpretation

The **same test account** had two failed sign-ins followed by a successful local interactive login. The sequence was user-authorised testing. Nearby process alerts were not proven to belong to that account. No unauthorised authentication or compromise can be established from the reviewed evidence.

## Visual exhibits from this investigation

| Observed evidence | Screenshot |
| --- | --- |
| Wider failed-login list | [16 — failure overview](../screenshots/16-failed-logins-overview.png) |
| `60118` success alert at 18:01:33 | [17 — successful logons](../screenshots/17-test-account-success-list.png) |
| Source loopback / Logon Type 2 | [18 — successful event context](../screenshots/18-success-logon-type-and-ip.png) |
| Confirmed `SOC-Lab-Test2` target | [19 — successful target username](../screenshots/19-success-target-username.png) |
| Two prior `60122` failures | [20 — two failed events](../screenshots/20-two-failures-targeted-account.png) |
| Later separate `4625` process details | [21 — WebView2-linked event](../screenshots/21-separate-webview-failure-process.png) |
| Nearby process alert names | [24 — process alert list](../screenshots/24-nearby-sysmon-process-alerts.png) |

**Important:** The two rows in screenshot 20 do not display the `targetUserName` filter. The account match was established during the live filtered Wazuh query, but that particular PNG is not a full proof of the username. The McAfee process-detail screenshot (`25`) is still missing from the public repository; see the [verified upload checklist](./INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md).



## Original evidence boundaries

The [Project 2 screenshot index](../screenshots/README.md) currently covers **19 images for Investigation 01 and 7 for Investigation 02**. It is a curated set of screenshot excerpts, not raw EVTX evidence. McAfee process detail image 25 remains absent.

See [Investigation 02](../investigations/02-failed-then-successful-login.md) for methodology, response and conclusions.
