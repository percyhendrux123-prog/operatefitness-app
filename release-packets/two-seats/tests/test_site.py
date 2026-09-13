import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "two-seats"


class TwoSeatsSiteContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (SITE / "index.html").read_text()
        cls.terms = (SITE / "terms.html").read_text()
        cls.privacy = (SITE / "privacy.html").read_text()
        cls.success = (SITE / "success.html").read_text()

    def test_offer_and_schedule_are_exact(self):
        required = [
            "Two people. Twelve weeks.",
            "coaching fee is sponsored in full",
            "Monday, September 14, 2026 at 8:00 p.m. CDT",
            "Monday, September 21, 2026",
            "Sunday, December 13, 2026",
            "Louisiana",
            "18 or older",
        ]
        for value in required:
            self.assertIn(value, self.index)

    def test_netlify_form_is_named_and_honeypotted(self):
        self.assertRegex(self.index, r'<form[^>]+name="pkfit-two-seats-2026"')
        self.assertIn('data-netlify="true"', self.index)
        self.assertIn('netlify-honeypot="bot-field"', self.index)
        self.assertIn('name="form-name" value="pkfit-two-seats-2026"', self.index)
        self.assertIn('action="/api/two-seats/apply"', self.index)

    def test_contact_route_values_match_server_contract(self):
        self.assertIn('<option value="email">Email</option>', self.index)
        self.assertIn('<option value="text">Text message</option>', self.index)

    def test_public_media_is_optional_and_not_collected(self):
        self.assertIn("Public media is optional", self.index)
        self.assertNotIn('name="public-checkpoints"', self.index)
        self.assertNotIn('name="identity-format"', self.index)

    def test_motion_can_be_paused_and_application_skipped_to(self):
        self.assertIn('class="skip-link" href="#application"', self.index)
        self.assertIn('id="application"', self.index)
        self.assertIn('id="motion-toggle"', self.index)
        self.assertIn("video.pause()", self.index)
        self.assertIn("addEventListener('click'", self.index)

    def test_required_minimized_fields_exist(self):
        fields = set(re.findall(r'name="([^"]+)"', self.index))
        required = {
            "full-name", "adult-confirmation", "city", "state", "primary-contact", "preferred-contact", "goal", "prior-barrier",
            "commitment-evidence", "training-access", "reliable-days",
            "schedule-constraint", "current-coach", "weekly-checkins",
            "safety-gate", "health-screen-agreement", "typed-signature", "terms-agreement",
        }
        self.assertTrue(required.issubset(fields), required - fields)
        forbidden = {"diagnosis", "medications", "medical-record", "payment-card", "government-id"}
        self.assertTrue(fields.isdisjoint(forbidden), fields & forbidden)

    def test_marketing_consent_is_not_bundled(self):
        self.assertNotIn("marketing-consent", self.index)
        self.assertIn("not be added to a general marketing list", self.privacy)

    def test_terms_disclose_selection_and_exclusions(self):
        terms_lower = self.terms.lower()
        for value in [
            "not a random drawing", "no purchase is required", "no result is guaranteed",
            "gym access", "healthcare", "medical clearance", "two sponsored seats",
        ]:
            self.assertIn(value, terms_lower)

    def test_terms_and_privacy_links_are_visible(self):
        self.assertIn('href="terms.html"', self.index)
        self.assertIn('href="privacy.html"', self.index)

    def test_success_page_does_not_promise_selection_or_message(self):
        self.assertIn("does not guarantee selection", self.success)
        self.assertIn("contacted privately", self.success)
        self.assertNotIn("check your inbox", self.success.lower())

    def test_no_obsolete_dates_or_placeholders(self):
        combined = "\n".join((self.index, self.terms, self.privacy, self.success))
        self.assertNotIn("September 18", combined)
        self.assertNotRegex(combined, r"\[[A-Z][A-Z0-9 _-]+\]")


if __name__ == "__main__":
    unittest.main()
