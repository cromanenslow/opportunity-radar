# Pre-check Report — 2026-05-16 22:03 CST

## Previously Pre-checked Candidates (Status Check)

### 1. vitejs/vite#22456 — Pnpm overrides docs URL fix ($100 sponsor)
- **Status**: ✅ OPEN, unassigned
- **Fix difficulty**: 🟢 Trivial — 1-line URL change in docs
- **Bounty**: $100 inferred (sponsor, not confirmed)
- **Competition**: 🟢 Low (1 comment from Vite member suggesting fix direction)
- **AI fit**: 🟢 High (simple docs update)
- **Verdict**: 🟢 **Still viable** — Previously confirmed 🟢

### 2. home-assistant/core#170880 — IntesisHome regression ($100 sponsor)
- **Status**: ✅ OPEN, unassigned
- **Fix difficulty**: 🟡 Medium — pyintesishome library bump (1.8.0→1.8.7), needs reproduction
- **Bounty**: $100 inferred (sponsor, not confirmed)
- **Competition**: 🟢 Low (only bot comment tagging @jnimmo)
- **AI fit**: 🟡 Medium (needs HA integration + library knowledge, 2-15 LOC fix)
- **Verdict**: 🟢 **Still viable** — Previously confirmed 🟢

### 3. home-assistant/core#170875 — Teleinfo USB probing ($100 sponsor)
- **Status**: ⚠️ OPEN, unassigned, but **code owner @esciara said "Will have a look today and post a fix asap"** (9h ago)
- **Fix difficulty**: 🟡 Medium — config flow USB probing fix (20-50 LOC)
- **Bounty**: $100 inferred (sponsor, not confirmed)
- **Competition**: 🟡 Code owner actively working on it (no PR posted yet though)
- **AI fit**: 🟢 High (well-understood HA pattern)
- **Verdict**: 🟡 **Downgraded to 🟡** — Code owner has claimed intent to fix. Risk of being pre-empted by @esciara's PR.

---

## Newly Discovered Candidates (7)

### 1. claude-builders-bounty/claude-builders-bounty#3 — HOOK: Block destructive bash ($100)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN, unassigned |
| **Fix difficulty** | 🟡 Medium — Claude Code hook creation |
| **Bounty confirmed?** | ✅ Confirmed ($100 bounty label) |
| **Competition** | 🔴 Extreme — 8+ PRs already submitted; `/opire try` from multiple users |
| **AI can do it?** | 🟢 High |
| **Verdict** | 🔴 **NOT viable** — Completely saturated |

### 2. claude-builders-bounty/claude-builders-bounty#5 — n8n+Claude weekly summary ($200)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN, unassigned |
| **Fix difficulty** | 🟡 Medium — n8n workflow + Claude Code |
| **Bounty confirmed?** | ✅ Confirmed ($200 bounty label) |
| **Competition** | 🔴 Extreme — 20+ PRs already submitted; many `/opire try` claims |
| **AI can do it?** | 🟢 High |
| **Verdict** | 🔴 **NOT viable** — Completely saturated |

### 3. coder/code-server#7198 — $100 Windows Binary Bounty ($100)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN, unassigned |
| **Fix difficulty** | 🔴 High — Native Windows compilation of code-server (VS Code/Electron), socket/ESM issues |
| **Bounty confirmed?** | ✅ Confirmed ($100 offered by user in issue body, email provided) |
| **Competition** | 🟡 3+ submissions exist (imaanmulji, wushange, treesilent-creator posted working binaries) but none accepted yet |
| **AI can do it?** | 🔴 Low — Requires native Windows environment, VS Code compilation expertise |
| **Verdict** | 🟡 **Watch only** — High difficulty, existing submissions unmerged, likely dead-end |

### 4. moorcheh-ai/memanto#397 — LangGraph Integration Challenge ($100)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN, unassigned |
| **Fix difficulty** | 🟡 Medium — LangGraph example with Memanto memory |
| **Bounty confirmed?** | ✅ Confirmed ($100 via BountyHub, posted by mjfekri) |
| **Competition** | 🔴 Extreme — **25+ PRs** submitted (#404, #405, #408, #409, #411, #412, #416, #418, #419, #423, #426, #427, #434, #445, #448, #451, #452, #459, #460, #464, #469, #471, #474, #475...); 35+ people commenting |
| **AI can do it?** | 🟢 High (many submissions are clearly AI-generated) |
| **Verdict** | 🔴 **NOT viable** — Massively oversaturated |

### 5-7. Three Unnamed Candidates

**Note**: I searched all scan reports and candidate files in `/Users/tao/桌面/项目文件夹/ai赚钱/opportunity-radar/` but could not find a report explicitly listing specific unnamed candidates #5-7. The most likely candidates from the heartbeat expansion scan (hot zone expansion from 32→52 repos, 2026-05-16) that were actively in the pipeline are:

#### 5. home-assistant/core#170846 — Apple TV loop error ($100 inferred)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN (confirmed earlier in scan reports) |
| **Fix difficulty** | 🟡 Medium — asyncio RuntimeError in apple_tv integration |
| **Bounty** | $100 inferred (sponsor, not confirmed) |
| **Competition** | 🟢 Low (no activity) |
| **AI fit** | 🟡 Medium (needs Apple TV ecosystem knowledge) |
| **Verdict** | 🟡 **Speculative** — No bounty confirmation |

#### 6. home-assistant/core#170849 — Zigbee network congestion ($100 inferred)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN (confirmed earlier) |
| **Fix difficulty** | 🔴 High — Zigbee protocol stack knowledge required |
| **Bounty** | $100 inferred (sponsor, not confirmed) |
| **Competition** | 🟢 Low (likely due to difficulty) |
| **AI fit** | 🔴 Low (deep hardware protocol knowledge needed) |
| **Verdict** | 🔴 **Not recommended** — High difficulty, uncertain payout |

#### 7. home-assistant/core#170850 — Backup storage path ($100 inferred)
| Criteria | Assessment |
|----------|-----------|
| **Open/Unassigned?** | ✅ OPEN (confirmed earlier) |
| **Fix difficulty** | 🟡 Medium — HA backup architecture |
| **Bounty** | $100 inferred (sponsor, not confirmed) |
| **Competition** | 🟢 Low (no activity) |
| **AI fit** | 🟡 Medium (needs HA backup system understanding) |
| **Verdict** | 🟡 **Speculative** — No bounty confirmation |

---

## Summary Table

### Previously Pre-checked (Status Update)
| # | Candidate | Bounty | Previous | Current | Change |
|---|-----------|--------|----------|---------|--------|
| 1 | vitejs/vite#22456 | $100* | 🟢 | 🟢 | — |
| 2 | HA/core#170880 | $100* | 🟢 | 🟢 | — |
| 3 | HA/core#170875 | $100* | 🟢 | 🟡 | ⚠️ Code owner @esciara claimed fix |

### New Candidates
| # | Candidate | Bounty | Verdict | Key Risk |
|---|-----------|--------|---------|----------|
| 1 | claude-bounty#3 | $100 ✅ | 🔴 | 8+ PRs, saturated |
| 2 | claude-bounty#5 | $200 ✅ | 🔴 | 20+ PRs, saturated |
| 3 | coder/code-server#7198 | $100 ✅ | 🟡 | High difficulty, existing submissions |
| 4 | memanto#397 | $100 ✅ | 🔴 | 25+ PRs, oversaturated |
| 5 | HA/core#170846 | $100* | 🟡 | No bounty confirmation |
| 6 | HA/core#170849 | $100* | 🔴 | High difficulty + no bounty confirmation |
| 7 | HA/core#170850 | $100* | 🟡 | No bounty confirmation |

*$100 = sponsor-inferred value, not a confirmed bounty

## Key Conclusions

1. **All 4 newly-discovered confirmed-bounty candidates are NOT viable** — Claude Builders Bounty and Memanto are massively oversaturated with 8-25+ PRs each. Code-server Windows build requires native Windows tooling and has multi-week-old unmerged submissions.

2. **The 3 previously 🟢 pre-checked candidates remain the best options** — vitejs/vite#22456 (docs URL fix), HA#170880 (IntesisHome regression), though #170875 (Teleinfo) is now at risk from code owner intervention.

3. **Pipeline remains dry** for truly actionable $100+ bounty issues. The reported candidates from the expansion scan are either oversaturated or have unconfirmed bounties (sponsor-inferred only).

4. **No files were modified** — this is a read-only pre-check report.
