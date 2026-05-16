# Heartbeat Scan — 2026-05-16 00:02 CST

## 本轮操作
- ✅ 运行 `python3 radar.py scan` 全量扫描
- ✅ Expensify watcher 健康检查（launchctl list + 日志审查）

## 扫描结果
- **总候选**：101 个（白名单扫描后）
- **过滤陈旧 issue**：21 个超过 90 天（高赏金例外）
- **打分完成**：99 个可执行 / 1 个跳过
- **深度预检过滤**：7 个已锁定/已有PR/已有人在做

## 赚钱榜 Top 3

| # | 候选 | 积分 | 赏金 | 时薪 | 状态 | 结论 |
|---|------|------|------|------|------|------|
| 1 | home-assistant/core#170803 — Victron GX: no entity names | 56.4 | $100 sponsor | $22.56/hr | ✅ 未分配 | 可自动 |
| 2 | home-assistant/core#170802 — Onboarding failure | 56.4 | $100 sponsor | $22.56/hr | ✅ 未分配 | 可自动 |
| 3 | home-assistant/core#170801 — No TTS with Apple HomePods | 56.4 | $100 sponsor | $22.56/hr | ✅ 未分配 | 可自动 |

## 练手池 Top 3

| # | 候选 | 积分 | 赏金 | 时薪 | 状态 |
|---|------|------|------|------|------|
| 1 | Scottcjn/rustchain-bounties#1102 — [EASY BOUNTY: 3-5 RTC] Find and Report a BoTTube Bug | 51.5 | $0 (RTC) | -$0.8/hr | ✅ 可自动 |
| 2 | Scottcjn/rustchain-bounties#100 — [BOUNTY] Discovery Mode — Find Elyan Labs Software, Open PRs, Earn RTC | 51.5 | $0 (RTC) | -$0.8/hr | ✅ 可自动 |
| 3 | Scottcjn/Rustchain#165 — [BOUNTY] Share Why You Starred RustChain | 47.4 | $0 (RTC) | -$0.8/hr | ✅ 可自动 |

练手池全部来自 IssueHunt 降级扫描，为 RustChain RTC token 赏金（实际 $0 价值）。

## 跳过项
- firebase/firebase-functions#1638: 安全任务无PoC，不提交（curl教训）

## Expensify Watcher 健康检查
- **launchd 状态**：`com.lflz.expensify-watcher` ✅ 已加载，LastExitStatus=0
- **结论**：✅ 正常工作中

## $250+ 未分配 Bounty 检查
- **Expensify/App**: 本次扫描未发现新的 unassigned $250+ External bounty
- **其他 proven payer**: 未发现 $250+ 未分配 bounty
- 所有已知 Expensify $250 issue 均有 assignee

## 候选清单已保存
- `/Users/tao/Desktop/项目文件夹/ai赚钱/opportunity-radar/reports/candidates_2026-05-16.json`

## 结论
管线持续枯竭。所有高价值 bounty 均有 assignee。本次无新 $250+ unassigned visible bounty 发现。等待下一批 Expensify $250 External 出现。
