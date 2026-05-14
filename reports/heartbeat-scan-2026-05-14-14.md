# Heartbeat Scan Report — 2026-05-14 14:00 (UTC+8)

## Scan Summary
- **Command**: `python radar.py scan` (timed out at 180s during hot-zone scan)
- **Fresh candidates file**: `reports/candidates_2026-05-14.json` (written before timeout)
- **Platform bounties found**: 20 (IssueHunt fallback — all Scottcjn/Rustchain token bounties, non-USD)
- **GitHub issue searches**: 49 new issues across TS/Py with good-first-issue, help-wanted, documentation labels
- **Proven-payer hot zone scan**: Ran partially — 8 proven-payer repos scanned before timeout

## Known Issues Encountered
| Issue | Status |
|-------|--------|
| Scan timed out (180s limit) | Hot-zone scan incomplete; some repos not fully evaluated |
| Algora API unavailable | Migrated to Phoenix LiveView; no REST API |
| IssueHunt API unavailable | SPA with auth tokens; using GitHub fallback |
| OnlyDust / huntr APIs unavailable | No JSON responses |
| GH CLI search query quoting errors | Several bounty-qualified repo queries failed |

## Top 3 NEW Money Candidates

### #1 — home-assistant/core#170536
- **Title**: Tapo P110: Connection drop / "Unavailable" state during periods of high system load
- **URL**: https://github.com/home-assistant/core/issues/170536
- **Bounty**: ~$100 (scanner estimate via `expected_bounty_range: [100, 2000]`; **not a confirmed bounty** — Home Assistant has no formal bug bounty program; this is an inferred sponsor amount)
- **Created**: 2026-05-13 (~1 day ago)
- **Comments/Assignees**: 0 / none
- **Assessment**:
  - **Difficulty**: 🟡 Medium — timeout/retry tuning in TP-Link Tapo Python integration
  - **Competition**: 🟢 None (zero activity)
  - **AI Feasibility**: 🟢 High — well-scoped bug; fix involves adjusting poll timeout or adding retry logic
  - **Risk**: 🔴 No confirmed payout; needs physical Tapo P110 device for testing
  - **Precheck status**: ⚠️ Watch — previously flagged as uncertain bounty

### #2 — home-assistant/core#170535
- **Title**: numeric_state trigger with "for" does not work correctly with counter entities
- **URL**: https://github.com/home-assistant/core/issues/170535
- **Bounty**: ~$100 (same inferred estimate as #170536)
- **Created**: 2026-05-13 (~1 day ago)
- **Comments/Assignees**: 0 / none
- **Assessment**:
  - **Difficulty**: 🟢 Low-Medium — logic bug in automation engine's numeric_state trigger when used with counter entities; clear expected vs actual behavior
  - **Competition**: 🟢 None
  - **AI Feasibility**: 🟢 High — well-described; workaround exists (use state trigger instead), so fix is non-critical
  - **Risk**: 🔴 No confirmed payout; requires deep knowledge of HA's automation engine internals (`homeassistant/helpers/trigger.py` etc.)
  - **Verdict**: Better AI candidate than #170536 (no hardware needed), but same payout uncertainty

### #3 — home-assistant/core#170528
- **Title**: Weheat client niet gevonden (OAuth integration failure)
- **URL**: https://github.com/home-assistant/core/issues/170528
- **Bounty**: ~$100 (same inferred estimate)
- **Created**: 2026-05-13 (~1 day ago)
- **Comments/Assignees**: 1 bot comment (CodeOwnersMention); code owner @barryvdh tagged
- **Labels**: `integration: weheat`
- **Assessment**:
  - **Difficulty**: 🟡 Medium — OAuth credential handling / client registration issue on Dutch heat pump integration
  - **Competition**: 🟢 None (no human comments)
  - **AI Feasibility**: 🟡 Medium — OAuth flows are environment-dependent; may be user config error rather than code bug
  - **Risk**: 🔴 No confirmed payout; Dutch-language integration (niche); may require Weheat account to test
  - **Verdict**: Least promising of the three — niche integration, may not be a code fix

## Evaluation Summary

| Rank | Issue | Bounty | Difficulty | AI Fit | Competition | Payout Certainty | Overall |
|------|-------|--------|------------|--------|-------------|------------------|---------|
| 1 | HA#170535 (numeric_state + counter) | ~$100* | Low-Med | High | None | 🔴 Low | ⚠️ Watch |
| 2 | HA#170536 (Tapo P110 timeout) | ~$100* | Med | High | None | 🔴 Low | ⚠️ Watch |
| 3 | HA#170528 (Weheat OAuth) | ~$100* | Med | Med | None | 🔴 Low | ❌ Skip |

*\* $100 is scanner-inferred from whitelist `expected_bounty_range: [100, 2000]`. Home Assistant does NOT have a formal bounty program — this is an estimate based on GitHub Sponsors presence.*

## Conclusion

**No actionable money candidates found.**

All three top candidates are from home-assistant/core, but:
1. **No confirmed bounty** — The $100 value is an inferred estimate from the scanner's whitelist heuristic, not an actual posted bounty
2. **No payment guarantee** — Home Assistant has no formal bug bounty program; contributions are volunteer-based
3. **Hardware/testing barriers** — Two of three issues require physical devices (Tapo P110 smart plug, Weheat heat pump)
4. **Zero activity** — All issues are 1 day old with no maintainer engagement

The best candidate for AI-assisted contribution would be **#170535** (numeric_state + counter bug) since it requires no hardware, has clear reproduction steps, and is a contained logic fix. However, without a confirmed payout, it's not worth pursuing for income.

### Recommendations for Next Scan
1. Fix the GH CLI search query quoting issues in the scanner to enable bounty-specific repo scanning
2. Add explicit confirmed-bounty-only filter to avoid inferred/sponsor estimates
3. Consider shorter hot-zone scan or split into phases to avoid timeout
4. Expensify/App remains the most reliable proven payer — prioritize its new issues next scan

## Files Created/Modified
- `reports/heartbeat-scan-2026-05-14-14.md` — this file
- `reports/candidates_2026-05-14.json` — updated by scanner (3 money + 10 practice candidates)
