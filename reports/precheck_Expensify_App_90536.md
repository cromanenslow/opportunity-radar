# 深度预检报告：Expensify/App#90536

**Issue**: [$250] Public room - Public room not display in LHN after anon user login from a thread of public room
**URL**: https://github.com/Expensify/App/issues/90536
**预检日期**: 2026-05-14
**评估人**: Hermes Agent (自动预检)

---

## 1. 基本信息

| 字段 | 值 |
|------|-----|
| **赏金** | $250 |
| **类型** | Bug |
| **状态** | OPEN |
| **创建时间** | 2026-05-13 (距今约1天) |
| **标签** | `External`, `Daily`, `Help Wanted`, `Bug` |
| **Assignee** | @hungvu193 (C+ reviewer) |
| **评论数** | 12 |
| **提案数** | 6个独特贡献者提交提案 |

## 2. Issue 活跃度分析

### 时间线
- **2026-05-13 16:20** — Issue 创建
- **2026-05-13 16:30** — MelvinBot 自动提案 + 4个人工提案（KJ21-ENG、MobileMage、aswin-s、trasnake87）
- **2026-05-13 16:38** — oqildev 提交提案
- **2026-05-14 00:20** — abbasifaizan70 提交提案
- **2026-05-14** — 当前状态：刚创建不到24小时，等待 C+ 审查

### 活跃度评估：🟢 极高
- 创建当天就有 6 个提案
- Daily 标签（意味着每天都要跟进）
- 已有 Upwork Job

## 3. 竞争分析

| 提交者 | 提案日期 | 方案概要 | 状态 |
|--------|----------|---------|------|
| **MelvinBot** (自动) | 05-13 | 在 SignInModal 中，sign-in 后调用 `joinRoom` 加入原本匿名浏览的 public room | 待审 |
| **KJ21-ENG** | 05-13 (已更新) | 记住 sign-in 来源 report ID，在 OpenApp 完成后 join 该 public room | 待审，已更新 |
| **MobileMage** | 05-13 | 在 `openReportFromDeepLink` 中同时 fetch parentReportID 确保 parent 在 Onyx 中 | 待审 |
| **aswin-s** | 05-13 (已更新) | 与 MobileMage 类似，使用 Onyx.connect 监听 thread 数据到达后 fetch parent | 待审 |
| **trasnake87** | 05-13 | SignInModal 中遍历所有 preserved public rooms，对缺少 participant entry 的调用 joinRoom | 待审 |
| **oqildev** | 05-13 | 在 `getOnyxDataForOpenOrReconnect` 的 preserve 阶段直接注入 participant + 调用 updateNotificationPreference | 待审 |
| **abbasifaizan70** | 05-14 | 在 SidebarUtils 中添加 `isPublicRoom` override + 在 ReportUtils 中排除 public room 的 empty-chat 隐藏 | 待审 |

### 竞争强度评估：🔴 高
- 7 个提案（1个自动 + 6个人工）
- 多种不同的修复方案
- 但尚未有提案被批准，无 PR

## 4. 技术分析

### 技术栈
- **主框架**: React Native (TypeScript)
- **关键文件**: `SignInModal.tsx`, `App.ts`, `SidebarUtils.ts`, `ReportUtils.ts`, `Link.ts`
- **关键概念**: Onyx 状态管理、anonymous→authenticated session 转换

### 根因共识
匿名用户浏览 public room 后 sign-in，OpenApp 虽然 preserves 了 public room 的 Onyx 数据，但 participant 映射中未包含新认证用户的 accountID，导致 LHN 过滤掉该 room。

### 修复难度评估：🟢 低-中
- TypeScript 纯前端修改
- 修改 1-2 个文件
- AI 可完全辅助

## 5. 盈利分析

| 维度 | 评估 |
|------|------|
| **赏金** | $250 |
| **预期投入时间** | 3-8 小时 |
| **时薪预期** | $31-$83/hr |
| **支付方式** | Tipping（Expensify 通过 Upwork 支付） |
| **风险调整后时薪** | 🟡 $20-40/hr（竞争激烈可能延迟） |

## 6. 综合评估

### 结论：🟡 可考虑 (Consider)

**优势：**
- 🟢 赏金明确 $250，刚发布
- 🟢 技术难度低，纯 TypeScript
- 🟢 Daily 标签，需要尽快推进

**风险：**
- 🔴 竞争极度激烈（6个竞争者）
- 🟡 刚发布不到24小时，C+ 尚未审查任何提案
- 🟡 payout-unknown（需要 Upwork + Expensify 账户注册）

### 建议策略
如果要参与：
1. 快速研究所有现有提案，找到未被覆盖的方案
2. 提供可直接运行的 PR（附带测试说明）
3. 在提案中明确区分与现有方案的不同

### 替代推荐
- `home-assistant/core#170536` 无竞争，优先级更高

---

*报告结束。本预检由 Hermes Agent 自动完成，仅供参考。*
