# CASE-0041 — Verified offline helper test

**Executed:** 11 October 2026 in the assistant's isolated Python environment; **not executed on the user's Windows laptop yet.**

```text
$ python -m unittest discover -s tests -v
test_already_defanged_input ... ok
test_defang_and_remove_query_secret ... ok
test_email_domain_extraction ... ok
test_parse_eml_without_executing ... ok

Ran 4 tests in 0.002s

OK
```

Then executed locally:
```text
$ python tools/email_triage.py /mnt/data/Project4_Phishing_Training_Case01.eml --output output/CASE-0041.json
Saved read-only triage results: output/CASE-0041.json
```

Reproducible structured [tool output](CASE-0041-tool-output.json) contains exact SHA-256, domains, claimed SPF/DKIM/DMARC statuses, and defanged URL. The original sample was the synthetic email supplied to the user in the previous session.

**Scope note:** Four passing unit tests verify only the behaviours covered by those tests. This is not evidence of real-world phishing, independently checked DNS, or user-run lab work. The user's next step is to run the same tool on the sourced redacted real-world email and share authentic screenshots.
