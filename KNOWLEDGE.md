# 机会雷达 KNOWLEDGE.md
最后更新：2026-05-14 21:37（Heartbeat 16：增量扫描完成 — 自16:01以来所有已知热区仓库无新issue，Algora API不可用，管线持续枯竭；热区表需维护3个仓库名变更）

## 项目名称与目标
**项目名称**：Opportunity Radar（机会雷达）
**项目目标**：多平台赏金/任务扫描 → 自动打分排序 → 本地预检 → 人类审批。第一阶段以赚取赏金为目标，AI 优先执行可验证、高确定性任务。

## 当前里程碑
### ✅ 已完成
- 多平台扫描：GitHub Issues、Algora、IssueHunt、OnlyDust、Huntr
- 打分引擎：6 维度权重评分（支付确定性 26% / 可验证性 22% / AI 适配度 18% / 维护者活跃度 12% / 上下文复用 7% / 竞争强度 15%）
- 白名单系统：100 初始仓库，stars 10-50000
- 任务追踪器：DeliveryTracker 记录候选→审批→预检→PR→付款全流程
- 每日扫描 & 日报：最后扫描 2026-05-14，发现 12 个候选
- Python Expensify watcher：`scripts/watch-expensify-issues.py` 跟踪 Expensify/App $250 External 赏金 Issue
- Git 版本控制已初始化（1 commit：初始提交）
- **已知赏金仓库热区表**（2026-05-14 07:30→13:00）：33 个已验证赏金仓库（TypeScript 23 + Python 8 + Other 2），含 Expensify/App、tscircuit/*、oppia/oppia、calcom/cal.com 等 proven payer。2026-05-14 13:00 热区扩展 +4：claude-builders-bounty（AI代理友好）、tsperf/tracer（Algora Challenge）、screenpipe/screenpipe、Spectral-Finance/lux。配套 config.yaml（known_bounty_scan_limit=10）+ scanner/github.py 专用扫描函数（三层兜底策略），白名单扫描从 5→20 个仓库
- ✅ **2026-05-14 11:41 新一轮完整扫描**：覆盖全部 29 个仓库（8 proven-payer + 19 轮换/手动补充 + 2 已确认禁用issues），发现 52+ 个候选 issue
- ✅ **降低star门槛策略试点**：搜索 50-500 stars 范围 + 100-2000 stars 范围的 bounty/reward issue，但未发现高价值的额外候选
- ✅ **Top 2 新候选 pre-check**：tscircuit/core #2281 和 calcom/cal.com #29341

### 🔄 进行中
- ✅ Heartbeat 11 已委托 Pre-check 分析：TOP 3 候选深度评估完成
  - ⭐⭐⭐⭐ calcom/cal.diy #29341 — 今晚首选（1天龄、0竞争、完整repro、AI可行性90%）
  - ⭐⭐ tscircuit/core #2281 — 已有PR被关闭，赏金不确定，不推荐
  - ⭐ boxyhq/saas-starter-kit #2511 — 无赏金+已有PR 19天未合并，不推荐
- 人工审批 / 实际动手阶段等待 Tao 决定
- Expensify watcher 已通过 launchd 每1h执行（com.lflz.expensify-watcher），正常工作中

## 团队配置
| 角色 | 成员 | 职责 |
|------|------|------|
| CEO/审批 | Hermes（Evan-Pro） | 每日审批（15min），方向与边界 |
| 工程师 | AI Agent | 扫描、打分、本地预检执行 |

## 运行状态
- **最后扫描**：2026-05-14 21:37（UTC+8），增量扫描（已知热区表 + Algora + GitHub Issues）
- **本轮发现**：自 16:01 以来无新高价值候选。已知热区仓库新增 issue = 0。管线继续枯竭。
- **赚钱榜 Top（本轮扫描）**：
  1. **Expensify/App#90628** — ⚠️ [$250] Email通知Bug，已有C+ reviewer和8+ proposals，竞争激烈
  2. **Expensify/App#90067** — ❌ [$250] DEW提交动画Bug，proposal已选定，讨论中
  3. **home-assistant/core#170591** — ⚠️ Withings date.today()时区Bug，无明确赏金，可做声誉贡献
- **待审批**: Expensify/App#90533 [$250] — 等待 Tao 审批
- **热区表维护提醒**: froglogic/tracetest 不存在；plasmic-hq/plasmic → plasmicapp/plasmic；postiz-app/postiz → gitroomhq/postiz-app
- **30天指标**：赚钱候选/天 0.2，预检通过率 0.0，合并率 0.0，$/agent-hour $0.0

## Pre-check Findings (2026-05-14 第三轮)

### 1. tscircuit/core #2281 — "manualEdits position double-counts the parent group's anchor"
- **Bounty**: 未明确标注 — tscircuit 通过 Algora 发放赏金，类似 issue 通常标注 💎 Bounty/$100
- **状态**: ✅ Open, Unassigned, 0 comments（全新issue）
- **要求**: 修复 `manualEdits.pcb_placements` 中的位置计算Bug — 当组件在 `<group>` 内时，group anchor 被重复计算两次
- **难度**: Medium — TypeScript PCB 布局计算，需理解 tscircuit 的坐标变换体系
- **AI可行性**: ✅ 有条件 — 有完整repro代码和预期行为的对比说明，但需理解 tscircuit 的 transform 链
- **竞争状况**: ✅ **低** — 0 assignees，0 comments，0 PR，全新issue（2026-05-13创建）
- **风险**: 中 — tscircuit/core 虽属 tscircuit 生态（proven-payer via Algora），但该 issue 未标注 bounty 标签，不一定有明确赏金
- **维护者活跃度**: 高 — tscircuit 生态活跃，seveibar 等频繁更新，最后 push 2026-05-08
- **结论**: ✅ **推荐关注** — 低竞争、TypeScript、有完整repro，适合作为ai赚钱候选。需确认是否通过 Algora 有赏金。建议在本地上做 preflight clone 验证修复可行性后再确认投入。

### 2. calcom/cal.com #29341 — "@calcom/atoms crashes in Next.js App Router beyond version 2.6.0"
- **Bounty**: 未明确标注 — cal.com 通过 Algora 发放赏金（预期 $100-1000），该 issue 暂无 bounty 标签
- **状态**: ✅ Open, Unassigned, 0 comments（2026-05-14创建）
- **要求**: 排查 @calcom/atoms v2.6.0→v2.11.0 之间的 bundle/import 变更，修复在 Next.js App Router 下的运行时崩溃
- **难度**: Medium — TypeScript/React，需要了解 Next.js App Router 的 SSR/CSR 边界和 cal.com 的 atom 构建配置
- **AI可行性**: ✅ 高 — 有完整的 repro repo 和 working/failing 分支对比，可以通过二分法定位
- **竞争状况**: ✅ **低** — 0 assignees，0 comments，全新的issue
- **风险**: 中 — 需要搭建 cal.com 本地环境，atom 构建可能涉及复杂 bundling 配置；不保证有赏金
- **维护者活跃度**: 高 — cal.com 是高频更新项目，Algora 赏金频繁发放
- **结论**: ✅ **推荐关注** — 全新issue、低竞争、完整repro。但需注意 cal.com 本地开发环境较庞大（monorepo），可在 Algora 上确认是否有对应赏金。建议标记为"需 Algora 确认"后进入预检流程。

### 3. boxyhq/saas-starter-kit #2511 — "Missing RBAC authorization on payment/billing API endpoints"
- **Bounty**: 未标注 — BoxyHQ 通过 GitHub Sponsors 发放，预期 $50-300
- **状态**: ✅ Open, Unassigned, 0 comments
- **要求**: 在3个 payment/billing API 端点中添加 RBAC 权限检查（`throwIfNotAllowed`）
- **难度**: Easy — TypeScript，明确的端点列表和修复方向，只需添加权限校验调用
- **AI可行性**: ✅ 高 — 3个端点的修复方式一致，代码量小，有同repo中其他端点的实现参考
- **竞争状况**: ✅ **低** — 0 assignees，0 comments
- **风险**: 低 — 安全Bug，修复明确；但赏金金额较低（$50-300）
- **维护者活跃度**: 中等 — BoxyHQ 项目活跃
- **结论**: ⚠️ **有条件推荐** — 技术门槛低、AI可行性高、无竞争，但潜在收益较低。可作为练手候选或快速$50+选项。

### 4. coder/coder #25275 — "bug: A lot of parallel refresh token request with SSO Keycloak configuration"
- **Bounty**: 未标注 — Coder 通过 GitHub Sponsors，预期 $50-500
- **状态**: ✅ Open, Unassigned, 0 comments
- **要求**: 修复 Keycloak SSO 下 token refresh 时的并发请求风暴问题（竞态条件）
- **难度**: Medium — TypeScript，需要理解 OAuth2/SSO token refresh 流程和 coder 的 auth 架构
- **AI可行性**: ⚠️ 有条件 — 需要搭建 Keycloak 环境才能复现和验证修复
- **竞争状况**: ✅ **低** — 0 assignees，0 comments
- **风险**: 中 — 需要 SSO 环境和 Keycloak 实例，复现成本高
- **维护者活跃度**: 高 — Coder 项目高频更新
- **结论**: ⚠️ **暂缓** — 修复方向明确但复现难度大，需要较多环境搭建工作。适合在有 Keycloak 环境时考虑。

### 5. SolFoundry/solfoundry #863 — "🏭 Bounty T3: SolFoundry TypeScript SDK"
- **Bounty**: 900K $FNDRY token（Solana代币），USD价值不确定
- **状态**: ✅ Open, Unassigned, 7 comments（活跃讨论中）
- **要求**: 构建全面的 TypeScript SDK，覆盖 bounty 管理、submission 处理和用户认证 API
- **难度**: Hard — 需要构建完整 SDK 架构、类型定义、文档和示例
- **AI可行性**: ⚠️ 有条件 — TypeScript SDK 开发适合 AI 辅助，但需要理解 SolFoundry API 设计
- **竞争状况**: ✅ **低-中** — 0 assignees，但有 7 条讨论，可能有多人关注
- **风险**: 高 — $FNDRY token 价值不确定（Solana 生态项目），可能价值很低或为零
- **维护者活跃度**: 活跃 — SolFoundry 是赏金平台自身，定期更新
- **结论**: ⚠️ **暂缓** — 工作量大（全SDK）、收益不确定（token价值未知）。建议先研究 $FNDRY 的流通性和兑换路径后再决定。

### 6. tscircuit/core #2272 — "Auto-packer pushes large chip off-board"
- **Bounty**: 未标注
- **状态**: ✅ Open, Unassigned, 0 comments
- **要求**: 修复当 group 内包含多个小元件时，auto-packer 将大芯片推出 board 边界的问题
- **难度**: Medium-Hard — 需理解 tscircuit autorouter/packer 算法
- **AI可行性**: ⚠️ 有条件 — TypeScript，但需要深入理解 packing 算法
- **竞争状况**: ✅ **低** — 全新 issue，无竞争者
- **结论**: ⚠️ **备选** — 比 #2281 更难，建议优先处理 #2281

### 总结建议
- ~~**本轮最佳候选**: tscircuit/core #2281~~ — ❌ 已 Preflight，Algora $0 赏金，放弃
- ~~**本轮最佳候选（更新）**: getkyo/kyo#390 IMAP, $2,500~~ — ❌ 已 Preflight，实际为 Scala 3 gRPC（非TypeScript IMAP），$1,000（非$2,500），7+ PR 激烈竞争，0 review，放弃
|- ~~**本轮最佳候选（更新）**: aietal/isaac#45 RAG Pipeline, $850~~ — ❌ 已 Preflight，仓库 private，maintainer 不响应，2 PR 未合并，10+ 人争抢，放弃
| ~~**archestra-ai/archestra#3858 Agent template, $450**~~ — ❌ 已 Preflight，标注为 "SE interview reserved"，非公开招募，maintainer 对 AI 提交有敌意
||- ~~**archestra-ai/archestra#3854 audit log, $250**~~ — ❌ 已 Preflight，虽非 interview reserved，但已有 assignee（abhinav-m22）积极讨论设计并被 maintainer 批准，6 个竞争者，其中一个已获奖金
||- ~~**archestra-ai/archestra#4464 soft delete, $150**~~ — ❌ 已 Preflight，虽非 interview reserved，但 Aqil-Ahmad 已提交 PR #4504（+13,633行），Algora 已发放奖金，issue 实际已无人可用
||- **本轮最佳候选（更新）**: ⭐ **tscircuit/dsn-converter#54 Smoothie Board, $170** — 已验证有赏金，TypeScript，最后一个未预检的 Algora 确认候选
||- **存档候选（待预检）**: calcom/cal.com #29341（Next.js crash，需确认 Algora 赏金）、boxyhq/saas-starter-kit #2511（简单RBAC，低金额）
- **快速$选项**: boxyhq/saas-starter-kit #2511（简单安全修复，但赏金较低）
- **不建议投入**: 
  - 所有3个 Expensify/App $250 新issue（均已有 assignees）
  - SolFoundry token bounties（代币价值不确定）
  - getkyo/kyo#390（Scala 3，竞争饱和，审查瓶颈，实际$1,000）
- **降低star门槛策略结论**: 搜索50-500 stars范围的显式bounty/reward issue返回了大量噪音（token项目为主），未发现优于已知热区表的候选。目前已知的29个热区仓库仍是最高价值来源。

## 下一步方向
1. ✅ 竞争强度因子优化 — 已加入第6维度（权重15%），通过 gh issue view 获取 assignees/PR 数据
2. ✅ Expensify watcher launchd 调度 — 已通过 launchd 配置为每小时自动执行
3. ✅ 评估 crosscompute/jupyterlab-crosscompute #39 可行性 — 已做，竞争过高，暂缓
4. ✅ 2026-05-14 06:32 新扫描 + Expensify/App#88700 pre-check — 结论：暂缓（assignee 卡住）
|5. ✅ 已知赏金仓库热区表（known-bounty-repos.yaml）— 33 个仓库（+4 新扩展），三层兜底扫描函数，白名单 5→20
6. ✅ 首次已知赏金仓库热区扫描验证完成（2026-05-14 08:09）
   - 扫描 29 个仓库中 10 个（8 proven-payer 始终扫描 + 2 轮换补充）
   - Bug 1 修复验证：`gh issue list --repo X` 替代 `gh search issues -- "repo:X..."`，无 API 报错
   - Bug 2 修复验证：proven-payer 仓库不再被 _day_rotation 轮换跳过
   - 发现 25 个候选，含 Expensify/App $250 External 赏金 #90556、tscircuit/schematic-trace-solver #29 $100 等
   - maybe-finance/maybe 已禁用 issues，后续可考虑从热区表移除
7. ✅ **2026-05-14 11:41 新一轮完整扫描 + 低star策略试点**
   - 扫描完整29个仓库（8 proven-payer + 19 手动补充 + 2 已确认禁用）
   - 实施降低star门槛策略（50-500 & 100-2000 stars范围）
   - pre-check top 2候选：tscircuit/core #2281 和 calcom/cal.com #29341
   - 发现 low-star 范围没有优于热区表的显式bounty候选
8. ✅ **Preflight tscircuit/core #2281 完成（2026-05-14 12:00）** — Bug 确认存在（PrimitiveComponent.ts 双重计数 + packer 覆盖），修复约 50-70 行。但 ❌ **Algora 上无赏金（$0）**，tscircuit/core 未被纳入 Algora bounty 体系。结论：不推荐投入。
9. ✅ **Algora 平台直接扫描完成（2026-05-14 12:08）** — 发现 Algora 精选 $2,500/IMAP、$850/RAG Pipeline、Archestra AI $450/$400 等**已确认赏金**候选。详情见 `bounty-platform-scan-2026-05-14.md`
10. ✅ **Preflight getkyo/kyo#390 完成（2026-05-14 12:30）** — ❌ 放弃。实际为 Scala 3 gRPC（非TypeScript IMAP），实际赏金 $1,000（非 $2,500），7+ PR 激烈竞争，0 review，维护者审查瓶颈严重。报告见 `reports/preflight_kyo_390.md`
11. ✅ **Preflight aietal/isaac#45 完成（2026-05-14 12:30）** — ❌ 放弃。仓库 private，maintainer 不响应，2 PR 未合并，10+ 人争抢。报告见 `reports/preflight_isaac_45.md`
13. ✅ **Preflight archestra-ai/archestra#3858 完成（2026-05-14 12:34）** — ❌ 放弃。标注为"SE interview reserved"，非公开招募；maintainer 对 AI 提交有敌意。附带确认 #3855（MCP Server）同为 interview reserved。但发现该仓库另有 8 个可参与的公开赏金（如 #3854 audit log $250, #4464 soft delete $150）。报告见 `reports/preflight_archestra_3858.md`
13.5. ✅ **Preflight archestra-ai/archestra#3854 和 #4464 完成（2026-05-14 13:35）** — ❌ 均放弃。虽非 interview reserved，但 #3854 已有 assignee（abhinav-m22）积极讨论设计并被 maintainer 批准，6 个竞争者；#4464 的 Aqil-Ahmad 已提交 PR #4504，Algora 已发放奖金。两个 issue 实际均无人可用。关键发现：archestra-ai/archestra 的所有非 interview-reserved 赏金均已饱和（每个都有活跃竞争者），不建议在该仓库进一步投入。报告见 `reports/preflight_archestra_3854_4464.md`
14. ✅ **Preflight tscircuit/dsn-converter#54 完成（2026-05-14 13:09）** — 结论：⚠️ 有条件推荐。$170 赏金已确认（Algora），但 4 个月内 29+ PR 未合并、50+ 竞争者、大量 spam、原始 DSN 参考文件 404。建议仅做极窄子问题（≤50行）或暂缓。详见 `reports/preflight_tscircuit_dsn-converter_54.md`
15. ✅ **管线枯竭全面复盘（所有候选已评估）**
16. ✅ **2026-05-14 16:01 Heartbeat 9 新一轮全量扫描** — 103 原始候选 → 106 可执行，Top1 Expensify/App #90533 $250
17. **下一步**: Tao 审批 Expensify/App #90533 $250 或其他 Top 候选后进入预检
18. ✅ **calcom/cal.com #29341 深度预检完成（2026-05-14 21:00 Heartbeat 15）** — 根因：`@calcom/atoms/package.json` 声明 `"sideEffects": false`，Webpack tree-shake 了 dayjs timezone plugin 的 side-effect import，导致 `dayjs.tz.guess()` 调用时 `tz` 未定义。修复方案：① `sideEffects: ["./dist/vendor/**/*.js"]` ② 延迟 getter 替代模块顶层调用。PR 范围 ~20行/2文件，AI 可行性 95%。❌ **无 Algora 赏金（API 返回 404）**。建议：可提交为社区贡献（建立 cal.com 声誉），或等 bounty 标签出现后再认领。报告见 `reports/cal29341-precheck-2026-05-14-2102.md`
19. **长期改进**: 
    - 修复 Algora 扫描质量：当前在 Description/Bounty 字段上误报严重（5/5 不合规）
    - 将 Algora 扫描加入机会雷达的日常管线
