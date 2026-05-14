# 深度预检报告：Expensify/App#87280

**Issue**: [$250] ND card column on reports for admins shows feed ID string, and not card program and last 4
**URL**: https://github.com/Expensify/App/issues/87280
**预检日期**: 2026-05-14
**评估人**: Hermes Agent (自动预检)

---

## 1. 基本信息

| 字段 | 值 |
|------|-----|
| **赏金** | $250 |
| **类型** | Bug |
| **状态** | OPEN |
| **创建时间** | 2026-04-07 (距今约37天) |
| **标签** | `External`, `Weekly`, `Help Wanted`, `Bug` |
| **Assignee** | @mananjadhav (C+ reviewer) |
| **评论数** | 34 |
| **提案数** | 6个独特贡献者提交提案 |

## 2. Issue 活跃度分析

### 时间线
- **2026-04-07** — Issue 创建；MelvinBot 自动提案；Abdullahtmk、wildan-m、samranahm 提交人工提案
- **2026-04-08 ~ 05-09** — 多轮催办；snakefood3232 多次提交重复提案被撤回
- **2026-05-02** — "Issue not reproducible during KI retests" (第一周)
- **2026-05-09** — "Issue not reproducible during KI retests" (第二周)
- **2026-05-14** — @mananjadhav: "I think it's safe to close this one out."

### 危险信号
- ⚠️ **两次 KI 回归测试均无法复现**
- ⚠️ **Assignee 本人建议关闭该 issue**
- ⚠️ **37 天零审批进展**

## 3. 竞争分析

| 提交者 | 提案日期 | 方案概要 | 状态 |
|--------|----------|---------|------|
| **MelvinBot** (自动) | 04-07 | 双管齐下：后端 Search API 返回友好名称 + 前端 Feed 名称映射 | 待审 |
| **Abdullahtmk** | 04-07 | 使用 `cardID` + `CARD_LIST` + `getCardDescriptionForSearchTable` 格式化 | 待审 |
| **wildan-m** | 04-07 | `TransactionItemRow` 中添加 `getBankName()` 解析和 `:` 检测 fallback | 待审，有 compare branch |
| **samranahm** | 04-07 | 改用 `PERSONAL_AND_WORKSPACE_CARD_LIST` 替代 `CARD_LIST` | 待审 |
| snakefood3232 | 04-08 | 多次重复提交，被自动撤回 | ❌ |

### 竞争强度评估：🟡 中
- 3个有质量的人工提案 + 1个自动提案
- wildan-m 已有 compare branch
- 但所有提案均未被批准，且 issue 面临被关闭风险

## 4. 技术分析

### 技术栈
- **主框架**: React Native (TypeScript)
- **关键组件**: `TransactionItemRow/index.tsx`, `CardUtils.ts`, `MoneyRequestReportTransactionList.tsx`
- **状态管理**: Onyx

### 根因分析
Admin 查看他人报告时，Card 列显示原始 Feed ID 而非友好名称。root cause 是 `customCardNames` 只包含当前用户自己的卡片，admin 无法通过 `cardID` 查找提交者的卡片名称。

### 修复难度评估：🟢 低
- 纯前端 TypeScript 修改
- 1-2 个文件改动量
- AI 可完全辅助

## 5. 盈利分析

| 维度 | 评估 |
|------|------|
| **赏金** | $250 |
| **预期投入时间** | 3-6 小时 |
| **时薪预期** | $42-$83/hr |
| **支付方式** | Tipping（Expensify 通过 Upwork 支付） |
| **风险调整后时薪** | 🟢 $30-50/hr（如果能快速合并） |

## 6. 综合评估

### 结论：🔴 不建议 (Skip)

**核心风险：**
1. **🔴 Issue 即将被关闭** — @mananjadhav 明确说 "safe to close"
2. **🔴 无法复现** — 两次 KI 回归测试均无法复现，这是致命问题
3. **🟡 37 天零审批进展** — Expensify 内部优先级极低

### 替代推荐
- 同一仓库的 `Expensify/App#90536` ($250) 更新，仍有竞争机会
- 关注 `home-assistant/core#170536` 无竞争

---

*报告结束。本预检由 Hermes Agent 自动完成，仅供参考。*
