# Project 5 — Screenshot Evidence Index

**Current status: 0/11 images uploaded or verified in this GitHub folder.** The analyst showed real Wireshark/Kali screenshots in chat. The table defines the curated originals to upload, and does **not** assert that any image is already in GitHub.

| ID | Proposed image filename | Genuine image content already observed | Upload status |
| --- | --- | --- | --- |
| 01 | `01-capture-opened.png` | Wireshark packet list with 39,427 packets | Pending |
| 02 | `02-ipv4-endpoints.png` | IPv4 endpoint statistics, including 10.1.17.215 | Pending |
| 03 | `03-dhcp-host-identity.png` | DHCP frame 3, Option 12 hostname, requested IP and MAC | Pending |
| 04 | `04-http-stage1-response.png` | Frames 5031 / 5033 with HTTP 200, 417 bytes and request link | Pending |
| 05 | `05-stage1-vbscript-stream.png` | TCP stream 60 showing VBScript launcher and matching .ps1 URL | Pending |
| 06 | `06-http-stage2-response.png` | Frame 5071 showing response to frame 5063 and 1,512-byte body | Pending |
| 07 | `07-obfuscated-powershell-stream.png` | TCP stream 61 showing obfuscated PowerShell-like content | Pending |
| 08 | `08-http-polling-timeline.png` | Filtered repeated GET /1517096937 requests and 404 responses | Pending |
| 09 | `09-tls-external-session.png` | TLS session to 45.125.66.32 on port 2917 | Pending |
| 10 | `10-kerberos-account-principal.png` | Kerberos AS-REQ frame 258 expanded to cname and realm | Pending |
| 11 | `11-pcap-sha256.png` | Kali terminal showing local SHA-256 of the analysed PCAP | Pending |

## Evidence handling rules

- Use the **original user-captured screenshots**, not manufactured terminal images or AI-generated evidence.
- Retain packet IDs, filters, context and relevant response details. Any crop or redaction must be explained and should not alter the interpretation.
- Screenshot 05 includes potentially executable malicious-looking commands. Keep it as passive image evidence; **never paste/run the commands or follow the referenced URL**.
- Screenshot 10 contains a training account principal; preserve only information necessary for the case and disclose any privacy crop.
- Do **not** upload raw PCAP, script payloads, downloaded executables or extra unused screenshots into the public portfolio.
- Once files are uploaded, verify each filename and rendering, compare to the investigation report, then update the table from **Pending** to **Verified**.

[Investigation report](../investigations/CASE-0051-INVESTIGATION-REPORT.md) · [Project summary](../README.md)
