from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tracker.tracker import DeliveryTracker, TaskRecord


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.reports = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_upsert_is_idempotent(self):
        tracker = DeliveryTracker(str(self.reports))
        record = TaskRecord(
            task_id="owner/repo#1",
            source="github",
            repo="owner/repo",
            issue_number=1,
            title="Initial",
            url="https://example.com/1",
            score=10,
            expected_value=1,
            lane="money",
            status="pending_review",
        )
        tracker.upsert(record)
        tracker.upsert(TaskRecord(task_id="owner/repo#1", repo="owner/repo", issue_number=1, title="Updated", score=20, expected_value=2, status="approved"))

        self.assertEqual(len(tracker.records), 1)
        self.assertEqual(tracker.records[0].title, "Updated")
        self.assertEqual(tracker.records[0].status, "approved")

    def test_generate_daily_report_contains_new_flow_sections(self):
        tracker = DeliveryTracker(str(self.reports))
        tracker.upsert(
            TaskRecord(
                task_id="owner/repo#2",
                source="github",
                repo="owner/repo",
                issue_number=2,
                title="Money task",
                url="https://example.com/2",
                score=50,
                expected_value=12,
                lane="money",
                status="pending_review",
            )
        )

        report = tracker.generate_daily_report()
        self.assertIn("流程状态", report)
        self.assertIn("待审批", report)


if __name__ == "__main__":
    unittest.main()
