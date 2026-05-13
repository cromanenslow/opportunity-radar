# 机会雷达 KNOWLEDGE.md
最后更新：2026-05-14

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
- **已知赏金仓库热区表**（2026-05-14 07:30）：29 个已验证赏金仓库（TypeScript 21 + Python 8），含 Expensify/App、tscircuit/*、oppia/oppia、calcom/cal.com 等 proven payer。配套 config.yaml（known_bounty_scan_limit=10）+ scanner/github.py 专用扫描函数（三层兜底策略），白名单扫描从 5→20 个仓库

### 🔄 进行中
- 人工审批 Top 赚钱候选
- 本地预检流程验证
- Expensify watcher 已通过 launchd 每1h执行（com.lflz.expensify-watcher），正常工作中

## 团队配置
| 角色 | 成员 | 职责 |
|------|------|------|
| CEO/审批 | Hermes（Evan-Pro） | 每日审批（15min），方向与边界 |
| 工程师 | AI Agent | 扫描、打分、本地预检执行 |

## 运行状态
- **最后扫描**：2026-05-14 06:32（UTC+8），竞争因子已集成并验证通过
- **发现候选**：79 个原始 → 66 可执行（1 money + 58 可执行 + 8 深度预检过滤 + 12 陈旧过滤）
- **赚钱榜 Top**：Expensify/App#88700 — 评分 58.0，$250 bounty，Android crash bug（pre-check 结论：⚠️ 暂缓 — assignee 20天无法复现，3竞争者）
- **练手池 Top**：
  1. **oppia/oppia #24807** — 评分 34.5，可自动化修复 pagination 组件显示问题
  2. **SolFoundry/solfoundry #861** — 评分 32.82，Bounty T3: Full Autonomous Bounty-Hunting Agent
  3. **vuetifyjs/vuetify #22376** — 评分 28.7，[Bug] iPad virtual keyboard causing VMenu position change
- **进行中任务**：lugassawan/swe-workbench #164 — reviewing 状态
- **30天指标**：赚钱候选/天 0.1，预检通过率 0.0，合并率 0.0，$/agent-hour $0.0
- **Expensify watcher**：✅ Python 脚本已创建，`com.lflz.expensify-watcher` 已通过 launchd 每小时自动执行，正常运行中；另存有 `com.user.expensify-watcher` 未加载
- **技术栈**：Python（主编排脚本），TypeScript（备选）
- **版本控制**：✅ Git 已初始化（1 commit），当前无远程仓库

## Pre-check Findings (2026-05-14)

### 1. crosscompute/jupyterlab-crosscompute #39 — "Detect cursor focus"
- **Bounty**: $100 (mentioned in issue body, no GitHub bounty label)
- **状态**: ✅ Open, Unassigned, 7 comments
- **要求**: JupyterLab extension modification — detect cursor/focus on shell tabs vs file browser, log paths accordingly
- **难度**: Easy-Medium — TypeScript JupyterLab extension, well-scoped, existing experiment code
- **AI可行性**: ✅ Yes — single `src/index.ts` modification, JupyterLab widget API
- **竞争状况**: ⚠️ 极高 — 仅2026-05-13一天就有4个PR提交 (#40, #41, #42, #43)，多人同时在抢
- **风险**: 高 — first-merged-wins模式，已有多个竞争者提交代码等待合并
- **维护者活跃度**: 中等 — invisibleroads创建了issue，但repo最后push是2025-04
- **结论**: ⚠️ **有条件可行** — 技术门槛低，但race condition极其严重。如果要投入，需要极快提交（< 24h内完成并PR）。建议观望1-2天看是否有PR被合并。

### 2. tscircuit/schematic-trace-solver #29 — "New Phase To combine same-net trace segments"
- **Bounty**: $100 (labeled 💎 Bounty + $100 on GitHub, also on Algora)
- **状态**: ✅ Open, Unassigned, 30 comments, 1 open PR (#290 by grantf04)
- **要求**: 实现新的pipeline phase，合并同一net中距离相近的trace segments
- **难度**: Medium-Hard — 需要理解PCB schematic trace solver的复杂pipeline架构
- **AI可行性**: ⚠️ 有条件 — TypeScript，但需要大量上下文理解现有solvers架构
- **竞争状况**: ⚠️ 极高 — 7+人/attempt，已有PR #290在队列中等待review
- **风险**: 极高 — 已有开放PR，如果grantf04的PR被合并则前功尽弃
- **维护者活跃度**: 高 — seveibar活跃，repo持续更新（最后push 2026-05-08），163 forks
- **结论**: ❌ **不建议投入** — 已有PR提交，多人竞争，复杂度高，AI需要大量时间理解代码库

### 3. tscircuit/schematic-trace-solver #66 (补充验证)
- **早报提及**$150 bounty，但实际是已关闭的PR（非open issue），saish9901提交后关闭但未合并
- **结论**: ❌ **不可用** — 非开放悬赏

### 总结建议
- 两个Top赚钱候选都面临**严重竞争**（多个PR已提交）
- 如果必须选择，**#39 (crosscompute)** 技术门槛低、更适合AI，但需极速执行
- **建议策略**：继续扫描新候选，同时关注这两个issue是否有PR被合并释放机会
- 可考虑降低star门槛以发现竞争较少的早期bounty

## 下一步方向
1. ✅ 竞争强度因子优化 — 已加入第6维度（权重15%），通过 gh issue view 获取 assignees/PR 数据
2. ✅ Expensify watcher launchd 调度 — 已通过 launchd 配置为每小时自动执行
3. ✅ 评估 crosscompute/jupyterlab-crosscompute #39 可行性 — 已做，竞争过高，暂缓
4. ✅ 2026-05-14 06:32 新扫描 + Expensify/App#88700 pre-check — 结论：暂缓（assignee 卡住）
5. ✅ 已知赏金仓库热区表（known-bounty-repos.yaml）— 29 个仓库，三层兜底扫描函数，白名单 5→20
6. 触发首次已知赏金仓库热区扫描，验证 money 发现率提升效果
7. 寻找下一个合适的 money 候选（$500+，JS/TS，竞争低，assignee 活跃）
8. 连接远程 Git 仓库，建立开发分支
9. 持续优化扫描精度，提升 money 候选发现率
10. 建立 KYC/税务过滤后的支付流水线
