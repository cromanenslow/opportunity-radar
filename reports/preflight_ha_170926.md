# Pre-check Report: home-assistant/core#170926

**Issue**: FRITZ!Box Tools: After HA Core Update "Call deflections" aren't available anymore
**URL**: https://github.com/home-assistant/core/issues/170926
**Created**: 2026-05-16 19:10 UTC
**State**: ✅ Open
**Assignee**: ❌ Unassigned (0)
**Comments**: 0
**Labels**: (none)

---

## 1. Summary

User reports that "Call deflections" switch entities disappeared after updating from core-2026.4.4 to core-2026.5.2. No logs, diagnostics, or error messages provided.

## 2. Technical Analysis

- Integration: `fritz` (FRITZ!Box Tools) — quality scale: gold
- Call deflections are `FritzBoxDeflectionSwitch` entities in `switch.py`
- Data fetched via `async_update_call_deflections()` → `X_AVM-DE_OnTel1.GetDeflections` → xmltodict parse
- **No fritz component files changed** between 2026.4.4 and 2026.5.2 (confirmed via git diff)
- Root cause likely: upstream `fritzconnection` library change, HA Core entity lifecycle change, or TR-064 service discovery change
- PR #170030 (May 7) added `ParseError` handling — unrelated
- PR #170542 (May 14) only cosmetic line-length fixes in switch.py — unrelated

## 3. Fix Complexity

| Factor | Assessment |
|--------|-----------|
| **Type** | Regression bug (was working in 2026.4.4) |
| **Root cause** | Unknown — needs debugging |
| **Lines to change** | Unknown — could be 1–20 once root cause found |
| **Skill needed** | Python, fritzconnection lib, FRITZ!Box TR-064 API |
| **Risk** | 🟡 Medium — no logs/diags provided, can't reproduce without FRITZ!Box |

## 4. Bounty

❌ **No sponsor/bounty confirmed.** No "sponsor" or "$" label. No bounty program. The "$100 inferred" is the radar's generic assumption for HA issues. FUNDING.yml points to Open Home Foundation donations.

## 5. Competition

🟢 **Zero competition** — no assignees, no PRs, 0 comments, <24h old.

## 6. Verdict

### 🔴 NOT RECOMMENDED

**Reasons:**
1. Root cause completely unknown — needs a FRITZ!Box device + debug logs to diagnose
2. No diagnostics provided by reporter
3. Core HA code didn't change — likely an upstream library or core platform issue
4. No actionable reproduction steps
5. No confirmed bounty

**If pursuing**: Ask for debug logs, check fritzconnection changelog between 1.15.x versions, test with HA dev environment + FRITZ!Box.
