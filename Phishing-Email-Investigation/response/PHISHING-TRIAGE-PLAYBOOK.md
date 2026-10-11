# Phishing Email Triage — Response Playbook

**Purpose:** General SOC response guidance arising from the Project 4 synthetic case. **No steps here were performed against production systems.**

## Triage and preservation

1. Open the email as source text or in a safe mail-analysis viewer. Preserve full headers, Message-ID and trace IDs, recipient, received times, original source, and chain of custody.
2. Establish which `Received` and `Authentication-Results` records were appended by trusted organisational mail infrastructure.
3. Compare display name, From, Reply-To, envelope sender and sending infrastructure; interpret SPF, DKIM and DMARC **in context**.
4. Extract URLs/domains/IPs/attachment names, defang for reports and seek safe enrichment. Never execute an unknown attachment or browse a suspect live URL directly.

## Scope and impact

5. Search mail-gateway logs for same/similar messages and identify delivery, quarantine and recipient counts.
6. Examine proxy/DNS/EDR/identity telemetry for click events, redirects, unusual sign-ins and further actions.
7. Determine whether there is evidence of submitted credentials, token/session theft, subsequent access or malware. Do **not** infer compromise from an email's existence alone.

## Response decisions

- **Phishing message, no compromise found in the checked scope:** Follow policy for quarantine/removal, mail filtering, notification, documentation, and closure.
- **Possible exposure or uncertain telemetry:** Escalate investigation and preserve relevant account activity.
- **Confirmed credential exposure or unauthorised access:** Escalate promptly and coordinate account lockout/reset, session/token revocation, MFA checks and post-compromise scoping under approved process.
- **Benign or authorised message:** Record why indicators are explained and close without unnecessary disruptive containment.

## Applicability to training CASE-0041

The file uses reserved `.example` domains and documentation-only addresses; no actionable production IOC exists here. This project **did not** access live email systems, block infrastructure, reset user passwords, observe clicks or verify compromise.
