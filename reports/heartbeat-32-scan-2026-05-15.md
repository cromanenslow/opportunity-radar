# Heartbeat 32 — 2026-05-15 07:29 UTC+8

## 本轮操作
- ✅ 运行 `python radar.py scan` 全量扫描
- ✅ Expensify watcher 健康检查（launchctl list + 日志审查）
- ✅ KNOWLEDGE.md 更新

## 扫描结果
- **总候选**：103 可执行（含 3 赚钱 + 100 练手/噪声）
- **热区扫描**：32 仓库 → 25 新 issue
- **平台降级**：Algora、OnlyDust、Huntr 均不可用；IssueHunt 20 条（全为 Scottcjn RTC token 噪声）
- **GitHub 搜索**：56 新 issue（good-first-issue/help-wanted/bug 标签）

## 赚钱榜 Top 3

| # | 候选 | 积分 | 赏金 | 状态 | 结论 |
|---|------|------|------|------|------|
| 1 | Expensify/App#89799 | 58.0 | $250 tipping | ❌ 已分配 mkhutornyi | 不可用 |
| 2 | home-assistant/core#170761 | 56.4 | $100 sponsor | ✅ 未分配，无确认赏金 | 支付不确定 |
| 3 | home-assistant/core#170757 | 56.4 | $100 sponsor | ✅ 未分配，无确认赏金 | 支付不确定 |

## 练手池 Top 3（全为噪声）
1. Scottcjn/rustchain-bounties#1102 — [EASY BOUNTY: 3-5 RTC] Find BoTTube Bug
2. Scottcjn/rustchain-bounties#100 — Discovery Mode
3. Scottcjn/Rustchain#165 — Share Why You Starred

练手池全部来自 IssueHunt 降级扫描，为 RustChain RTC token 赏金（实际 $0 价值）。

## 待审批状态变化
- Expensify/App#90533 [$250] — **之前：** ⏳ 等待 Tao 审批 | **现在：** ❌ 已分配给 QichenZhu

## 之前 Top 候选状态
| 候选 | Heartbeat 28 状态 | Heartbeat 32 状态 |
|------|-------------------|-------------------|
| Expensify/App#90693 [$250] | Top 1 🆕 | ❌ 已分配 ZhenjaHorbach |
| home-assistant/core#170683 | Top 2 | ✅ 未分配（无赏金） |
| home-assistant/core#170680 | Top 3 | ✅ 未分配（无赏金） |

## Expensify Watcher 健康检查
- **launchd 状态**：`com.lflz.expensify-watcher` ✅ 已加载，LastExitStatus=0
- **24h 运行次数**：13 次（每 ~2h 一次）
- **最近运行**：2026-05-15 05:34 UTC+8
- **日志错误**：0
- **未分配 $250 发现**：0（过去 24h 所有 External issue 均有 assignee）
- **结论**：✅ 正常工作中，但近期无新 unassigned $250 issue

## 结论
管线持续枯竭。所有 Expensify $250 已知 issue 均有 assignee。等待下一批 $250 External 出现。
