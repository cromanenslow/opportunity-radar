from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from radar import _clone_target_path, _detect_commands, _is_partial_clone, _looks_like_missing_tests, _preflight_record
from tracker.tracker import TaskRecord


class ExecuteHelpersTests(unittest.TestCase):
    def test_clone_target_path_uses_owner_repo_issue(self):
        workspace_root = Path("/tmp/workspaces")
        record = TaskRecord(repo="owner/repo", issue_number=42)
        self.assertEqual(_clone_target_path(workspace_root, record), workspace_root / "owner__repo__42")

    def test_detect_commands_for_unknown_python_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "requirements.txt").write_text("pytest\n", encoding="utf-8")
            record = TaskRecord(repo="owner/repo", issue_number=1)
            install_cmd, test_cmd = _detect_commands(repo_path, {}, record)
            self.assertIn("-m pip install -r requirements.txt", install_cmd)
            self.assertIn("-m unittest discover", test_cmd)

    def test_detect_commands_prefers_whitelist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            record = TaskRecord(repo="owner/repo", issue_number=1)
            install_cmd, test_cmd = _detect_commands(
                repo_path,
                {"owner/repo": {"install_cmd": "pnpm install", "test_cmd": "pnpm test"}},
                record,
            )
            self.assertEqual(install_cmd, "pnpm install")
            self.assertEqual(test_cmd, "pnpm test")

    def test_preflight_triages_missing_bun(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "bunfig.toml").write_text("", encoding="utf-8")
            record = TaskRecord(repo="owner/repo", issue_number=1)
            config = {"execution": {"workspace_dir": tmpdir, "clone_timeout_seconds": 1, "install_timeout_seconds": 1, "test_timeout_seconds": 1}}
            with patch("radar._clone_target_path", return_value=repo_path):
                with patch("radar.shutil.which", return_value=None):
                    status, _, install_cmd, test_cmd, note = _preflight_record(record, config, {})
            self.assertEqual(status, "needs_manual_triage")
            self.assertEqual(install_cmd, "bun install")
            self.assertEqual(test_cmd, "bun test")
            self.assertIn("缺少本地工具: bun", note)

    def test_detect_commands_prefers_unittest_folder_for_python_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "pyproject.toml").write_text("", encoding="utf-8")
            (repo_path / "UNITTESTS").mkdir()
            record = TaskRecord(repo="owner/repo", issue_number=1)
            install_cmd, test_cmd = _detect_commands(repo_path, {}, record)
            self.assertIn("-m pip install -e .", install_cmd)
            self.assertIn("-m unittest discover UNITTESTS", test_cmd)

    def test_partial_clone_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir) / "repo"
            repo_path.mkdir()
            (repo_path / ".git").mkdir()
            self.assertTrue(_is_partial_clone(repo_path))

    def test_missing_tests_output_is_treated_as_triage_signal(self):
        self.assertTrue(_looks_like_missing_tests("Ran 0 tests in 0.000s\n\nNO TESTS RAN"))


if __name__ == "__main__":
    unittest.main()
