"""Opportunity Radar - GitHub Issue 扫描器

通过 gh CLI 和 GitHub API 搜索符合条件的 issue 和 repo。
gh search issues 使用 flag 语法：--label, --language, --sort, --order 等。
关键词放在 -- 之后的位置。
"""

from __future__ import annotations
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional

# Rate limit 保护
_request_count = 0
MAX_REQUESTS_PER_HOUR = 180
MIN_INTERVAL = 1.0


@dataclass
class RawIssue:
    repo: str
    issue_number: int
    title: str
    url: str
    labels: list[str] = field(default_factory=list)
    body: str = ""
    created_at: str = ""
    updated_at: str = ""
    state: str = "open"
    comments_count: int = 0


@dataclass
class RawRepo:
    full_name: str
    stars: int
    language: str = ""
    description: str = ""
    updated_at: str = ""
    license: str = ""
    fork: bool = False
    archived: bool = False


def run_gh(args: list[str], timeout: int = 30) -> dict | list | None:
    """执行 gh 命令并返回 JSON 结果，带 rate limit 保护"""
    global _request_count
    _request_count += 1

    if _request_count > MAX_REQUESTS_PER_HOUR:
        print(f"  ⚠️ 达到每小时请求上限 ({MAX_REQUESTS_PER_HOUR})，停止扫描", file=sys.stderr)
        return None

    # 最小间隔
    time.sleep(MIN_INTERVAL)

    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            err = result.stderr[:200]
            if "rate limit" in err.lower():
                print(f"  ⚠️ GitHub API rate limit，等待 60s...", file=sys.stderr)
                time.sleep(60)
                return None
            print(f"  gh error: {err}", file=sys.stderr)
            return None
        if "--json" in args:
            return json.loads(result.stdout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  gh timeout: {' '.join(args)[:100]}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        return None


def search_issues(
    query: str = "",
    labels: list[str] | None = None,
    languages: list[str] | None = None,
    sort: str = "updated",
    order: str = "desc",
    limit: int = 30,
    assignee: str | None = None,  # "none" for unassigned
) -> list[RawIssue]:
    """搜索 GitHub issues

    gh search issues [keywords] --label X --language Y --sort Z --limit N
    """
    args = ["search", "issues", "--limit", str(limit)]

    # JSON 字段 — 使用 gh search issues 支持的字段名
    args += ["--json", "number,title,url,labels,body,createdAt,updatedAt,repository,commentsCount"]
    args += ["--sort", sort, "--order", order]

    if labels:
        for label in labels:
            args += ["--label", label]
    if languages:
        for lang in languages:
            args += ["--language", lang]
    if assignee:
        args += ["--assignee", assignee]

    # 关键词放最后
    if query:
        args += ["--", query]

    results = run_gh(args)
    if not results:
        return []

    issues = []
    for item in results:
        repo_name = ""
        repo = item.get("repository")
        if isinstance(repo, dict):
            repo_name = repo.get("nameWithOwner", "")
        if not repo_name:
            url = item.get("url", "")
            parts = url.split("/issues/")[0].replace("https://github.com/", "")
            repo_name = parts

        label_list = []
        raw_labels = item.get("labels", [])
        if isinstance(raw_labels, list):
            label_list = [l.get("name", "") if isinstance(l, dict) else str(l) for l in raw_labels]

        issues.append(RawIssue(
            repo=repo_name,
            issue_number=item.get("number", 0),
            title=item.get("title", ""),
            url=item.get("url", ""),
            labels=label_list,
            body=(item.get("body") or "")[:2000],
            created_at=item.get("createdAt", ""),
            updated_at=item.get("updatedAt", ""),
            state="open",
            comments_count=item.get("commentsCount", 0),
        ))
    return issues


def search_repos(
    query: str,
    stars: str | None = None,
    languages: list[str] | None = None,
    sort: str = "stars",
    limit: int = 30,
) -> list[RawRepo]:
    """搜索 GitHub repos

    gh search repos [query] --stars X --language Y --sort Z
    """
    args = ["search", "repos", "--limit", str(limit)]
    args += ["--json", "fullName,stargazersCount,description,updatedAt,language,isArchived,isFork"]
    args += ["--sort", sort]

    if stars:
        args += ["--stars", stars]
    if languages:
        for lang in languages:
            args += ["--language", lang]

    args += ["--", query]

    results = run_gh(args)
    if not results:
        return []

    repos = []
    for item in results:
        repos.append(RawRepo(
            full_name=item.get("fullName", ""),
            stars=item.get("stargazersCount", 0),
            language=item.get("language", ""),
            description=item.get("description", ""),
            updated_at=item.get("updatedAt", ""),
            archived=item.get("isArchived", False),
            fork=item.get("isFork", False),
        ))
    return repos


def get_repo_stats(owner_repo: str) -> Optional[dict]:
    """获取 repo 详细统计：外部PR合并率、响应速度等"""
    since_30d = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    since_90d = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    result = {
        "merged_ext_pr_30d": 0,
        "merged_ext_pr_90d": 0,
        "avg_response_days": 14.0,
    }

    prs = run_gh([
        "search", "issues",
        "--limit", "50",
        "--json", "number,author,mergedAt",
        "--", f"repo:{owner_repo} is:pr is:merged merged:>={since_90d}"
    ])
    if prs:
        owner = owner_repo.split("/")[0] if "/" in owner_repo else ""
        ext_count = 0
        for pr in prs:
            author = pr.get("author", {})
            login = author.get("login", "") if isinstance(author, dict) else str(author)
            if login and login != owner and not login.endswith("[bot]"):
                ext_count += 1
                merged_at = pr.get("mergedAt", "")
                if merged_at >= since_30d:
                    result["merged_ext_pr_30d"] += 1
        result["merged_ext_pr_90d"] = ext_count

    return result


# 预定义搜索策略
SEARCH_STRATEGIES = [
    # 显性赏金
    {
        "name": "bounty-typescript",
        "query": "bounty",
        "languages": ["typescript"],
        "labels": None,
        "sort": "updated",
    },
    {
        "name": "bounty-python",
        "query": "bounty",
        "languages": ["python"],
        "labels": None,
        "sort": "updated",
    },
    {
        "name": "reward-typescript",
        "query": "reward",
        "languages": ["typescript"],
        "labels": None,
        "sort": "updated",
    },
    {
        "name": "reward-python",
        "query": "reward",
        "languages": ["python"],
        "labels": None,
        "sort": "updated",
    },
    # 显性标签
    {
        "name": "good-first-issue-ts",
        "query": "",
        "languages": ["typescript"],
        "labels": ["good first issue"],
        "sort": "updated",
    },
    {
        "name": "good-first-issue-py",
        "query": "",
        "languages": ["python"],
        "labels": ["good first issue"],
        "sort": "updated",
    },
    {
        "name": "help-wanted-ts",
        "query": "",
        "languages": ["typescript"],
        "labels": ["help wanted"],
        "sort": "updated",
    },
    {
        "name": "help-wanted-py",
        "query": "",
        "languages": ["python"],
        "labels": ["help wanted"],
        "sort": "updated",
    },
    # 文档和测试
    {
        "name": "documentation-ts",
        "query": "",
        "languages": ["typescript"],
        "labels": ["documentation"],
        "sort": "updated",
    },
    {
        "name": "documentation-py",
        "query": "",
        "languages": ["python"],
        "labels": ["documentation"],
        "sort": "updated",
    },
    # bug
    {
        "name": "bug-ts",
        "query": "",
        "languages": ["typescript"],
        "labels": ["bug", "good first issue"],
        "sort": "updated",
    },
    {
        "name": "bug-py",
        "query": "",
        "languages": ["python"],
        "labels": ["bug", "good first issue"],
        "sort": "updated",
    },
]

REPO_SEARCH_STRATEGIES = [
    {
        "name": "good-first-issues-ts",
        "query": "good-first-issues:>5",
        "languages": ["typescript"],
        "stars": "10..50000",
    },
    {
        "name": "good-first-issues-py",
        "query": "good-first-issues:>5",
        "languages": ["python"],
        "stars": "10..50000",
    },
]


def _day_rotation(items: list, count: int) -> list:
    """按日期轮换选取子集，保证每天扫不同的一部分。"""
    if not items or count <= 0:
        return []
    offset = date.today().toordinal() % len(items)
    rotated = items[offset:] + items[:offset]
    return rotated[:count]


def run_daily_github_scan(config: dict) -> list[RawIssue]:
    """执行每日 GitHub issue 扫描"""
    all_issues: list[RawIssue] = []
    seen_urls: set[str] = set()
    stacks = config.get("stacks", ["typescript", "python"])
    stack_langs = [s.capitalize() if s == "python" else "TypeScript" for s in stacks]

    # 筛选适合当前技术栈的策略
    active_strategies = []
    for s in SEARCH_STRATEGIES:
        s_langs = s.get("languages") or []
        if not s_langs or any(l.lower() in [sl.lower() for sl in stack_langs] for l in s_langs):
            active_strategies.append(s)

    # 每天只跑一部分策略，减少请求量
    daily_strategies = _day_rotation(active_strategies, 6)

    print("=== GitHub Issue 搜索 ===")
    for strategy in daily_strategies:
        name = strategy["name"]
        query = strategy.get("query", "")
        labels = strategy.get("labels")
        langs = strategy.get("languages")
        sort = strategy.get("sort", "updated")

        # 只搜索当前技术栈
        filtered_langs = [l for l in (langs or []) if l.lower() in [s.lower() for s in stacks]]

        print(f"  [{name}] 查询: query='{query}' labels={labels} langs={filtered_langs}")
        issues = search_issues(
            query=query,
            labels=labels,
            languages=filtered_langs if filtered_langs else None,
            sort=sort,
            limit=10,
        )
        new = [i for i in issues if i.url not in seen_urls]
        seen_urls.update(i.url for i in new)
        all_issues.extend(new)
        print(f"    找到 {len(new)} 个新 issue (总: {len(all_issues)})")

    # Repo 搜索 → 再抓 issue
    print(f"\n=== GitHub Repo 搜索 ===")
    for strategy in REPO_SEARCH_STRATEGIES:
        name = strategy["name"]
        print(f"  [{name}]...")
        repos = search_repos(
            query=strategy["query"],
            stars=strategy.get("stars"),
            languages=strategy.get("languages"),
            limit=6,
        )
        # 每天只扫 3 个 repo，每个 repo 只抓一个标签
        for repo in _day_rotation([r for r in repos if not r.archived and not r.fork], 3):
            issues = search_issues(
                query=f"repo:{repo.full_name}",
                labels=["help wanted"],
                limit=5,
                sort="updated",
            )
            new = [i for i in issues if i.url not in seen_urls]
            seen_urls.update(i.url for i in new)
            all_issues.extend(new)
        print(f"    扫描了 {min(3, len(repos))} 个 repo")

    print(f"\n总计: {len(all_issues)} 个候选 issue")
    return all_issues


if __name__ == "__main__":
    issues = search_issues(
        query="bounty",
        languages=["typescript"],
        sort="updated",
        limit=5,
    )
    for i in issues:
        print(f"  [{i.repo}#{i.issue_number}] {i.title[:60]}")
