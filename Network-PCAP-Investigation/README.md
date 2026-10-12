# Project 5 — Network PCAP Investigation

**Status:** In progress — setup and source selection only (12 October 2026). **No packet findings, screenshots or completed analysis are claimed yet.**

## Purpose

Conduct a reproducible, evidence-based Wireshark investigation of a published SOC training PCAP. Document what the packets actually support, distinguishing observed network facts, reasonable hypotheses and unverified assertions.

## Training case

**Case ID:** PCAP-0051 (portfolio case label)

**Source:** [Malware-Traffic-Analysis.net — 22 January 2025 traffic analysis exercise: Download from Fake Software Site](https://malware-traffic-analysis.net/2025/01/22/index.html)

**Scenario supplied by the exercise:** A simulated SOC receives a report about a suspected fake Google Authenticator download; an existing packet capture is provided for investigation. This is **third-party training evidence, not traffic captured by me or a live incident I handled**.

**Published lab context:** Internal subnet `10.1.17.0/24`; domain `bluemoontuesday.com`; published gateway `10.1.17.1` and domain controller `10.1.17.2`. These are **source-provided facts, not independently verified findings**.

**Acquisition:** The provider offers a password-protected ZIP containing a PCAP (~20.5 MB compressed). File acquisition, local hashes and capture opening remain pending. Do not upload the raw PCAP or extracted malicious files to this repository.

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

Open the source exercise page, obtain the training PCAP in an isolated analysis environment (Kali Linux VM recommended), check the file's SHA-256 and open it in Wireshark. Capture a real first screenshot of the loaded packet list for review.

---
This portfolio documents a published training exercise, not an investigation into a user's real workplace or network.