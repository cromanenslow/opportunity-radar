# 机会雷达 KNOWLEDGE.md 归档

> 归档时间：2026-05-16
> 本文件包含从 KNOWLEDGE.md 移出的 Pre-check 分析详情、旧里程碑记录和已完成待办项。

## Pre-check Findings（2026-05-14 第三轮）

### 1. tscircuit/core #2281 — "manualEdits position double-counts the parent group's anchor"
- **Bounty**: 未明确标注 — tscircuit 通过 Algora 发放赏金，类似 issue 通常标注 💎 Bounty/$100
- **状态**: ✅ Open, Unassigned, 0 comments（全新issue）
- **要求**: 修复 `manualEdits.pcb_placements` 中的位置计算Bug — 当组件在 `<group>` 内时，group anchor 被重复计算两次
- **难度**: Medium — TypeScript PCB 布局计算，需理解 tscircuit 的坐标变换体系
- **AI可行性**: ✅ 有条件 — 有完整repro代码和预期行为的对比说明，但需理解 tscircuit 的 transform 链
- **竞争状况**: ✅ **低** — 0 assignees，0 comments，0 PR，全新issue（2026-05-13创建）
- **风险**: 中 — tscircuit/core 虽属 tscircuit 生态（proven-payer via Algora），但该 issue 未标注 bounty 标签
- **维护者活跃度**: 高 — tscircuit 生态活跃，seveibar 等频繁更新，最后 push 2026-05-08
- **结论**: ✅ **推荐关注** — 低竞争、TypeScript、有完整repro，适合作为ai赚钱候选。需确认是否通过 Algora 有赏金。

### 2. calcom/cal.com #29341 — "@calcom/atoms crashes in Next.js App Router beyond version 2.6.0"
- **Bounty**: 未明确标注 — cal.com 通过 Algora 发放赏金（预期 $100-1000）
- **状态**: ✅ Open, Unassigned, 0 comments（2026-05-14创建）
- **要求**: 排查 @calcom/atoms v2.6.0→v2.11.0 之间的 bundle/import 变更，修复在 Next.js App Router 下的运行时崩溃
- **难度**: Medium — TypeScript/React，需要了解 Next.js App Router 的 SSR/CSR 边界和 cal.com 的 atom 构建配置
- **AI可行性**: ✅ 高 — 有完整的 repro repo 和 working/failing 分支对比，可以通过二分法定位
- **竞争状况**: ✅ **低** — 0 assignees，0 comments，全新的issue
- **风险**: 中 — 需要搭建 cal.com 本地环境，atom 构建可能涉及复杂 bundling 配置；不保证有赏金
- **维护者活跃度**: 高 — cal.com 是高频更新项目，Algora 赏金频繁发放
- **结论**: ✅ **推荐关注** — 全新issue、低竞争、完整repro。需注意 cal.com 本地开发环境较庞大。

### 3. boxyhq/saas-starter-kit #2511 — "Missing RBAC authorization on payment/billing API endpoints"
- **Bounty**: 未标注 — BoxyHQ 通过 GitHub Sponsors 发放，预期 $50-300
- **状态**: ✅ Open, Unassigned, 0 comments
- **要求**: 在3个 payment/billing API 端点中添加 RBAC 权限检查（`throwIfNotAllowed`）
- **难度**: Easy — TypeScript，明确的端点列表和修复方向
- **AI可行性**: ✅ 高 — 3个端点的修复方式一致，代码量小
- **竞争状况**: ✅ **低** — 0 assignees，0 comments
- **风险**: 低 — 安全Bug，修复明确；但赏金金额较低（$50-300）
- **维护者活跃度**: 中等 — BoxyHQ 项目活跃
- **结论**: ⚠️ **有条件推荐** — 技术门槛低、AI可行性高、无竞争，但潜在收益较低。

### 4. coder/coder #25275 — "bug: A lot of parallel refresh token request with SSO Keycloak configuration"
- **Bounty**: 未标注 — Coder 通过 GitHub Sponsors，预期 $50-500
- **状态**: ✅ Open, Unassigned, 0 comments
- **要求**: 修复 Keycloak SSO 下 token refresh 时的并发请求风暴问题（竞态条件）
- **难度**: Medium — TypeScript，需要理解 OAuth2/SSO token refresh 流程
- **AI可行性**: ⚠️ 有条件 — 需要搭建 Keycloak 环境才能复现和验证修复
- **竞争状况**: ✅ **低** — 0 assignees，0 comments
- **风险**: 中 — 需要 SSO 环境和 Keycloak 实例，复现成本高
- **维护者活跃度**: 高 — Coder 项目高频更新
- **结论**: ⚠️ **暂缓** — 修复方向明确但复现难度大，需要较多环境搭建工作。

### 5. SolFoundry/solfoundry #863 — "🏭 Bounty T3: SolFoundry TypeScript SDK"
- **Bounty**: 900K $FNDRY token（Solana代币），USD价值不确定
- **状态**: ✅ Open, Unassigned, 7 comments（活跃讨论中）
- **要求**: 构建全面的 TypeScript SDK
- **难度**: Hard — 需要构建完整 SDK 架构、类型定义、文档和示例
- **AI可行性**: ⚠️ 有条件 — TypeScript SDK 开发适合 AI 辅助
- **竞争状况**: ✅ **低-中** — 0 assignees，但有 7 条讨论
- **风险**: 高 — $FNDRY token 价值不确定
- **维护者活跃度**: 活跃
- **结论**: ⚠️ **暂缓** — 工作量大、收益不确定。

### 6. tscircuit/core #2272 — "Auto-packer pushes large chip off-board"
- **Bounty**: 未标注
- **状态**: ✅ Open, Unassigned, 0 comments
- **要求**: 修复 auto-packer 将大芯片推出 board 边界的问题
- **难度**: Medium-Hard — 需理解 tscircuit autorouter/packer 算法
- **AI可行性**: ⚠️ 有条件 — TypeScript，但需要深入理解 packing 算法
- **竞争状况**: ✅ **低** — 全新 issue，无竞争者
- **结论**: ⚠️ **备选** — 比 #2281 更难，建议优先处理 #2281

### 总结建议
- ~~**本轮最佳候选**: tscircuit/core #2281~~ — ❌ 已 Preflight，Algora $0 赏金，放弃
- ~~**本轮最佳候选（更新）**: getkyo/kyo#390 IMAP, $2,500~~ — ❌ 已 Preflight，实际为 Scala 3 gRPC，$1,000，7+ PR 激烈竞争
- ~~**本轮最佳候选（更新）**: aietal/isaac#45 RAG Pipeline, $850~~ — ❌ 已 Preflight，仓库 private
- ~~archestra-ai/archestra#3858 Agent template, $450~~ — ❌ interview reserved
- ~~archestra-ai/archestra#3854 audit log, $250~~ — ❌ 已有 assignee
- ~~archestra-ai/archestra#4464 soft delete, $150~~ — ❌ 已有 PR 提交
- ⭐ **tscircuit/dsn-converter#54 Smoothie Board, $170** — 已验证有赏金，TypeScript
- **存档候选**: calcom/cal.com #29341、boxyhq/saas-starter-kit #2511
- **降低star门槛策略结论**: 搜索50-500 stars范围的显式bounty/reward issue返回了大量噪音

## 归档里程碑详情

### ✅ 已完成
- 多平台扫描：GitHub Issues、Algora、IssueHunt、OnlyDust、Huntr
- 打分引擎：6 维度权重评分（支付确定性 26% / 可验证性 22% / AI 适配度 18% / 维护者活跃度 12% / 上下文复用 7% / 竞争强度 15%）
- 白名单系统：100 初始仓库，stars 10-50000
- 任务追踪器：DeliveryTracker 记录候选→审批→预检→PR→付款全流程
- 每日扫描 & 日报：最后扫描 2026-05-14，发现 12 个候选
- Python Expensify watcher：`scripts/watch-expensify-issues.py`
- Git 版本控制已初始化（1 commit）
- **已知赏金仓库热区表**（2026-05-14）：33 个已验证赏金仓库
- ✅ **2026-05-14 11:41 新一轮完整扫描**：覆盖全部 29 个仓库
- ✅ **降低star门槛策略试点**：搜索 50-500 stars 范围
- ✅ **Top 2 新候选 pre-check**：tscircuit/core #2281 和 calcom/cal.com #29341

### 🔄 进行中（已归档）
- ✅ Heartbeat 11 已委托 Pre-check 分析：TOP 3 候选深度评估完成
- ✅ Expensify/App#90693 Pre-check 完成 — 结论：❌ 不投入
- ✅ **Heartbeat 32（2026-05-15 07:29）新一轮全量扫描 + Expensify watcher 健康检查**
- ✅ **calcom/cal.com #29341 深度预检完成（2026-05-14 21:00 Heartbeat 15）**
- ✅ **Preflight tscircuit/core #2281 完成** — Algora 上无赏金（$0）
- ✅ **Algora 平台直接扫描完成**（2026-05-14 12:08）
- ✅ **Preflight getkyo/kyo#390 完成** — ❌ 放弃
- ✅ **Preflight aietal/isaac#45 完成** — ❌ 放弃
- ✅ **Preflight archestra-ai/archestra#3858 完成** — ❌ 放弃
- ✅ **Preflight archestra-ai/archestra#3854 和 #4464 完成** — ❌ 均放弃
- ✅ **Preflight tscircuit/dsn-converter#54 完成** — ⚠️ 有条件推荐
- ✅ **管线枯竭全面复盘**
- ✅ **2026-05-14 16:01 Heartbeat 9 新一轮全量扫描** — 103 原始候选

## 归档下一步方向（已完成项）
1. ✅ 竞争强度因子优化
2. ✅ Expensify watcher launchd 调度
3. ✅ 评估 crosscompute/jupyterlab-crosscompute #39 可行性
4. ✅ 2026-05-14 06:32 新扫描 + Expensify/App#88700 pre-check
5. ✅ 已知赏金仓库热区表（known-bounty-repos.yaml）
6. ✅ 首次已知赏金仓库热区扫描验证完成（2026-05-14 08:09）
7. ✅ 2026-05-14 11:41 新一轮完整扫描 + 低star策略试点
8. ✅ Preflight tscircuit/core #2281 完成
9. ✅ Algora 平台直接扫描完成
10. ✅ Preflight getkyo/kyo#390 完成
11. ✅ Preflight aietal/isaac#45 完成
12. ✅ Preflight archestra-ai/archestra#3858 完成
13. ✅ Preflight tscircuit/dsn-converter#54 完成
14. ✅ 管线枯竭全面复盘
15. ✅ 2026-05-14 16:01 Heartbeat 9 新一轮全量扫描
16. ✅ calcom/cal.com #29341 深度预检完成
