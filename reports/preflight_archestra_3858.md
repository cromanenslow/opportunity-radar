# Preflight Report: archestra-ai/archestra#3858 — Agent Template Catalog

**Date:** 2026-05-14
**Analyst:** Hermes Agent (Preflight Subagent)
**Bounty:** $450 (Algora, confirmed via `/bounty 450` command)
**Status:** ❌ ٔ弃 (Ðbandon)

---

## 1. Issue Overview

|Field| Value|
|---|---|
|**Title**| Agent template catalog |
|**Repository**| archestra-ai/archestra |
|**Issue #**| 3858 |
|**State**| OPEN |
|**Created**| 2026-04-16 |
|**Labels**| `💌 Bounty`, `$450`, `**Reserved for SE interview**` |
|**URL(*| [https://github.com/archestra-ai/archestra/issues/3858](https://github.com/archestra-ai/archestra/issues/3858) |

### Description (abridged)
> Add a quickstart catalog of pre-built agent templates so users can spin up a fully-configured agent (system prompt, model, tool assignments) and install agent's MCP servers in a single click.

---

## 2. ⏵ Critical Blocker: "Reserved for SE Interview"

The issue carries the label **`Reserved for SE interview`** with the description:

> **Please don't take it if you're not interviewing https://archestra.ai/careers**

**This makes the issue ineligible for general bounty hunters.** Archestra uses these issues specifically as part of their software engineering interview process. Taking it as a non-interview candidate would likely result in rejection and negative reputation with the maintainers.

---

## 3. Competition & Assignment Status

| Contributor | Role | Status | PR # | Algora Status |
|------------|----|-----|-----|-----------|
| @wandrounik | Assigned original | PR rejected | #4266 | WIP (dropped) |
| @void0x14 | Unauthorized attempt | PR closed, blocked by maintainer | #4304 | ⚠ Shows "Reward" |
| @avaughey | Attempted | WIP x — | | WIP |
| @sayidilxs-web | Attempted | PR closed | #4476 | 🌵 Shows "Reward" (Completed) |

**Key details:**
- *@wandrounik* was the original assignee (Apr 24). Submitted PR #4266 which was **rejected** by maintainer @iskhakov: *"unfortunately I cannot accept this PR. It doesn't look production ready... Closing it, best of luck"
- *@void0x14* submitted PR #4304 (claimed within 24h, first time using TypeScript/React). @iskhakov **blocked** them for working on an assigned issue and sending negative emojis.
- *@sayidilxs-web* submitted PR #4476. Algora shows "Status: Completed" on the claim page. Multiple comments marked as **SPAM** by maintainers.
- *@Avaughey* has WIP status since May 7.

**Algora bot table shows 2 "Reward" links** — suggesting the $450 bounty may have been paid to both void0x14 and sayidilxs-web, which is highly irregular. This indicates the bounty process for this issue is chaotic.

---

## 4. Maintainer Behavior & Risks

From comments analysis, the Archestra team (especially @iskhakov and @Matevy-Kuk) is:

- **Strict on quality**: wandrounik's substantial PR was rejected as "not production ready."
- **Anti-AI-responses**: They explicitly called out "unresponsible use of AI" when blocking @Darshan3690 on #3855.
- **Anti-spam**: Multiple comments minimized as SPAM, users blocked for negative behavior.
- **Testing "design and product thinking"*: <@iskhakov> stated: *"we intentionally added an open ended task to see your design and product thinking, not claude outputs."*

**Risk: Low tolerance for AI-assisted submissions.** This is a significant concern for AI-agent-based bounty hunting.

---

## 5. Bounty Verification

- *$450 confirmed** via `/bounty 450` by @Matevy-Kuk (2026-04-28)
- Algora bot posted confirmation with attempt tracking table
- The claim page (saydilxs-web) shows "Status: Completed"
- **Legitimate bounty, but effectively exhausted** — already paid out to at least 1-2 people

---

## 6. Repository Health & Activity

| Metric | Value |
|----|----|
| **Stars*** | 3,653 |
| **Forks** | 724 |
| **Open Issues** | 113 |
| **Language**| TypeScript |
| **Latest Release** | v1.2.47 (today, 2026-05-14) |
| **Last Push** | 2026-05-14 |
| **Description**| Enterprise AI Platform with guardrails, MCP registry, gateway & orchestrator |

**Verdict:** Extremely active, high-quality project. Well-funded and professionally maintained.

---

## 7. Technical Feasibility

- **Stack:** TypeScript (Next.js frontend + Node backend), MCP SDK, PostgreSQL
- **Scope:** Build template manifest, backend API endpoints (GET /agent_templates, GET /agent_templates/:id/requirements), MCP server provisioning flow, frontend catalog UI with guided install
- **Complexity**: Medium-High. The issue is intentionally open-ended. Maintainers expect architectural design thinking, not just code.
- **AI Feasibility**: Moderate. The code is straightforward, but the **expectation of original design thinking** and **maintainer hostility toward AI-generated responses** makes this risky for automated hunting.

---

## 8. Overall Risk Assessment

| Risk Factor | Level | Notes |
|---------------|------|------|
| **Interview-only label**| 📴 CRITICAL | Makes issue ineligible |
| **Competition**| 📴 CRITICAL | Multiple attempts, 2 rewarded, chaos |
| **Maintainer receptiveness** | 🔼 MODERATE | Strict, anti-AI, quality-focused |
| **Bounty remaining**| 📴 CRITICAL | Appears already paid |
| **Technical complexity** | 🔼 MODERATE | Open-ended design challenge |
| **Repo accessibility** | 🔼 MODERATE | Full clone timed out (large repo) |

---

## 9. Recommendation: ❌ 放弃 (Ðbandon)

### Reasons:
1. **"Reserved for SE interview" label** explicitly prohibits non-interview contributors
2. **Bounty appears already exhausted** — 2 reward links in Algora bot table
3. **High chaos signal** — blocked users, spam flags, rejected PRs, negative emojis
4. **Maintainers openly hostile to AI-assisted work** — a direct risk for AI-agent bounty hunting
5. **Original assignee's quality PR was rejected** — bar is high

### Do NOT attempt #3855 either
Issue #3855 (WindMill MCP Server, $400) also carries the **"Reserved for SE interview"** label and has similar chaos (blocked users, spam marks, multiple attempts). Same conclusion.

---

## 10. Alternative Opportunities in Same Repo

The following **bounty issues are OPEN (not interview-reserved)** in archestra-ai/archestra:

| Issue | Title | Bounty |
|-----|------|------|
| #4468 | Add support for Anthropic Workload Identity Federation | $25 |
| #4464 | Ability to "soft delete" all objects | $150 |
| #4463 | Site notification/announcements bar | $75 |
| #4461 | Specify limit cleanup interval | $50 |
| #4225 | Blocked Tool Result Policy bypass | $80 |
| #3854 | Add audit log to UI | $250 |
| #3218 | Auto sync permissions ACL for Jira/Confluence | $150 |
| #3012 | Chat reloading lost messages bug | $150 |

These may be worth investigating for future bounty opportunities, though each would need its own preflight assessment.

---

*Report generated for opportunity-radar project.*