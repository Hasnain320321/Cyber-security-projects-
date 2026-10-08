# SOC Portfolio Session Handoff — 8 October 2026

**Current state:** Project 1 (SOC Home Lab) complete v1; Project 2 (Windows Authentication Investigation) complete v1. Project 3 (Phishing Email Investigation) deferred until the learner explicitly asks to begin.

## Project 1 — Baseline retained unchanged

Project 1 lives in `SOC-Home-Lab/`. The Wazuh/Sysmon home lab, three controlled investigations, custom PowerShell rule 100100 and its interview summary are complete. Its files were **not edited during Project 2**.

## Project 2 — Completed work

- Two local test accounts: `SOC-Lab-Test` and `SOC-Lab-Test2`.
- Windows Event ID 4625 (failed login), 4624 (successful login); Wazuh 60122 individual failure and 60118 successful workstation logon in the lab.
- Custom Wazuh rule **100101** stored in `local_rules.xml`: `frequency=3`, `timeframe=60`, `if_matched_sid=60122`, `same_field=win.eventdata.targetUserName`, level 10, MITRE T1110.
- Four controlled tests completed: three failures Account 1 (alert), one isolated failure (no higher-level alert in reviewed window), two failures Account 1 plus one failure Account 2 (no higher-level alert), and three failures Account 2 (alert).
- Investigation 02: **18:01:21 and 18:01:26** failures for SOC-Lab-Test2 followed by **18:01:33** successful 4624 interactive login, event source `127.0.0.1`. Authorised benign activity. Neighbouring Wazuh shell-related alerts showed McAfee WebAdvisor BrowserHost.exe in process fields, but were **not proved to originate from the SOC-Lab-Test2 session**.
- Project 2 now has an expanded [interview summary](../../Windows-Authentication-Investigation/INTERVIEW-SUMMARY.md), [two investigation reports](../../Windows-Authentication-Investigation/), [response playbook](../../Windows-Authentication-Investigation/response/01-authentication-alert-triage-playbook.md), and [essential memorisation notes](../../Windows-Authentication-Investigation/notes/WHAT-TO-MEMORISE.md).
- [Daily mixed 40-card flashcards](../SOC-FLASHCARDS-PROJECTS-1-2.md): twenty Project 1 cards plus twenty Project 2 cards.

## Evidence verification and remaining optional upload

- **26 screenshots now verified on GitHub**: the original 19 for Investigation 01 plus seven curated Investigation 02 exhibits. See the [evidence index](../../Windows-Authentication-Investigation/screenshots/README.md).
- Six key GitHub PNGs were checked against local original Git blob hashes and matched byte-for-byte.
- **Of the ten originally prepared Investigation 02 PNGs, seven are retained in GitHub, two low-value fragments (22 and 23) were removed, and image 25 (McAfee process details) remains absent.** See the [Investigation 02 evidence audit](../../Windows-Authentication-Investigation/evidence/INVESTIGATION-02-SCREENSHOT-UPLOAD-CHECKLIST.md).
- Do not claim 29 uploaded images: current total is 26 (19 + 7); uploading missing image 25 would make 27.

## Five daily anchors

1. `4625` failed, `4624` successful.
2. Account -> source IP -> logon type -> attempts -> device -> after-login activity.
3. `60122` individual failure; `100101` correlated same-account failures.
4. Positive and negative detection tests both matter.
5. An alert is not proof of an attacker or compromise.

## Next session

- First do the [40 daily flashcards](../SOC-FLASHCARDS-PROJECTS-1-2.md) and five anchors.
- If the learner wants one further relevant visual exhibit, upload only image 25 and verify it; ideally also capture an uncropped 4625 account-filter screenshot if another lab session is undertaken.
- Do not rebuild or modify Project 1. Project 3 begins only when specifically requested.
- Portfolio repo: https://github.com/Hasnain320321/Cyber-security-projects-
