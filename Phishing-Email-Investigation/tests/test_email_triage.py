import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from email_triage import examine, safe_url, extract_domains


class EmailTriageTests(unittest.TestCase):
    def test_defang_and_remove_query_secret(self):
        result = safe_url("https://login.example.com/verify?session=PRIVATE123")
        self.assertEqual(result["domain"], "login.example.com")
        self.assertEqual(result["defanged_url_no_query"], "hxxps://login[.]example[.]com/verify")
        self.assertNotIn("PRIVATE123", str(result))

    def test_already_defanged_input(self):
        result = safe_url("hxxps://example[.]org/signin")
        self.assertEqual(result["defanged_url_no_query"], "hxxps://example[.]org/signin")

    def test_email_domain_extraction(self):
        self.assertEqual(extract_domains('"Support" <alert@service.example>'), ["service.example"])

    def test_parse_eml_without_executing(self):
        sample = (b"From: Example <alert@one.example>\nReply-To: help@other.example\n"
                  b"Subject: Please verify\nAuthentication-Results: mx.example; spf=fail; dkim=none; dmarc=fail\n"
                  b"Content-Type: text/plain; charset=utf-8\n\n"
                  b"See https://login.example/verify?token=SECRET\n")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "case.eml"
            path.write_bytes(sample)
            result = examine(path)
        self.assertEqual(result["received_header_count"], 0)
        self.assertEqual(result["from_domains"], ["one.example"])
        self.assertEqual(result["reply_to_domains"], ["other.example"])
        self.assertEqual(result["authentication_results_claimed_by_headers"][0]["reported_results_only"]["spf"], "fail")
        self.assertNotIn("SECRET", str(result))
        self.assertEqual(result["urls"][0]["domain"], "login.example")


if __name__ == "__main__":
    unittest.main()
