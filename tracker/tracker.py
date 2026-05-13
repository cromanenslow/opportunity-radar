"""Opportunity Radar - 交付追踪器

记录每个任务从发现到收款的全生命周期。
事实源以 task_records.csv 为准，scan/review/execute/report 都围绕它运转。
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


ACTIVE_STATUSES = {
    "pending_review",
    "approved",
    "preflight_running",
    "preflight_passed",
    "needs_manual_triage",
    "patching",
    "pr_opened",
    "ci_pass",
    "reviewing",
}

PR_SUBMITTED_STATUSES = {"pr_opened", "ci_pass", "reviewing", "merged", "paid"}
MERGED_STATUSES = {"merged", "paid"}
PREFLIGHT_ATTEMPTED_STATUSES = {"preflight_passed", "preflight_failed", "needs_manual_triage", "patching", "pr_opened", "ci_pass", "reviewing", "merged", "paid"}


@dataclass
class TaskRecord:
    """单个任务的完整记录。"""

    task_id: str = ""
    source: str = ""
    repo: str = ""
    issue_number: int = 0
    title: str = ""
    url: str = ""
    discovered_at: str = ""

    score: float = 0.0
    expected_value: float = 0.0
    is_security: bool = False
    human_approved: bool = False
    lane: str = "practice"
    payment_type: str = "none"
    selection_reason: str = ""
    blocked_reason: str = ""
    preflight_command_hint: str = ""

    status: str = "discovered"
    started_at: str = ""
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    workspace_path: str = ""
    install_cmd: str = ""
    test_cmd: str = ""
    preflight_ran_at: str = ""

    pr_number: int = 0
    pr_url: str = ""
    pr_opened_at: str = ""
    pr_merged_at: str = ""

    bounty_amount: float = 0.0
    bounty_claimed: bool = False
    bounty_paid: bool = False
    paid_at: str = ""
    payment_method: str = ""

    maintainer_response_days: float = 0.0
    maintainer_comment: str = ""

    why_failed: str = ""
    repo_reuse_possible: bool = True
    notes: str = ""


CSV_FIELDS = [
    "task_id",
    "source",
    "repo",
    "issue_number",
    "title",
    "url",
    "discovered_at",
    "score",
    "expected_value",
    "is_security",
    "human_approved",
    "lane",
    "payment_type",
    "selection_reason",
    "blocked_reason",
    "preflight_command_hint",
    "status",
    "started_at",
    "estimated_hours",
    "actual_hours",
    "workspace_path",
    "install_cmd",
    "test_cmd",
    "preflight_ran_at",
    "pr_number",
    "pr_url",
    "pr_opened_at",
    "pr_merged_at",
    "bounty_amount",
    "bounty_claimed",
    "bounty_paid",
    "paid_at",
    "payment_method",
    "maintainer_response_days",
    "maintainer_comment",
    "why_failed",
    "repo_reuse_possible",
    "notes",
]


def _bool_from_row(value: str, default: bool = False) -> bool:
    if value == "":
        return default
    return str(value).lower() in ("true", "1", "yes")


def _float_from_row(value: str, default: float = 0.0) -> float:
    if value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int_from_row(value: str, default: int = 0) -> int:
    if value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class DeliveryTracker:
    """交付追踪器。"""

    def __init__(self, data_dir: str = "reports"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.records_file = self.data_dir / "task_records.csv"
        self.records: list[TaskRecord] = []
        self._load()

    def _load(self):
        """加载历史记录。"""
        if not self.records_file.exists():
            return

        with open(self.records_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append(self._record_from_row(row))

    def _record_from_row(self, row: dict[str, str]) -> TaskRecord:
        return TaskRecord(
            task_id=row.get("task_id", ""),
            source=row.get("source", ""),
            repo=row.get("repo", ""),
            issue_number=_int_from_row(row.get("issue_number", "")),
            title=row.get("title", ""),
            url=row.get("url", ""),
            discovered_at=row.get("discovered_at", ""),
            score=_float_from_row(row.get("score", "")),
            expected_value=_float_from_row(row.get("expected_value", "")),
            is_security=_bool_from_row(row.get("is_security", "")),
            human_approved=_bool_from_row(row.get("human_approved", "")),
            lane=row.get("lane", "practice") or "practice",
            payment_type=row.get("payment_type", "none") or "none",
            selection_reason=row.get("selection_reason", ""),
            blocked_reason=row.get("blocked_reason", ""),
            preflight_command_hint=row.get("preflight_command_hint", ""),
            status=row.get("status", "discovered") or "discovered",
            started_at=row.get("started_at", ""),
            estimated_hours=_float_from_row(row.get("estimated_hours", "")),
            actual_hours=_float_from_row(row.get("actual_hours", "")),
            workspace_path=row.get("workspace_path", ""),
            install_cmd=row.get("install_cmd", ""),
            test_cmd=row.get("test_cmd", ""),
            preflight_ran_at=row.get("preflight_ran_at", ""),
            pr_number=_int_from_row(row.get("pr_number", "")),
            pr_url=row.get("pr_url", ""),
            pr_opened_at=row.get("pr_opened_at", ""),
            pr_merged_at=row.get("pr_merged_at", ""),
            bounty_amount=_float_from_row(row.get("bounty_amount", "")),
            bounty_claimed=_bool_from_row(row.get("bounty_claimed", "")),
            bounty_paid=_bool_from_row(row.get("bounty_paid", "")),
            paid_at=row.get("paid_at", ""),
            payment_method=row.get("payment_method", ""),
            maintainer_response_days=_float_from_row(row.get("maintainer_response_days", "")),
            maintainer_comment=row.get("maintainer_comment", ""),
            why_failed=row.get("why_failed", ""),
            repo_reuse_possible=_bool_from_row(row.get("repo_reuse_possible", ""), default=True),
            notes=row.get("notes", ""),
        )

    def save(self):
        """保存记录。"""
        with open(self.records_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for record in self.records:
                writer.writerow(asdict(record))

    def _normalize_record(self, record: TaskRecord) -> TaskRecord:
        if not record.discovered_at:
            record.discovered_at = date.today().isoformat()
        if not record.task_id:
            record.task_id = f"{record.repo}#{record.issue_number}"
        return record

    def add(self, record: TaskRecord):
        """兼容旧接口，行为等同于 upsert。"""
        self.upsert(record)

    def upsert(self, record: TaskRecord):
        """按 task_id 幂等写入记录。"""
        record = self._normalize_record(record)
        existing = self.find_by_task_id(record.task_id)
        if existing:
            clearable_fields = {"selection_reason", "blocked_reason", "preflight_command_hint", "workspace_path", "install_cmd", "test_cmd", "notes"}
            for field_name, value in asdict(record).items():
                if field_name == "task_id":
                    continue
                if value not in ("", 0, 0.0, False) or field_name in clearable_fields:
                    setattr(existing, field_name, value)
            if record.human_approved:
                existing.human_approved = True
            if record.status and record.status != "discovered":
                existing.status = record.status
        else:
            self.records.append(record)
        self.save()

    def update_status(self, task_id: str, status: str, **kwargs):
        """更新任务状态。"""
        for record in self.records:
            if record.task_id == task_id:
                record.status = status
                for key, value in kwargs.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                self.save()
                return True
        return False

    def update_record(self, task_id: str, **kwargs):
        """更新任务其他字段，不改变状态。"""
        for record in self.records:
            if record.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                self.save()
                return True
        return False

    def find_by_task_id(self, task_id: str) -> TaskRecord | None:
        for record in self.records:
            if record.task_id == task_id:
                return record
        return None

    def get_by_status(self, statuses: set[str]) -> list[TaskRecord]:
        return [record for record in self.records if record.status in statuses]

    def get_active(self) -> list[TaskRecord]:
        return self.get_by_status(ACTIVE_STATUSES)

    def get_by_lane_and_status(self, lane: str, statuses: set[str]) -> list[TaskRecord]:
        return [record for record in self.records if record.lane == lane and record.status in statuses]

    def get_today_discovered(self) -> list[TaskRecord]:
        today = date.today().isoformat()
        return [record for record in self.records if record.discovered_at == today]

    def compute_metrics(self, days: int = 30) -> dict:
        """计算核心指标。"""
        cutoff = date.today().toordinal() - days
        recent = [
            record
            for record in self.records
            if record.discovered_at
            and date.fromisoformat(record.discovered_at).toordinal() >= cutoff
        ]

        if not recent:
            return {"message": f"近 {days} 天无数据"}

        submitted = [record for record in recent if record.status in PR_SUBMITTED_STATUSES]
        merged = [record for record in recent if record.status in MERGED_STATUSES]
        paid = [record for record in recent if record.bounty_paid or record.status == "paid"]
        money_candidates = [record for record in recent if record.lane == "money"]
        preflight_attempted = [record for record in recent if record.status in PREFLIGHT_ATTEMPTED_STATUSES]
        preflight_passed = [record for record in preflight_attempted if record.status == "preflight_passed"]

        merge_rate = len(merged) / len(submitted) if submitted else 0.0
        total_hours = sum(record.actual_hours for record in merged if record.actual_hours > 0)
        total_paid = sum(record.bounty_amount for record in paid)
        dollar_per_hour = total_paid / total_hours if total_hours > 0 else 0.0
        preflight_pass_rate = len(preflight_passed) / len(preflight_attempted) if preflight_attempted else 0.0

        repo_stats: dict[str, dict] = {}
        source_stats: dict[str, dict] = {}
        status_counts: dict[str, int] = {}

        for record in recent:
            repo_stats.setdefault(record.repo, {"total": 0, "merged": 0, "paid": 0.0})
            repo_stats[record.repo]["total"] += 1
            if record.status in MERGED_STATUSES:
                repo_stats[record.repo]["merged"] += 1
            if record.bounty_paid:
                repo_stats[record.repo]["paid"] += record.bounty_amount

            source_stats.setdefault(record.source, {"total": 0, "merged": 0, "paid": 0.0})
            source_stats[record.source]["total"] += 1
            if record.status in MERGED_STATUSES:
                source_stats[record.source]["merged"] += 1
            if record.bounty_paid:
                source_stats[record.source]["paid"] += record.bounty_amount

            status_counts[record.status] = status_counts.get(record.status, 0) + 1

        return {
            "period_days": days,
            "total_discovered": len(recent),
            "money_candidates": len(money_candidates),
            "total_submitted": len(submitted),
            "total_merged": len(merged),
            "total_paid": len(paid),
            "merge_rate": round(merge_rate, 2),
            "preflight_pass_rate": round(preflight_pass_rate, 2),
            "total_earned_usd": round(total_paid, 2),
            "total_agent_hours": round(total_hours, 1),
            "dollar_per_agent_hour": round(dollar_per_hour, 2),
            "money_candidates_per_day": round(len(money_candidates) / days, 2),
            "accepted_pr_per_day": round(len(merged) / days, 2),
            "paid_pr_per_day": round(len(paid) / days, 2),
            "repo_stats": repo_stats,
            "source_stats": source_stats,
            "status_counts": status_counts,
        }

    def generate_daily_report(self) -> str:
        """生成日报。"""
        today = date.today().isoformat()
        discovered = self.get_today_discovered()
        active = self.get_active()
        metrics = self.compute_metrics(30)

        status_groups = {
            "pending_review": len([record for record in discovered if record.status == "pending_review"]),
            "approved": len([record for record in active if record.status == "approved"]),
            "preflight_running": len([record for record in active if record.status == "preflight_running"]),
            "reviewing": len([record for record in active if record.status == "reviewing"]),
            "merged": metrics.get("total_merged", 0),
            "paid": metrics.get("total_paid", 0),
        }

        lines = [
            f"# Opportunity Radar - 日报 {today}",
            "",
            f"## 候选任务 ({len(discovered)} 个发现)",
            "| # | Lane | Repo | Issue | Score | EV | 状态 |",
            "|---|------|------|-------|-------|----|------|",
        ]

        for index, record in enumerate(discovered[:15], 1):
            lines.append(
                f"| {index} | {record.lane} | {record.repo} | #{record.issue_number} | "
                f"{record.score} | ${record.expected_value}/hr | {record.status} |"
            )

        lines.extend(
            [
                "",
                "## 流程状态",
                f"- 待审批: {status_groups['pending_review']}",
                f"- 已批准: {status_groups['approved']}",
                f"- 本地预检中: {status_groups['preflight_running']}",
                f"- PR Review 中: {status_groups['reviewing']}",
                f"- 已合并: {status_groups['merged']}",
                f"- 已付款: {status_groups['paid']}",
                "",
                "## 进行中任务",
                "| Repo | Issue | 状态 | 备注 |",
                "|------|-------|------|------|",
            ]
        )

        for record in active:
            note = record.blocked_reason or record.selection_reason or "-"
            lines.append(f"| {record.repo} | #{record.issue_number} | {record.status} | {note[:80]} |")

        lines.extend(
            [
                "",
                "## 30天指标",
                f"- 赚钱候选/天: {metrics.get('money_candidates_per_day', 'N/A')}",
                f"- 预检通过率: {metrics.get('preflight_pass_rate', 'N/A')}",
                f"- 合并率: {metrics.get('merge_rate', 'N/A')}",
                f"- $/agent-hour: ${metrics.get('dollar_per_agent_hour', 'N/A')}",
                f"- 总收入: ${metrics.get('total_earned_usd', 'N/A')}",
            ]
        )

        report = "\n".join(lines)
        report_file = self.data_dir / f"daily_{today}.md"
        report_file.write_text(report, encoding="utf-8")
        return report


if __name__ == "__main__":
    tracker = DeliveryTracker()
    tracker.upsert(
        TaskRecord(
            task_id="vercel/next.js#12345",
            source="algora",
            repo="vercel/next.js",
            issue_number=12345,
            title="Fix hydration mismatch",
            url="https://github.com/vercel/next.js/issues/12345",
            score=82,
            expected_value=45,
            human_approved=True,
            lane="money",
            payment_type="escrow",
            status="approved",
            estimated_hours=3,
            bounty_amount=500,
        )
    )
    print(tracker.generate_daily_report())
