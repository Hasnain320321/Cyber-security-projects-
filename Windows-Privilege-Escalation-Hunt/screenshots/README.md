# Project 3 — Screenshot Evidence

**Status: 26 screenshots were staged in a downloadable ZIP on 10 October 2026, including final cleanup. The actual PNG evidence has not yet been committed to this GitHub folder.** Do not treat this checklist as screenshot files.

Evidence must be kept **separate** from Project 1's and Project 2's screenshots. When uploading, choose the most legible original captured image (avoid redundant crops). Review public screenshots for local usernames, endpoint names, internal IPs and identifiers before publishing; don't obscure fields necessary to support a claim.

## Curated screenshot upload plan

| Suggested file | Captured during session? | What should be visible |
| --- | --- | --- |
| `01-audit-policy.png` | Yes | `Security Group Management: Success` |
| `02-wazuh-collection.png` | Yes | Wazuh agent running and collecting `Security` eventchannel |
| `03-admin-baseline.png` | Yes | Administrators list before testing |
| `04-disabled-test-account.png` | Yes | `SOC-PrivEsc-Test` and `Enabled=False` |
| `05-original-admin-4732.png` | Yes | Event 4732, Administrators target SID `-544`, subject/member |
| `06-event-4733-rollback.png` | Yes | Event 4733 removal from Administrators, matching member |
| `07-rule-created-manager-active.png` | Yes | New custom rule configuration and manager restart `active` |
| `08-positive-rule-100102.png` | Yes | `rule.id=100102`, `rule.level=13`, same 4732 event (may need two related captures) |
| `09-positive-safe-end-state.png` | Yes | Rollback and disabled account |
| `10-negative-removal.png` | Yes | Rule 100102 + Event 4733 produces no matches, and separate 4733 results appear |
| `11-negative-normal-group-4732.png` | Yes | Target group `SOC-NonAdmin-Test`, SID ending `-1006`, Event 4732 |
| `12-negative-rule-60144.png` | Yes | Same non-admin event handled by rule `60144`, level 5 |
| `13-negative-group-cleanup.png` | Yes | Group deletion Event 4734 or PowerShell cleanup output |

"Captured during session" means the evidence was seen in the chat, **not** that a matching PNG file is present on GitHub.

| `14-logon-correlation-no-matches.png` | Yes | Read-only Windows query of Security Event 4624/4672 in 22:15–22:50 lab window returned no account matches; interpret cautiously |

| `15-sysmon-powershell-high-2235.png` | Yes | Elevated `powershell.exe` started by Explorer at 22:35:57 |
| `16-sysmon-ssh-wazuh-2230.png` | Yes | `ssh.exe` to Wazuh VM started by PowerShell at 22:30:46 |
| `17-sysmon-powershell-correlated-2222.png` | Yes | Elevated PowerShell process at 22:22:19 preceding controlled administrator group-change event |

| `18-final-test-account-deleted.png` | Yes | After checking no test membership or temporary group, `Remove-LocalUser` succeeded and subsequent lookup found no test account |

## Upload verification checklist

- [ ] PNG files have actually been uploaded to this GitHub directory
- [ ] Every cited screenshot corresponds to the correct event/test and includes relevant visible context
- [ ] Positive detection and negative cases are clearly separated
- [ ] Personally identifying/internal information reviewed for public disclosure
- [ ] Links in the investigation document updated to point to the committed screenshot files
