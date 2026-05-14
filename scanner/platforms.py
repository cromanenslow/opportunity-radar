"""Opportunity Radar - 赏金平台扫描器

从 Algora、IssueHunt 等平台抓取公开赏金。
优先使用 gh api 或 curl，失败时记录错误继续。
支持降级策略：当平台 API 不可用时，通过 GitHub 搜索已知赏金仓库的 issue。
"""

from __future__ import annotations
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
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


# ---------------------------------------------------------------------------
# 日志辅助
# ---------------------------------------------------------------------------
_api_status: dict[str, str] = {}  # platform -> "ok" | "unavailable" | "degraded"


def _log_api_status(platform: str, status: str, reason: str = "") -> None:
    _api_status[platform] = status
    if status == "unavailable":
        print(f"  ⚠ {platform}: API 不可用 — {reason}")
    elif status == "degraded":
        print(f"  ⚡ {platform}: API 降级 — {reason}")
    else:
        print(f"  ✓ {platform}: OK")


def get_api_status() -> dict[str, str]:
    return dict(_api_status)


# ---------------------------------------------------------------------------
# HTTP / API 辅助
# ---------------------------------------------------------------------------
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


def _curl_json_with_headers(url: str, headers: list[str] | None = None,
                            timeout: int = 15) -> list | dict | None:
    """curl 抓取 JSON，支持自定义 headers"""
    cmd = ["curl", "-sL"]
    if headers:
        for h in headers:
            cmd.extend(["-H", h])
    cmd.append(url)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass
    return None


def _curl_text(url: str, timeout: int = 15) -> str | None:
    """curl 获取文本内容（不限 JSON），失败返回 None"""
    try:
        result = subprocess.run(
            ["curl", "-sL", url],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except subprocess.TimeoutExpired:
        pass
    return None


def _gh_api(endpoint: str, method: str = "GET", body: str | None = None,
            timeout: int = 15) -> list | dict | None:
    """通过 gh api 调用 GitHub API"""
    try:
        cmd = ["gh", "api", "--method", method, endpoint]
        if body:
            cmd.extend(["--input", "-"])
            result = subprocess.run(
                cmd, input=body, capture_output=True, text=True, timeout=timeout
            )
        else:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass
    return None


def _gh_graphql(query: str, timeout: int = 30) -> dict | None:
    """通过 gh api graphql 执行 GraphQL 查询"""
    try:
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass
    return None


# ---------------------------------------------------------------------------
# Algora
# ---------------------------------------------------------------------------
def _check_algora_api() -> tuple[bool, str]:
    """
    检查 Algora API 可用性。
    返回 (available, reason)
    """
    # 尝试 1: 标准 REST API
    for url in [
        "https://algora.io/api/bounties?status=open",
        "https://algora.io/api/v1/bounties",
    ]:
        resp = _curl_text(url)
        if resp:
            # 检查返回的是 JSON 还是 HTML
            content_type = ""
            try:
                json.loads(resp)
                return True, "REST API 响应 JSON"
            except (json.JSONDecodeError, ValueError):
                if "phx-" in resp or "<!DOCTYPE html>" in resp:
                    continue  # LiveView HTML, 不是 JSON API
    return False, (
        "Algora 已迁移到 Phoenix LiveView 架构，不再提供公开 REST API。"
        "平台数据通过 WebSocket 实时加载，无法通过 HTTP API 抓取。"
        "降级策略：通过 GitHub 搜索已知赏金仓库的 issue。"
    )


def fetch_algora_bounties() -> list[PlatformBounty]:
    """抓取 Algora 公开赏金 — 通过 GitHub 搜索作为降级"""
    bounties = []
    available, reason = _check_algora_api()
    if not available:
        _log_api_status("algora", "unavailable", reason)
        # 降级：通过 GitHub 搜索已知使用 Algora 的仓库
        print("  ↳ 降级: 搜索 GitHub 上已知 Algora 管理仓库的 Bounty issue")
        return _fetch_algora_fallback()
    _log_api_status("algora", "ok")

    data = _curl_json("https://algora.io/api/bounties?status=open")
    if not data:
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


def _fetch_algora_fallback() -> list[PlatformBounty]:
    """降级策略：通过 GitHub GraphQL 搜索已知使用 Algora 的仓库的 Bounty issue"""
    bounties = []
    # 已知在 Algora 上发布赏金的仓库
    algora_known_repos = [
        "tscircuit/schematic-trace-solver",
        "tscircuit/tscircuit-autorouter",
        "calcom/cal.com",
        "keephq/keep",
    ]
    query_template = """
    {{
      search(query: "repo:{repo} label:bounty is:issue is:open", type: ISSUE, first: 20) {{
        nodes {{
          ... on Issue {{
            number
            title
            url
            state
            body
            labels(first: 10) {{
              nodes {{ name }}
            }}
            repository {{ nameWithOwner }}
          }}
        }}
      }}
    }}
    """
    for repo in algora_known_repos:
        query = query_template.format(repo=repo)
        result = _gh_graphql(query)
        if result and "data" in result:
            nodes = result["data"].get("search", {}).get("nodes", [])
            for item in nodes:
                if not item:
                    continue
                try:
                    labels = [l["name"] for l in item.get("labels", {}).get("nodes", []) if l]
                    # 从标题/body 提取金额
                    amount = _extract_amount(item.get("title", "") + " " + str(item.get("body", "")))
                    bounties.append(PlatformBounty(
                        platform="algora-fallback",
                        repo=item.get("repository", {}).get("nameWithOwner", repo),
                        issue_number=item.get("number", 0),
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        amount=amount,
                        labels=labels,
                        description=str(item.get("body", ""))[:500],
                        payment_type="escrow",
                    ))
                except (ValueError, TypeError):
                    continue
    print(f"    ↳ 降级搜索找到 {len(bounties)} 个赏金 issue")
    return bounties


def _extract_amount(text: str) -> float:
    """从文本中提取美元金额"""
    import re
    # 匹配 $100, $1,000, $50-$100, $50+
    patterns = [
        r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)',
    ]
    amounts = []
    for pat in patterns:
        for match in re.finditer(pat, text):
            try:
                amounts.append(float(match.group(1).replace(",", "")))
            except ValueError:
                continue
    if amounts:
        return max(amounts)
    return 0.0


# ---------------------------------------------------------------------------
# IssueHunt
# ---------------------------------------------------------------------------
def _check_issuehunt_api() -> tuple[bool, str]:
    """
    检查 IssueHunt API 可用性。
    IssueHunt 使用 SPA (React) 架构，后端 API 需要认证。
    """
    # 尝试主 API 端点
    for url in [
        "https://issuehunt.io/api/issues?status=open",
        "https://api.issuehunt.io/api/programs",
    ]:
        resp = _curl_text(url)
        if resp:
            if "Something went wrong" in resp:
                continue
            try:
                json.loads(resp)
                return True, "API 可用"
            except json.JSONDecodeError:
                continue
    return False, (
        "IssueHunt 使用 React SPA 架构，其 API (api.issuehunt.io) 需要身份认证令牌。"
        "公共 API 端点已不再可用。降级策略：通过 GitHub 搜索赏金 issue。"
    )


def fetch_issuehunt_bounties() -> list[PlatformBounty]:
    """抓取 IssueHunt 公开赏金 — 通过 GitHub 搜索作为降级"""
    bounties = []
    available, reason = _check_issuehunt_api()
    if not available:
        _log_api_status("issuehunt", "unavailable", reason)
        print("  ↳ 降级: 搜索 GitHub 上已知 IssueHunt 相关仓库")
        return _fetch_issuehunt_fallback()
    _log_api_status("issuehunt", "ok")

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


def _fetch_issuehunt_fallback() -> list[PlatformBounty]:
    """IssueHunt 降级：搜索日本公司的 bug bounty 标签"""
    bounties = []
    query = """
    {
      search(query: "label:bounty is:issue is:open stars:>500 sort:updated-desc", type: ISSUE, first: 20) {
        nodes {
          ... on Issue {
            number
            title
            url
            state
            body
            labels(first: 10) { nodes { name } }
            repository { nameWithOwner }
          }
        }
      }
    }
    """
    result = _gh_graphql(query)
    if result and "data" in result:
        nodes = result["data"].get("search", {}).get("nodes", [])
        for item in nodes:
            if not item:
                continue
            try:
                labels = [l["name"] for l in item.get("labels", {}).get("nodes", []) if l]
                amount = _extract_amount(item.get("title", "") + " " + str(item.get("body", "")))
                bounties.append(PlatformBounty(
                    platform="issuehunt-fallback",
                    repo=item.get("repository", {}).get("nameWithOwner", ""),
                    issue_number=item.get("number", 0),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    amount=amount,
                    labels=labels,
                    description=str(item.get("body", ""))[:500],
                    payment_type="unknown",
                ))
            except (ValueError, TypeError):
                continue
    print(f"    ↳ 降级搜索找到 {len(bounties)} 个赏金 issue")
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


# ---------------------------------------------------------------------------
# BountyHub
# ---------------------------------------------------------------------------
def fetch_bountyhub_bounties() -> list[PlatformBounty]:
    """抓取 BountyHub 公开赏金"""
    bounties = []
    data = _curl_json("https://bountyhub.io/api/bounties?status=open")
    if not data:
        print("  ⚠ bountyhub: API 无响应或返回非 JSON 数据")
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


# ---------------------------------------------------------------------------
# OnlyDust
# ---------------------------------------------------------------------------
def fetch_onlydust_bounties() -> list[PlatformBounty]:
    """抓取 OnlyDust 公开任务"""
    bounties = []
    data = _curl_json("https://www.onlydust.xyz/api/projects?status=active")
    if not data:
        print("  ⚠ onlydust: API 无响应或返回非 JSON 数据")
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


# ---------------------------------------------------------------------------
# huntr.dev
# ---------------------------------------------------------------------------
def fetch_huntr_bounties() -> list[PlatformBounty]:
    """抓取 huntr.dev 安全赏金"""
    bounties = []
    data = _curl_json("https://huntr.dev/api/bounties?status=open&limit=30")
    if not data:
        print("  ⚠ huntr: API 无响应或返回非 JSON 数据")
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


# ---------------------------------------------------------------------------
# GitHub bounty issue 搜索（通用）
# ---------------------------------------------------------------------------
def fetch_algora_github_bounties() -> list[PlatformBounty]:
    """通过 GitHub 搜索 Algora 托管的赏金 issue — 使用 GraphQL"""
    bounties = []
    query = """
    {
      search(query: "org:algora-io label:bounty is:issue", type: ISSUE, first: 30) {
        nodes {
          ... on Issue {
            number
            title
            url
            state
            body
            labels(first: 10) { nodes { name } }
            repository { nameWithOwner }
          }
        }
      }
    }
    """
    result = _gh_graphql(query)
    if result and "data" in result:
        nodes = result["data"].get("search", {}).get("nodes", [])
        for item in nodes:
            if not item:
                continue
            try:
                labels = [l["name"] for l in item.get("labels", {}).get("nodes", []) if l]
                amount = _extract_amount(item.get("title", "") + " " + str(item.get("body", "")))
                bounties.append(PlatformBounty(
                    platform="algora-github",
                    repo=item.get("repository", {}).get("nameWithOwner", ""),
                    issue_number=item.get("number", 0),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    amount=amount,
                    labels=labels,
                    description=str(item.get("body", ""))[:500],
                    payment_type="escrow",
                ))
            except (ValueError, TypeError):
                continue
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
            print(f"  → 找到 {len(new)} 个赏金")
        except Exception as e:
            print(f"  → 错误: {e}")

    print(f"\n总计: {len(all_bounties)} 个平台赏金")
    return all_bounties


def run_daily_platform_scan_detailed(platforms: list[str] | None = None) -> dict:
    """
    执行每日平台赏金扫描，返回包含详细状态信息的字典。
    用于报告和监控。
    """
    bounties = run_daily_platform_scan(platforms)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_bounties": len(bounties),
        "bounties": [
            {
                "platform": b.platform,
                "repo": b.repo,
                "issue_number": b.issue_number,
                "title": b.title[:80],
                "url": b.url,
                "amount": b.amount,
                "status": b.status,
            }
            for b in bounties
        ],
        "api_status": get_api_status(),
    }


if __name__ == "__main__":
    bounties = run_daily_platform_scan(["algora", "algora-github", "issuehunt"])
    for b in bounties[:10]:
        print(f"  [{b.platform}] ${b.amount:.0f} - {b.title[:60]} ({b.repo})")
