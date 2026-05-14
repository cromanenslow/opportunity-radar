# 机会雷达 · 审批摘要 2026-05-14

> 生成时间：2026-05-14 16:06 | 审批人：Tao | 预计耗时：5 分钟

---

## 赚钱榜 Top 3 候选评估

### ① ⭐ Expensify/App #90533 — $250 （优先关注）

| 维度 | 评估 |
|------|------|
| **问题描述** | Android 端粘贴含 `+` 别名的邮箱（如 `dreamnitethedragon+vegst@gmail.com`）到费用参与人选择器后，删除别名部分时 App 崩溃。React Native FlashList/Hermes regex 交互 Bug。 |
| **赏金** | **$250** — Upwork 支付。Expensify 是 proven payer，过去 $250 External 赏金均正常支付。支付确定性评分 70/100。 |
| **技术难度** | **中等** — React Native / TypeScript。有完整 crash log 和复现步骤。需搭建 RN 本地环境。 |
| **AI 可行性** | ⚠️ 中等 — 有 6+ 个已提交的提案可供参考，但需要理解 FlashList 渲染机制和字符串正则处理链。AI 可辅助生成修复但需要人工 review RN 原生兼容性。 |
| **竞争情况** | 🔴 **激烈** — 32 条评论，6+ 个活跃提案（yusufdeveloper2903, KJ21-ENG, mukhrr, aswin-s, Hossiy21 等），reviewer QichenZhu 已指派审阅提案。0 个 PR 但提案已进入评审。 |
| **风险** | 中 — 竞争饱和，Expensify 审阅严格（常多次拒绝提案），即使 AI 写出高质量修复也可能被其他人抢先。 |
| **建议** | **⚠️ 有条件投入** — 这是当前唯一 $250 真金白银机会。如果投入需：① 立即克隆仓库本地复现 ② 分析 6 个已提交提案的差异，找到未被覆盖的边界情况 ③ 24h 内提交差异化提案。否则容易被竞争淹没。 |

---

### ② home-assistant/core #170556 — Tuya battery_state

| 维度 | 评估 |
|------|------|
| **问题描述** | Tuya WSDCG 门磁传感器的电池状态（low/medium/high）不显示在 Maintenance 面板，因为缺少 `device_class: battery`。但电池值是文本型而非百分比，无法直接应用 device_class。 |
| **赏金** | **$100** — Sponsor 赞助支付。HA 是成熟开源项目，Sponsor 赏金体系稳定。支付确定性评分 80/100。 |
| **技术难度** | **中等** — Python。有 diagnostics JSON 数据。epenet 评论提示可通过 template sensor 映射为百分比作为 workaround，但真正修复可能需要修改 Tuya 集成的 battery state 映射逻辑。 |
| **AI 可行性** | ✅ **高** — Python 代码库，有 diagnostics 数据，修复方向明确（修改 Tuya 集成的 device class 映射或在 sensor 定义中补充）。AI 在 HA 集成开发上有不少训练数据。 |
| **竞争情况** | 🟢 **极低** — 仅 2 条评论（bot + epenet），0 assignee，0 PR，0 reactions。全新 issue（2026-05-14 创建）。 |
| **风险** | 低-中 — 主要风险是实际修复可能比表面更复杂（Tuya 集成涵盖大量设备类型，battery 映射需要兼容各种设备），以及 sponsor 可能不认可 quick fix。 |
| **建议** | **✅ 投入** — 低竞争、Python 生态、有诊断信息、修复方向明确。建议进入预检：克隆 HA 仓库，在 dev 环境验证 Tuya 集成 battery 映射逻辑，提交针对性 PR。 |

---

### ③ home-assistant/core #170549 — Verisure cookie

| 维度 | 评估 |
|------|------|
| **问题描述** | Verisure 集成每天凌晨 3:00 准时失效，出现 "Failed to read cookie" 错误。用户已尝试完全删除并重新添加集成，问题依旧。 |
| **赏金** | **$100** — Sponsor 赞助支付。与 #170556 相同。支付确定性评分 80/100。 |
| **技术难度** | **中-高** — Python。没有 diagnostics 数据，没有日志，仅描述"每天 3:00 准时出错"。需要理解 Verisure API 的 cookie 认证和刷新机制，可能涉及反向工程。 |
| **AI 可行性** | ⚠️ **低-中** — 缺少诊断信息，复现条件苛刻（需等凌晨 3:00），修复方向不明确。AI 在没有足够上下文的情况下较难定位问题。 |
| **竞争情况** | 🟢 **极低** — 0 条评论，0 assignee，0 PR，0 reactions。 |
| **风险** | 中-高 — 信息不足是最大风险。可能需要在用户环境中添加日志调试，反复沟通成本高。修复可能涉及 Verisure 的 session/cookie 管理重构，不确定 scope。 |
| **建议** | **⚠️ 暂缓** — 缺乏 diagnostics 和明确复现步骤，投入风险较高。建议：① 先看 HA Verisure 集成源码评估 cookie refresh 逻辑复杂度 ② 在 issue 中请求 reporter 提供完整诊断信息/日志 ③ 等补充信息后再决定是否投入。 |

---

## 全局概况

| 指标 | 值 |
|------|-----|
| 本轮扫描时间 | 2026-05-14 16:01 |
| 原始候选总数 | 103 → 106（可执行） |
| 赚钱榜候选 | **3 个**（1 Expensify + 2 Home Assistant） |
| 练习榜候选 | 10 个（均为 Scottcjn/Rustchain 生态，EV 负数 ❌） |
| 已 Preflight 并放弃 | 7 个（kyo#390, isaac#45, archestra#3858/3854/4464, tscircuit/core#2281, dsn-converter#54） |
| 进行中 | 0 |
| 已付款 | $0 |

## 决策矩阵

| 候选 | 建议 | 预期时薪 | 竞争 | AI可行 | 投入优先级 |
|------|------|---------|------|--------|-----------|
| Expensify/App #90533 | ⚠️ 有条件投入 | $49.95/h | 🔴 高 | ⚠️ 中 | **P1** ⭐ |
| HA/core #170556 | ✅ 投入 | $22.56/h | 🟢 极低 | ✅ 高 | **P2** |
| HA/core #170549 | ⚠️ 暂缓 | $22.56/h | 🟢 极低 | ⚠️ 低 | P3 |

## Tao 的 5 分钟决策指南

1. **先看 #90533**：如果愿意接受高竞争 + 严格审阅，立即进入预检。否则跳过。
2. **再看 #170556**：低风险 Python 修复，建议直接批准进入预检。
3. **#170549 暂缓**：等 reporter 补充信息后再看。
4. **练习榜 10 个候选全部放弃**：EV 均为负数（-0.8/h），RTC 代币价值不确定。

---

> ⚠️ **注意**：Expensify 的提交流程要求先通过 Upwork 申请 + 提案审核通过后才能提交 PR，无法直接开 PR。HA 的 Sponsor 流程则更灵活，提交 PR 后由 maintainer 决定是否支付。
