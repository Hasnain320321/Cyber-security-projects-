# Project 5 — Verified Screenshot Evidence Index

**Verification: COMPLETE — 11/11 genuine PNG files uploaded to GitHub and checked against the originals supplied by the analyst in chat (12 October 2026).** Git blob SHA-1 values are exact matches to independently computed Git object hashes of those original screenshots. These hashes verify byte-for-byte image equality, not that the depicted packets establish host compromise.

| ID | Genuine screenshot | What it demonstrates | Upload QA |
| --- | --- | --- | --- |
| 01 | [01-capture-opened.png](./01-capture-opened.png) | Capture opened with 39,427 packets | **Verified** |
| 02 | [02-ipv4-endpoints.png](./02-ipv4-endpoints.png) | 145 IPv4 endpoints; client traffic context | **Verified** |
| 03 | [03-dhcp-host-identity.png](./03-dhcp-host-identity.png) | DHCP host, MAC, requested address | **Verified** |
| 04 | [04-http-stage1-response.png](./04-http-stage1-response.png) | Frame 5033 417-byte HTTP response linked to 5031 | **Verified** |
| 05 | [05-stage1-vbscript-stream.png](./05-stage1-vbscript-stream.png) | Read-only VBScript-style stage-one script stream | **Verified** |
| 06 | [06-http-stage2-response.png](./06-http-stage2-response.png) | Frame 5071 1,512-byte HTTP response linked to 5063 | **Verified** |
| 07 | [07-obfuscated-powershell-stream.png](./07-obfuscated-powershell-stream.png) | Read-only obfuscated PowerShell-like stream | **Verified** |
| 08 | [08-http-polling-timeline.png](./08-http-polling-timeline.png) | Periodic HTTP GETs; matching 404s | **Verified** |
| 09 | [09-tls-external-session.png](./09-tls-external-session.png) | Later TLS connection to external address on port 2917 | **Verified** |
| 10 | [10-kerberos-account-principal.png](./10-kerberos-account-principal.png) | Kerberos AS-REQ cname and realm | **Verified** |
| 11 | [11-pcap-sha256.png](./11-pcap-sha256.png) | Local PCAP SHA-256 command output | **Verified** |

## Exact-match screenshot manifest (Git blob SHA-1)

| Screenshot | Git blob SHA-1 |
| --- | --- |
| `01-capture-opened.png` | `93c14c6a39f34b386adf3fce517b2a8a802850ab` |
| `02-ipv4-endpoints.png` | `391e02b6ea77deb6dc569696aaef4c5f7dbdf492` |
| `03-dhcp-host-identity.png` | `bfefa40e19ae0f2d5644a201edafb80506934393` |
| `04-http-stage1-response.png` | `5b279b0ed2f650ead4ab4854be978d1de4cb376d` |
| `05-stage1-vbscript-stream.png` | `3dbb2a2186c5dd14ac17e3ad278d7b33ac9249f8` |
| `06-http-stage2-response.png` | `85743afd8818aca7a288cb2705536d524dd99e8a` |
| `07-obfuscated-powershell-stream.png` | `b4b03d4a8e463a884bd219179e1cd76cb5a2c104` |
| `08-http-polling-timeline.png` | `088e6f090dc55fdef1d230054d4739bd2214ebb1` |
| `09-tls-external-session.png` | `255d9c93ed9931e9d91e72a91518cda0d353c786` |
| `10-kerberos-account-principal.png` | `3607c9d28d3f0e0dd25253fd25fb72d7a7a355e2` |
| `11-pcap-sha256.png` | `59f1c00be8a1e02cd5103fd4e788486919208d99` |

## Disclosure and safety

- All screenshots are real user-captured Kali/Wireshark outputs from the published training exercise. No synthetic packet displays were created.
- Evidence images contain visible training payload **text** and an account principal; both are contextual for this historical lab. Do **not** execute any commands shown in the screenshots, browse to captured IPs or extract executable payloads.
- The captured account name is an observed Kerberos principal; it is **not** proof the user executed malware.
- These are unchanged screenshots rather than new cropped copies. No alterations are claimed.
- The raw training PCAP and script artifacts remain local and are **not** hosted in this repository.

[Investigation report](../investigations/CASE-0051-INVESTIGATION-REPORT.md) · [Project README](../README.md)
