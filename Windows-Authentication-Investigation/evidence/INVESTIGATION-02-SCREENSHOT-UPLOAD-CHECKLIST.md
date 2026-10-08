# Investigation 02 — Additional Screenshot Evidence Upload Checklist

**Status:** Prepared from the original Wazuh screenshots shared on 8 October 2026; **not yet committed to GitHub**.

**Location when uploaded:** `Windows-Authentication-Investigation/screenshots/`.

The project's first 19 verified images (01–15, including lettered subnumbers) support Investigation 01 and **must not be renamed, overwritten, or removed**. These 10 proposed new PNGs are distinct, numbered 16–25, for Investigation 02. No Project 1 path is involved.

## What each new screenshot should demonstrate

| Planned filename | Evidence | Investigation phase |
| --- | --- | --- |
| `16-failed-logins-overview.png` | 4625 failure list near 18:01 | Establish timestamp candidates |
| `17-test-account-success-list.png` | Filtered successful-logon results for the lab account | Find successful event |
| `18-success-logon-type-and-ip.png` | 4624 with Logon Type 2 and loopback IP | Identify source and method |
| `19-success-target-username.png` | Target username SOC-Lab-Test2 | Confirm account identity |
| `20-two-failures-targeted-account.png` | 18:01:21 and 18:01:26 failed logins | Correlate failures to success |
| `21-separate-webview-failure-process.png` | Different later 4625 process entry | Investigate adjacent event separately |
| `22-separate-failure-context.png` | Context for later event | Do not over-attribute |
| `23-separate-failure-rule.png` | Wazuh 60122 for later event | Detection details |
| `24-nearby-sysmon-process-alerts.png` | Nearby CMD-related alert list | Post-login scoping (unattributed) |
| `25-mcafee-webadvisor-process-details.png` | BrowserHost.exe, McAfee metadata/command line | Process attribution caution |

## Accuracy safeguards

1. The two filtered 4625 events and 4624 success are for **SOC-Lab-Test2**.
2. The McAfee WebAdvisor-related event is **not proven to be caused by that account's sign-in**. Keep the report's caveat.
3. The additional 18:01:48 failure's target account is **not established** in supplied field screenshots.
4. The existing 19 PNGs support Detection/Investigation 01. Don't move them into Investigation 02.
5. These are image captures, not a raw Windows EVTX export.
6. Review these images for personally identifying information before publishing to the public repository.

## Upload workflow

1. Download and extract the prepared Investigation 02 ZIP supplied in the conversation.
2. Open GitHub at **Windows-Authentication-Investigation -> screenshots**.
3. Select **Add file -> Upload files** and choose only the ten PNGs named 16–25 from the extracted folder.
4. Confirm all ten names and the correct directory, then commit directly to `main`.
5. Verify each new image opens. Update the screenshot evidence index to link those files and mark them uploaded.

This checklist remains **pending** until those PNGs appear in the live repository.
