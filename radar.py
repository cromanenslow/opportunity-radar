"""Opportunity Radar - 主编排脚本

每日运行入口：
  python radar.py scan
  python radar.py review
  python radar.py execute
  python radar.py report
  python radar.py metrics
"""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from scoring.engine import Candidate, PaymentType, ScoredCandidate, batch_score, load_weights_from_config
from scanner.github import (
    run_daily_github_scan,
    search_issues,
    scan_known_bounty_repos,
    load_known_bounty_repos,
)
from scanner.platforms import PlatformBounty, run_daily_platform_scan
from tracker.tracker import DeliveryTracker, TaskRecord
from whitelist.initial_whitelist import load_whitelist


TERMINAL_PREFLIGHT_FLAGS = {"closed", "locked", "already-contested", "has-linked-pr", "has-pr-in-thread"}
MANUAL_APPROVAL_FLAGS = {"new-repo", "ui-manual-check", "large-change-risk", "payout-unknown"}


def load_config() -> dict:
    config_path = PROJECT_ROOT / "config.yaml"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def platform_bounty_to_candidate(bounty: PlatformBounty, whitelist_names: set[str]) -> Candidate:
    payment_map = {
        "escrow": PaymentType.ESCROW,
        "platform": PaymentType.PLATFORM,
        "tipping": PaymentType.TIPPING,
        "sponsor": PaymentType.SPONSOR,
        "implied": PaymentType.IMPLIED,
    }

    is_security = "security" in bounty.labels or bounty.platform in ("huntr",)

    return Candidate(
        source=bounty.platform,
        repo=bounty.repo,
        issue_number=bounty.issue_number,
        title=bounty.title,
        url=bounty.url,
        labels=bounty.labels,
        bounty_amount=bounty.amount,
        payment_type=payment_map.get(bounty.payment_type, PaymentType.PLATFORM),
        has_repro_steps=bool(bounty.description and ("repro" in bounty.description.lower() or "steps" in bounty.description.lower())),
        has_failing_test=False,
        has_acceptance_criteria=bool(bounty.description and ("accept" in bounty.description.lower() or "criteria" in bounty.description.lower())),
        is_local_modifiable=True,
        has_test_suite=True,
        maintainer_response_days=7.0,
        repo_in_whitelist=bounty.repo in whitelist_names,
        is_familiar_repo=False,
        estimated_hours=2.0,
        is_security=is_security,
        has_poc=is_security and bool(bounty.description and "poc" in bounty.description.lower()),
        has_scope=is_security and bool(bounty.description and ("scope" in bounty.description.lower() or "authorized" in bounty.description.lower())),
        has_sponsors=False,
        bounty_history=0.0,
        description=bounty.description,
    )


def _days_since_github_timestamp(timestamp: str) -> float:
    if not timestamp:
        return 0.0
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 86400)
    except ValueError:
        return 0.0


def _preflight_flags(
    repo: str,
    combined: str,
    labels: list[str],
    in_whitelist: bool,
    bounty_amount: float = 0.0,
    payment_type: PaymentType = PaymentType.NONE,
) -> list[str]:
    flags: list[str] = []
    labels_lower = [label.lower() for label in labels]

    if not in_whitelist:
        flags.append("new-repo")
    if any(term in combined for term in ["ui", "frontend", "visual", "design", "layout", "avatar", "banner"]):
        flags.append("ui-manual-check")
    if any(term in combined for term in ["migration", "refactor", "rewrite", "architecture"]):
        flags.append("large-change-risk")
    if any(term in combined for term in ["repro", "steps to reproduce", "expected", "actual"]):
        flags.append("clear-repro")
    if "bug" in labels_lower:
        flags.append("bug")
    if "good first issue" in labels_lower:
        flags.append("good-first-issue")

    kyc_terms = ["kyc", "tax form", "tax forms", "1099", "w-8", "w8", "w-9", "w9", "invoice required"]
    no_kyc_terms = ["no kyc", "without kyc", "no tax form", "no tax forms", "tip", "github sponsors", "paypal", "wise"]

    if any(term in combined for term in kyc_terms) and not any(term in combined for term in no_kyc_terms):
        flags.append("payout-blocked")
    elif bounty_amount > 0 and payment_type in (PaymentType.TIPPING, PaymentType.IMPLIED):
        if not any(term in combined for term in no_kyc_terms):
            flags.append("payout-unknown")

    return flags


def github_issue_to_candidate(issue, whitelist_names: set[str], whitelist_data: dict) -> Candidate:
    body = issue.body or ""
    title = issue.title or ""
    combined = f"{title} {body}".lower()
    bounty_amount = 0.0
    payment_type = PaymentType.NONE
    issue_age_days = _days_since_github_timestamp(getattr(issue, "updated_at", ""))

    label_names_lower = [label.lower() for label in issue.labels]
    has_bounty_signal = "bounty" in label_names_lower or "bounty" in combined or "reward" in combined or "$" in title
    if has_bounty_signal:
        import re

        title_amounts = re.findall(r"\$(\d+)", title)
        body_amounts = re.findall(r"\$(\d+)", body)
        all_amounts = [int(amount) for amount in (title_amounts + body_amounts) if int(amount) > 0]
        if all_amounts:
            bounty_amount = max(all_amounts)
            payment_type = PaymentType.TIPPING
        elif "bounty" in label_names_lower:
            payment_type = PaymentType.IMPLIED

    in_whitelist = issue.repo in whitelist_names
    repo_info = whitelist_data.get(issue.repo, {})

    if in_whitelist:
        maint_days = repo_info.get("maintainer_response_days", 7.0)
        ext_pr_30d = repo_info.get("ext_pr_30d", 1)
        ext_pr_90d = repo_info.get("ext_pr_90d", 3)
        has_sponsors = repo_info.get("has_sponsors", False)
        bounty_history = repo_info.get("bounty_history", 0)
        if payment_type == PaymentType.NONE:
            if has_sponsors:
                payment_type = PaymentType.SPONSOR
                implicit_amount = min(250, max(50, bounty_history * 0.05)) if bounty_history > 0 else 75
                bounty_amount = max(bounty_amount, implicit_amount)
            elif bounty_history > 0:
                payment_type = PaymentType.IMPLIED
                bounty_amount = max(bounty_amount, min(250, bounty_history * 0.05))
    else:
        maint_days = 14.0
        ext_pr_30d = 0
        ext_pr_90d = 0

    estimated_hours = 2.0
    if any(term in combined for term in ["migration", "refactor", "rewrite", "new api", "behavior"]):
        estimated_hours = 4.0
    elif any(term in combined for term in ["typo", "spelling", "broken link"]):
        estimated_hours = 0.5
    elif "docs" in combined and not any(term in combined for term in ["api", "behavior", "support"]):
        estimated_hours = 1.0

    is_security = "security" in label_names_lower or "vulnerability" in label_names_lower or "cve" in combined

    return Candidate(
        source="github",
        repo=issue.repo,
        issue_number=issue.issue_number,
        title=issue.title,
        url=issue.url,
        labels=issue.labels,
        bounty_amount=bounty_amount,
        payment_type=payment_type,
        has_repro_steps="repro" in combined or "steps to reproduce" in combined or "stack trace" in combined or "error:" in combined,
        has_failing_test="failing test" in combined or "regression test" in combined,
        has_acceptance_criteria="accept" in combined or "criteria" in combined or "definition of done" in combined or "expected" in combined,
        is_local_modifiable=True,
        has_test_suite=repo_info.get("has_test_suite", in_whitelist),
        maintainer_response_days=maint_days,
        maintainer_merged_ext_pr_30d=ext_pr_30d,
        maintainer_merged_ext_pr_90d=ext_pr_90d,
        repo_in_whitelist=in_whitelist,
        is_familiar_repo=False,
        estimated_hours=estimated_hours,
        is_security=is_security,
        has_poc="poc" in combined or "proof of concept" in combined,
        has_scope="authorized" in combined or "scope" in combined,
        has_sponsors=bool(repo_info.get("has_sponsors", False)),
        bounty_history=float(repo_info.get("bounty_history", 0.0)),
        issue_age_days=issue_age_days,
        preflight_flags=_preflight_flags(issue.repo, combined, issue.labels, in_whitelist, bounty_amount=bounty_amount, payment_type=payment_type),
        description=body[:1000],
    )


def _build_whitelist_data() -> tuple[list, set[str], dict[str, dict]]:
    whitelist = load_whitelist()
    whitelist_names = {repo.full_name for repo in whitelist}
    whitelist_data = {
        repo.full_name: {
            "language": repo.language,
            "install_cmd": repo.install_cmd,
            "test_cmd": repo.test_cmd,
            "maintainer_response_days": repo.maintainer_response_days,
            "ext_pr_30d": int(repo.ext_pr_merge_rate_90d * 3),
            "ext_pr_90d": int(repo.ext_pr_merge_rate_90d * 10),
            "has_test_suite": True,
            "has_sponsors": repo.has_sponsors,
            "bounty_history": repo.bounty_history,
        }
        for repo in whitelist
    }
    return whitelist, whitelist_names, whitelist_data


def _deep_preflight_issue(candidate: dict) -> list[str]:
    repo = candidate.get("repo", "")
    issue_number = str(candidate.get("issue_number", ""))
    if not repo or not issue_number:
        return []

    result = subprocess.run(
        [
            "gh",
            "issue",
            "view",
            issue_number,
            "--repo",
            repo,
            "--json",
            "body,comments,closed,closedByPullRequestsReferences,state,url",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        return ["deep-preflight-failed"]

    data = json.loads(result.stdout)
    flags: list[str] = []
    text_parts = [data.get("body", "") or ""]
    for comment in data.get("comments", []) or []:
        text_parts.append(comment.get("body", "") or "")
    text = "\n".join(text_parts).lower()

    if data.get("closed") or data.get("state") == "CLOSED":
        flags.append("closed")
    if "automatically locked" in text or "locked due to inactivity" in text:
        flags.append("locked")
    if "already in progress" in text or "i would like to work" in text or "/attempt" in text:
        flags.append("already-contested")
    if data.get("closedByPullRequestsReferences"):
        flags.append("has-linked-pr")
    if "pr is merged" in text or "pr is already" in text or "already have another pr" in text or "pull/" in text:
        flags.append("has-pr-in-thread")
    if "supported countries" in text or "eligible for payouts" in text:
        flags.append("payout-eligibility-unknown")
    return flags


def _enrich_competition_data(candidate: Candidate) -> Candidate:
    """
    通过 gh CLI 查询 issue 的 assignees 和开放 PR 数量，
    用于竞争强度评分。
    """
    if candidate.source != "github" or not candidate.repo or not candidate.issue_number:
        return candidate  # 非 GitHub 来源无法查询

    result = subprocess.run(
        [
            "gh", "issue", "view", str(candidate.issue_number),
            "--repo", candidate.repo,
            "--json", "assignees,closedByPullRequestsReferences,body,comments,state",
        ],
        capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        return candidate

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return candidate

    # assignee count
    candidate.assignee_count = len(data.get("assignees", []) or [])

    # Count open PRs from closedByPullRequestsReferences
    open_pr_count = 0
    for pr in data.get("closedByPullRequestsReferences", []) or []:
        if pr.get("state") == "OPEN":
            open_pr_count += 1

    # Also count "/attempt" and PR mentions in comments/body as additional competition signal
    text_parts = [data.get("body", "") or ""]
    for comment in data.get("comments", []) or []:
        text_parts.append(comment.get("body", "") or "")
    text = " ".join(text_parts).lower()
    # Count /attempt and "pull/" mentions
    attempt_count = text.count("/attempt")
    pull_mention_count = text.count("pull/")
    # Add these as approximate open PR count (already counted in closedByPullRequestsReferences)
    combined_pr_estimate = max(open_pr_count, attempt_count + (pull_mention_count > 0))

    candidate.open_pr_count = combined_pr_estimate

    return candidate


def _candidate_to_row(scored: ScoredCandidate, require_payment_for_top: bool, min_expected_value: float) -> dict:
    flags = list(scored.candidate.preflight_flags)
    payment_type = scored.candidate.payment_type.value
    payment_ready = scored.candidate.bounty_amount > 0 or scored.candidate.payment_type != PaymentType.NONE
    blocked_reason = scored.blocked_reason
    lane = scored.lane
    selection_reason = scored.selection_reason

    if lane == "money":
        if require_payment_for_top and not payment_ready:
            lane = "practice"
            selection_reason = "暂无明确支付路径，转入练手池"
        elif scored.expected_value <= min_expected_value:
            lane = "practice"
            selection_reason = f"EV={scored.expected_value}，未达到赚钱榜门槛"
            blocked_reason = selection_reason

    return {
        "task_id": f"{scored.candidate.repo}#{scored.candidate.issue_number}",
        "repo": scored.candidate.repo,
        "issue_number": scored.candidate.issue_number,
        "title": scored.candidate.title,
        "url": scored.candidate.url,
        "score": scored.total_score,
        "expected_value": scored.expected_value,
        "bounty": scored.candidate.bounty_amount,
        "source": scored.candidate.source,
        "is_security": scored.candidate.is_security,
        "needs_human_approval": scored.needs_human_approval,
        "issue_age_days": scored.candidate.issue_age_days,
        "preflight_flags": flags,
        "payment_score": scored.payment_score,
        "verifiability_score": scored.verifiability_score,
        "ai_fitness_score": scored.ai_fitness_score,
        "maintainer_score": scored.maintainer_score,
        "context_score": scored.context_score,
        "competition_score": scored.competition_score,
        "risk_penalty": scored.risk_penalty,
        "lane": lane,
        "payment_type": payment_type,
        "selection_reason": selection_reason,
        "blocked_reason": blocked_reason,
        "preflight_command_hint": "",
    }


def _sync_candidates_to_tracker(tracker: DeliveryTracker, rows: list[dict]):
    for row in rows:
        existing = tracker.find_by_task_id(row["task_id"])
        status = existing.status if existing else "pending_review"
        tracker.upsert(
            TaskRecord(
                task_id=row["task_id"],
                source=row["source"],
                repo=row["repo"],
                issue_number=row["issue_number"],
                title=row["title"],
                url=row["url"],
                score=row["score"],
                expected_value=row["expected_value"],
                is_security=row["is_security"],
                lane=row["lane"],
                payment_type=row["payment_type"],
                selection_reason=row["selection_reason"],
                blocked_reason=row["blocked_reason"],
                preflight_command_hint=row["preflight_command_hint"],
                status=status,
                estimated_hours=2.0,
                bounty_amount=row["bounty"],
            )
        )


def _write_candidates_file(payload: dict):
    candidates_file = PROJECT_ROOT / "reports" / f"candidates_{date.today().isoformat()}.json"
    candidates_file.parent.mkdir(parents=True, exist_ok=True)
    with open(candidates_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return candidates_file


def _load_candidates_payload() -> dict:
    candidates_file = PROJECT_ROOT / "reports" / f"candidates_{date.today().isoformat()}.json"
    if not candidates_file.exists():
        raise FileNotFoundError("未找到今日候选清单，请先运行 scan")
    with open(candidates_file, encoding="utf-8") as f:
        return json.load(f)


def _print_candidate_summary(title: str, rows: list[dict]):
    print(f"\n{title}")
    if not rows:
        print("  - 无")
        return
    for index, row in enumerate(rows, 1):
        approval = "需审批" if row["needs_human_approval"] else "可自动"
        print(f"  {index}. [{row['score']}] ${row['expected_value']}/hr {approval}")
        print(f"     {row['repo']}#{row['issue_number']} - {row['title'][:72]}")
        print(f"     bounty=${row['bounty']} payment={row['payment_type']} lane={row['lane']}")


def cmd_scan(config: dict):
    print("=" * 60)
    print(f"Opportunity Radar - 每日扫描 {date.today().isoformat()}")
    print("=" * 60)

    whitelist, whitelist_names, whitelist_data = _build_whitelist_data()
    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))

    platforms = config.get("scanner", {}).get("platforms", [])
    platform_bounties = run_daily_platform_scan(platforms)
    github_issues = run_daily_github_scan(config)

    print("\n=== 白名单 Repo 定向扫描 ===")
    # 按 bounty_history 排序，优先扫描有赏金历史/打赏渠道的仓库
    priority_repos = sorted(
        [repo for repo in whitelist if repo.bounty_history > 0 or repo.has_algora_tipping or repo.has_sponsors or repo.has_opencollective],
        key=lambda r: r.bounty_history,
        reverse=True,
    )
    scan_limit = min(20, len(priority_repos))  # 从 5 -> 20（来自优化建议2）
    print(f"  扫描 {scan_limit} 个高优先级 repo（按赏金历史排序）...")
    seen_urls = {issue.url for issue in github_issues}
    for repo in priority_repos[:scan_limit]:
        try:
            # 对有 bounty_history 的 repo，同时搜 bounty 标签
            labels_to_search = ["help wanted"]
            if repo.bounty_history > 0:
                labels_to_search = ["bounty", "help wanted"]
            issues = search_issues(query=f"repo:{repo.full_name}", labels=labels_to_search, limit=5, sort="updated")
            new_issues = [issue for issue in issues if issue.url not in seen_urls]
            seen_urls.update(issue.url for issue in new_issues)
            github_issues.extend(new_issues)
            print(f"  {repo.full_name}: +{len(new_issues)}")
        except Exception:
            continue

    # 已知赏金仓库补充扫描（从热区表加载不在白名单中的仓库）
    known_repos = load_known_bounty_repos(config)
    known_repo_names = {r["repo"] for r in known_repos}
    whitelist_names_set = {r.full_name for r in whitelist}
    extra_bounty_repos = [r for r in known_repos if r["repo"] not in whitelist_names_set]
    if extra_bounty_repos:
        print(f"  热区补充扫描: {len(extra_bounty_repos)} 个不在白名单的赏金仓库...")
        for repo_info in extra_bounty_repos[:5]:  # 限制5个避免太多请求
            repo_name = repo_info.get("repo", "")
            if not repo_name:
                continue
            try:
                issues = search_issues(query=f"repo:{repo_name} is:issue is:open", labels=["help wanted", "bounty"], limit=5, sort="updated")
                new_issues = [issue for issue in issues if issue.url not in seen_urls]
                seen_urls.update(issue.url for issue in new_issues)
                github_issues.extend(new_issues)
                if new_issues:
                    print(f"    {repo_name}: +{len(new_issues)}")
            except Exception:
                continue

    print(f"  白名单扫描后总计: {len(github_issues)} 个候选 issue")

    all_candidates: list[Candidate] = []
    for bounty in platform_bounties:
        all_candidates.append(platform_bounty_to_candidate(bounty, whitelist_names))
    for issue in github_issues:
        all_candidates.append(github_issue_to_candidate(issue, whitelist_names, whitelist_data))

    max_issue_age_days = config.get("scanner", {}).get("max_issue_age_days", 90)
    before_age_filter = len(all_candidates)
    all_candidates = [candidate for candidate in all_candidates if candidate.issue_age_days <= max_issue_age_days or candidate.bounty_amount >= 500]
    filtered_stale = before_age_filter - len(all_candidates)
    if filtered_stale:
        print(f"\n过滤陈旧 issue: {filtered_stale} 个超过 {max_issue_age_days} 天（高赏金例外）")

    payout_cfg = config.get("payout", {})
    if payout_cfg.get("filter_required_kyc", True):
        before_payout_filter = len(all_candidates)
        all_candidates = [candidate for candidate in all_candidates if "payout-blocked" not in candidate.preflight_flags]
        filtered_payout = before_payout_filter - len(all_candidates)
        if filtered_payout:
            print(f"过滤收款受阻候选: {filtered_payout} 个需要 KYC/税务资料")

    # 竞争强度数据预取
    print("\n=== 竞争强度数据预取 ===")
    enriched = 0
    for i, candidate in enumerate(all_candidates):
        if candidate.source != "github":
            continue
        if i >= 15:  # 最多预取前15个，控制API调用
            break
        _enrich_competition_data(candidate)
        enriched += 1
    print(f"  已预取 {enriched} 个候选的竞争数据")

    weights = load_weights_from_config(str(PROJECT_ROOT / "config.yaml"))
    scored = batch_score(all_candidates, weights)
    actionable = [item for item in scored if not item.skip_reason]
    skipped = [item for item in scored if item.skip_reason]

    scanner_cfg = config.get("scanner", {})
    top_n = scanner_cfg.get("top_n_candidates", 3)
    practice_backlog_size = scanner_cfg.get("practice_backlog_size", 10)
    require_payment_for_top = scanner_cfg.get("require_payment_for_top", True)
    min_expected_value = float(scanner_cfg.get("min_expected_value", 0))

    processed_rows: list[dict] = []
    blocked_by_deep_preflight = 0
    for index, scored_candidate in enumerate(actionable[:40]):
        row = _candidate_to_row(scored_candidate, require_payment_for_top, min_expected_value)
        if index < 10:
            deep_flags = _deep_preflight_issue(row)
            for flag in deep_flags:
                if flag not in row["preflight_flags"]:
                    row["preflight_flags"].append(flag)
            if TERMINAL_PREFLIGHT_FLAGS & set(row["preflight_flags"]):
                row["blocked_reason"] = "issue 已锁定、已有人处理或已有 PR"
                blocked_by_deep_preflight += 1
                continue
        processed_rows.append(row)

    money_candidates = [
        row for row in processed_rows
        if row["lane"] == "money"
        and row["expected_value"] > min_expected_value
        and "payout-blocked" not in row["preflight_flags"]
        and not row["blocked_reason"]
    ]
    practice_candidates = [row for row in processed_rows if row["lane"] != "money" or row["blocked_reason"]]

    money_top = money_candidates[:top_n]
    practice_backlog = practice_candidates[:practice_backlog_size]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "money_candidates": money_top,
        "practice_candidates": practice_backlog,
        "skipped": [
            {"task_id": f"{item.candidate.repo}#{item.candidate.issue_number}", "skip_reason": item.skip_reason}
            for item in skipped
        ],
    }

    _sync_candidates_to_tracker(tracker, money_top + practice_backlog)
    candidates_file = _write_candidates_file(payload)

    print(f"\n{'=' * 60}")
    print(f"打分完成: {len(actionable)} 个可执行 / {len(skipped)} 个跳过")
    if blocked_by_deep_preflight:
        print(f"深度预检过滤: {blocked_by_deep_preflight} 个已锁定/已有PR/已有人在做")
    print(f"{'=' * 60}")

    _print_candidate_summary("赚钱榜 Top", money_top)
    _print_candidate_summary("练手池", practice_backlog[:3])

    if skipped:
        print(f"\n⏭️ 跳过 {len(skipped)} 个：")
        for item in skipped[:5]:
            print(f"  - {item.candidate.repo}#{item.candidate.issue_number}: {item.skip_reason}")

    print(f"\n候选清单已保存: {candidates_file}")
    return payload


def cmd_review(config: dict):
    try:
        payload = _load_candidates_payload()
    except FileNotFoundError as exc:
        print(str(exc))
        return

    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))
    money_candidates = payload.get("money_candidates", [])

    if not money_candidates:
        print("今日没有赚钱榜候选。")
        return

    print(f"\n📋 今日赚钱榜审批 (共 {len(money_candidates)} 个)")
    print("=" * 72)
    for index, candidate in enumerate(money_candidates, 1):
        flags = candidate.get("preflight_flags", [])
        flags_text = ", ".join(flags) if flags else "none"
        print(f"{index}. [{candidate['score']}] ${candidate['expected_value']}/hr | {candidate['repo']}#{candidate['issue_number']}")
        print(f"   {candidate['title'][:96]}")
        print(f"   bounty=${candidate['bounty']} payment={candidate['payment_type']} flags={flags_text}")
    print("=" * 72)

    for index, candidate in enumerate(money_candidates, 1):
        flags = candidate.get("preflight_flags", [])
        print(f"\n[{index}/{len(money_candidates)}] {candidate['repo']}#{candidate['issue_number']}")
        decision = input("  决策 [y/n/s=暂存/q=退出]: ").strip().lower()
        if decision == "q":
            break
        if decision in ("y", "yes"):
            if candidate["is_security"] or any(flag in flags for flag in MANUAL_APPROVAL_FLAGS):
                confirm = input("  继续批准? [y/N]: ").strip().lower()
                if confirm not in ("y", "yes"):
                    tracker.update_status(candidate["task_id"], "pending_review", blocked_reason="人工确认后暂存")
                    print("  ⏸️ 已暂存")
                    continue

            tracker.upsert(
                TaskRecord(
                    task_id=candidate["task_id"],
                    source=candidate["source"],
                    repo=candidate["repo"],
                    issue_number=candidate["issue_number"],
                    title=candidate["title"],
                    url=candidate["url"],
                    score=candidate["score"],
                    expected_value=candidate["expected_value"],
                    is_security=candidate["is_security"],
                    human_approved=True,
                    lane=candidate["lane"],
                    payment_type=candidate["payment_type"],
                    selection_reason=candidate.get("selection_reason", ""),
                    blocked_reason="",
                    preflight_command_hint=candidate.get("preflight_command_hint", ""),
                    status="approved",
                    estimated_hours=2.0,
                    bounty_amount=candidate["bounty"],
                )
            )
            print("  ✅ 已批准")
        elif decision == "s":
            tracker.update_status(candidate["task_id"], "pending_review", blocked_reason="人工暂存")
            print("  ⏸️ 已暂存")
        else:
            tracker.update_status(candidate["task_id"], "pending_review", blocked_reason="人工拒绝")
            print("  ❌ 已跳过")


def _append_note(record: TaskRecord, note: str) -> str:
    return f"{record.notes}\n{note}".strip() if record.notes else note


def _clone_target_path(workspace_root: Path, record: TaskRecord) -> Path:
    owner, repo = record.repo.split("/", 1)
    return workspace_root / f"{owner}__{repo}__{record.issue_number}"


def _run_command(cmd: str, cwd: Path, timeout_seconds: int) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, shell=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else (exc.stdout.decode(errors="ignore") if exc.stdout else "")
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else (exc.stderr.decode(errors="ignore") if exc.stderr else "")
        combined = "\n".join(part for part in [stdout.strip(), stderr.strip(), f"timeout after {timeout_seconds}s"] if part).strip()
        return False, combined[:2000]
    combined = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part).strip()
    return result.returncode == 0, combined[:2000]


def _current_python_cmd() -> str:
    return shlex.quote(sys.executable)


def _is_partial_clone(repo_path: Path) -> bool:
    if not repo_path.exists():
        return False
    entries = [entry.name for entry in repo_path.iterdir()]
    return entries == [".git"] or entries == []


def _clone_repo(record: TaskRecord, workspace_root: Path, target_name: str, timeout_seconds: int) -> tuple[bool, str]:
    clone_attempts = [
        f"git clone --depth=1 --filter=blob:none https://github.com/{record.repo}.git {target_name}",
        f"gh repo clone {record.repo} {target_name} -- --depth=1",
    ]
    outputs: list[str] = []
    for cmd in clone_attempts:
        success, output = _run_command(cmd, workspace_root, timeout_seconds)
        outputs.append(f"$ {cmd}\n{output}".strip())
        if success:
            return True, "\n".join(outputs).strip()
    return False, "\n".join(outputs).strip()


def _looks_like_missing_tests(output: str) -> bool:
    lowered = output.lower()
    return "ran 0 tests" in lowered or "no tests ran" in lowered or "collected 0 items" in lowered


def _detect_commands(repo_path: Path, whitelist_data: dict, record: TaskRecord) -> tuple[str, str]:
    repo_info = whitelist_data.get(record.repo, {})
    install_cmd = repo_info.get("install_cmd", "")
    test_cmd = repo_info.get("test_cmd", "")
    python_cmd = _current_python_cmd()

    if not install_cmd:
        if (repo_path / "bun.lock").exists() or (repo_path / "bun.lockb").exists() or (repo_path / "bunfig.toml").exists():
            install_cmd = "bun install"
        elif (repo_path / "pnpm-lock.yaml").exists():
            install_cmd = "pnpm install"
        elif (repo_path / "package-lock.json").exists():
            install_cmd = "npm install"
        elif (repo_path / "yarn.lock").exists():
            install_cmd = "yarn install"
        elif (repo_path / "pyproject.toml").exists():
            install_cmd = f"{python_cmd} -m pip install -e ."
        elif (repo_path / "requirements.txt").exists():
            install_cmd = f"{python_cmd} -m pip install -r requirements.txt"

    if not test_cmd:
        if (repo_path / "bun.lock").exists() or (repo_path / "bun.lockb").exists() or (repo_path / "bunfig.toml").exists():
            test_cmd = "bun test"
        elif (repo_path / "pnpm-lock.yaml").exists():
            test_cmd = "pnpm test -- --help"
        elif (repo_path / "yarn.lock").exists():
            test_cmd = "yarn test --help"
        elif (repo_path / "package.json").exists():
            test_cmd = "npm test -- --help"
        elif (repo_path / "UNITTESTS").exists():
            test_cmd = f"{python_cmd} -m unittest discover UNITTESTS"
        elif (repo_path / "pyproject.toml").exists() or (repo_path / "requirements.txt").exists():
            test_cmd = f"{python_cmd} -m unittest discover"

    return install_cmd, test_cmd


def _preflight_record(record: TaskRecord, config: dict, whitelist_data: dict) -> tuple[str, str, str, str, str]:
    execution_cfg = config.get("execution", {})
    workspace_root = PROJECT_ROOT / execution_cfg.get("workspace_dir", "workspaces")
    workspace_root.mkdir(parents=True, exist_ok=True)
    clone_timeout = int(execution_cfg.get("clone_timeout_seconds", 120))
    install_timeout = int(execution_cfg.get("install_timeout_seconds", 300))
    test_timeout = int(execution_cfg.get("test_timeout_seconds", 300))

    target_path = _clone_target_path(workspace_root, record)
    clone_note = ""
    if _is_partial_clone(target_path):
        shutil.rmtree(target_path)
        clone_note = f"detected partial clone, removed: {target_path}"
    if not target_path.exists():
        success, output = _clone_repo(record, workspace_root, target_path.name, clone_timeout)
        clone_note = f"{clone_note}\n{output}".strip()
        if not success:
            return "needs_manual_triage", str(target_path), "", "", clone_note
    else:
        clone_note = f"workspace exists: {target_path}"

    install_cmd, test_cmd = _detect_commands(target_path, whitelist_data, record)
    if not install_cmd or not test_cmd:
        note = f"{clone_note}\n命令探测不足: install='{install_cmd}' test='{test_cmd}'".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note

    if install_cmd.startswith("pnpm ") and not shutil.which("pnpm"):
        note = f"{clone_note}\n缺少本地工具: pnpm".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note
    if install_cmd.startswith("yarn ") and not shutil.which("yarn"):
        note = f"{clone_note}\n缺少本地工具: yarn".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note
    if install_cmd.startswith("bun ") and not shutil.which("bun"):
        note = f"{clone_note}\n缺少本地工具: bun".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note
    if test_cmd.startswith("pnpm ") and not shutil.which("pnpm"):
        note = f"{clone_note}\n缺少本地工具: pnpm".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note
    if test_cmd.startswith("yarn ") and not shutil.which("yarn"):
        note = f"{clone_note}\n缺少本地工具: yarn".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note
    if test_cmd.startswith("bun ") and not shutil.which("bun"):
        note = f"{clone_note}\n缺少本地工具: bun".strip()
        return "needs_manual_triage", str(target_path), install_cmd, test_cmd, note

    install_ok, install_output = _run_command(install_cmd, target_path, install_timeout)
    if not install_ok:
        note = f"{clone_note}\n$ {install_cmd}\n{install_output}".strip()
        return "preflight_failed", str(target_path), install_cmd, test_cmd, note

    test_ok, test_output = _run_command(test_cmd, target_path, test_timeout)
    note = f"{clone_note}\n$ {install_cmd}\n{install_output}\n$ {test_cmd}\n{test_output}".strip()
    if test_ok:
        status = "preflight_passed"
    elif _looks_like_missing_tests(test_output):
        status = "needs_manual_triage"
    else:
        status = "preflight_failed"
    return status, str(target_path), install_cmd, test_cmd, note


def cmd_execute(config: dict):
    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))
    approved = [record for record in tracker.records if record.status == "approved"]

    if not approved:
        print("没有已批准任务，先运行 review 批准候选。")
        return

    _, _, whitelist_data = _build_whitelist_data()
    print(f"\n🚀 本地预检队列 (共 {len(approved)} 个 approved 任务)")
    print("-" * 60)

    for record in approved:
        tracker.update_status(record.task_id, "preflight_running", preflight_ran_at=datetime.now(timezone.utc).isoformat())
        status, workspace_path, install_cmd, test_cmd, note = _preflight_record(record, config, whitelist_data)
        tracker.update_status(
            record.task_id,
            status,
            workspace_path=workspace_path,
            install_cmd=install_cmd,
            test_cmd=test_cmd,
            preflight_command_hint=" && ".join(part for part in [install_cmd, test_cmd] if part),
            notes=_append_note(record, note),
        )
        print(f"{record.repo}#{record.issue_number} -> {status}")


def cmd_report(config: dict):
    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))
    print(tracker.generate_daily_report())


def cmd_metrics(config: dict):
    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))
    print(json.dumps(tracker.compute_metrics(30), indent=2, ensure_ascii=False, default=str))


def _build_pr_template(record: TaskRecord) -> str:
    return f"""## Summary
- Fix {record.repo}#{record.issue_number}

## Repro
- {record.title}

## Verification
- [ ] test command passes
- [ ] regression test added
- [ ] issue linked

## Notes
- bounty: ${record.bounty_amount}
- expected_value: ${record.expected_value}/hr
"""


def _build_no_kyc_claim_template(record: TaskRecord) -> str:
    pr_ref = record.pr_url or (f"PR #{record.pr_number}" if record.pr_number else "the merged PR")
    return f"""Hi, thanks for merging {pr_ref} for {record.repo}#{record.issue_number}.

Could you confirm whether this bounty can be paid through a no-KYC / no-tax-form method such as GitHub Sponsors, PayPal, Wise, or a direct tip?

I cannot provide KYC or tax paperwork. If that is required for this bounty, please let me know before I submit any payout claim.

Thanks!
"""


def cmd_claim(config: dict):
    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))
    claimable = [
        record
        for record in tracker.records
        if record.status == "merged" and record.bounty_amount > 0 and not record.bounty_claimed and not record.bounty_paid
    ]

    if not claimable:
        print("没有待 claim 的已合并 bounty。")
        return

    print(f"\n💰 待收款任务 (共 {len(claimable)} 个)")
    print("-" * 72)
    for record in claimable:
        print(f"\n{record.repo}#{record.issue_number} | bounty=${record.bounty_amount}")
        print(f"  {record.title[:100]}")
        if record.pr_url:
            print(f"  PR: {record.pr_url}")
        print("  收款模板:")
        print(_build_no_kyc_claim_template(record))
        tracker.update_record(
            record.task_id,
            bounty_claimed=True,
            payment_method="no-kyc-requested",
            notes=_append_note(record, "claim template generated"),
        )
        print("  → 已标记 bounty_claimed=True, payment_method=no-kyc-requested")


def cmd_watch(config: dict):
    tracker = DeliveryTracker(str(PROJECT_ROOT / "reports"))
    watching = [record for record in tracker.records if record.status in ("pr_opened", "ci_pass", "reviewing") and record.pr_url]
    if not watching:
        print("没有需要 watch 的 PR。")
        return

    print(f"\n👀 PR Watch (共 {len(watching)} 个)")
    print("-" * 72)
    for record in watching:
        print(f"\n{record.repo}#{record.issue_number}")
        print(f"  PR: {record.pr_url}")
        result = subprocess.run(
            ["gh", "pr", "view", record.pr_url, "--json", "state,mergeStateStatus,reviewDecision,statusCheckRollup,url"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"  watch failed: {result.stderr[:160]}")
            continue

        data = json.loads(result.stdout)
        state = data.get("state")
        checks = data.get("statusCheckRollup") or []
        failing = [check for check in checks if check.get("conclusion") not in (None, "SUCCESS")]
        pending = [check for check in checks if check.get("status") not in (None, "COMPLETED")]
        print(f"  state={state} review={data.get('reviewDecision')} checks={len(checks)}")

        if state == "MERGED":
            tracker.update_status(record.task_id, "merged", pr_merged_at=datetime.now(timezone.utc).isoformat())
            print("  → 状态推进: merged")
        elif failing:
            tracker.update_status(record.task_id, "reviewing", maintainer_comment="CI failing")
            print("  → 需要处理 CI failure")
        elif not pending and checks:
            tracker.update_status(record.task_id, "ci_pass")
            print("  → 状态推进: ci_pass")
        else:
            tracker.update_status(record.task_id, "reviewing")
            print("  → 状态推进: reviewing")


def cmd_team(config: dict):
    print("Opportunity Radar AI Team")
    print("=" * 72)
    print("1) Scanner Agent: 扫描候选并生成 money/practice JSON")
    cmd_scan(config)
    print("\n2) Watcher Agent: 检查已开 PR 状态")
    cmd_watch(config)
    print("\n3) Claim Agent: 检查可 claim 的 merged 任务")
    cmd_claim(config)
    print("\n人工闸门仍然保留：review 批准、patch、push/PR、对外评论、claim 收款。")


def main():
    config = load_config()
    if len(sys.argv) < 2:
        print("Usage: python radar.py [team|scan|review|execute|watch|claim|report|metrics]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "team":
        cmd_team(config)
    elif cmd == "scan":
        cmd_scan(config)
    elif cmd == "review":
        cmd_review(config)
    elif cmd == "execute":
        cmd_execute(config)
    elif cmd == "watch":
        cmd_watch(config)
    elif cmd == "claim":
        cmd_claim(config)
    elif cmd == "report":
        cmd_report(config)
    elif cmd == "metrics":
        cmd_metrics(config)
    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
