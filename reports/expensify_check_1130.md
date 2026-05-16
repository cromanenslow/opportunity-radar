# Expensify/App External Issues Check
**Date:** 2026-05-16 11:33  
**Report:** expensify_check_1130.md

---

## Summary

| Metric | Value |
|---|---|
| Total open External issues | **523** (per GitHub Search API) |
| Unassigned External issues | **0** |
| $250 unassigned issues | **0** |
| Issues checked (via Issues API) | 200 (all assigned) |

## Detailed Findings

### Method 1: Watcher Script (`watch-expensify-issues.py`)
- Ran with `--once` flag
- Confirmed: **0 new unassigned $250 issues** found
- Watcher has tracked 3 issues total in state

### Method 2 & 3: GitHub API (gh + curl)
- Fetched and inspected the first **200 open External issues** (2 pages × 100) — all have assignees
- GitHub Search API query `repo:Expensify/App state:open label:External no:assignee` returns **0 results**
- All 100% of open External issues are currently assigned

### Sample of Recent $250 Issues (all assigned)
| Issue | Title | Assignee |
|---|---|---|
| #90850 | [$250] Odometer distance expenses to self-DM lose start/end readings | Julesssss |
| #90807 | [$250] Distance - After deleting a distance rate... | bernhardoj |
| #90794 | [$250] Onboarding modal is show... | marufsharifi |
| #90779 | [$250] Travel - Cursor position... | hoangzinh |
| #90776 | [$250] Two workspaces screens... | ikevin127 |
| #90775 | [$250] The user gets a 'You don't have access...' | suneox |
| #90770 | [$250] Single Expense Appears... | brunovjk |
| #90756 | [$250] Web app crashes intermittently... | eVoloshchak |
| #90747 | [$250] Update Approved! Partner Help Page... | dubielzyk-expensify |
| #90729 | [$250] Link redirects... | dmkt9 |

*(First 10 of 92+ $250 issues — all have assignees)*

## Conclusion

**管线仍枯竭 (Pipeline is still dry).**  

There are **no new $250 unassigned External issues** available on Expensify/App at this time. Every open External issue — including all $250 bounty issues — already has at least one assignee. The bounty pipeline remains empty for new contributors looking for unclaimed work.

**Next check recommended:** Next cron cycle or as scheduled.
