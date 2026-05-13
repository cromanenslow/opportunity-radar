# 机会雷达 KNOWLEDGE.md
最后更新：2026-05-14

## 项目名称与目标
**项目名称**：Opportunity Radar（机会雷达）
**项目目标**：多平台赏金/任务扫描 → 自动打分排序 → 本地预检 → 人类审批。第一阶段以赚取赏金为目标，AI 优先执行可验证、高确定性任务。

## 当前里程碑
### ✅ 已完成
- 多平台扫描：GitHub Issues、Algora、IssueHunt、OnlyDust、Huntr
- 打分引擎：5 维度权重评分（支付确定性 30% / 可验证性 25% / AI 适配度 20% / 维护者活跃度 15% / 上下文复用 10%）
- 白名单系统：100 初始仓库，stars 50-50000
- 任务追踪器：DeliveryTracker 记录候选→审批→预检→PR→付款全流程
- 每日扫描 & 日报：最后扫描 2026-05-14，发现 12 个候选

### 🔄 进行中
- 人工审批 Top 赚钱候选
- 本地预检流程验证

## 团队配置
| 角色 | 成员 | 职责 |
|------|------|------|
| CEO/审批 | Hermes（Evan-Pro） | 每日审批（15min），方向与边界 |
| 工程师 | AI Agent | 扫描、打分、本地预检执行 |

**当前无 Git 版本控制**，建议初始化 Git 仓库。

## 运行状态
- **最后扫描**：2026-05-14，扫描结果正常
- **发现候选**：12 个（2 money + 10 practice）
- **Top 赚钱候选**：
  1. **crosscompute/jupyterlab-crosscompute #39** — $6.55/hr (money lane)，评分 21.0
  2. **tscircuit/schematic-trace-solver #29** — $6.55/hr (money lane)，评分 21.0
- **进行中任务**：lugassawan/swe-workbench #164 — reviewing 状态
- **30天指标**：赚钱候选/天 0.1，预检通过率 0.0，合并率 0.0，$/agent-hour $0.0
- **技术栈**：Python（主编排脚本），TypeScript（备选）
- **版本控制**：❌ 无 Git

## 下一步方向
1. 考虑将 Expensify watcher 加入定期调度
2. 评估 crosscompute/jupyterlab-crosscompute #39 可行性
3. 运行本地预检流程验证候选可行性
4. 初始化 Git 版本控制，建立开发分支
5. 优化扫描精度，提升 money 候选发现率
6. 建立 KYC/税务过滤后的支付流水线
