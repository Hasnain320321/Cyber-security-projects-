# Offline EML triage tool (work in progress)

- `email_triage.py`: local read-only Python 3 script. Uses only the standard library; **no network requests, no clicking, no executing attachments**.
- `test_email_triage.py`: four initial unit tests (defanging, domain extraction, synthetic MIME parsing).
- Input: `.eml` file. Output: JSON with SHA-256, date and subject, sender identity **domains** (not full addresses), reported authentication statuses, Received header count, defanged URLs without query/fragment and attachment **metadata only**.
- This is an **indicator extractor, not a phishing classifier or independently verified authentication validator**.

## Windows PowerShell

Download this project's `tools/email_triage.py` and `tests/test_email_triage.py`, or use the starter ZIP shared in the companion session. Install Python 3 if not installed.

```powershell
py -3 -m unittest discover -s tests -v
py -3 tools/email_triage.py samples/CASE-0042-real-redacted.eml --output output/CASE-0042.json
```

If the `py` launcher is not available but Python is installed, use `python` instead.

Never execute .eml attachments, click unknown URLs, use live credentials or share private emails publicly.
