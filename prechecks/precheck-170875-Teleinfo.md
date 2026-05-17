# Pre-check Analysis: home-assistant/core#170875

## Meta
| Field | Value |
|-------|-------|
| Issue | https://github.com/home-assistant/core/issues/170875 |
| Title | Teleinfo integration breaking serial port on HA startup |
| Labels | integration: teleinfo |
| State | Open |
| Bounty | $100 sponsor |
| Score | 56.4 |
| Created | 2026-05-16 |
| Related | #170078 (duplicate), zigbee2mqtt#31927 |

## Summary

The Teleinfo integration (added in HA 2026.5.0) aggressively probes every USB serial port matching VID=10C4 PID=EA60 (CP2102N) or VID=0403 PID=6015 (FTDI) on every Home Assistant startup. This opens the serial port with pyserial and attempts to read a Teleinfo frame, which disrupts other integrations and add-ons (Zigbee2MQTT, RFXtrx, etc.) already using that device.

## Root Cause

**Primary cause**: The teleinfo integration's `manifest.json` declares two USB matchers with overly generic VID/PID combinations:

```json
"usb": [
    {"pid": "6015", "vid": "0403"},   // FTDI FT232 — widely used
    {"pid": "EA60", "vid": "10C4"}    // CP2102N — extremely common USB-to-serial chip
]
```

When HA starts, the USB discovery subsystem fires `async_step_usb` for every connected device matching these matchers. The config flow's `async_step_usb` method calls `_validate_serial_port()`, which executes `teleinfo.read_frame(serial_port)` from the `pyteleinfo` library.

**What `read_frame` does**: Opens the serial port with pyserial at 1200 baud, 7 data bits, even parity, 1 stop bit, with RTS/CTS flow control enabled, and a 5-second timeout. It then attempts to read a Teleinfo frame (STX/ETX delimited) from the port. If the device is not a Teleinfo meter, it times out after 5 seconds.

**The impact**: Simply opening the serial port with pyserial — especially with different baud rate / parity settings than what the target device expects — can:
- Disrupt active serial communication for other integrations
- Cause Zigbee coordinators, RFXtrx, and other serial devices to lose their connection
- Force users to restart their add-ons or even HA again

## Modification Scope

### Change 1: `homeassistant/components/teleinfo/config_flow.py`
**Type**: Core fix (mandatory)

**Problem**: `async_step_usb` eagerly probes any discovered USB device by opening the serial port and calling `read_frame()` before the user has confirmed they want to set up the integration. This is the primary source of disruption.

**Required fix options** (choose one):

**Option A (recommended)**: Remove the probing from `async_step_usb`. Instead, match on additional USB descriptor fields (manufacturer, product string, serial number prefix known for Teleinfo hardware) in `manifest.json` if possible. If not, change the flow to only show the discovery notification without opening the port, and defer the validation probe to `async_step_usb_confirm` (only after the user explicitly clicks "Set up").

**Option B**: Keep probing but significantly reduce the timeout (e.g., 1 second instead of 5) and ensure the serial port is cleaned up even more aggressively. However, this is a band-aid — even a brief open+close with mismatched serial settings can disrupt some devices.

**Option C**: Add a `usb` dependency filter in `async_step_usb` that checks manufacturer/description strings from `UsbServiceInfo` before probing. Look for known Teleinfo USB adapter identifiers (e.g., manufacturer containing "Enedis" or specific product strings).

**Lines changed**: ~15–30 lines (core change), plus error handling improvements.

### Change 2: `homeassistant/components/teleinfo/manifest.json`
**Type**: Mitigation (recommended)

**Problem**: The USB matchers are too broad. VID=10C4 PID=EA60 matches *any* CP2102N-based device (Zigbee coordinators, GPS receivers, Arduino clones, countless others).

**Required fix**: Narrow down the USB matchers by adding `manufacturer` and/or `description` fields if the Teleinfo hardware has identifiable strings. Otherwise, this file may need a comment or the matchers may need to be removed entirely (forcing users to configure serial port manually).

**Lines changed**: ~5–10 lines.

### Change 3: `homeassistant/components/teleinfo/strings.json`
**Type**: Optional (if new error/abort messages are needed)

**Problem**: If the flow changes to defer validation, new user-facing strings may be needed.

**Lines changed**: ~5 lines (if needed).

## Estimated Implementation Effort

| Aspect | Estimate |
|--------|----------|
| Lines of code changed | ~20–50 across 2–3 files |
| New tests needed | Yes — config flow tests for USB discovery path |
| Test files | `tests/components/teleinfo/test_config_flow.py` |
| Complexity | Low–Medium — standard HA config flow pattern |
| Review time | Medium — needs core contributor familiar with USB discovery |

## Can an AI Agent Safely Implement This?

**Verdict**: Yes, with caveats.

**Feasibility**: The fix follows well-established HA patterns. The config flow needs to be adjusted so that USB discovery does not probe the serial port eagerly. There are multiple existing examples in the codebase (e.g., integrations that defer probing to user confirmation step).

**Challenges**:
1. **Understanding the Teleinfo hardware**: To properly narrow USB matchers, the developer needs to know what USB descriptors actual Teleinfo hardware exposes. This may require asking on the issue or researching French Teleinfo hardware.
2. **Testing**: The fix must be tested both for the bug (non-Teleinfo device is not disrupted) and for the happy path (real Teleinfo device is still discoverable). The AI would need to understand how to write/update the config flow tests.
3. **The `pyteleinfo` dependency**: The `read_frame` function is synchronous and runs in the executor thread. This is already handled correctly in the current code, but any new code must maintain this pattern.

**Recommended approach for AI implementation**:
1. Change `async_step_usb` to *not* call `_validate_serial_port`. Instead, just present the discovered device to the user for confirmation (similar to many other integrations).
2. Move the validation probe into `async_step_usb_confirm` so it only runs after the user explicitly clicks "Set up".
3. If validation fails at confirm step, show an appropriate error message instead of silently aborting.
4. Keep the manual `async_step_user` path unchanged.

## Risks and Unknowns

| Risk | Severity | Mitigation |
|------|----------|------------|
| Breaking legitimate Teleinfo discovery | High | Need real Teleinfo hardware or reliable test data; check with @esciara (code owner, who commented they'll look at it) |
| Not all Teleinfo hardware uses the same descriptors | Medium | If USB descriptors vary, the manual config path must remain as a fallback |
| The code owner @esciara already said "Will have a look today and post a fix asap" | Low | The bounty is available but the owner may submit a PR first. Check if a PR has been opened before starting work. |
| Non-obvious interaction with other serial subsystems | Medium | Changes should be tested with at least one other serial integration running |

## Recommendation

**Worth implementing**: Yes. The issue is clear, the root cause is well understood, and the fix is relatively contained. The $100 sponsor bounty adds incentive.

**Priority actions**:
1. Monitor if @esciara submits a PR (they commented they'd look at it on May 16)
2. If no PR within a few days, proceed with implementing Option A (defer probing to user confirmation step)
3. Add config flow tests that verify USB discovery doesn't open serial ports proactively

## References

- Issue: https://github.com/home-assistant/core/issues/170875
- Related issue: https://github.com/home-assistant/core/issues/170078
- Related issue: https://github.com/Koenkk/zigbee2mqtt/issues/31927
- Code comment by @elupus pointing to config_flow.py line 94: https://github.com/home-assistant/core/issues/170875#issuecomment-4466441076
- Teleinfo source directory: https://github.com/home-assistant/core/tree/dev/homeassistant/components/teleinfo
- pyteleinfo library: https://github.com/esciara/pyteleinfo
- USB discovery service info: `homeassistant/helpers/service_info/usb.py`
