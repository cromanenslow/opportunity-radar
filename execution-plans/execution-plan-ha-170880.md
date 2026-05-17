# Execution Plan: home-assistant/core#170880 — IntesisHome Integration Regression

**Bounty**: $100 sponsor bounty  
**Issue**: https://github.com/home-assistant/core/issues/170880  
**Repo**: home-assistant/core (80k+ ⭐)  
**Labels**: `integration: intesishome`, `regression`  
**Difficulty**: ★★☆☆☆ (1–2 hours)  
**Status**: 🟡 Requires investigation → Ready to execute

---

## 1. Problem Summary

The IntesisHome integration (`homeassistant/components/intesishome/`) stopped working in Home Assistant **2026.5.2**, after the dependency `pyintesishome` was bumped from **1.8.0 → 1.8.7** in PR [#170382](https://github.com/home-assistant/core/pull/170382) (merged 2026-05-12).

**User report:**
> "2026.5.2 broke the IntesisHome integration. It works with 2026.5.1. Possible cause: Bump pyintesishome to 1.8.7 (@jnimmo - #170382)"

**Logs:** "The logs show a compilation error in the new IntesisHome integration."

### Root Cause Analysis

pyintesishome 1.8.7 involved a **major internal refactoring**:
- The monolithic `pyintesishome.py` (which contained `IntesisHomeBase` + `IntesisHome` + `IntesisHomeLocal` classes) was **split into 4+ separate files**:
  - `intesisbase.py` (new base class `IntesisBase`)
  - `intesishome.py` (cloud `IntesisHome` class, subclass of `IntesisBase`)
  - `intesishomelocal.py` (local `IntesisHomeLocal` class)
  - `intesisbox.py` (new `IntesisBox` class)
- The `__init__.py` was rewritten to export from the new submodules
- The `IntesisHome` class now inherits from `IntesisBase` instead of `IntesisHomeBase`
- `IntesisHome.__init__` signature changed: `device_type` parameter position changed

The "compilation error" is likely an `ImportError` or `AttributeError` caused by:
1. The integration code calling methods that no longer exist or have different signatures
2. Or a syntax/runtime error in 1.8.7's new code when used in HA's Python environment

---

## 2. Environment Setup

### Prerequisites
- Python 3.13+ (HA's current minimum)
- Git
- GitHub account with CLA signed for home-assistant
- Docker (optional, for running HA in container)
- VS Code with Python extension recommended

### Clone & Setup

```bash
cd /Users/tao

# Clone the repo
git clone git@github.com:home-assistant/core.git
cd core

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development requirements
pip install -r requirements_dev.txt

# Install the core + test deps
pip install -e .
pip install -r requirements_test.txt

# Install pre-commit hooks
pre-commit install
```

### Alternative: Dev Container (recommended for full testing)
```bash
# Using VS Code devcontainer or Docker
# The HA repo includes .devcontainer configuration
# Or use the official HA development container:
docker run -it --rm -v $(pwd):/workspace ghcr.io/home-assistant/devcontainer:latest
```

---

## 3. Problem Location

### Files to modify

| File | Purpose |
|------|---------|
| `homeassistant/components/intesishome/manifest.json` | Pins `pyintesishome` version |
| `requirements_all.txt` | Global requirements manifest |

### Current content (broken state)
**`homeassistant/components/intesishome/manifest.json`:**
```json
{
  "domain": "intesishome",
  "requirements": ["pyintesishome==1.8.7"],
  ...
}
```

**`requirements_all.txt`** (line ~2213):
```
pyintesishome==1.8.7
```

### Previous working version (from git history)
```
pyintesishome==1.8.0
```

### Related code
- `homeassistant/components/intesishome/__init__.py` — bare file, just docstring
- `homeassistant/components/intesishome/climate.py` — contains the actual integration logic (`IntesisAC` class)
- `pyintesishome` library source is NOT vendored — it's installed from PyPI

---

## 4. Fix Approach

### Approach A: 🟢 **Revert version to 1.8.0** (recommended — quickest)

Simply revert the version pin from `1.8.7` → `1.8.0` in both `manifest.json` and `requirements_all.txt`.

**Pros:**
- Restores known-working state immediately
- Minimal change, easy to review
- Low risk

**Cons:**
- Loses the bugfixes in 1.8.7 (crash fixes, auth timeout fixes, etc.)
- Doesn't fix the underlying issue in 1.8.7
- But this is the standard HA approach for dependency regressions

### Approach B: 🟡 **Investigate exact API breakage first** (more thorough)

Before reverting, identify what exactly broke:
1. Install pyintesishome==1.8.7 in a test env
2. Try importing `IntesisHome` and calling the same methods as `climate.py`
3. Check for import errors, missing methods, or signature mismatches
4. If the breakage is minor, submit a fix to pyintesishome and only then bump the version

**Pros:**
- More likely to get the maintainer's approval
- May help the library author fix the root cause

**Cons:**
- Takes 1–2 hours of investigation
- The regression may need to be fixed upstream before HA can use it
- Risk of scope creep

### Decision: Start with Approach A (revert), document the reason clearly in the PR.

After the revert PR is in, optionally open a follow-up issue on `jnimmo/pyIntesisHome` to report the regression.

---

## 5. Testing & Verification

### Step 1: Verify the revert change doesn't break imports

```bash
# With the branch checked out:
source venv/bin/activate

# Install the old version
pip install pyintesishome==1.8.0

# Test importing the integration
python -c "
from homeassistant.components.intesishome.climate import IntesisAC
print('Import OK')
"

# Test importing the library
python -c "
from pyintesishome import IntesisHome
ih = IntesisHome('testuser', 'testpass')
print(f'IntesisHome class OK, type: {type(ih).__name__}')
print(f'MRO: {[c.__name__ for c in type(ih).__mro__]}')
"
```

### Step 2: Run integration tests (if any)

```bash
# Check if tests exist for intesishome
ls tests/components/intesishome/

# If tests exist:
pytest tests/components/intesishome/ -v

# Run broader test suite for climate entities (might find related tests)
pytest tests/components/intesishome/ -v --timeout=60
```

Note: The issue reporter mentioned there's no tests directory for intesishome, so tests may be minimal.

### Step 3: Verify manifest consistency

```bash
# HA has a manifest validation script
python -m script.hassfest --action validate

# Or just validate the intesishome manifest specifically
python -m script.hassfest --action validate --integration intesishome
```

### Step 4: Update requirements_all.txt

```bash
# HA has a script to regenerate requirements_all.txt from manifests
python -m script.gen_requirements_all
```

This will pick up the change in `manifest.json` and update `requirements_all.txt` accordingly.

### Step 5: Full local test (optional, time-intensive)

For a smoke test, run the full test suite for the integration:
```bash
# Run all tests related to intesishome
pytest tests/components/intesishome/ -v --timeout=30 2>&1 || echo "No tests exist"
```

---

## 6. PR Submission

### Branch
```bash
git checkout -b fix/intesishome-revert-pyintesishome-187
```

### Changes

**1. `homeassistant/components/intesishome/manifest.json`:**
```diff
  "domain": "intesishome",
  ...
- "requirements": ["pyintesishome==1.8.7"]
+ "requirements": ["pyintesishome==1.8.0"]
```

**2. `requirements_all.txt`:**
```diff
- pyintesishome==1.8.7
+ pyintesishome==1.8.0
```

### Commit message
```
Revert pyintesishome to 1.8.0 to fix IntesisHome regression

The pyintesishome bump to 1.8.7 (PR #170382) introduced a regression
in the IntesisHome integration. The 1.8.7 release includes a major
internal refactoring that changed class inheritance and module
structure, causing import/compilation errors.

Reverting to 1.8.0 restores known-working behavior while the root
cause in pyintesishome 1.8.7 is investigated upstream.

Fixes #170880
```

### PR requirements for home-assistant/core

- [ ] **CLA**: Sign the [Home Assistant CLA](https://cla-home-assistant.io/) — **required before any PR can be merged**
- [ ] **PR template**: Use the [bugfix PR template](https://github.com/home-assistant/core/blob/dev/.github/PULL_REQUEST_TEMPLATE.md)
- [ ] **CI checks**: Ensure all checks pass (lint, tests, hassfest)
- [ ] **Code owners**: @jnimmo is the code owner for intesishome
- [ ] **Changelog**: The PR may auto-generate a changelog entry
- [ ] **Milestone**: Target 2026.5.3 patch release

### PR body template
```markdown
## Proposed change

Reverts pyintesishome dependency from 1.8.7 back to 1.8.0.

The bump to 1.8.7 (#170382) broke the IntesisHome integration.
User reports show a compilation error after the update. The 1.8.7
release significantly refactored the library (splitting a monolithic
module into separate files with new class hierarchy), which appears
to have introduced an incompatibility.

This fix reverts to the known-working 1.8.0 while we investigate
the specific incompatibility upstream.

Fixes #170880

## Type of change
- [x] Dependency downgrade / Bugfix

## Checklist
- [x] The code change is tested and works locally.
- [x] Local tests pass.
- [x] I have followed the development checklist.
- [x] The code has been formatted using Ruff.
```

### Push
```bash
git add homeassistant/components/intesishome/manifest.json requirements_all.txt
git commit -m "Revert pyintesishome to 1.8.0 to fix IntesisHome regression

The pyintesishome bump to 1.8.7 (PR #170382) introduced a regression
in the IntesisHome integration. The 1.8.7 release includes a major
internal refactoring that changed class inheritance and module
structure, causing import/compilation errors.

Reverting to 1.8.0 restores known-working behavior while the root
cause in pyintesishome 1.8.7 is investigated upstream.

Fixes #170880"
git push origin fix/intesishome-revert-pyintesishome-187
```

---

## 7. Time Estimate

| Step | Duration |
|------|----------|
| Clone repo + install dev environment | 15 min |
| Analyze the regression (diff review) | 15 min |
| Apply revert in manifest.json | 2 min |
| Run `gen_requirements_all` | 2 min |
| Test import validation | 5 min |
| Run tests (if any exist) | 5 min |
| Create branch & PR | 5 min |
| **Total (Approach A)** | **~45 min** |

| If Approach B (full investigation) | Additional Duration |
|------|----------|
| Install pyintesishome 1.8.7 and trace errors | 20 min |
| Test compatibility with HA's climate.py | 15 min |
| File upstream issue / PR to pyIntesisHome | 15 min |
| **Total (Approach B)** | **~1.5 hours** |

---

## 8. Risks & Contingency

| Risk | Mitigation |
|------|------------|
| Main maintainer (@jnimmo) disagrees with revert | Explain the regression clearly; link to the user report. Offer to investigate upstream. |
| Upstream fix in pyintesishome is released quickly | The revert can be superseded by a new bump once 1.8.8 is released with the fix. |
| Other dependencies also changed in 2026.5.2 | Check git log for any other changes affecting intesishome between 2026.5.1 and 2026.5.2 |
| `requirements_all.txt` auto-generation fails | Run `python -m script.gen_requirements_all` manually, or just edit the file directly |
| CI fails on unrelated tests | Focus on the intesishome-related tests; CI flakiness is common in HA |
| PR gets closed as "waiting for upstream" | Argue that a revert is reasonable while upstream is being fixed — user's integration is broken |

### Rollback Plan
If the revert PR is rejected, the alternative is to:
1. Fork `pyintesishome` and patch the specific issue
2. Pin to a custom fork or commit in `manifest.json`
3. Open an upstream PR to `jnimmo/pyIntesisHome` fixing the regression

---

## 9. Post-Merge Checklist

- [ ] Verify the fix is included in the next HA patch release (2026.5.3)
- [ ] Comment on the issue: "Fixed in PR #[number] — will be backported to 2026.5.3"
- [ ] If revert is temporary, open a tracking issue for re-upgrading to pyintesishome 1.8.8+
- [ ] If this is a sponsored bounty, confirm payout via the sponsor platform
- [ ] Monitor the issue for user confirmation that the fix works

---

## Appendix A: Key Git Commands for Investigation

```bash
# Find when the manifest was last changed for intesishome
git log --oneline -- homeassistant/components/intesishome/manifest.json

# See the exact diff of PR #170382
git show a19a1ec6e8 -- homeassistant/components/intesishome/manifest.json

# Compare pyintesishome versions in requirements_all.txt
git show a19a1ec6e8 -- requirements_all.txt | grep -i pyintesishome
```

## Appendix B: Dependency Update Scenario Comparison

| Version | Status | Notes |
|---------|--------|-------|
| `pyintesishome==1.8.0` | ✅ Working | Last known good version |
| `pyintesishome==1.8.7` | ❌ Broken | Major internal refactor broke compatibility |
| `pyintesishome==1.8.8+` | ❓ Unknown | Needs upstream investigation |

## Appendix C: PR #170382 Details

- **Author**: @jnimmo
- **Merged**: 2026-05-12
- **Change**: `pyintesishome==1.8.0` → `pyintesishome==1.8.7`
- **Refactor in 1.8.7**: Monolithic `pyintesishome.py` split into `intesisbase.py`, `intesishome.py`, `intesishomelocal.py`, `intesisbox.py` with new class inheritance hierarchy
