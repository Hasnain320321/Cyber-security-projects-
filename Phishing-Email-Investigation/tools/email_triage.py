#!/usr/bin/env python3
"""Offline, read-only .eml triage helper. No network or attachment execution.

Run: python tools/email_triage.py path/to/sample.eml --output output/case.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

TOOL_VERSION = "1.0"
URL_RX = re.compile(r"(?i)\b(?:https?|hxxps?)://[^\s<>\"'`]+")
STATUS_RX = re.compile(r"\b(spf|dkim|dmarc)\s*=\s*([a-z_-]+)", re.I)


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() not in {"a", "area"}:
            return
        for key, val in attrs:
            if key.lower() == "href" and val:
                self.links.append(val)


def extract_domains(value: str | None) -> list[str]:
    if not value:
        return []
    result: set[str] = set()
    for _name, addr in getaddresses([value]):
        if "@" in addr:
            result.add(addr.rsplit("@", 1)[1].lower().strip(">"))
    return sorted(result)


def safe_url(raw: str) -> dict[str, str] | None:
    """Normalize for parsing, then only emit a defanged URL without query/fragment."""
    cleaned = raw.strip().rstrip(".,;!)]}")
    restored = re.sub(r"\[\.\]", ".", cleaned, flags=re.I)
    restored = re.sub(r"(?i)^hxxp", "http", restored)
    try:
        parts = urlsplit(restored)
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
            return None
        host = parts.hostname.lower()
        # Strip username, password, query and fragments: these may contain secrets.
        port = f":{parts.port}" if parts.port else ""
        path = parts.path[:90]
        redacted_path = re.sub(r"[^a-zA-Z0-9/._~%-]", "_", path)
        result = f"{parts.scheme.lower().replace('http', 'hxxp')}://{host.replace('.', '[.]')}{port}{redacted_path}"
        return {"domain": host, "defanged_url_no_query": result}
    except ValueError:
        return None


def examine(path: Path) -> dict:
    if not path.is_file() or path.suffix.lower() != ".eml":
        raise ValueError("Specify an existing .eml file")
    raw = path.read_bytes()
    if len(raw) > 5 * 1024 * 1024:
        raise ValueError("Refusing .eml larger than 5 MiB")
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    auth_headers = msg.get_all("Authentication-Results", [])
    auth = []
    for header in auth_headers:
        text = str(header)
        statuses = {key.lower(): status.lower() for key, status in STATUS_RX.findall(text)}
        auth.append({"reported_results_only": statuses})

    found: dict[str, dict] = {}
    attachments: list[dict] = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        filename = part.get_filename()
        if filename or part.get_content_disposition() == "attachment":
            attachments.append({"filename": filename or "(unnamed)", "content_type": part.get_content_type()})
            continue
        if part.get_content_type() not in {"text/plain", "text/html"}:
            continue
        try:
            content = part.get_content()
        except (UnicodeError, LookupError, ValueError, TypeError):
            continue
        candidates = URL_RX.findall(content)
        if part.get_content_type() == "text/html":
            collector = LinkCollector()
            collector.feed(content)
            candidates.extend(collector.links)
        for candidate in candidates:
            item = safe_url(candidate)
            if item:
                found[item["defanged_url_no_query"]] = item

    return {
        "tool_version": TOOL_VERSION,
        "source_filename": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "subject": str(msg.get("Subject", "")),
        "date_header_unverified": str(msg.get("Date", "")),
        "message_id": str(msg.get("Message-ID", "")),
        "from_domains": extract_domains(str(msg.get("From", ""))),
        "reply_to_domains": extract_domains(str(msg.get("Reply-To", ""))),
        "return_path_domains": extract_domains(str(msg.get("Return-Path", ""))),
        "received_header_count": len(msg.get_all("Received", [])),
        "authentication_results_claimed_by_headers": auth,
        "urls": sorted(found.values(), key=lambda x: x["defanged_url_no_query"]),
        "attachments_metadata_only": attachments,
        "limitations": [
            "This script never verifies SPF, DKIM or DMARC, and never sends network requests.",
            "Routing headers and authentication results may be incomplete, redacted or forged.",
            "Extracted URLs are defanged and queries/fragments omitted; this is not a malware verdict.",
            "No attachments or URLs were opened or executed.",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("email", type=Path, help="Local .eml file")
    ap.add_argument("--output", type=Path, help="Save results as JSON")
    args = ap.parse_args()
    result = examine(args.email)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Saved read-only triage results: {args.output}")
    print(rendered)


if __name__ == "__main__":
    main()
