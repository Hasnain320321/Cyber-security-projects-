# Test matrix and reproduction — 16 October 2026

All commands were run on the owned Windows lab host. Encoded test text only prints PROJECT7_ENCODED_TEST. The use of an encoded switch is the tested behaviour; no malicious code is required.

## Commands

Baseline:
```powershell
powershell.exe -NoProfile -Command "Write-Output 'PROJECT7_BASELINE'"
```

Prepare the harmless payload and test the full switch:
```powershell
$testCommand = "Write-Output 'PROJECT7_ENCODED_TEST'"
$encodedCommand = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($testCommand))
powershell.exe -NoProfile -EncodedCommand $encodedCommand
```

Short-switch test, in the same PowerShell session:
```powershell
powershell.exe -NoProfile -enc $encodedCommand
```

Final negative control:
```powershell
powershell.exe -NoProfile -Command "Write-Output 'PROJECT7_FINAL_NEGATIVE'"
```

Commands above are a written reproduction of the guided lab steps, not exported console history. Screenshot evidence verifies the generated command lines and alert outcomes. Recreate the two variables if opening a new PowerShell session.

## Results

| Stage / dashboard time BST | Test | Expected / observed | Evidence |
| --- | --- | --- | --- |
| Baseline 22:03:48 | Ordinary nested PowerShell | Collected under 92027 / 4 | 01–02 |
| Initial 22:18:08 | Full encoded switch | Built-in 92057 / 12; initial custom rule absent | 03–04 |
| First refinement 22:26:29 | Full encoded switch | Custom 100107 / 12 | 06 |
| Initial negative 22:28:45 | PROJECT7_NEGATIVE_TEST | 92027 / 4, not custom rule; inspected live but superseded by final regression evidence | Final negative evidence below preferred |
| Gap test 22:32:56 | -enc before expansion | Only generic 92027 / 4; custom miss | 07–08 |
| Final short-switch 22:41:18 | -enc after expansion | 100107 / 12 | 10–12 |
| Final full-switch 22:43:05 | -EncodedCommand after expansion | 100107 / 12 | 12, 14 |
| Final negative 22:43:13 | PROJECT7_FINAL_NEGATIVE | 92027 / 4; no custom match for reviewed event | 12–13 |

Final result: **two positive cases and one collected negative control passed**. These are lab observations, not a statistically meaningful production benchmark. The command-detail captures for the last two cases were supplied after opening the identified overview rows; they do not themselves display the rule ID. The overview and companion detail captures support each result together.

## Dashboard checks

Use agent.name: "Windows-Host" AND data.win.system.eventID: "1" within the relevant time window. For custom alerts, search rule.id: "100107". Remove restrictive rule filters before looking for negative-control events. Confirm the command line and timestamp, not merely the existence of an old matching alert.

## Not performed

No native EVTX/alerts.json export, wazuh-logtest replay, production noise measurement, PowerShell 7 test or other-parent coverage test was captured. Do not represent screenshots as native event exports or regex-only checks as live Wazuh tests.
