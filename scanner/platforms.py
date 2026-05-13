"""Opportunity Radar - 赏金平台扫描器

从 Algora、IssueHunt 等平台抓取公开赏金。
优先使用 gh api 或 curl，失败时记录错误继续。
"""

from __future__ import annotations
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from pathlib import Path


@dataclass
class PlatformBounty:
    platform: str
    repo: str
    issue_number: int
    title: str
    url: str
    amount: float
    currency: str = "USD"
    deadline: str = ""
    status: str = "open"
    labels: list[str] = field(default_factory=list)
    description: str = ""
    payment_type: str = "platform"


def _curl_json(url: str, timeout: int = 15) -> list | dict | None:
    """curl 抓取 JSON，失败返回 None"""
    try:
        result = subprocess.run(
            ["curl", "-sL", "-H", "Accept: application/json", url],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        pass
    return None


def _gh_api(endpoint: str, timeout: int = 15) -> list | dict | None:
    """通过 gh api 调用 GitHub API"""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass
    return None


def fetch_algora_bounties() -> list[PlatformBounty]:
    """抓取 Algora 公开赏金"""
    bounties = []
    data = _curl_json("https://algora.io/api/bounties?status=open")
    if not data:
        # 尝试另一个端点
        data = _curl_json("https://algora.io/api/v1/bounties")
    if not data:
        return bounties

    items = data if isinstance(data, list) else data.get("bounties", data.get("data", []))
    for item in items:
        try:
            bounties.append(PlatformBounty(
                platform="algora",
                repo=item.get("repo", item.get("repository", "")),
                issue_number=item.get("issue_number", item.get("number", 0)),
                title=item.get("title", ""),
                url=item.get("url", item.get("html_url", "")),
                amount=float(item.get("amount", item.get("reward", 0))),
                currency=item.get("currency", "USD"),
                status=item.get("status", "open"),
                labels=item.get("labels", []),
                description=str(item.get("description", item.get("body", "")))[:500],
                payment_type="escrow" if item.get("escrow") else "platform",
            ))
        except (ValueError, TypeError):
            continue
    return bounties


def fetch_issuehunt_bounties() -> list[PlatformBounty]:
    """抓取 IssueHunt 公开赏金"""
    bounties = []
    data = _curl_json("https://issuehunt.io/api/issues?status=open&limit=50")
    if not data:
        return bounties

    items = data if isinstance(data, list) else data.get("issues", data.get("data", []))
    for item in items:
        try:
            repo_data = item.get("repo", item.get("repository", {}))
            repo_name = repo_data.get("full_name", "") if isinstance(repo_data, dict) else ""
            bounties.append(PlatformBounty(
                platform="issuehunt",
                repo=repo_name,
                issue_number=item.get("number", 0),
                title=item.get("title", ""),
                url=item.get("url", item.get("html_url", "")),
                amount=float(item.get("bounty", item.get("funded_amount", item.get("reward", 0)))),
                currency="USD",
                status=item.get("status", "open"),
                description=str(item.get("body", item.get("description", "")))[:500],
                payment_type="platform",
            ))
        except (ValueError, TypeError):
            continue
    return bounties


def fetch_bountyhub_bounties() -> list[PlatformBounty]:
    """抓取 BountyHub 公开赏金"""
    bounties = []
    data = _curl_json("https://bountyhub.io/api/bounties?status=open")
    if not data:
        return bounties

    items = data if isinstance(data, list) else data.get("bounties", data.get("data", []))
    for item in items:
        try:
            bounties.append(PlatformBounty(
                platform="bountyhub",
                repo=item.get("repo", ""),
                issue_number=item.get("issue_number", 0),
                title=item.get("title", ""),
                url=item.get("url", ""),
                amount=float(item.get("amount", 0)),
                currency=item.get("currency", "USD"),
                status=item.get("status", "open"),
                description=str(item.get("description", ""))[:500],
                payment_type="platform",
            ))
        except (ValueError, TypeError):
            continue
    return bounties


def fetch_onlydust_bounties() -> list[PlatformBounty]:
    """抓取 OnlyDust 公开任务"""
    bounties = []
    data = _curl_json("https://www.onlydust.xyz/api/projects?status=active")
    if not data:
        return bounties

    items = data if isinstance(data, list) else data.get("projects", data.get("data", []))
    for item in items:
        try:
            bounties.append(PlatformBounty(
                platform="onlydust",
                repo=item.get("github_repo", ""),
                issue_number=0,
                title=item.get("name", ""),
                url=item.get("url", item.get("github_url", "")),
                amount=float(item.get("reward", 0)),
                currency=item.get("currency", "USD"),
                status=item.get("status", "open"),
                description=str(item.get("description", ""))[:500],
                payment_type="tipping",
            ))
        except (ValueError, TypeError):
            continue
    return bounties


def fetch_huntr_bounties() -> list[PlatformBounty]:
    """抓取 huntr.dev 安全赏金"""
    bounties = []
    data = _curl_json("https://huntr.dev/api/bounties?status=open&limit=30")
    if not data:
        return bounties

    items = data if isinstance(data, list) else data.get("bounties", data.get("data", []))
    for item in items:
        try:
            bounties.append(PlatformBounty(
                platform="huntr",
                repo=item.get("repo", ""),
                issue_number=item.get("issue_number", 0),
                title=item.get("title", ""),
                url=item.get("url", ""),
                amount=float(item.get("bounty", 0)),
                currency="USD",
                status=item.get("status", "open"),
                labels=["security"],
                description=str(item.get("description", ""))[:500],
                payment_type="platform",
            ))
        except (ValueError, TypeError):
            continue
    return bounties


# GitHub 本身也有赏金 issue — 用 gh search 在 algora 管理的 repo 中搜索
def fetch_algora_github_bounties() -> list[PlatformBounty]:
    """通过 GitHub 搜索 Algora 托管的赏金 issue"""
    bounties = []
    try:
        result = subprocess.run(
            ["gh", "search", "issues",
             "--limit", "30",
             "--json", "number,title,url,labels,body,repository",
             "--sort", "updated",
             "--label", "bounty",
             "--", "org:algora-io"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            items = json.loads(result.stdout)
            for item in items:
                repo = item.get("repository", {})
                repo_name = repo.get("nameWithOwner", "") if isinstance(repo, dict) else ""
                bounties.append(PlatformBounty(
                    platform="algora-github",
                    repo=repo_name,
                    issue_number=item.get("number", 0),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    amount=0,  # 需要解析 body 中的金额
                    labels=[l.get("name", "") if isinstance(l, dict) else str(l) for l in item.get("labels", [])],
                    description=str(item.get("body", ""))[:500],
                    payment_type="escrow",
                ))
    except Exception:
        pass
    return bounties


PLATFORM_FETCHERS = {
    "algora": fetch_algora_bounties,
    "issuehunt": fetch_issuehunt_bounties,
    "bountyhub": fetch_bountyhub_bounties,
    "onlydust": fetch_onlydust_bounties,
    "huntr": fetch_huntr_bounties,
    "algora-github": fetch_algora_github_bounties,
}


def run_daily_platform_scan(platforms: list[str] | None = None) -> list[PlatformBounty]:
    """执行每日平台赏金扫描"""
    if platforms is None:
        platforms = list(PLATFORM_FETCHERS.keys())

    all_bounties: list[PlatformBounty] = []
    seen_urls: set[str] = set()

    print("=== 平台赏金扫描 ===")
    for platform_name in platforms:
        fetcher = PLATFORM_FETCHERS.get(platform_name)
        if not fetcher:
            print(f"  {platform_name}: 无对应抓取器，跳过")
            continue

        print(f"  {platform_name}...", end=" ", flush=True)
        try:
            bounties = fetcher()
            new = [b for b in bounties if b.url not in seen_urls and b.url]
            seen_urls.update(b.url for b in new)
            all_bounties.extend(new)
            print(f"找到 {len(new)} 个赏金")
        except Exception as e:
            print(f"错误: {e}")

    print(f"\n总计: {len(all_bounties)} 个平台赏金")
    return all_bounties


if __name__ == "__main__":
    bounties = run_daily_platform_scan(["algora", "algora-github", "issuehunt"])
    for b in bounties[:10]:
        print(f"  [{b.platform}] ${b.amount} - {b.title[:50]} ({b.repo})")
