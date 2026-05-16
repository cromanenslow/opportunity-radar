# Pre-check Report: home-assistant/core#170846

**Issue**: `apple_tv` integration: `RuntimeError: loop is not the running loop` when adding `AppleTVKeyboardFocused` binary sensor during reconnect dispatch
**URL**: https://github.com/home-assistant/core/issues/170846
**Reported by**: didusee
**Created**: 2026-05-15 21:15 UTC (Korean timezone)
**Updated**: 2026-05-15 21:15 UTC
**State**: ✅ Open
**Assignee**: ❌ Unassigned (0 assignees)
**Comments**: 0
**Labels**: None yet (expected: `integration: apple_tv`, `bug`)

---

## 1. Issue Summary

### The Problem
When the Apple TV integration re-dispatches the `apple_tv_connected_<mac>` signal after a Companion-protocol reconnect, the binary-sensor platform raises `RuntimeError: loop is not the running loop` while trying to add the `AppleTVKeyboardFocused` entity. The dispatched task is then garbage-collected before it can run, producing a follow-up `Task was destroyed but it is pending!` warning.

### Root Cause (well-diagnosed by reporter)
The call chain is:

1. `_async_connect()` finishes → calls `_dispatch_send(SIGNAL_CONNECTED, self.atv)`
2. `_dispatch_send()` → `async_dispatcher_send()` (runs on event loop)
3. `async_dispatcher_send_internal()` iterates registered callbacks
4. `setup_entities` (in `binary_sensor.py`) is a **plain sync function** (not `@callback`, not `async`)
5. `get_hassjob_callable_job_type(setup_entities)` → `HassJobType.Executor`
6. `_async_add_hass_job()` → `self.loop.run_in_executor(None, target, *args)` — runs on **SyncWorker thread**
7. Inside `setup_entities`, `async_add_entities([...])` is called
8. `_async_schedule_add_entities_for_entry()` → `config_entry.async_create_task(..., eager_start=True)`
9. `async_create_task_internal()` → `create_eager_task(target, loop=self.loop, eager_start=True)`
10. **Python 3.14's `Task(coro, loop=loop, eager_start=True)` validates that `loop` is the running loop on the calling thread**
11. We're on a SyncWorker thread, not the event loop thread → **RuntimeError**

The eager-start validation is new in Python 3.13→3.14 transition. On older Python versions, the same code silently scheduled the task on the event loop.

### Impact
- ✅ Non-fatal — `media_player` entity continues to work
- ❌ Fires on **every reconnect** (frequent on Gen 3 Apple TV 4K due to tvOS 26.5 Companion silent-drop)
- ❌ Dozens of ERROR-level stack traces per day in logs
- ❌ Follow-up warning: `Task was destroyed but it is pending!`

### Affected Environment
- HA Core 2026.5.1
- Python 3.14
- Apple TV 4K Gen 3 (AppleTV14,1) on tvOS 26.5
- Affected file: `homeassistant/components/apple_tv/binary_sensor.py`

---

## 2. Bounty / Sponsor Analysis

| Aspect | Status |
|--------|--------|
| **GitHub Sponsors** | Home Assistant is under the Open Home Foundation (custom funding link: openhomefoundation.org). No direct `$` bounty on this issue. |
| **Labels** | No bounty/sponsor labels applied yet |
| **Bug Bounty Program** | Home Assistant does NOT have a formal bug bounty program. Contributions are community-driven. |
| **Sponsor-backed Issues** | Some HA issues have been sponsored (~$100) but this is rare and not official policy |
| **Hacktoberfest** | Repository has `hacktoberfest` topic, but that's not monetary |
| **Expected Bounty** | **$0** — No monetary bounty confirmed. This is a pure community contribution unless a sponsor steps in. |

**Verdict**: ❌ No confirmed bounty/sponsor. Home Assistant does not have a formal bounty program.

---

## 3. Competition Analysis

| Factor | Status |
|--------|--------|
| Assignees | **0** — completely unassigned |
| Comments | **0** — no discussion yet |
| PRs | **0** — no one has submitted a fix |
| Age | **< 24 hours** (created May 15 2026) — extremely fresh |
| Reporter's intent | Reporter (didusee) provided detailed diagnosis + fix suggestions, offered to test a patch, but did **not** submit a PR |
| Cross-references | 1 — cross-ref to #168210 (related tvOS 26.5 issue, also open) |

**Verdict**: 🟢 **Zero competition** — completely uncontested. First PR wins.

---

## 4. Complexity Analysis

### Technical Depth: EASY-MEDIUM

**What needs to change**:

The fix is in **one file**: `homeassistant/components/apple_tv/binary_sensor.py`

Three possible approaches (all valid, reporter suggested them):

#### Option A: Make `setup_entities` an async function (✅ Recommended)
```python
async def setup_entities(atv: AppleTV) -> None:
    if atv.features.in_state(FeatureState.Available, FeatureName.TextFocusState):
        name: str = config_entry.data[CONF_NAME]
        async_add_entities(
            [AppleTVKeyboardFocused(name, config_entry.unique_id, manager)]
        )
        cb()
```
- The dispatch happens on the event loop thread
- `async` function → `HassJobType.Coroutinefunction` → eagerly started on event loop
- `async_add_entities` (sync) runs on event loop → `create_eager_task` validation passes
- **~3 lines changed**

#### Option B: Add `@callback` decorator (Simpler)
```python
@callback
def setup_entities(atv: AppleTV) -> None:
    ...
```
- `@callback` → `HassJobType.Callback` → runs directly on event loop
- Same effect as Option A, even simpler
- But `async_add_entities` calls `async_create_task` internally, which creates a new task — this is fine from within a callback

Wait — let me verify. If `setup_entities` is `@callback`, then `async_dispatcher_send_internal` would call `job.target(*args)` directly (on the event loop thread). Then `async_add_entities` (sync function `_async_schedule_add_entities_for_entry`) would run on the event loop thread, calling `async_create_task` with `eager_start=True`. Since we're on the event loop thread, Python 3.14's validation passes.

Yes, Option B is the simplest fix.

#### Option C: Pass `eager_start=False` (Core-level fix)
- Change `binary_sensor.py`'s `async_add_entities` call or the platform-level `_async_schedule_add_entities_for_entry`
- More invasive, affects broader codebase
- Not recommended for a focused fix

### Lines of Code Change
- **Option A**: ~3 lines (add `async` keyword, possibly add `await` if needed — but `async_add_entities` is sync, so no `await` needed)
- **Option B**: ~1 line (add `@callback` decorator)
- **Minimal, targeted fix**

### Testing
- Requires an Apple TV device to test (or a mocked pyatv session)
- The error only reproduces on disconnection/reconnection cycle
- Could be tested with unit tests mocking the disconnect flow

### AI Feasibility
- ✅ **High** — The root cause is clearly diagnosed
- ✅ Fix is simple (1-3 lines in one file)
- ⚠️ Testing requires environment setup (or trusting the logic analysis)

---

## 5. Opportunity Scoring

| Dimension | Weight | Score (1-10) | Weighted |
|-----------|--------|--------------|----------|
| Payment Certainty | 26% | 0 | 0.00 |
| Verifiability | 22% | 9 | 1.98 |
| AI Suitability | 18% | 9 | 1.62 |
| Maintainer Activity | 12% | 8 | 0.96 |
| Context Reuse | 7% | 7 | 0.49 |
| Competition Intensity | 15% | 10 | 1.50 |
| **TOTAL** | **100%** | | **6.55** |

### Breakdown

**Payment Certainty: 0/10**
- No bounty, no sponsor, no formal bug bounty program
- This is a pure community contribution
- **However**: Home Assistant is a FOSS project with 87k+ stars. Contributions build reputation, and some issues do attract sponsors later. But there is $0 guarantee.

**Verifiability: 9/10**
- Full traceback provided
- Complete root cause analysis by reporter
- Clear reproduction steps
- Well-documented code paths and relevant source files
- Fix is logically verifiable even without hardware

**AI Suitability: 9/10**
- Python, single file change
- Clear before/after traceback
- Well-understood async programming pattern
- Minimal code change (1-3 lines)
- HA has extensive test infrastructure

**Maintainer Activity: 8/10**
- Home Assistant is extremely active (dev branch commits daily)
- apple_tv integration is actively maintained
- Integration label expected to be added soon
- HA core team responsive to well-documented issues

**Context Reuse: 7/10**
- HA ecosystem knowledge reusable for future HA issues
- asyncio/eager_start knowledge transferable to other Python projects
- Similar pattern may affect other integrations using dispatcher + sync callbacks

**Competition Intensity: 10/10**
- Zero assignees, zero comments, zero PRs
- Fresh issue (< 24 hours old)
- First mover advantage is decisive

---

## 6. Recommendation

### ⚠️ **CONDITIONAL RECOMMENDATION**

**For bounty hunting**: ❌ **Not recommended** — No confirmed bounty. Home Assistant does not have a formal bounty program. The reporter didn't mention any sponsor.

**For reputation building / portfolio**: ✅ **Strongly recommended** (if Tao wants to invest time for non-monetary reasons)
- Extremely low-hanging fruit (1-3 line fix)
- Zero competition
- Well-documented issue with complete root cause analysis
- Home Assistant is a high-visibility project (87k+ stars)
- Good for building OSS contribution track record

**For speculative bounty**: ⚠️ **Low probability** — While some HA issues occasionally get sponsor attention, there's no mechanism to request or expect payment. The issue itself mentions $0.

### Fix Strategy (if pursued)

**Approach**: Add `@callback` decorator to `setup_entities` in `binary_sensor.py`

```python
@callback
def setup_entities(atv: AppleTV) -> None:
    if atv.features.in_state(FeatureState.Available, FeatureName.TextFocusState):
        assert config_entry.unique_id is not None
        name: str = config_entry.data[CONF_NAME]
        async_add_entities(
            [AppleTVKeyboardFocused(name, config_entry.unique_id, manager)]
        )
        cb()
```

**Rationale**:
1. `@callback` makes `get_hassjob_callable_job_type` return `HassJobType.Callback`
2. `async_dispatcher_send_internal` runs Callback targets directly (on event loop thread)
3. `async_add_entities` → `async_create_task(eager_start=True)` runs on event loop thread → Python 3.14 validation passes
4. Minimal diff (1 line added), no behavioral change for pre-3.14 Python

**PR Scope**: 1 file, 1-3 lines changed, 5-10 minute coding + test verification

---

## 7. Summary

```
Issue:            home-assistant/core#170846 — Apple TV RuntimeError 循环 Bug
Bounty:           ❌ $0 (no confirmed bounty/sponsor)
Competition:      🟢 Zero (0 assignees, 0 comments, 0 PRs, <24h old)
Complexity:       🟢 Easy (1-3 line fix in 1 file)
AI Feasibility:   ✅ High
Payment Certainty: ❌ None
Reputation Value: ✅ High (Home Assistant, 87k★)
Recommendation:   ⚠️ Conditional — Good for portfolio/reputation but NO monetary bounty
```

**Final Verdict**: ⭐⭐ (for reputation building) / ❌ (for bounty hunting)
