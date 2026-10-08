# Investigation 02 — Screenshot Review and Evidence Manifest

**Audited:** 8 October 2026 against the live GitHub files. **Seven Investigation 02 PNGs are currently retained and published. One important PNG remains missing.**

**Location:** [Project 2 screenshots](../screenshots/README.md) under `Windows-Authentication-Investigation/screenshots/`.

The 19 original images from Investigation 01 remain in place. **Do not modify Project 1 (`SOC-Home-Lab/`).**

## Audit disposition for the ten originally prepared PNGs

| Original filename | Decision | Explanation |
| --- | --- | --- |
| [16-failed-logins-overview.png](../screenshots/16-failed-logins-overview.png) | **Keep** | Context: observed failure timestamps, but no usernames in the crop |
| [17-test-account-success-list.png](../screenshots/17-test-account-success-list.png) | **Keep** | Includes success at 18:01:33, Wazuh rule 60118 |
| [18-success-logon-type-and-ip.png](../screenshots/18-success-logon-type-and-ip.png) | **Keep** | Expanded event shows interactive Type 2 and loopback IP |
| [19-success-target-username.png](../screenshots/19-success-target-username.png) | **Keep** | Confirms SOC-Lab-Test2 target for expanded success |
| [20-two-failures-targeted-account.png](../screenshots/20-two-failures-targeted-account.png) | **Keep** | Shows the 18:01:21 and 18:01:26 Wazuh 60122 failures; the cropped rows do not display the username filter |
| [21-separate-webview-failure-process.png](../screenshots/21-separate-webview-failure-process.png) | **Keep (supporting only)** | Shows a separate subsequent failed sign-in and WebView2 process; target account unverified |
| `22-separate-failure-context.png` | **Removed** | Fragment of separate event; mostly subject-account fields and could mislead a reader about the target username |
| `23-separate-failure-rule.png` | **Removed** | Low-value duplicate context; rule 60122 already established elsewhere |
| [24-nearby-sysmon-process-alerts.png](../screenshots/24-nearby-sysmon-process-alerts.png) | **Keep** | Documents process-related Wazuh alert rows after the success (not attributable to test account without further evidence) |
| `25-mcafee-webadvisor-process-details.png` | **Not uploaded** | Needed to evidence the McAfee BrowserHost.exe process details mentioned in Investigation 02 |

**Total after cleanup: 26 original PNGs on GitHub = 19 Investigation 01 + 7 Investigation 02.**

## Remaining user action — only if you want the last exhibit

From the additional evidence ZIP supplied earlier, upload **only** `25-mcafee-webadvisor-process-details.png` to `Windows-Authentication-Investigation/screenshots/` using GitHub's Add file → Upload files. Review its contents for information you do not want on a public repository before committing.

Once uploaded, update the [evidence index](../screenshots/README.md), [Investigation 02](../investigations/02-failed-then-successful-login.md) and [timeline](./02-authentication-timeline.md) to link the actual image. The eventual total would be **27** (19 + 8), *not* 29.

## Evidence limitations

- The live Wazuh query confirmed the failed logins targeted SOC-Lab-Test2, but screenshots 16 and 20 crop out filter chips and target usernames. The written timeline therefore records the observed filtered search, not a complete exported raw event chain.
- The process alert near 18:01:47 was **not conclusively tied** to the SOC-Lab-Test2 session.
- The later WebView2-related failure is **not proven** to involve SOC-Lab-Test2.
- Keep exact event names and timestamps; do not classify an alert as malicious purely because of its title.
- These are screenshot excerpts, **not** EVTX or a complete forensic acquisition.
