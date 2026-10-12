# CASE-0051 — Network PCAP Investigation Report

**Prepared:** 12 October 2026  
**Status:** **COMPLETE — scoped offline training capture investigation; 11/11 original screenshot files uploaded and exact Git blob SHA verified (12 October 2026)**  
**Case classification:** High-confidence *suspicious staged script retrieval*, with subsequent *suspected automated HTTP polling*. **Compromise and actual code execution not proven.**  
**Source context:** Public, historical SOC training exercise from [Malware-Traffic-Analysis.net](https://malware-traffic-analysis.net/2025/01/22/index.html), dated 22 January 2025. Not a real incident at an employer or the analyst's own network.

## 1. Executive summary

A published PCAP was examined offline in Wireshark. A Windows client (`10.1.17.215`) retrieved two small HTTP objects from external address `5.252.153.241`. The first returned 417 bytes of a Windows Script Component-style VBScript body containing commands to launch a hidden PowerShell downloader. Its embedded URL matched the later HTTP request for a `.ps1` file. The matching HTTP 200 response delivered 1,512 bytes of obfuscated PowerShell-like text containing decoding transformations and `iex`, consistent with a staged script-execution design.

Immediately afterward, the same client made ten visible requests for a single numeric HTTP path at intervals averaging approximately 5.19 seconds. These requests received HTTP `404 Not Found` responses. This is consistent with periodic automated polling and warrants a command-and-control hypothesis, but the capture does **not** show successful instruction delivery, operating-system process creation, endpoint execution or confirmed compromise. A later separate TLS session to `45.125.66.32:2917` was observed; its encrypted content and relation to the script chain remain unknown.

## 2. Scope, evidence and integrity

| Field | Evidence |
| --- | --- |
| Evidence format | Historical training PCAP, inspected read-only in Kali Wireshark |
| Local filename | `2025-01-22-traffic-analysis-exercise.pcap` |
| Local path | `/home/kali/Downloads/2025-01-22-traffic-analysis-exercise.pcap` |
| User-run SHA-256 | `e59db1c07c6fdefafa0abdbca03248c341cdc36c09c34753204d3162802a3586` |
| Capture volume | 39,427 packets shown; 145 IPv4 endpoints in Wireshark endpoint statistics |
| Evidence type | User's genuine Wireshark screenshots, reviewed in chat; **11/11 source screenshots uploaded and hash-verified by Git blob SHA against originals supplied in chat** |
| Time reference | All seconds below are **relative to capture start**, not wall-clock attack timestamps |

SHA-256 records the bytes of the locally analysed file and is not itself a certificate of publisher authenticity or safety. The website lists the ZIP at roughly 20.5 MB; the extracted PCAP size was not separately verified. The source exercise discusses a suspected fake-software download; that initial landing page has **not** been independently established from the screenshots.

## 3. Affected endpoint and authentication context

| Attribute | Value | Evidence |
| --- | --- | --- |
| Hostname | `DESKTOP-L8C5GSJ` | DHCP frame **3**, Option 12 |
| Client IPv4 | `10.1.17.215` | DHCP frame **3**, Option 50 (requested); observed source in HTTP/TLS |
| MAC | `00:0d:b7:26:4a:74` | DHCP frame **3** |
| DHCP/domain infrastructure | `10.1.17.2` | DHCP Option 54, DNS/Kerberos exchanges |
| Kerberos client principal | `shutchenson` | AS-REQ frame **258**, `req-body → cname → CNameString` |
| Kerberos realm | `BLUEMOONTUESDAY` | AS-REQ frame **258** |

The principal is visible in an authentication request, **not proven to be the logged-on human who ran, opened, or downloaded a file**. Kerberos frames **250–272** include initial AS-REQ, a normal `KRB5KDC_ERR_PREAUTH_REQUIRED` negotiation, AS-REP and service-ticket exchange. This does not independently imply a brute-force incident.

## 4. Packet-level timeline

| Relative time | Frame(s) | Observation | Interpretation / bounds |
| ---: | --- | --- | --- |
| 0.001889 s | **3** | DHCP Request; host/IP/MAC context | Device identification |
| 14.374722 s | **258** | Kerberos AS-REQ with client principal | Authentication context, not script attribution |
| 60.297799 s | **5031** | GET `/api/file/get-file/264872` to `5.252.153.241` | First-stage resource request |
| 60.464642 s | **5033** | HTTP 200; `Request in frame: 5031`; `Content-Length: 417` | Server delivered 417 bytes; body inspected statically |
| 62.145732 s | **5063** | GET `/api/file/get-file/29842.ps1` | Matches URL embedded in first-stage script |
| 62.309349 s | **5071** | HTTP 200; `Request in frame: 5063`; `Content-Length: 1512` | Server delivered obfuscated script-like content |
| 62.366091–109.104654 s | **5073, 7279, 7602, 7688, 7696, 7841, 7864, 7878, 7888, 7907** | Ten GETs for `/1517096937`, approximately every 5.19 s | Suspected automated polling; responses 404, not proven successful C2 |
| 889.561525 s | **19302–19304** | TCP handshake to `45.125.66.32:2917` | Additional external connection, attribution unknown |
| 889.755043–890.366 s | **19305–19321** | TLS 1.2 handshake, then encrypted application data | Content not decoded; purpose undetermined |

Observed packet timings describe traffic within this PCAP only. The later TLS event is around 14 minutes 50 seconds after capture start, **not** necessarily after any proven execution event.

## 5. Technical findings

### 5.1 First-stage VBScript-style content

Wireshark's read-only Follow TCP Stream for request 5031 / response 5033 showed markup resembling a script component (`<component>` and `<script language="VBScript">`). Key observed behaviours:

- `On Error Resume Next` suppresses error interruptions.
- `CreateObject("Wscript.Shell")` and `objShell.Run` provide the ability to launch OS commands.
- `cmd /c start /min` and `powershell -NoProfile -WindowStyle Hidden` would conceal or minimise user-facing windows if executed.
- A `System.Net.WebClient` `DownloadString` operation targets the same URL later observed in frame **5063**, with `iex` used to interpret fetched text.
- The text mentions legitimate Microsoft-related URLs as well; these could be camouflage or incidental. Their precise role has not been established.

**Finding:** The bytes contain a coherent downloader/launcher instruction chain. Whether Windows executed them is unknown.

### 5.2 Obfuscated second-stage PowerShell-like body

HTTP 200 in **5071** directly references request **5063**. The response declared `Content-Type: application/octet-stream` and `Content-Length: 1512`. TCP stream **61** displayed text with `iex`, `UTF8.GetString`, `System.Convert` and repeated `.replace(...)` transformations.

**Finding:** Consistent with an obfuscated second-stage payload that reconstructs text and attempts to execute it. **Payload not executed or fully decoded; behaviour beyond the visible expression is unverified.**

### 5.3 Repeated HTTP polling / suspected beaconing

For `GET /1517096937`, ten client requests were visible between **62.366091 s** and **109.104654 s**, approximately **5.17–5.24 s apart** (mean about **5.19 s**). Corresponding responses shown in Wireshark were mostly/repeatedly `404 Not Found`.

**Finding:** Highly regular repeated requests to the same server just after staged script delivery are consistent with automated polling and support further C2 investigation. A periodic request **does not by itself prove malware-generated beaconing**, and HTTP 404 is not proof of successful command retrieval.

### 5.4 Separate TLS session

At frame **19302** the client initiated a connection to **45.125.66.32:2917**. Frame **19305** is a TLS Client Hello with visible SNI corresponding to the IP. Frame **19307** includes Server Hello and Certificate; the negotiated TLS 1.2 cipher suite was `TLS_RSA_WITH_AES_128_GCM_SHA256`. Encrypted application data followed.

**Finding:** Nonstandard port and high volume merit investigation, but no evidence supplied links this session definitively to the earlier script chain. Certificate subject/issuer and contents of encrypted traffic were not verified.

### 5.5 DNS/SNI review and negative findings

Early DNS activity included expected Windows infrastructure and Microsoft service names. Client Hello/SNI inspection of the first 65 seconds showed names such as `azure.microsoft.com`, `www.microsoft.com`, `play.vidyard.com`, `publisher.liveperson.net`, and `assets.adobedtm.com`. These are **observed requested hostnames, not automatic proof of manual visits or safety**. No specific fake-software landing-page hostname was established in the displayed subset.

## 6. Assessment, limitations and false-positive considerations

**Evidence-backed conclusion:** Two HTTP-delivered stages are explicitly correlated by packet links and embedded URL. The first contains clear script-launching and downloader commands; the second is obfuscated and uses `iex`. Subsequent repeated HTTP polling is suspicious. This warrants a **high-priority suspected staged malware event** in a SOC training context.

**Not established:** host-level execution; initial website provenance; complete decoded stage-two functionality; malware family; persistence; credential theft; successful C2 commands; specific user culpability; actual victim harm or organisational incident.

**Alternative considerations:** Administration scripts can use PowerShell; periodic HTTP access can arise from ordinary software; TLS on a nonstandard port can have legitimate uses. Here, the linked script-launching behaviour and timing make the combined sequence more concerning than any one isolated field.

## 7. Defensive next actions (recommendations, not actions performed)

1. For a **real authorised incident**, isolate the affected endpoint as appropriate after validating business impact and coordinating with incident response; do not act against hosts or IPs in this published training exercise.
2. Examine Windows Security, Sysmon, EDR and PowerShell Script Block Logging for process creation, parent-child relationships, command lines and script execution near the capture time. These logs were **not supplied**.
3. Search approved network logs for the suspicious destination and repeated same-path timing; validate scope before blocking, and avoid treating all traffic to external Microsoft-related domains as malicious.
4. Preserve original evidence and hashes, timestamped chain of custody, observed host identity, and bounded indicators before case closure.
5. Tune rules for suspicious script-launching activity and anomalous HTTP polling; test legitimate administrative activity to reduce false positives.

**Possible MITRE ATT&CK technique associations (behavioural themes only):** T1059.005 (Visual Basic), T1059.001 (PowerShell) and T1105 (Ingress Tool Transfer). These are not evidence of endpoint execution or confirmed adversary attribution.

## 8. Evidence register and completion gate

The [evidence index](../screenshots/README.md) contains working relative links to **all 11 verified PNG screenshots**. All file names and uploaded Git blob hashes were checked against locally computed Git object hashes of the user's original images. The report is **complete for its stated offline PCAP investigation scope**, not proof of victim compromise, endpoint code execution or full malware reverse engineering.

No raw PCAP, executable samples or standalone malicious script files were published. Evidence screenshots include inert text of the script, kept for analysis only. The case is a third-party training analysis.
