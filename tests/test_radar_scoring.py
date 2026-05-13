from __future__ import annotations

import unittest

from radar import _candidate_to_row
from scoring.engine import Candidate, PaymentType, score_candidate


class RadarScoringTests(unittest.TestCase):
    def test_zero_bounty_issue_moves_to_practice_lane(self):
        candidate = Candidate(
            source="github",
            repo="example/repo",
            issue_number=1,
            title="Fix docs typo",
            url="https://github.com/example/repo/issues/1",
            labels=["documentation"],
            bounty_amount=0,
            payment_type=PaymentType.NONE,
            has_repro_steps=True,
            has_acceptance_criteria=True,
            is_local_modifiable=True,
            has_test_suite=True,
            estimated_hours=1.0,
        )

        scored = score_candidate(candidate)
        row = _candidate_to_row(scored, require_payment_for_top=True, min_expected_value=0)
        self.assertEqual(row["lane"], "practice")

    def test_positive_ev_bounty_stays_in_money_lane(self):
        candidate = Candidate(
            source="algora",
            repo="vercel/next.js",
            issue_number=2,
            title="Fix bug with payout",
            url="https://github.com/vercel/next.js/issues/2",
            labels=["bug", "good first issue"],
            bounty_amount=500,
            payment_type=PaymentType.ESCROW,
            has_repro_steps=True,
            has_failing_test=True,
            has_acceptance_criteria=True,
            is_local_modifiable=True,
            has_test_suite=True,
            maintainer_merged_ext_pr_30d=5,
            maintainer_merged_ext_pr_90d=10,
            maintainer_response_days=2,
            repo_in_whitelist=True,
            estimated_hours=2.0,
        )

        scored = score_candidate(candidate)
        row = _candidate_to_row(scored, require_payment_for_top=True, min_expected_value=0)
        self.assertEqual(row["lane"], "money")
        self.assertGreater(row["expected_value"], 0)

    def test_security_without_poc_is_skipped(self):
        candidate = Candidate(
            source="huntr",
            repo="secure/repo",
            issue_number=3,
            title="Security issue",
            url="https://example.com/3",
            payment_type=PaymentType.PLATFORM,
            is_security=True,
            has_scope=True,
        )

        scored = score_candidate(candidate)
        self.assertIsNotNone(scored.skip_reason)

    def test_payout_blocked_flag_survives_candidate_row(self):
        candidate = Candidate(
            source="github",
            repo="pay/repo",
            issue_number=4,
            title="Bounty issue",
            url="https://example.com/4",
            bounty_amount=100,
            payment_type=PaymentType.TIPPING,
            preflight_flags=["payout-blocked"],
            is_local_modifiable=True,
        )

        scored = score_candidate(candidate)
        row = _candidate_to_row(scored, require_payment_for_top=True, min_expected_value=0)
        self.assertIn("payout-blocked", row["preflight_flags"])


if __name__ == "__main__":
    unittest.main()
