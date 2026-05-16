from __future__ import annotations

import unittest

from radar import _expensify_money_issue_flags


class ExpensifyPreflightTests(unittest.TestCase):
    def test_closed_non_money_issue_is_terminal(self):
        flags = _expensify_money_issue_flags(
            {
                "title": "Web - Workspace issues are not aligned in workspace list",
                "state": "CLOSED",
                "closed": True,
                "labels": [{"name": "Daily"}, {"name": "Bug"}],
                "assignees": [{"login": "garrettmknight"}],
            }
        )

        self.assertIn("closed", flags)
        self.assertIn("has-assignee", flags)
        self.assertIn("not-expensify-money", flags)

    def test_open_unassigned_250_external_help_wanted_passes(self):
        flags = _expensify_money_issue_flags(
            {
                "title": "[$250] Fix a focused UI bug",
                "state": "OPEN",
                "closed": False,
                "labels": [{"name": "External"}, {"name": "Help Wanted"}, {"name": "Bug"}],
                "assignees": [],
            }
        )

        self.assertEqual(flags, [])

    def test_assigned_250_issue_is_terminal(self):
        flags = _expensify_money_issue_flags(
            {
                "title": "[$250] Fix a focused UI bug",
                "state": "OPEN",
                "closed": False,
                "labels": [{"name": "External"}, {"name": "Help Wanted"}],
                "assignees": [{"login": "someone"}],
            }
        )

        self.assertEqual(flags, ["has-assignee"])


if __name__ == "__main__":
    unittest.main()
