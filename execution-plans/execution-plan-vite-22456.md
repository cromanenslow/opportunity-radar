# Execution Plan: vitejs/vite#22456 — Docs URL Fix (pnpm overrides)

**Bounty**: $100 sponsor bounty  
**Issue**: https://github.com/vitejs/vite/issues/22456  
**Repo**: vitejs/vite (71k+ ⭐)  
**Labels**: `documentation`  
**Difficulty**: ★☆☆☆☆ (15–25 min)  
**Status**: 🟢 Ready to execute

---

## 1. Problem Summary

The docs page at `https://vite.dev/guide/#using-unreleased-commits` contains a tip that links to pnpm overrides documentation:

```
::: tip Dependencies using Vite
To replace the Vite version used by dependencies transitively, you should use
[npm overrides](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#overrides) or
[pnpm overrides](https://pnpm.io/9.x/package_json#pnpmoverrides).
:::
```

The pnpm URL `https://pnpm.io/9.x/package_json#pnpmoverrides` **redirects (HTTP 308)** to `https://pnpm.io/package_json` which drops the anchor — the `#pnpmoverrides` section no longer exists on the new page. In pnpm 11.x, overrides documentation moved to `https://pnpm.io/settings#overrides`.

**Maintainer direction** (from [bluwy's comment](https://github.com/vitejs/vite/issues/22456#issuecomment-4466534595)):
> "I don't know if we should still be updating the old docs, especially that rolldown-vite shouldn't be used directly now. But we should update the link for 'pnpm overrides' here though: https://vite.dev/guide/#using-unreleased-commits"

---

## 2. Environment Setup

```bash
# Clone the repo
cd /Users/tao
git clone git@github.com:vitejs/vite.git
cd vite

# Install dependencies (pnpm required)
pnpm install

# Verify docs build (optional but recommended)
pnpm run docs-build  # or `pnpm run docs` for dev server
```

**Prerequisites:**
- Node.js ≥ 20.19+ or 22.12+
- pnpm (latest) — install via `npm i -g pnpm` if needed
- A GitHub account with CLA signed for vitejs/vite
- Git configured with your user.name and user.email

---

## 3. Problem Location

| Item | Value |
|------|-------|
| **File** | `docs/guide/index.md` |
| **Section** | "Using Unreleased Commits" |
| **Line** | ~360 (near the bottom of the file) |
| **Content to change** | The tip block at the end of the section |

**Current content:**
```markdown
::: tip Dependencies using Vite
To replace the Vite version used by dependencies transitively, you should use [npm overrides](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#overrides) or [pnpm overrides](https://pnpm.io/9.x/package_json#pnpmoverrides).
:::
```

**Verification commands:**
```bash
# Find the exact line
grep -n "pnpm.io" docs/guide/index.md
# Output should show the line with the old URL
```

---

## 4. Fix Details

### Change

Update the pnpm overrides URL from:
```
https://pnpm.io/9.x/package_json#pnpmoverrides
```
to:
```
https://pnpm.io/settings#overrides
```

### Why this URL?

| Evidence | Detail |
|----------|--------|
| Old URL | `https://pnpm.io/9.x/package_json#pnpmoverrides` → HTTP 308 redirects to `/package_json` |
| Redirect target | `https://pnpm.io/package_json` — no longer has the `overrides` section |
| New location | `https://pnpm.io/settings#overrides` — confirmed to contain full overrides documentation with YAML examples for `pnpm-workspace.yaml` |
| Why updated | pnpm restructured their docs for v11.x; the settings page is now the canonical location for all config including overrides |

### Exact diff

```diff
- [pnpm overrides](https://pnpm.io/9.x/package_json#pnpmoverrides)
+ [pnpm overrides](https://pnpm.io/settings#overrides)
```

### What NOT to change

- The issue author also suggests updating the rolldown-vite section to use `pnpm-workspace.yaml` instead of `package.json` for overrides — **skip this** per maintainer direction.
- Do **not** change the npm overrides URL (still valid).
- Do **not** change any other content in the file.

---

## 5. Testing & Verification

### Method 1: Visual inspection (quick)
```bash
grep -n "pnpm.io" docs/guide/index.md
# Verify the URL is now https://pnpm.io/settings#overrides
```

### Method 2: Docs build (thorough)
```bash
# Build the docs site locally
pnpm run docs-build

# If there's a dev server:
pnpm run docs
# Open http://localhost:4173/guide/#using-unreleased-commits
# Scroll to the tip and click the link — should go to pnpm.io/settings#overrides
```

### Method 3: Validate link is live
```bash
curl -sI "https://pnpm.io/settings#overrides" | head -5
# Should return HTTP/2 200
```

---

## 6. PR Submission

### Branch
```bash
git checkout -b fix/pnpm-overrides-url
```

### Commit message
```
docs: update pnpm overrides URL link (#22456)

The old URL (pnpm.io/9.x/package_json#pnpmoverrides) now redirects
and the anchor no longer exists. Updated to the new canonical location
at pnpm.io/settings#overrides.

Closes #22456
```

### PR requirements for vitejs/vite
- [ ] **CLA**: Sign the [Vite Contributor License Agreement](https://cla.github.com/vitejs/vite) — required before PR can be merged
- [ ] **PR template**: No specific template required for docs-only PRs
- [ ] **Title**: `docs: update pnpm overrides URL link`
- [ ] **Description**: Brief explanation referencing the issue
- [ ] **Reviews**: May need 1 maintainer approval (typically @bluwy or @patak-dev)

### Push
```bash
git add docs/guide/index.md
git commit -m "docs: update pnpm overrides URL link (#22456)

The old URL (pnpm.io/9.x/package_json#pnpmoverrides) now redirects
and the anchor no longer exists. Updated to the new canonical location
at pnpm.io/settings#overrides.

Closes #22456"
git push origin fix/pnpm-overrides-url
```

### PR body template
```markdown
## Description

Updates the pnpm overrides documentation link in the "Using Unreleased Commits"
section. The old URL `https://pnpm.io/9.x/package_json#pnpmoverrides` now
redirects and the anchor fragment is lost. The correct new URL is
`https://pnpm.io/settings#overrides`.

Fixes #22456

## Changes
- Updated pnpm overrides URL in `docs/guide/index.md`
```

---

## 7. Time Estimate

| Step | Duration |
|------|----------|
| Clone repo + install deps | 5 min |
| Locate the exact line | 2 min |
| Apply the fix | 1 min |
| Build & verify | 3 min |
| Create branch & PR | 3 min |
| **Total** | **~15 min** |

---

## 8. Risks & Contingency

| Risk | Mitigation |
|------|------------|
| pnpm moves the overrides URL again | Check `https://pnpm.io/settings#overrides` is still live before PR |
| PR gets rejected as "too trivial" | It's a legitimate docs fix; maintainer explicitly requested it in the issue comments |
| CLA signing issues | Sign ahead of time: https://cla.github.com/vitejs/vite |
| Merge conflicts with other docs changes | Rebase on latest `main` branch before pushing |

---

## 9. Post-Merge Checklist

- [ ] Verify the link is updated on the live site (vite.dev) after deploy
- [ ] Comment on the issue: "Fixed in PR #[number]"
- [ ] If this is a sponsored bounty, confirm payout via the sponsor platform
