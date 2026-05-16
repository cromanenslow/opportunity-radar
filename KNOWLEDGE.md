# 机会雷达 KNOWLEDGE.md
最后更新：2026-05-16 16:05（Heartbeat 90：日间续检 + #170850 Pre-check 完成 🟡 需人工复核。管线持续枯竭：0 可执行赚钱候选。等待 Tao 审批策略。）

_(16:05 更新) Heartbeat 90：日间续检完成。#170850 Pre-check 完成——🟡 需人工复核。Issue 描述明确（regression in core-2026.5.2），但无确认赏金（$100 为算法推断）。竞争为 0（无 assignee）。推荐跳过此 issue 或等 Tao 决策。Scheduler PID 66506 运行正常（15h uptime）。所有 4 项待办仍等待 Tao。_

_(10:30 更新) Heartbeat 81：home-assistant/core#170853 预检完成——🟢 可做。根因：tts.py cmn-CN vs zh-CN 语言代码不匹配，修复仅 3-6 行。管线仍枯竭，等待 Tao 审批后进入执行。_

_(07:32 更新) Heartbeat 77：06:30 全量扫描完成——3个赚钱候选但Top1已分配，管线持续枯竭。已开始热区表扩容+分配检测修复。_

> 完整 Pre-check 分析详情、旧里程碑记录及已完成待办项请见 [KNOWLEDGE-archive.md](./KNOWLEDGE-archive.md)

## 项目名称与目标
**项目名称**：Opportunity Radar（机会雷达）
**项目目标**：多平台赏金/任务扫描 → 自动打分排序 → 本地预检 → 人类审批。第一阶段以赚取赏金为目标，AI 优先执行可验证、高确定性任务。

## 当前里程碑
### ✅ 已完成（概要）
- 多平台扫描、6 维度打分引擎、白名单系统（100 仓库）
- 任务追踪器 DeliveryTracker、Expensify watcher（launchd 调度）
- Git 版本控制已初始化
- 已知赏金仓库热区表（52 仓库，含 proven-payer + 轮换仓库）
- 多轮全量扫描 + 深度 Pre-check（tscircuit、cal.com、archestra 等）

### 🔄 进行中
- ⏳ **人工审批 / 实际动手阶段**：等待 Tao 决定
- ❌ **home-assistant/core#170853** 已关闭（原 🟢 可做）
- ✅ **#170868** Pre-check 完成（🔴 不可做）
- ✅ **#170870** Pre-check 完成（🟡 需人工复核）
- Expensify watcher 正常（每1h执行）
- 管线持续枯竭：所有 Expensify $250 已知 issue 均有 assignee

## 团队配置
| 角色 | 成员 | 职责 |
|------|------|------|
| CEO/审批 | Hermes（Evan-Pro） | 每日审批（15min），方向与边界 |
| 工程师 | AI Agent | 扫描、打分、本地预检执行 |

## 运行状态
- **最后扫描**：2026-05-16 15:30，Heartbeat 89 日间续检扫描
- **赚钱榜 Top（本轮）**：
  1. **home-assistant/core#170870** — HA VOICE PE Google TTS 修复（已预检 🟡 需人工复核）
  2. **home-assistant/core#170868** — Tuya polling 修复（已预检 🔴 不可做）
  3. **home-assistant/core#170850** — Backup storage 问题（未预检）
- **热区表**：52 仓库（含扩容）
- **待审批**：🟢 #170853 已关闭，不可操作
- **30天指标**：赚钱候选/天 0.2，预检通过率 0.0，合并率 0.0，$/agent-hour $0.0

## 下一步方向
1. ⏳ Tao 审批策略（管线枯竭，需要方向性决策）
2. ⏳ 考虑是否对 #170850（Backup issue）进行 Pre-check
3. ⏳ 考虑是否放弃 home-assistant/core 的 $100 sponsor 推断值管线
4. 持续监控 Expensify/App 新 $250 External 出现
5. 将 Algora 扫描加入日常管线
6. 长期改进：修复 Algora 扫描质量（当前 Description/Bounty 误报严重）
