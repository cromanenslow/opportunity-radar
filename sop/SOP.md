# Opportunity Radar - SOP（标准作业流程）

## 概述

人类可介入的 AI 代理流水线，每天 15 分钟审批。
核心原则：**不是全自动赚钱机器人，是筛选+执行+闸门的协作系统。**

---

## 每日流水线

```
06:00  自动扫描 → 打分 → 生成 Top N 候选
06:15  人类审批（15分钟闸门）
06:30  Agent 执行获批任务
持续   跟进 CI / review
收盘   记录复盘数据
```

---

## 闸门设计（人类介入点）

### 闸门 1：每日候选审批 ⏰ 15分钟

**输入**：Top 3-5 候选任务（已打分，含评分详情）
**人类动作**：
- ✅ 批准执行 / ⏸️ 暂存 / ❌ 拒绝
- 可调整预估时间
- 可添加备注

**自动规则**：
- 非安全任务，评分 ≥ 65：自动批准
- 安全任务：**必须人工批准**（无例外）
- 评分 < 40：自动跳过
- 评分 40-65：待审批

### 闸门 2：安全任务审批 🛡️ 强制

**触发条件**：任务标签含 `security` / `vulnerability` / `cve`
**硬性规则**：
- ❌ 无 PoC → 不提交（curl 教训）
- ❌ 无授权范围 → 不提交
- ✅ 有 PoC + 有 scope + 人工批准 → 可以提交

### 闸门 3：PR 提交前检查 📋

**自动检查**：
- [ ] 测试通过
- [ ] Lint 通过
- [ ] 没有引入新 warning
- [ ] 修改范围 ≤ 5 文件（大改动需人工）
- [ ] 有对应 test case

**人工确认**：
- PR 描述是否准确
- 是否需要 claim bounty

### 闸门 4：领赏确认 💰

**必须人工确认**：
- 领赏金额与预期一致
- 支付方式确认
- KYC/税务信息（如需要）

---

## 执行流程

### Step 1：发现候选
```
scanner → raw_issues + platform_bounties
```
- 每日自动扫描平台赏金 + GitHub issue
- 去重（URL + repo#issue）

### Step 2：打分
```
raw_candidates → scoring_engine → scored_candidates
```
- 每个候选算 EV 和总分
- 自动标记需要人工审批的安全任务
- 自动跳过无 PoC 安全报告

### Step 3：clone + 安装 + 跑测试
```
approved_candidate → clone → install → test
```
- 从白名单 repo 直接用已知命令
- 新 repo 需要自动探测 install/test 命令
- 测试不过 → 降分或跳过

### Step 4：复现 + 估时
```
test_pass → reproduce → estimate
```
- 按描述复现问题
- 评估修复时间
- 超过 4 小时 → 暂存，不自动开始

### Step 5：最小 patch + 测试
```
reproduced → patch → add_test → verify
```
- 最小修改原则
- 必须加 regression test
- 本地验证通过

### Step 6：开 PR
```
verified → push → create_pr → monitor_ci
```
- PR 描述模板化
- 关联原始 issue
- 提及 bounty（如有）

### Step 7：跟进 review
```
ci_pass → wait_review → respond → merge
```
- 48 小时无回复 → 一次 polite ping
- 7 天无回复 → 标记维护者冷漠，repo 降权

### Step 8：领赏 + 复盘
```
merged → claim → record → analyze
```

---

## 每日输出格式

```markdown
# Opportunity Radar - 日报 2026-05-11

## 候选任务 (Top 5)
| # | Repo | Issue | Score | EV | 类型 | 决策 |
|---|------|-------|-------|----|------|------|
| 1 | vercel/next.js | #12345 | 82 | $45/hr | bug | ✅ 批准 |
| 2 | fastapi/fastapi | #6789 | 75 | $30/hr | docs | ✅ 自动批准 |
| 3 | huntr/xxx | #100 | 55 | $80/hr | security | 🛡️ 需审批 |

## 进行中任务
| Repo | Issue | 状态 | 预计完成 |
|------|-------|------|----------|

## 今日复盘
- 合并: 1 | 提交: 2 | 拒绝: 0
- $/agent-hour: $32
- 累计合并率: 45%
```

---

## 避开清单

| 类型 | 原因 |
|------|------|
| 含糊的大 feature | 无验收标准 |
| 需要产品/审美判断 | 主观性强 |
| 无测试+复杂构建 | 高风险 |
| 维护者不活跃(>30天) | 等待成本 |
| 安全无 PoC | curl 教训，5% 确认率 |
| 安全无授权范围 | 合规风险 |

---

## 30 天淘汰机制

每月 1 号回顾：
- 合并率 < 20% 的渠道 → 降权
- 30 天无 PR 合并的 repo → 移出白名单
- EV 最低的 10% repo → 替换为新发现的 repo
- 新增 repo 需通过基础检查（测试可跑、维护者活跃）

---

## 紧急情况

- **维护者投诉**：立即停止该 repo 所有任务，人工介入
- **安全漏洞争议**：停止所有安全任务，人工审查所有待提交
- **CI 红灯**：暂停该 repo 新任务，排查
