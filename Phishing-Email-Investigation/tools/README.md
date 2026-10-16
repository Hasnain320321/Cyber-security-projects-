# Offline EML triage tool (version 1.0)

- `email_triage.py`: local read-only Python 3 script. Uses only the standard library; **no network requests, no clicking, no executing attachments**.
- `test_email_triage.py`: four unit tests (defanging, domain extraction, synthetic MIME parsing).
- Input: `.eml` file. Output: JSON with SHA-256, date and subject, sender identity **domains** (not full addresses), reported authentication statuses, Received header count, defanged URLs without query/fragment and attachment **metadata only**.
- This is an **indicator extractor, not a phishing classifier or independently verified authentication validator**.

## Windows PowerShell

Download or clone the repository, open PowerShell in `Phishing-Email-Investigation`, and install Python 3 if needed. The example uses the included synthetic benign control; the historical CASE-0042 sample is not redistributed here.

```powershell
py -3 -m unittest discover -s tests -v
py -3 tools/email_triage.py samples/CASE-0043-benign-control.eml --output output/CASE-0043.json
```

If the `py` launcher is not available but Python is installed, use `python` instead.

Never execute .eml attachments, click unknown URLs, use live credentials or share private emails publicly.
