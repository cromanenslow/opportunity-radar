#!/usr/bin/env python3
"""
Expensify/App $250 External Bounty Issue Watcher
=================================================

Part of the 机会雷达 (Opportunity Radar) system.
Monitors GitHub for new, unassigned $250 External bounty issues
on the Expensify/App repository.

Strategy:
  Uses the GitHub Issues List API (not Search API) because the
  Search API has a known quirk where 'label:External no:assignee'
  returns 0 results even though unassigned issues exist in the repo.
  The Issues API does not have this limitation.

  We fetch issues labeled 'External' (sorted by newest first),
  filter client-side for [$250] title + no assignee, and track
  seen issues in a JSON state file.

Usage:
  python watch-expensify-issues.py            # Full run with state tracking
  python watch-expensify-issues.py --once     # Single run (cron-compatible)

Environment:
  GITHUB_TOKEN          GitHub Personal Access Token (strongly recommended)

Output:
  - New issues printed to stdout (simple report)
  - All discovered issues appended to issues.log
  - Tracked state saved to state.json (seen issue IDs, last-checked time)

Files (all relative to script directory):
  state.json            Persistent state (seen issue IDs, last_checked)
  issues.log            Append-only log of all discovered issues

Exit codes:
  0  — normal execution (new issues found or not)
  1  — error during execution
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse, urljoin

# ── Paths ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
STATE_FILE = SCRIPT_DIR / "state.json"
LOG_FILE = SCRIPT_DIR / "issues.log"

# ── GitHub API ─────────────────────────────────────────────────────────────

GITHUB_API = "https://api.github.com"
OWNER = "Expensify"
REPO = "App"
ISSUES_URL = f"{GITHUB_API}/repos/{OWNER}/{REPO}/issues"

USER_AGENT = "opportunity-radar-watcher/2.0"
PAGE_SIZE = 100  # max per_page for Issues API

# ── Logging ────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("expensify-watcher")


# ── Helpers ────────────────────────────────────────────────────────────────

def build_headers() -> dict:
    """Build request headers, optionally with GitHub token auth."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": USER_AGENT,
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        log.debug("Using GITHUB_TOKEN for authentication")
    return headers


def make_request(url: str, headers: dict, retries: int = 2) -> tuple[Optional[Union[list, dict]], dict]:
    """
    Make a GET request and return (parsed_json, response_headers).
    Returns (None, {}) on failure after retries.
    """
    for attempt in range(1, retries + 2):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data, dict(resp.headers)
        except HTTPError as e:
            status = e.code
            resp_headers = dict(e.headers) if e.headers else {}

            if status in (403, 429):
                reset_epoch = e.headers.get("X-RateLimit-Reset")
                remaining = e.headers.get("X-RateLimit-Remaining")
                reset_time = (
                    datetime.fromtimestamp(int(reset_epoch), tz=timezone.utc).isoformat()
                    if reset_epoch else "unknown"
                )
                log.warning(
                    "Rate limited (status=%d, remaining=%s, resets at=%s) "
                    "attempt %d/%d",
                    status, remaining or "?", reset_time, attempt, retries + 1,
                )
                if attempt <= retries:
                    delay = 5 * attempt
                    log.info("Retrying in %ds...", delay)
                    time.sleep(delay)
                    continue
                return None, resp_headers

            if status == 422:
                body = e.read().decode("utf-8", errors="replace")[:1000]
                log.error("GitHub API validation error %d: %s", status, body)
                return None, resp_headers

            body = e.read().decode("utf-8", errors="replace")[:500]
            log.error("GitHub API error %d: %s — %s", status, e.reason, body)
            return None, resp_headers

        except URLError as e:
            log.error("Network error: %s (attempt %d/%d)",
                      e.reason, attempt, retries + 1)
            if attempt <= retries:
                time.sleep(3 * attempt)
                continue
            return None, {}

        except json.JSONDecodeError as e:
            log.error("Invalid JSON: %s", e)
            return None, {}

    return None, {}


def build_issues_url(params: dict) -> str:
    """Build Issues List API URL with query params."""
    base = f"{ISSUES_URL}?{urlencode(params)}" if params else ISSUES_URL
    return base


def parse_link_header(header: str) -> dict[str, str]:
    """Parse RFC 5988 Link header into {rel: url} dict."""
    links = {}
    if not header:
        return links
    for part in header.split(","):
        match = re.match(r'<([^>]+)>;\s*rel="([^"]+)"', part.strip())
        if match:
            links[match[2]] = match[1]
    return links


def is_bounty_issue(issue: dict) -> bool:
    """
    Check if an issue is a $250 bounty.
    Title typically starts with '[$250]' — check title and labels.
    """
    title = issue.get("title", "")
    if re.search(r'\[\s*\$250\s*\]', title):
        return True
    for label in issue.get("labels", []):
        name = label.get("name", "")
        if "$250" in name or name.strip() == "250":
            return True
    body = issue.get("body") or ""
    if re.search(r'\$250', body):
        return True
    return False


def is_unassigned(issue: dict) -> bool:
    """Check if an issue has NO assignee(s)."""
    if issue.get("assignee"):
        return False
    if issue.get("assignees") and len(issue["assignees"]) > 0:
        return False
    return True


def fetch_labeled_issues(
    headers: dict,
    since: Optional[str] = None,
    max_pages: int = 10,
) -> list[dict]:
    """
    Fetch all open issues with label 'External' via Issues List API,
    handling pagination via Link header.  Uses the 'since' parameter
    to only fetch issues updated after a given timestamp (ISO 8601).

    Returns a flat list of issue dicts (newest first).
    """
    all_issues: list[dict] = []
    params = {
        "labels": "External",
        "state": "open",
        "sort": "created",
        "direction": "desc",
        "per_page": str(PAGE_SIZE),
    }
    if since:
        params["since"] = since

    url = build_issues_url(params)
    page = 0

    while url and page < max_pages:
        page += 1
        log.debug("Fetching page %d...", page)

        data, resp_headers = make_request(url, headers)
        if data is None:
            log.warning("Stopping after error on request")
            break

        if not isinstance(data, list):
            log.warning("Unexpected response type: %s", type(data).__name__)
            break

        all_issues.extend(data)
        log.debug("Page %d: got %d items (total: %d)",
                  page, len(data), len(all_issues))

        # Follow pagination via Link header
        link_header = resp_headers.get("Link", "")
        links = parse_link_header(link_header)
        url = links.get("next", None)

        # Polite delay between pages
        if url:
            time.sleep(0.3)

    log.info("Fetched %d issues across %d page(s)", len(all_issues), page)
    return all_issues


# ── State Management ───────────────────────────────────────────────────────

def load_state() -> dict:
    """Load persistent state from state.json."""
    try:
        if STATE_FILE.exists():
            raw = STATE_FILE.read_text(encoding="utf-8")
            return json.loads(raw)
    except (json.JSONDecodeError, OSError) as e:
        log.warning("Could not load state file, starting fresh: %s", e)
    return {"seen": {}, "last_checked": None}


def save_state(state: dict) -> None:
    """Save persistent state to state.json."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as e:
        log.error("Could not save state file: %s", e)


def append_log(issue: dict) -> None:
    """Append a single discovered issue to the log file."""
    timestamp = datetime.now(timezone.utc).isoformat()
    body = (issue.get("body") or "").replace("\n", " ")[:200]
    line = (
        f"[{timestamp}] #{issue['number']} | {issue['title']} | {issue['html_url']}\n"
        f"    Body: {body}\n"
    )
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as e:
        log.error("Could not write to log file: %s", e)


def format_issue(issue: dict) -> str:
    """Format a single issue for human-readable output."""
    lines = [
        f"  #{issue['number']} — {issue['title']}",
        f"    URL: {issue['html_url']}",
    ]
    body = issue.get("body") or ""
    if body:
        first_line = body.strip().split("\n")[0][:120]
        lines.append(f"    Desc: {first_line}")
    labels = [lab["name"] for lab in issue.get("labels", [])]
    if labels:
        lines.append(f"    Labels: {', '.join(labels)}")
    lines.append(f"    Created: {issue.get('created_at', 'unknown')}")
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Expensify/App $250 External Bounty Issue Watcher"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once (single pass) — compatible with cron",
    )
    args = parser.parse_args()

    # ── Load state ──────────────────────────────────────────────────────
    state = load_state()
    seen_ids: dict = state.get("seen", {})
    last_checked: Optional[str] = state.get("last_checked")

    log.info(
        "Starting Expensify/App watcher (tracked=%d issues, last_checked=%s)",
        len(seen_ids),
        last_checked or "never",
    )

    # ── Fetch all External issues (since last check if available) ───────
    headers = build_headers()
    all_external = fetch_labeled_issues(headers, since=last_checked)

    if all_external is None:
        log.warning("Failed to fetch issues from GitHub API")
        print("⚠  Failed to fetch issues — API error or rate limit hit.")
        return 1

    if not all_external:
        log.info("No External issues returned (empty result)")
        # Still update last_checked
        state["last_checked"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        print("ℹ  No issues returned (no new External issues since last check).")
        return 0

    # ── Filter: unassigned + $250 bounty ────────────────────────────────
    unassigned = [i for i in all_external if is_unassigned(i)]
    bounty = [i for i in unassigned if is_bounty_issue(i)]
    all_bounty = [i for i in all_external if is_bounty_issue(i)]

    log.info(
        "Fetched %d External issues → %d unassigned → %d $250 unassigned "
        "(%d total $250 including assigned)",
        len(all_external), len(unassigned), len(bounty), len(all_bounty),
    )

    # ── Detect new issues ───────────────────────────────────────────────
    new_issues: list[dict] = []
    updated_seen: dict[str, str] = dict(seen_ids)

    for issue in bounty:
        number = str(issue["number"])
        title = issue["title"]
        updated_seen[number] = title

        if number not in seen_ids:
            new_issues.append(issue)
            log.info("NEW $250 unassigned issue #%s: %s", number, title)
        elif seen_ids[number] != title:
            new_issues.append(issue)
            log.info("UPDATED $250 unassigned issue #%s: %s (was: %s)",
                     number, title, seen_ids[number])

    # ── Persist state ───────────────────────────────────────────────────
    state["seen"] = updated_seen
    state["last_checked"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    # ── Log new issues ──────────────────────────────────────────────────
    for issue in new_issues:
        append_log(issue)

    # ── Build report ────────────────────────────────────────────────────
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report_lines = [
        f"{'=' * 60}",
        f"  Expensify/App $250 External Bounty Watcher Report",
        f"  {now_str}",
        f"{'=' * 60}",
        f"  External issues fetched:              {len(all_external)}",
        f"  Unassigned:                           {len(unassigned)}",
        f"  Unassigned + $250 bounty:             {len(bounty)}",
        f"  Newly discovered this run:            {len(new_issues)}",
        f"  Total tracked issues:                 {len(updated_seen)}",
        f"{'=' * 60}",
    ]

    if new_issues:
        report_lines.append("")
        report_lines.append(f"  ⚡  NEW UNASSIGNED $250 ISSUES ({len(new_issues)}):")
        report_lines.append("")
        for i, issue in enumerate(new_issues, 1):
            report_lines.append(f"  [{i}] {format_issue(issue)}")
            report_lines.append("")
    else:
        report_lines.append("")
        report_lines.append("  ✓  No new unassigned $250 issues found since last check.")
        report_lines.append("")

    # Show all current unassigned $250 issues as reference
    if bounty:
        report_lines.append("")
        report_lines.append(f"  📋  CURRENT UNASSIGNED $250 ISSUES ({len(bounty)}):")
        report_lines.append("")
        for i, issue in enumerate(bounty, 1):
            report_lines.append(f"  [{i}] #{issue['number']} — {issue['title']}")
            report_lines.append(f"       {issue['html_url']}")
            labels = [l["name"] for l in issue.get("labels", [])]
            report_lines.append(f"       Labels: {', '.join(labels)}")
            report_lines.append(f"       Created: {issue.get('created_at', 'unknown')}")
            report_lines.append("")

    report_lines.append(f"{'=' * 60}")
    report = "\n".join(report_lines)

    print(report)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        log.exception("Unhandled error: %s", e)
        sys.exit(1)
