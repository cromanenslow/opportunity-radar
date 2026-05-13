# 深度预检报告：Expensify/App#88700

**Issue**: [$250] Android - App crashes reopening while the GPS trip is in progress after discard tracking twice
**URL**: https://github.com/Expensify/App/issues/88700
**预检日期**: 2026-05-14
**评估人**: Hermes Agent (自动预检)

---

## 1. 基本信息

| 字段 | 值 |
|------|-----|
| **赏金** | $250 |
| **类型** | Bug |
| **状态** | OPEN |
| **创建时间** | 2026-04-24 (距今约20天) |
| **标签** | `External`, `Daily`, `Help Wanted`, `Overdue`, `Bug` |
| **Assignee** | @truph01 (External 贡献者) |
| **平台限定** | Android-only（iOS 无法复现） |
| **设备** | Android 13 / Xiaomi Poco F5 |

## 2. Issue 活跃度分析

### 时间线
- **2026-04-24** — Issue 创建；MelvinBot 自动提案；twilight2294 和 15antonian 提交人工提案
- **2026-04-27** — mearaj 提交提案；truph01 询问复现步骤；twilight2294 回应"与 OP 一致"
- **2026-04-30 ~ 05-13** — 连续多轮 MelvinBot 自动催办（overdue）；truph01 回应"还在尝试复现"
- **2026-05-08** — 赏金已从 $50 涨至 $250（"Last Price Increase: 2026-05-08"）
- **2026-05-14** — 当前状态：仍无提案被批准，无 PR

### 维护者响应
- @truph01 作为 External assignee，20 天内未批准任何提案
- 多次逾期催办后仍表示"trying to reproduce it"
- **危险信号**：维护者本人无法稳定复现该 bug

## 3. 竞争分析

### 已提交提案 (4个)

| 提交者 | 提案日期 | 方案概要 | 状态 |
|--------|----------|---------|------|
| **MelvinBot** (自动) | 04-24 | 修复 Android 原生层：在 `GpsTripService.onTaskRemoved()` 中结束 Airship LiveUpdate；`GpsLiveUpdateHandler.onUpdate()` 加 try-catch；移除重复的 `checkAndCleanGpsNotification()` 调用 | 模板化提案，待审 |
| **twilight2294** | 04-24 | JS 层修复：`backgroundLocationTrackingTask` 中增加 null/`isTracking` 守卫；`useUpdateGpsTripOnReconnect` 加可选链；`GPSDraftDetailsUtils` 修复不安全访问 | 待审 |
| **15antonian** | 04-24 | 在 Discard 确认处理器中先调用 `stopGpsTripUtil()` 再清空 Onyx（已有 compare branch） | 待审，最详细 |
| **mearaj** | 04-27 | 修补 `expo-task-manager` 依赖，在原生 `TaskJobService` 路径加防御性异常处理 | 待审 |
| hanif-2000 | 04-24 | 提交了重复提案，被 ProposalPolice 自动撤回 | ❌ 已撤回 |

### 竞争强度评估：🟡 中高
- 4 个提案（1 个自动 + 3 个竞争者）
- 15antonian 已有 compare branch（最快可提 PR）
- twilight2294 和 mearaj 持续在 issue 中活跃等待
- 目前无人被正式 assign 来实施

## 4. 技术分析

### 技术栈
- **主框架**: React Native (TypeScript ~48MB 代码量)
- **Android 原生**: Kotlin/Java
- **关键依赖**: Expo TaskManager, Airship (Urban Airship) SDK, Onyx (状态管理)
- **相关核心文件**:
  - `.kt`: `GpsTripService.kt`, `GpsLiveUpdateHandler.kt`
  - `.tsx`: `GPSTripStateChecker/index.native.tsx`, `GPSButtons/index.tsx`
  - `.ts`: `GPSDraftDetails.ts`, `GPSDraftDetailsUtils.ts`, `useUpdateGpsTripOnReconnect.ts`
  - 后台任务: `backgroundLocationTrackingTask/index.native.ts`

### 根因分析（多理论）

| 理论 | 根因 | 修复范围 | 可靠性 |
|------|------|---------|--------|
| **MelvinBot**: Airship LiveUpdate 在 app kill 后未清理 | 原生 Kotlin | 小（2-3 文件） | 可能是必要条件但不是充分条件 |
| **twilight2294**: 后台任务写入了不完整的 Onyx 数据 | TS + Kotlin | 中（3-4 文件） | 与具体复现步骤吻合度较高 |
| **15antonian**: Discard 未停止位置更新 → 后台任务回写部分数据 | TS | 小（1-2 文件） | 与复现步骤高度吻合，逻辑链完整 |
| **mearaj**: Expo TaskManager 原生 JobService 崩溃 | Kotlin patch | 中（dependency patch） | 解释了 crash loop，但可能是下游表现而非根因 |

### 修复难度评估：🟡 中等

**难度系数：3.5/5**
- 需要理解 Android 前台服务生命周期、Expo TaskManager 调度机制
- 需要熟悉 Expensify 特有的 Onyx 状态管理模式
- 需要 Airship SDK 知识
- **AI 可辅助度**: 中高 — 只要给出清晰的文件路径和上下文，AI 可以分析代码路径并生成修复代码

**关键风险**：
1. ⚠️ Bug 可能高度依赖于 Android 厂商版本（MIUI/Xiaomi 上可复现，其他设备可能不同）
2. ⚠️ assignee 自己无法复现 → 提案审查可能延迟或被拒
3. ⚠️ 多个根因理论并存，真正的修复可能需要组合方案

## 5. 盈利分析

| 维度 | 评估 |
|------|------|
| **赏金** | $250 |
| **预期投入时间** | 8-20 小时（含环境搭建、复现、代码审查、PR 流程） |
| **时薪预期** | $12.5-$31.25/hr（低于系统评分的 $49.95/hr） |
| **支付方式** | Tipping（非 Upwork 合同制） |
| **风险调整后时薪** | 🟢 $15-20/hr（如果能快速通过提案阶段） |

**最大风险**：时间成本不可控。如果 assignee 继续拖延，可能数周后才能合并 PR。

## 6. 进入壁垒分析

| 壁垒 | 评级 | 说明 |
|------|------|------|
| 环境搭建 | 🟡 中 | 需要 Android 开发环境 + 物理 Android 设备（模拟器可能无法复现） |
| 复现难度 | 🔴 高 | assignee 自己 20 天都没能稳定复现 |
| 提案竞争 | 🟡 中 | 已有 3 个活跃竞争者，且 15antonian 已有 compare branch |
| 审批速度 | 🔴 慢 | 20 天零审批进展，多次 overdue |
| 代码审查标准 | 🟡 中 | Expensify 有标准化的 PR 流程和 contributor 指南 |

## 7. 综合评估与建议

### 结论：⚠️ 暂缓 (Defer)

### 决策矩阵

| 因素 | 权重 | 评分 (1-5) | 加权 |
|------|------|-----------|-------|
| 赏金吸引力 | 20% | 2 ($250 较低) | 0.4 |
| 技术可行性 | 25% | 3 (可做但需 Android 环境) | 0.75 |
| 竞争强度 | 20% | 3 (3 个竞争者，但都不是正式 assignee) | 0.6 |
| 审批效率 | 20% | 1 (20 天零进展) | 0.2 |
| 复现确定性 | 15% | 1 (assignee 无法复现) | 0.15 |
| **总分** | **100%** | | **2.1/5** |

### 不建议立即投入的原因

1. **🔴 核心风险：Assignee 无法复现** — @truph01 明确说"still trying to reproduce"，这是个巨大红旗。即使你提交了完美的提案和 PR，如果 reviewer 无法验证修复，合并流程会无限期阻塞。
2. **🔴 审批停滞** — 20 天零进展，多次 overdue 催办，表明这个 issue 在 Expensify 内部优先级很低。
3. **🟡 竞争拥挤** — 3 个有质量的提案在排队，15antonian 已经有了 compare branch。现在进入是追赶而不是领跑。
4. **🟡 根因不确定** — 4 种不同的根因理论，真正的修复可能需要组合方案，增加风险。
5. **🟡 $250 偏低** — 考虑到需要 Android 物理设备 + 多轮代码审查，实际时薪可能不到 $20/hr。

### 如果仍要投入，建议策略

如果决定尝试，建议：
1. **不要提交通用提案** — 直接 fork 并实现 15antonian 的方案（最完整、最小改动），或组合方案（JS 层 + Kotlin 层）
2. **提供一个可直接运行的 PR** — 附带 Android 复现视频证据
3. **在提案中强调"已实现可工作修复"** — 与 twighlight2294 和 mearaj 区分开来
4. **时间预算控制在 8 小时内** — 超过 8 小时立刻止损

### 替代推荐

同项目中性价比更好的 candidate：
- 寻找 assignee 响应迅速的 issue（External + Help Wanted，无 Overdue 标签）
- 寻找 JS-only 的 bug（不需要 Android 物理设备调试）
- 寻找赏金 ≥ $500 的 issue（投入产出比更高）
- 或关注 `payout-unknown` 但维护者活跃的 issue

---

*报告结束。本预检由 Hermes Agent 自动完成，仅供参考。*
