# Preflight Report: tscircuit/dsn-converter#54 — Smoothie Board DSN Conversion

**Date**: 2026-05-14
**Analyst**: Hermes Agent (AI Preflight)
**Bounty**: $170 (Algora-confirmed, plus $5 secondary)
**Repo**: https://github.com/tscircuit/dsn-converter
**Issue**: https://github.com/tscircuit/dsn-converter/issues/54
**Algora**: https://app.algora.io/org/tscircuit

---

## Issue Summary

**Title**: "We can't convert Smoothie Board to Circuit JSON"

**Description**: The DSN converter fails to correctly parse/convert a specific PCB DSN file from the freerouting project — the Smoothie Board test case (`Issue145-smoothieboard.dsn`). The issue describes this as "probably a pretty hard multi-step issue" and suggests contributors should break work into smaller PRs.

The Smoothie Board DSN file has numerous special characteristics not handled by the converter:
- Uppercase `(PCB ...)` root keyword
- Custom via padstack naming convention (`Via[0-3]_800:400_um`)
- Pins with rotation specifiers
- Named/symbolic pin labels (`+`, `-`, `2@1`)
- Quoted string values in net references
- Custom DSN parser directives (`string_quote`, `space_in_quoted_tokens`)

The maintainer explicitly noted: *"In addition to the bounty, we will likely tip for steps along the way because doing it in one big PR may be counter-productive."*

**Labels**: None visible (likely unlabeled)
**State**: Open (created ~Feb 2026)
**Comments**: 199 comments

---

## Bounty Status — Algora Confirmed

✅ **Bounty is still listed as OPEN on Algora** (as of 2026-05-14)

The Algora page for tscircuit shows two active entries for `dsn-converter#54`:
- **$5** — "We can't convert Smoothie Board to Circuit JSON"
- **$170** — "We can't convert Smoothie Board to Circuit JSON"

**Original bounty pool** (per Algora bot comment on issue):
| Amount | Sponsor | Status |
|--------|---------|--------|
| $5 | NguyenCong2k | Open |
| $170 | AntDags | Open |
| $30 | Mohan | Likely paid |
| $70 | aifunmobi | Likely paid |
| $70 | tscircuit | Likely paid |

Many intermediate rewards have been paid for partial progress (see attempt table in issue — 50+ entries with many marked "Reward"). However, the main $170 and $5 bounties remain open.

**Note**: The Algora bounty-specific page URL (`/org/tscircuit/bounties/54`) returns 404, but the issue appears twice on the main open bounties list.

---

## Bug Reproduction

### Setup
- Repo cloned to `/tmp/tscircuit-dsn-converter`
- Node.js + npm used for dependencies; Bun installed for test runner
- DSN fixture at `tests/assets/repro/smoothieboard-repro.dsn` (2984 lines)

### Test Results
```
bun test tests/repros/repro7-smoothie-board.test.ts
→ ✅ PASS (smoothieboard repro [31ms])

Full test suite (48 tests):
→ 42 pass, 1 skip, 5 fail
```

**The smoothie board repro test passes on current `main`.** This means the basic conversion path works. The remaining work involves edge cases and fidelity improvements.

### Failing Tests
5 tests fail, all with the same error:
```
TypeError: Attempting to define property on object that is not extensible.
  at render (@tscircuit/core/dist/index.js:7406:5)
```
These failures appear to be pre-existing issues with the `@tscircuit/core` dependency (version incompatibility), not related to the Smoothie Board issue.

### Key Observation
The freerouting reference file (the original `Issue145-smoothieboard.dsn`) at `https://github.com/freerouting/freerouting/blob/master/tests/Issue145-smoothieboard.dsn` **returns 404** — the file was likely moved or removed from the upstream repo. The existing fixture may differ from the original.

---

## Fix Complexity & AI Feasibility

### Complexity: 🔴 VERY HIGH

| Factor | Assessment |
|--------|-----------|
| **Scope** | Multi-step, multi-bug issue with ~10 distinct sub-problems |
| **Domain knowledge** | Requires deep understanding of PCB DSN file format, freerouting conventions, KiCad compatibility, and the tscircuit suite |
| **Codebase size** | ~4,000+ lines of TypeScript across ~30 files |
| **Existing PRs** | 29+ PRs attempt partial fixes — none merged. Indicates maintainer has high standards or the problem space is fragmented |
| **Reproduction clarity** | Basic test passes; unclear what "done" looks like (no merged PRs, no closed issue) |
| **Maintainer activity** | Active (PRs reviewed, repo getting releases), but no issue #54 PRs merged |

### AI Feasibility: ⚠️ QUESTIONABLE

- **What's being asked is not a single TypeScript bug fix** but a series of compatibility enhancements for a complex DSN file
- An AI (Codex/Claude) could potentially handle ONE specific sub-problem (e.g., "parse uppercase PCB root" or "fix via padstack dimensions"), but claiming the full $170 requires a comprehensive solution
- The issue explicitly encourages incremental work with tipping, which rewards the multi-PR approach
- However, the maintainer has not merged ANY of the 29+ PRs, creating significant risk that even good work won't be accepted
- The codebase uses Bun + TypeScript with path aliases (`lib/`) which can confuse AI code generation tools
- Domain-specific knowledge (DSN sexpr parsing, PCB terminology) is hard for general-purpose AI

### Estimated Code Change
Each sub-fix: **10–50 lines** in 1–2 files
Complete solution: **200–500+ lines** across 5–10 files

---

## Competition

| Metric | Value |
|--------|-------|
| **Comments** | 199 |
| **Linked PRs** | 29 (open) + many closed/spam |
| **Active attempters** | 50+ according to Algora table |
| **Spam/bot PRs** | Significant — one account (`toiyeugym19-cmyk`) created 30+ identical PRs titled "fix: automated bounty verification 54" |
| **Legitimate contributors** | ~15–20 real-looking PRs with different approaches |
| **Merged PRs** | **0** — none of the #54-related PRs have been merged |
| **Last activity** | May 13, 2026 (just yesterday) — multiple new attempts |

### Notable PRs
| PR | Author | Approach |
|----|--------|----------|
| #411 | realkoreanbeef | Via padstack dimensions |
| #410 | Treasure520520 | Preserve session network vias |
| #409 | realkoreanbeef | Unique via IDs |
| #408 | Adysekus | Uppercase PCB, string_quote, rotation, pill shapes |
| #407 | Donutking20 | Placement rotation |
| #406 | himanalot | Session coordinate scaling |
| #352 | thanhdatloveyou18-coder | Comprehensive smoothie board fix |

The competition is **fierce and messy** — both legitimate contributors and spammers are flooding the issue. The signal-to-noise ratio is poor.

---

## Recommendation: ⚠️ Conditional

**Overall Verdict**: Recommend proceeding with CAUTION — only if a specific, narrow sub-problem can be identified and solved independently.

### Rationale

**Reasons to Go:**
- ✅ Bounty is confirmed active on Algora ($170 + $5)
- ✅ The project is active (recent releases, maintainer responds)
- ✅ Basic infrastructure works (clone, install, test)
- ✅ Previous preflight candidates failed; this is the last best hope
- ✅ The multi-step nature means a well-scoped PR could get rewarded

**Reasons to Skip/Be Cautious:**
- ❌ **Zero PRs merged** despite 4+ months and 29+ attempts — major red flag
- ❌ 199 comments with 50+ attempters — extremely crowded
- ❌ Heavy spam/bot PR pollution
- ❌ Not a single TypeScript bug but a complex feature compatibility issue
- ❌ Original reference DSN file 404s
- ❌ Maintainer may be selective or the problem may be harder than it appears
- ❌ The basic test already passes — what's the remaining "definition of done"?

### Recommended Approach (if pursuing)

1. **Pick one VERY narrow sub-problem** from the issue, ideally one no PR has addressed yet
2. Scope to **≤50 lines changed, ≤2 files**
3. Submit a PR with `/claim #54` in the body
4. Be prepared to iterate — don't expect first PR to be merged
5. Consider targeting the **$5 bounty** first (lower risk) rather than the $170

**Alternatively**: Monitor the issue for 1–2 weeks. If any of the current PRs (#408, #411, etc.) get merged, the bounty landscape changes significantly and could indicate maintainer is now accepting PRs.

---

## Risk Factors

| Risk | Severity | Mitigation |
|------|----------|------------|
| PRs never merge (4-month track record) | 🔴 High | Pick tiny win; don't invest heavily |
| Spam pollution drowns quality PRs | 🟡 Medium | Engage on Discord first |
| Original DSN file unavailable | 🟡 Medium | Use existing fixture |
| 5 unrelated tests fail on main | 🟡 Medium | Not our problem to fix |
| "Done" criteria unclear | 🔴 High | Clarify on issue before coding |
| Bounty may be split among many | 🟡 Medium | Accept smaller payout |
| Dependency issues (@tscircuit/core) | 🟡 Medium | Work around them |
| Strong AI competition | 🟡 Medium | Focus on niche sub-problem |

---

## Files Created
- `/Users/tao/Desktop/项目文件夹/ai赚钱/opportunity-radar/reports/preflight_tscircuit_dsn-converter_54.md`

## Previous Preflight References
- `/Users/tao/Desktop/项目文件夹/ai赚钱/opportunity-radar/reports/preflight_tscircuit_dsn-converter_54.md` (this report)
- Previous reports: getkyo/kyo#390 (❌), aietal/isaac#45 (❌), archestra-ai/archestra#3858 (❌)
- `/Users/tao/Desktop/项目文件夹/ai赚钱/opportunity-radar/KNOWLEDGE.md`

---

*End of preflight report*
