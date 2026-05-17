# Pre-check Report: home-assistant/core#170923

**Issue**: I cannot upload my songs in FLAC to the media panel
**URL**: https://github.com/home-assistant/core/issues/170923
**Created**: 2026-05-16 18:23 UTC
**State**: ✅ Open
**Assignee**: ❌ Unassigned (0)
**Comments**: 0
**Labels**: (none)

---

## 1. Summary

User wants to upload FLAC audio files (>20 MB) to the HA media panel. The upload limit is hardcoded at 20 MB. References PR #161436 which bumped it from 10 MB to 20 MB. User requests raising/removing the limit entirely (suggests 10 GB).

## 2. Technical Analysis

- File: `homeassistant/components/media_source/local_source.py`
- Line 27: `MAX_UPLOAD_SIZE = 1024 * 1024 * 20` (20 MB)
- Line 355: `request._client_max_size = MAX_UPLOAD_SIZE`
- This is the **only** limit — no per-file-type or per-format filtering

**Two possible fixes:**
1. **(Easy) Bump the limit**: Change `20` to `10240` (10 GB) — 1 line
2. **(Better) Make it configurable**: Add config option via integration options flow — ~20–50 lines

The user phrase "ideally... removed, but failing that, boldly increase to 10 GB" suggests option 1 would satisfy them.

## 3. Fix Complexity

| Factor | Assessment |
|--------|-----------|
| **Type** | Feature request / config change |
| **Lines to change** | 1 (simple bump) or ~20–50 (configurable option) |
| **Skill needed** | Python (basic) |
| **Risk** | 🟢 Very Low — no logic change, just raising a limit |

## 4. Bounty

❌ **No sponsor/bounty confirmed.** No "sponsor" or "$" label. No bounty program. The "$100 inferred" is the radar's generic assumption. FUNDING.yml points to Open Home Foundation donations.

## 5. Competition

🟢 **Zero competition** — no assignees, no PRs, 0 comments, <24h old.

## 6. Verdict

### 🟡 NEEDS TAO REVIEW

**Why not 🟢:**
1. ✅ **Technically trivial** — 1-line change, low risk
2. ✅ **Zero competition** — nobody is working on this
3. ⚠️ **No bounty confirmed** — this is purely a community contribution (no $100)
4. ⚠️ **Acceptance risk** — Maintainers may want a configurable option instead of a hardcoded bump (PR #161436 just bumped the number once before)
5. ⚠️ **No urgency** — 0 comments, 0 👍 reactions, no maintainer response

**What Tao should decide:**
- Is this worth doing as a **free contribution** (reputation building)?
- Or wait to see if maintainers indicate they'd accept a configurable approach?
- Potential PR: Raise `MAX_UPLOAD_SIZE` to 100 MB as a middle-ground (covers FLAC without being excessive)
