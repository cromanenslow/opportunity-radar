# Pre-check: Expensify/App#90693 [$250]

## 概要评分
- **AI 可行性**: ⭐⭐⭐⭐☆ (4/5)
- **复现清晰度**: ⭐⭐⭐⭐⭐ (5/5)
- **竞争状况**: 🔴 高 (High)
- **推荐投入**: ❌ 否 (竞争过于激烈,时间窗口已关闭)

---

## Issue 详情

| 项目 | 内容 |
|------|------|
| **URL** | https://github.com/Expensify/App/issues/90693 |
| **标题** | [$250] Onboarding - Setup specialist has the onboarded user's email and a fallback avatar |
| **赏金** | $250 (通过 Upwork,非 Expensify tipping) |
| **标签** | `Bug`, `External`, `Help Wanted`, `Daily` |
| **创建时间** | 2026-05-14 15:43 UTC (~9 小时前) |
| **Assignee** | @ZhenjaHorbach (C+ 审核人,非开发者) |
| **PR 数量** | 0 |
| **评论数** | 13 (含 6 个详细提案) |

### 复现步骤 (清晰度: 5/5)
1. 进入 staging.expensify.com (OldDot)
2. 选择 "Manage my company's expenses (10+)"
3. 用 `[anything]@tstsg.com` 格式注册
4. 点击 "Get Started" 完成注册
5. 跳转到 NewDot 后,选择 51-100 - QBO - 完成 onboarding
6. 在 #admins 房间查看 setup specialist 的邮箱和头像

**Expected**: Setup specialist 显示为 `qa.guide@team.expensify.com` 且头像为真实头像
**Actual**: Setup specialist 显示为新 onboarding 用户的邮箱 + 默认占位头像

**证据**: 附有视频复现,影响 iOS/Windows Chrome/MacOS Chrome+Safari

---

## AI 可行性分析

### 1. Bug 类型: ✅ 纯前端逻辑 Bug
- 非环境搭建问题,非后端问题
- 纯 React Native / Onyx 状态管理竞态条件

### 2. 根因明确
多个提案(含官方 MelvinBot)已精确定位:
```
prepareOnboardingOnyxData() 中:
1. Onyx.merge() 异步写入 setup specialist 个人详情
2. 下一行立即同步调用 buildOptimisticAddCommentReportAction()
3. 该函数从模块级变量 allPersonalDetails[...] 同步读取
4. Onyx.merge 尚未 flush → allPersonalDetails 为 undefined
5. displayName 回退到 currentUserEmail → 显示 onboarding 用户的邮箱
6. avatar 回退到 undefined → 显示默认占位头像
```

同时 `CONST.SETUP_SPECIALIST_LOGIN = 'Setup Specialist'` 是显示字符串而非真实邮箱,导致 `generateAccountID()` 生成无对应的虚假 accountID,后端永远无法匹配。

### 3. 修改范围: 小 (2-10 行代码)
- **方案 A** (MelvinBot/trasnake87): 向 `buildOptimisticAddCommentReportAction` 传递 `actorDisplayName` + `actorAvatar` 参数,消除竞态
- **方案 B** (mukhrr/dilshodmackbook-sketch/aswin-s): 将 `CONST.SETUP_SPECIALIST_LOGIN` 替换为 `CONST.EMAIL.QA_GUIDE`,使用已知的 `CONST.ACCOUNT_ID.QA_GUIDE`
- **方案 C** (wildan-m): 在 `prepareOnboardingOnyxData` 中构造后直接覆盖 `person[0].text` 和 `avatar`

任何方案改动都在 `src/libs/ReportUtils.ts` 单一文件中,影响范围小。

### 4. AI 验证能力: ⚠️ 部分可行
- **代码逻辑验证**: ✅ AI 可以通过审查代码确认竞态条件被消除
- **E2E 功能验证**: ❌ 需要本地运行 Expensify App + 完整 onboarding 流程 + 特殊测试邮箱 @tstsg.com
- **CI 测试**: ✅ 项目有自动化测试,AI 可运行

### 5. 已有参考实现
- wildan-m 已提供 compare branch: `main...wildan-m:App:wildan/90693-onboarding-guide-display`
- MelvinBot 提供了完整提案和代码 diff
- 6 个提案都包含具体代码修改

---

## 竞争分析 🔴 高

### 提案竞争格局

| 提案人 | 时间 | 方案类型 | 状态 |
|--------|------|---------|------|
| **MelvinBot** (官方) | 15:49 UTC | 传递 actorDisplayName/actorAvatar 参数 | 第一个提案,有 Next Steps |
| **mukhrr** | 15:49 UTC | 替换 fallback 为 QA_GUIDE | 被要求修改格式 |
| **dilshodmackbook-sketch** | 15:50 UTC | 替换 fallback 为 QA_GUIDE | 被要求修改格式,已更新 |
| **wildan-m** | 15:51 UTC | 构造后直接覆盖 person/avatar | **有 compare branch + 实现代码** |
| **aswin-s** | 15:52 UTC | 替换 fallback 为 QA_GUIDE | 完整分析 |
| **trasnake87** | 15:54 UTC | 扩展 builder 参数 | 最详细分析,覆盖所有 3 个 action |

### 关键竞争风险
1. **提案过多**: 已有 6 个详细提案,每个都有完整根因分析和代码 diff
2. **有实现代码**: wildan-m 已提供 compare branch,可直接转为 PR
3. **官方已介入**: MelvinBot 自动生成了提案,且有 C+ 已分配审核
4. **时间窗口**: Issue 创建仅 9 小时,但已经有 13 条评论,节奏极快
5. **新提案需有实质性差异**: 根据 CONTRIBUTING.md,新提案必须与现有提案有重要、有意义或实质性的区别

### 建议
此时再提交 AI 生成的提案,很难与现有 6 个提案形成实质性区别。如果 MelvinBot 的提案被采用(它是第一个),竞争就结束了。wildan-m 已经有可运行的 compare branch,是当前最领先的竞争者。

---

## Expensify Tipping 确认

- 该 issue 使用 **Upwork** 支付($250),而非 Expensify tipping
- Expensify tipping 仅适用于成为贡献者 18 个月以上且完成 ≥5 个 job 的 contributors
- 流程: Proposal 被选中 → Upwork 雇佣 → 写代码 → PR 合入 → 部署到生产 7 天后付款
- 通过 CONTRIBUTING.md 确认了完整流程

---

## 推荐决策: ❌ 不投入

### 理由
1. **竞争过于激烈**: 6 个提案已提交,含 MelvinBot 官方自动提案 + wildan-m 可运行代码
2. **时间窗口已基本关闭**: Issue 创建后 9 小时内已有 13 条评论,节奏极快
3. **差异化空间极小**: 根因单一(竞态条件 + fallback 字符串),修复方案有限,已有提案覆盖了所有可行路径
4. **投入产出比低**: 即使 AI 能快速生成提案,被选中的概率远低于 10%

### 如果仍要尝试 (有条件推荐)
- **唯一可能的差异化角度**: 将方案 A(消除竞态)和方案 B(替换 fallback)结合起来,提出一个既解决竞态又解决 accountID 不一致的综合方案
- **必须在 2 小时内提交**,并附上完整可运行的 fork/PR
- **风险提示**: 即使提交了,MelvinBot 的官方提案有优先权

---

## 附录: 关键文件引用

- `src/libs/ReportUtils.ts` L11691-L11713: prepareOnboardingOnyxData 中的竞态代码
- `src/libs/ReportUtils.ts` L6337-L6345: buildOptimisticAddCommentReportAction 中的 allPersonalDetails 同步读取
- `src/CONST/index.ts` L8771: `SETUP_SPECIALIST_LOGIN = 'Setup Specialist'`
- `src/CONST/index.ts` L3187-L3189: `ACCOUNT_ID.QA_GUIDE = 14365522` (已存在)
- `src/CONST/index.ts` L194: `EMAIL.QA_GUIDE` (已存在)
