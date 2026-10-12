# Project 5 — Network PCAP Investigation

**Status:** In progress — initial local Wireshark triage performed 12 October 2026. Preliminary observations are documented below; HTTP responses, payload interpretation and final report are pending. Genuine user screenshots were reviewed in chat but have not yet been uploaded to this repository.

## Purpose

Conduct a reproducible, evidence-based Wireshark investigation of a published SOC training PCAP. Document what the packets actually support, distinguishing observed network facts, reasonable hypotheses and unverified assertions.

## Training case

**Case ID:** PCAP-0051 (portfolio case label)

**Source:** [Malware-Traffic-Analysis.net — 22 January 2025 traffic analysis exercise: Download from Fake Software Site](https://malware-traffic-analysis.net/2025/01/22/index.html)

**Scenario supplied by the exercise:** A simulated SOC receives a report about a suspected fake Google Authenticator download; an existing packet capture is provided for investigation. This is **third-party training evidence, not traffic captured by me or a live incident I handled**.

**Published lab context:** Internal subnet `10.1.17.0/24`; domain `bluemoontuesday.com`; published gateway `10.1.17.1` and domain controller `10.1.17.2`. These are **source-provided facts, not independently verified findings**.

**Acquisition:** The provider offers a password-protected ZIP containing a PCAP (~20.5 MB compressed). The user downloaded/extracted the training capture and opened `2025-01-22-traffic-analysis-exercise.pcap` in Wireshark on Kali. **Capture SHA-256, extracted file size and local acquisition log are still pending.** Do not upload the raw PCAP or extracted malicious files to this repository.

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

## Immediate next investigation

**Now confirmed:** HTTP frame 5071 corresponds to `.ps1` request frame 5063, and the stream shows visibly obfuscated PowerShell-like text. Next, investigate the repeated `GET /1517096937` requests and associated HTTP `404` replies to establish timing/intervals, then check related sessions and calculate the PCAP's SHA-256. Never execute the script or follow its URLs.

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