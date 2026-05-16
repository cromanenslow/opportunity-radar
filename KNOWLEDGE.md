# 机会雷达 KNOWLEDGE.md
最后更新：2026-05-17 01:35（Heartbeat 109：深度预检 + Algora 扫描 ✅ — HA#170914 🟢 可做但无真实赏金，管线确认仍枯竭）

_(18:04 更新) Heartbeat 92：全量扫描完成（~174s）。Algora 质量修复 `_clean_description()` + `_parse_bounty_amount()` 正常运行，未报错。新出现 3 个赚钱候选：vitejs/vite#22456（pnpm overrides 配置问题 $100）、home-assistant/core#170880（IntesisHome 集成停止工作 $100）、home-assistant/core#170875（Teleinfo 集成串口问题 $100）。管线从枯竭转为有候选可做。等待 Tao 审批。_

_(01:35 更新) Heartbeat 109：深度预检 + Algora 扫描 ✅——HA#170914 深度预检完成：技术可做 🟢（commit devcontainer lock file, 0代码修改, ~30min），但**无真实赏金** 🔴（$100 为机会雷达推断值，HA 无 sponsor 标签，FUNDING.yml 指向非营利基金会）。Algora API 不可用（Phoenix LiveView 架构无公开 REST API），0 新 $100+ 候选。vite#22456 🟢 + HA#170880 🟢 仍 OPEN/无人。管线确认仍枯竭——所有"新"候选的 $100 均为推断值，无真实赏金来源。Tao 决策摘要已生成至 00_总控/。等待 Tao 审批策略（推荐快速执行 Top-2 试水 vs 优化推断检测）。_

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
- **最后扫描**：2026-05-16 18:04，Heartbeat 92 全量扫描
- **赚钱榜 Top（本轮）**：
  1. **vitejs/vite#22456** — Pnpm overrides 配置问题（$100 sponsor, $26.84/hr, 得分67.1 🆕）
  2. **home-assistant/core#170880** — IntesisHome 集成停止工作（$100 sponsor, $22.56/hr, 得分56.4 🆕）
  3. **home-assistant/core#170875** — Teleinfo 集成串口问题（$100 sponsor, $22.56/hr, 得分56.4 🆕）
- **热区表**：52 仓库（含扩容）
- **待审批**：🆕 vitejs/vite#22456、home-assistant/core#170880、home-assistant/core#170875
- **30天指标**：赚钱候选/天 0.2 → 0.8，预检通过率 0.0，合并率 0.0，$/agent-hour $0.0

## 下一步方向
1. ⏳ Tao 审批策略（管线枯竭，需要方向性决策）
2. ⏳ 考虑是否对 #170850（Backup issue）进行 Pre-check
3. ⏳ 考虑是否放弃 home-assistant/core 的 $100 sponsor 推断值管线
4. 持续监控 Expensify/App 新 $250 External 出现
5. 将 Algora 扫描加入日常管线
6. ✅ Algora 扫描质量已修复（Heartbeat 91：description 净化 + bounty 解析鲁棒性，47 测试全通过）
