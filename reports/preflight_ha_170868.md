# Pre-check Report: home-assistant/core#170868

**Issue**: Tuya integration does not poll data from the cloud
**URL**: https://github.com/home-assistant/core/issues/170868
**Reported by**: xbeaudouin
**Created**: 2026-05-16 02:55 UTC
**Updated**: 2026-05-16 04:33 UTC
**State**: ✅ Open
**Assignee**: ❌ Unassigned (0 assignees)
**Comments**: 2
**Labels**: `integration: tuya`

---

## 1. Issue Summary

### The Problem
The user has a single Tuya device — a **liquid level sensor** (outdoor tanker sensor, `sensor.dehors_tanker_niveau_du_liquide`) — that does not update its data in Home Assistant. The Smart Life app shows correct/updated data, but HA data remains stale. After 12+ hours, no update occurs. The user created a workaround automation that reloads the config entry every 5 minutes using `homeassistant.reload_config_entry`.

### Reporter's Device & Setup
- **Device**: Outdoor tank liquid level sensor (Tuya category `YWCGQ` — liquid level sensor)
- **HA Core version**: 2026.5.1
- **HA Installation type**: Home Assistant OS
- **Workaround**: Cron-like automation reloading the Tuya config entry every 5 minutes

### What the User Is Asking For
> "Is this possible to add time to force polling data from tuya cloud?"

---

## 2. Root Cause Analysis

### Architectural Context

The Tuya integration is designed as **`cloud_push`** (per `manifest.json` IoT class). The data flow is:

1. **Initial setup**: `manager.update_device_cache()` in `DeviceListener.initialize()` fetches all device states from Tuya cloud
2. **MQTT subscription**: `manager.refresh_mq()` subscribes to MQTT topics for real-time push updates
3. **Push updates**: When Tuya cloud sends a push, `DeviceListener.update_device()` dispatches via signal → `TuyaEntity._handle_state_update()` → `async_write_ha_state()`
4. **No polling**: `_attr_should_poll = False` in `TuyaEntity` — entities never proactively fetch updates

### Likely Root Cause(s)

**Primary**: **Battery-powered sensors (like liquid level sensors) do not push state changes to Tuya cloud in real-time.** The sensor sleeps to conserve battery and only wakes periodically to report data. When it does report, it may go to the Tuya cloud but not trigger an MQTT push event. This is a well-known limitation of battery-powered IoT devices.

**Secondary possibilities**:
1. MQTT connection may drop and not reconnect properly (Tuya's MQTT is known to be flaky)
2. The specific DP codes for liquid level (`LIQUID_LEVEL_PERCENT`, `LIQUID_DEPTH`, `LIQUID_STATE`) may not be included in the push event payload
3. The device may only update via cloud polling (Smart Life app triggers a poll when opened)

**Historical pattern**: This exact issue has been reported many times:
- #65758 (2022): "Tuya - no status update after changing a switch state"
- #88133 (2023): "Home Assistant updates sensor energy, voltage status of Smart Plug only when Tuya smartphone App is started"
- PR #74640 (2022): "Fix smart energy polling for Tuya plugs" — a previous attempt to add polling

### What's Missing
There is **no periodic polling fallback** in the integration. The `tuya_sharing` library (via `tuya-device-sharing-sdk`) provides:
- `manager.update_device_cache()` — fetches all device states from cloud (used only during init)
- `manager.refresh_mq()` — refreshes MQTT connection

But neither is called periodically. There is no `DataUpdateCoordinator` or scheduled update mechanism.

---

## 3. Comments & Discussion

| # | Author | Date | Summary |
|---|--------|------|---------|
| 1 | home-assistant[bot] | 2026-05-16 04:30 | Bot: Labeled `integration: tuya`, pinged code owners @Tuya, @zlinoliver |
| 2 | epenet (contributor) | 2026-05-16 04:33 | Asked for logs/diagnostics. Stated *"Polling should not be needed... data should be pushed over automatically. It may be that the problem is specific to your device (maybe unrecognised push data)"* |

**Key takeaway**: The contributor suggests this may be device-specific rather than a general integration flaw. No fix has been proposed or discussed.

---

## 4. Competition Analysis

| Factor | Status |
|--------|--------|
| **Assignees** | **0** — completely unassigned |
| **Comments from maintainers** | 1 — epenet requested diagnostics (no fix discussion) |
| **Linked PRs** | **0** — no one has submitted a fix |
| **Code owners** | @Tuya (org), @zlinoliver — neither has responded |
| **Age** | **< 12 hours** (created May 16 2026) — extremely fresh |
| **Cross-references** | Several historical issues (#65758, #88133) and PR #74640 show this is a known pain point |

**Verdict**: 🟢 **No active competition**. No PRs, no assignees. But the issue is still in "diagnostic collection" phase — the root cause is not yet confirmed.

---

## 5. Complexity Analysis

### Technical Depth: MEDIUM-HARD

**What would need to change**:

This is significantly more complex than a 1-line fix. The solution would likely involve one of these approaches:

#### Option A: Add periodic cloud polling (Coordinator pattern)
- Add a `DataUpdateCoordinator` with a configurable `scan_interval` (or a fixed one like 5-10 minutes)
- Periodically call `manager.update_device_cache()` to refresh device states from Tuya cloud
- Diff entities and dispatch updates for changed data
- **Files affected**: `coordinator.py`, `entity.py`, `__init__.py`
- **~30-80 lines of new code**
- **Pro**: Proper HA pattern; addresses root cause broadly
- **Con**: Increases Tuya API calls; may hit rate limits; needs careful design

#### Option B: Add a `_async_update` method (simpler poll fallback)
- Override `async_update()` in `TuyaEntity` to call `manager.update_device_cache()` selectively
- Change `_attr_should_poll` to `True` with a conservative `scan_interval`
- **Files affected**: `entity.py`
- **~10-20 lines**
- **Pro**: Simpler, uses built-in entity polling
- **Con**: Could flood Tuya API if many devices; doesn't batch updates

#### Option C: Fix MQTT push reliability (upstream fix)
- The `tuya-sharing` library's MQTT implementation may need fixes
- Could involve reconnection logic, keepalive, or subscribing to additional topics
- **Files affected**: Possibly none in HA core (upstream library change)
- **Pro**: Fixes root cause (push should work)
- **Con**: Not in HA control; requires upstream `tuya-device-sharing-sdk` change

### Key Challenge: Device-Specific vs General
The contributor suspects this is device-specific. Adding blanket polling for all devices would be wasteful. A targeted approach (configurable polling per device or per category) would be more appropriate but adds complexity.

### Testing
- Requires actual Tuya devices to test (MQTT push vs cloud poll)
- A liquid level/battery-powered sensor is ideal but may be hard to mock
- Could potentially test with unit tests mocking the `Manager` class

### AI Feasibility
- ⚠️ **Medium** — The root cause is understood but not 100% confirmed
- ⚠️ Fix is moderate complexity (10-80 lines, not 1-3)
- ⚠️ Requires understanding of Tuya cloud API, MQTT, and HA coordinator pattern
- ❌ Cannot be verified without Tuya device or comprehensive mocking

---

## 6. Bounty / Sponsor Analysis

| Aspect | Status |
|--------|--------|
| **GitHub Sponsors** | Home Assistant is under Open Home Foundation. No direct bounty on this issue. |
| **Labels** | No bounty/sponsor labels applied |
| **Bug Bounty Program** | Home Assistant does NOT have a formal bug bounty program |
| **Sponsor-backed Issues** | Rare, unofficial, typically ~$100 |
| **Expected Bounty** | **$0** — No monetary bounty confirmed |

**Verdict**: ❌ No confirmed bounty/sponsor. Home Assistant has no formal bounty program.

---

## 7. Opportunity Scoring

| Dimension | Weight | Score (1-10) | Weighted |
|-----------|--------|--------------|----------|
| Payment Certainty | 26% | 0 | 0.00 |
| Verifiability | 22% | 4 | 0.88 |
| AI Suitability | 18% | 5 | 0.90 |
| Maintainer Activity | 12% | 6 | 0.72 |
| Context Reuse | 7% | 6 | 0.42 |
| Competition Intensity | 15% | 8 | 1.20 |
| **TOTAL** | **100%** | | **4.12** |

### Breakdown

**Payment Certainty: 0/10**
- Same as all HA issues — no formal bounty program, no sponsor attached

**Verifiability: 4/10**
- No logs or diagnostics provided (contributor asked but none given yet)
- No traceback or error message
- Root cause is uncertain (device-specific? MQTT? missing DP code?)
- Cannot reproduce without a Tuya liquid level sensor
- Historical pattern suggests this is a known but unresolved pain point

**AI Suitability: 5/10**
- Python, familiar patterns (coordinator, entity update)
- But root cause not fully confirmed — needs human investigation first
- Fix would be moderate complexity (10-80 lines)
- Testing requires real hardware
- Could write the solution based on coordinator pattern but verification is impossible

**Maintainer Activity: 6/10**
- Home Assistant is very active
- Tuya integration has dedicated code owners (@Tuya org, @zlinoliver)
- BUT: neither has responded yet; contributor asked for more info
- Previous attempts (PR #74640) were merged but didn't fully solve it

**Context Reuse: 6/10**
- Knowledge of Tuya cloud API and MQTT patterns is somewhat reusable
- Coordinator pattern knowledge is highly reusable
- But this is quite Tuya-specific

**Competition Intensity: 8/10**
- Zero competition currently (no assignees, no PRs)
- BUT: the issue is still in triage phase with no confirmed root cause
- Several historical attempts suggest others have tried and hit complexity walls
- The issue may stall if user doesn't provide diagnostics

---

## 8. Recommendation

### ❌ **NOT RECOMMENDED for immediate action**

This issue is different from #170846 in several critical ways:

1. **No confirmed root cause** — The contributor suspects it's device-specific. Without diagnostics, any fix is speculative.
2. **Higher complexity** — Not a 1-3 line fix. Would require architecting a polling mechanism into a push-based integration.
3. **Historical precedent** — Similar issues have been reported for years. PR #74640 tried to address this in 2022 but only covered "smart energy" polling, not general state polling.
4. **Verification impossible** — Cannot test without Tuya hardware or comprehensive mock setup.
5. **Push vs Poll design tension** — The integration is intentionally `cloud_push`. Adding polling is a design change that maintainers may not accept without strong justification.

### When to Revisit
- If the user provides diagnostics confirming the device doesn't push updates
- If the contributor/maintainers agree that polling is an acceptable fallback
- If a Tuya device becomes available for testing
- If the issue gains traction (more 👍 reactions, more comments)

### What Would Be Needed for a Fix
```python
# In coordinator.py, add periodic polling via DataUpdateCoordinator
class TuyaPollingCoordinator(DataUpdateCoordinator):
    """Poll Tuya cloud for device updates."""
    
    async def _async_update_data(self):
        """Fetch device data from Tuya cloud."""
        await self.hass.async_add_executor_job(
            self.manager.update_device_cache
        )
        # Compare with cached state and dispatch updates
        ...
```

### Alternative: Feature Request Instead of Bug Fix
This may better be framed as a **feature request** (configurable polling interval) rather than a bug fix, since the push design is intentional.

---

## 9. Summary

```
Issue:            home-assistant/core#170868 — Tuya cloud push updates not received for 
                  battery-powered liquid level sensor
Bounty:           ❌ $0 (no confirmed bounty/sponsor)
Competition:      🟢 Zero (0 assignees, 0 PRs, <12h old)
Complexity:       🟡 Medium-Hard (10-80 lines in multiple files, or upstream library fix)
AI Feasibility:   ⚠️ Medium (root cause unconfirmed, no diagnostics, can't test)
Payment Certainty: ❌ None
Reputation Value: ⚠️ Moderate (but risk of incomplete fix due to device-specific nature)
Recommendation:   ❌ Skip for now — wait for diagnostics and maintainer guidance
```

**Final Verdict**: ⭐ (for reputation building, with significant risk) / ❌ (for bounty hunting)

### Next Actions (if pursued)
1. Ask user for debug logs and diagnostics (`epenet` already requested this)
2. Wait for code owners (@Tuya, @zlinoliver) to confirm device-specific vs general issue
3. If confirmed general: implement `DataUpdateCoordinator`-based periodic polling in `coordinator.py`
4. If device-specific: investigate DP code mappings for YWCGQ category liquid level sensors
