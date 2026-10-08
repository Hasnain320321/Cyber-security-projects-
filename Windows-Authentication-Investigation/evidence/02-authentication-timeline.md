# Investigation 02 — Reconstructed Evidence Timeline

**Evidence type:** Manual transcription of screenshots reviewed during the 8 October 2026 lab session; **not** an original Wazuh export or independently captured raw log.  
**Scope:** Project 2 only. No screenshots of Investigation 02 have been committed to this folder as original PNG evidence.

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

## Additional original screenshot upload status

Ten distinct original Wazuh screenshots numbered 16–25 have been prepared for manual upload into the dedicated Project 2 screenshots folder. See the [Investigation 02 screenshot evidence checklist](./INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md). **At the time of this writing, they remain pending; this timeline is a transcription, not a substitute for original screenshots.**

## Original evidence boundaries

The [Project 2 screenshot index](../screenshots/README.md) contains **19 GitHub-hosted images for the first investigation**. The second investigation was supported by screenshots submitted in the ChatGPT conversation; those separate PNGs were **not uploaded into GitHub**. This markdown record makes the distinction explicit.

See [Investigation 02](../investigations/02-failed-then-successful-login.md) for methodology, response and conclusions.
