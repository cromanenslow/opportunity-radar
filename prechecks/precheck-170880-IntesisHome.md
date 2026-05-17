# Pre-check Analysis: home-assistant/core#170880

## Meta
| Field | Value |
|-------|-------|
| Issue | https://github.com/home-assistant/core/issues/170880 |
| Title | The IntesisHome integration stopped working |
| Labels | (none) |
| State | Open |
| Bounty | $100 sponsor |
| Created | 2026-05-16 |
| Score | 56.4 |

## Issue Summary
The IntesisHome integration stopped working in HA 2026.5.2 (works in 2026.5.1). The user reports a "compilation error" in the logs but lost the logs after reverting. The suspected cause is PR #170382, which bumped the `pyintesishome` dependency from 1.8.0 to 1.8.7.

## Root Cause Analysis

### Primary suspect: `pyintesishome` library bump (1.8.0 → 1.8.7)

The library was **significantly restructured** between 1.8.0 and 1.8.7:

| Change | 1.8.0 | 1.8.7 |
|--------|-------|-------|
| Module structure | Single `pyintesishome.py` (removed) | Split into `intesisbase.py`, `intesishome.py`, `intesisbox.py`, `intesishomelocal.py` |
| Class hierarchy | `IntesisHomeBase` (self-contained) | `IntesisBase` (base) → `IntesisHome` (cloud, inherits) |
| Exceptions | `IHAuthenticationError`, `IHConnectionError` | Same (still exported) |
| Constructor signature | `(username, password, loop=None, websession=None, device_type=...)` | Same |
| Public methods | All methods used by HA | All present and API-compatible |

### Detailed behavioral differences between 1.8.0 and 1.8.7

After exhaustive comparison, the public API is **nominally backwards compatible** — all classes, methods, and signatures that HA relies on are present. However, there are **subtle behavioral changes** that could cause runtime failures:

1. **`connect()` method order change** (`intesishome.py`):
   - 1.8.0: send auth message → clear token → create receive task
   - 1.8.7: create receive task → send auth message → clear token
   - The receive task is now created BEFORE sending the auth message. This ensures responses aren't missed, but changes the timing.

2. **`_send_command()` timeout mechanism change** (`intesisbase.py`):
   - 1.8.0/1.8.5: Used `asyncio.wait_for(self._received_response.wait(), timeout=5.0)`
   - 1.8.7: Polling loop with `asyncio.sleep(0.1)` checking `_received_response.is_set()`
   - The new polling loop might behave differently under heavy load or fast responses.

3. **`_connected` flag placement change** (`intesishome.py`):
   - 1.8.0: `self._connected = False` was always set after the `try/except` block
   - 1.8.7: `self._connected = False` is set only inside the `except` block
   - **This is a behavioral change**: in 1.8.7, if `connect()` succeeds, `_connected` is left at its initial value (`False`) until the `connect_rsp` response is parsed. If the response arrives asynchronously, there's a window where `is_connected` returns `False` unexpectedly.

4. **`poll_status()` safety guards** (`intesishome.py`):
   - 1.8.0: `for installation in config.get("inst"):` — crashes if `inst` is missing/`None`
   - 1.8.7: `for installation in config.get("inst") or []:` — safe
   - The old code would throw `TypeError: 'NoneType' object is not iterable` if the API response lacked the `inst` field. The new code silently skips.

5. **Falsy-value bug fixes** (`intesisbase.py`):
   - Methods like `get_setpoint()`, `get_temperature()`, `get_outdoor_temperature()`, `get_max_setpoint()`, `get_min_setpoint()` changed from `if X:` to `if X is not None:`
   - **This means: when the value is `0` or `0.0`, the old code treated it as falsy and returned the raw value without dividing by 10. The new code correctly divides by 10.** This is a behavior change for devices reporting 0.0°C temperatures or 0° setpoints.

6. **`set_fan_speed()` now has early returns** (`intesisbase.py`):
   - If `fan_map` is not a dict or the fan speed is unknown, the method silently returns without setting anything.
   - Previously, it would crash with `AttributeError` or `KeyError`.

7. **`keepalive` interval changed** (`intesishome.py`):
   - 1.8.0: 240 seconds
   - 1.8.7: 120 seconds
   - More frequent keepalives might interact with rate limiting or connection stability.

### What "compilation error" likely means

In HA context, a "compilation error" during integration loading is most likely:
- **An `ImportError`** if the `pyintesishome` package structure didn't load correctly
- **A `TypeError`** during `async_setup_platform()` if the library's constructor or method behavior changed
- **An `AttributeError`** if a method or property changed behavior

The most plausible scenario: the constructor `IntesisHome(ih_user, ih_pass, hass.loop, websession=..., device_type=...)` triggers `connect()` → `poll_status()` internally at some point, and a `TypeError` or `KeyError` from the API response handling cascades up as what the user sees as a "compilation error."

### Risk assessment

| Factor | Assessment |
|--------|------------|
| **Is the cause identifiable?** | Yes — the library bump is the only change. The exact error needs reproduction. |
| **Can an AI agent implement safely?** | Yes, but **requires careful testing**. The fix may involve either (a) adapting HA's code to the new library behavior, or (b) fixing the pyintesishome library if a bug is found. Option (b) is riskier. |
| **Testing complexity** | Moderate-high. Requires an IntesisHome device or mocked API to test. No unit tests exist for the HA integration. |
| **Risk of regression** | Low-to-moderate, if changes are isolated to the intesishome component. |

## Modification Scope

### Change 1: `homeassistant/components/intesishome/climate.py`
**Description:**
The HA integration code needs to be reviewed and potentially adapted for subtle behavioral differences in pyintesishome 1.8.7. There are two potential approaches:

**Approach A (Safer — pin to working version):**
Downgrade the dependency from `pyintesishome==1.8.7` back to `pyintesishome==1.8.0` (or 1.8.5) in `manifest.json` and `requirements_all.txt`. This restores the working state while investigation continues.

**Approach B (Proper fix — adapt to 1.8.7):**
- Review the `async_setup_platform()` flow for any assumptions about library behavior that changed
- The constructor call `IntesisHome(ih_user, ih_pass, hass.loop, websession=..., device_type=...)` is compatible
- `poll_status()` behavior: the new code handles missing `inst` gracefully (was crashing before), so this is an improvement
- No method signature changes needed in the HA code
- The `_connected` flag behavior change in 1.8.7's `connect()` should be verified — if `is_connected` returns `False` incorrectly, the HA integration's `async_update_callback` reconnection logic might malfunction

**Estimated LOC:** 2-15 lines (minor adjustments to HA code, if any) OR 2 lines (revert version pin)

### Change 2: `homeassistant/components/intesishome/manifest.json`
**Description:**
If Approach A is chosen: change `"requirements": ["pyintesishome==1.8.7"]` back to `"requirements": ["pyintesishome==1.8.0"]`.

If Approach B: no change needed (already at 1.8.7).

**Estimated LOC:** 1 line

### Change 3: `requirements_all.txt`
**Description:**
If Approach A is chosen: change `pyintesishome==1.8.7` back to `pyintesishome==1.8.0`.

If Approach B: no change needed.

**Estimated LOC:** 1 line

## Recommended Action

**Approach A (Revert)** is the safest short-term fix to restore functionality. The true root cause needs more investigation — ideally with actual error logs from the reporter. The pyintesishome library maintainer (@jnimmo, also the HA codeowner) should be looped in to investigate the 1.8.7 behavioral issues.

**Approach B (Adapt)** is possible but risky without being able to reproduce the error. Key areas to examine:
1. The `_connected` flag timing in `IntesisHome.connect()` 
2. The `_send_command()` timeout polling mechanism
3. Any `KeyError` or `AttributeError` from the restructured `__init__.py` exports

## Verification

After any change, the following should be verified:
1. `from pyintesishome import IntesisHome, IHAuthenticationError, IHConnectionError` works without errors
2. `IntesisHome(username, password, loop, websession, device_type)` construction succeeds
3. `controller.poll_status()` returns device data correctly
4. `controller.connect()` establishes connection without timeout
5. Integration starts and climate entities appear in HA
6. Temperature reading, mode setting, fan speed, and swing operations work end-to-end
7. Reconnection after connection loss works

## Files Referenced
- `homeassistant/components/intesishome/__init__.py` — minimal, just docstring
- `homeassistant/components/intesishome/climate.py` — main integration logic (imports `IntesisHome` from `pyintesishome`)
- `homeassistant/components/intesishome/manifest.json` — dependency version pin
- `requirements_all.txt` — global dependency version pin
- `pyintesishome` library (external): `__init__.py`, `intesisbase.py`, `intesishome.py`, `const.py`
