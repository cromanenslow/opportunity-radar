# 扫描报告 — 2026-05-16 10:02 中午扫描

## 扫描概要
- **命令**: `python radar.py scan`（全量扫描）
- **时间**: 2026-05-16 10:02 CST
- **上次全量扫描**: 2026-05-16 06:30 CST（约 3.5 小时前）
- **产出来源**: `reports/candidates_2026-05-16.json`（本次扫描覆盖原文件）
- **赚钱候选**: 3 个
- **练手候选**: 10 个（RustChain token 任务）
- **跳过**: 1 个（安全任务无 PoC）
- **管线状态**: 🔴 管线仍枯竭 — 无新的未分配 $250+ bounty issue

---

## 扫描范围

### 平台赏金扫描
| 平台 | 状态 | 结果 |
|------|------|------|
| Algora | ❌ API 不可用 (Phoenix LiveView) | 降级搜索 → 0 个 |
| Algora-GitHub | ⚠️ | 0 个 |
| IssueHunt | ❌ API 不可用 (SPA 架构) | 降级搜索 → 20 个 (Scottcjn/RustChain tokens) |
| OnlyDust | ❌ 无响应 | 0 个 |
| Huntr | ❌ 无响应 | 0 个 |

### GitHub Issue 搜索
- 6 个搜索策略执行（help-wanted, documentation, bug）
- TypeScript + Python 技术栈
- 共 60 个新原始 issue 找到

### 已知赏金仓库热区扫描 (52 个仓库)
- **Proven-payer 始终扫描**: 11 个（Expensify/App, tscircuit/*, twentyhq/twenty, oppia/oppia, home-assistant/core, mattermost/mattermost, supabase/supabase, directus/directus, appsmithorg/appsmith）
- **轮换补充**: 0/41 个
- **热区新增候选**: 31 个
- **本轮热区仓库产出明细**:
  - 📡 Expensify/App → 3 个新 issue
  - 📡 tscircuit/schematic-trace-solver → 1 个新 issue
  - 📡 tscircuit/tscircuit-autorouter → 3 个新 issue
  - 📡 twentyhq/twenty → 3 个新 issue
  - 📡 oppia/oppia → 3 个新 issue
  - 📡 home-assistant/core → 3 个新 issue
  - 📡 mattermost/mattermost → 3 个新 issue
  - 📡 supabase/supabase → 3 个新 issue
  - 📡 directus/directus → 3 个新 issue
  - 📡 appsmithorg/appsmith → 3 个新 issue
  - 📡 strapi/strapi → 3 个新 issue（含 gh 查询错误不影响结果）

### 白名单定向扫描
- 20 个高优先级仓库 + 44 个热区补充仓库
- 白名单新增: 5 个（eslint/eslint）
- 白名单扫描后总计: 106 个候选 issue
- 过滤陈旧 issue: 20 个超过 90 天（高赏金例外）

---

## Top 3 赚钱候选

### #1 — home-assistant/core#170853 [$100]
- **标题**: Gemini ai TTS still not available in chinese
- **URL**: https://github.com/home-assistant/core/issues/170853
- **分值**: 56.4 | **期望价值**: $22.56/hr
- **赏金**: $100 (sponsor — 未确认)
- **竞争**: 🟢 极低
- **评估**: 🟡 Home Assistant 无正式赏金计划，$100 为 sponsor 推断值。该 issue 发布于 ~40 分钟前，极新。问题较明确（中文 TTS 不可用），适合 AI 处理。无 assignee，无 linked PR。
- **建议**: 可尝试，但需先人工确认 sponsor 支付意愿。

### #2 — home-assistant/core#170850 [$100]
- **标题**: hassio.backup_partial allows backs up to external storage drive rather than the hosts backup drive
- **URL**: https://github.com/home-assistant/core/issues/170850
- **分值**: 56.4 | **期望价值**: $22.56/hr
- **赏金**: $100 (sponsor — 未确认)
- **竞争**: 🟢 极低
- **评估**: 🟡 备份功能相关，涉及外部存储驱动 vs 主机备份驱动。问题约 1.2 小时前发布。无 assignee，无 linked PR。AI 适配度尚可（75分），但需理解 Home Assistant 备份架构。
- **建议**: 需要人工评估技术复杂度，备选方案。

### #3 — home-assistant/core#170849 [$100]（本轮第三次出现）
- **标题**: ZHA: Zigbee network congestion with burst commands causing lost/dropped commands on large mixed-manufacturer networks
- **URL**: https://github.com/home-assistant/core/issues/170849
- **分值**: 56.4 | **期望价值**: $22.56/hr
- **赏金**: $100 (sponsor — 未确认)
- **竞争**: 🟢 极低
- **评估**: 🟡 该 issue 仍保持未分配。上次扫描（06:30）即在 Top 3 中。Zigbee 网络拥塞问题，技术门槛较高。无 assignee。
- **建议**: 技术复杂度高，优先考虑 #170853 或 #170850。

---

## $250+ 候选检查结果

| Issue | 赏金 | 状态 |
|-------|------|------|
| Expensify/App#89064 | $250 | ❌ 已分配（上次扫描已确认） |
| 其他 | — | 无新的 $250+ 候选 |

**结论**: 本轮扫描未发现新的未分配 $250+ bounty issue。

### Expensify/App 热区扫描详情
- **新发现 issue 数**: 3 个
- **其中 $250 未分配**: ❌ 0 个
- **上次 $250 候选 Expensify/App#89064**: 已从赚钱榜移除（雷达正确识别为已分配）
- **Expensify Watcher `state.json` 最后检查**: 2026-05-16 01:35 UTC (09:35 北京)
- **Watcher 已追踪 issue**: #89799, #90533, #90693（均非未分配 $250）

---

## 对比上次扫描 (2026-05-16 06:30)

| 指标 | 上次 (06:30) | 本次 (10:02) | 变化 |
|------|-------------|-------------|------|
| 赚钱候选 | 3 个 | 3 个 | → 持平 |
| 练手候选 | 10 个 | 10 个 | → 持平 |
| $250+ 未分配 | 无 | 无 | → 持平 |
| 管线状态 | 🔴 枯竭 | 🔴 枯竭 | → 持平 |

### 赚钱候选变化明细
| Issue | 上次 | 本次 | 变化原因 |
|-------|------|------|----------|
| home-assistant/core#170846 [$100] | ✅ Top 1 | ❌ 移除 | 可能已分配/关闭/超过过滤阈值 |
| Expensify/App#89064 [$250] | ✅ Top 2 (误判) | ❌ 移除 | ✅ 雷达正确过滤（已有 assignee） |
| home-assistant/core#170849 [$100] | ✅ Top 3 | ✅ Top 3 (重新) | 保持未分配 |
| home-assistant/core#170853 [$100] | — | ✅ 新增 (Top 1) | 新 issue（~40 分钟前） |
| home-assistant/core#170850 [$100] | — | ✅ 新增 (Top 2) | 新 issue（~1.2 小时前） |

### 热区对比变化
| 指标 | 上次 (06:30) | 本次 (10:02) |
|------|-------------|-------------|
| 扫描仓库数 | 32 个 | 52 个（热区二期扩容+20） |
| 热区新增候选 | 28 个 | 31 个 |
| Proven-payer 始终扫描 | 8 个 | 11 个 |
| 总候选数（过滤前） | 101 个 | 106 个 |

---

## 管线枯竭状态

| 指标 | 值 |
|------|-----|
| 今日新增赚钱候选 | 3 个（但均为 $100 推断值，非确认赏金） |
| 今日新增练手候选 | 10 个（RustChain token 任务，0 价值） |
| 热区新增 issue | 31 个 |
| 管线状态 | 🔴 **枯竭** — 无新的可执行的 $250+ 未分配 issue |
| 关键发现 | 3 个赚钱候选全部来自 home-assistant/core，为 sponsor 推断值（非确认赏金） |

---

## Top 3 候选简要评估

### 🥇 home-assistant/core#170853 — Gemini AI TTS 中文不可用
- **赏金确定度**: 🟡 低（sponsor 推断 $100，非确认）
- **AI 适配度**: 🟢 高（75分）— 明确的功能请求，配置/API 调用类问题
- **技术复杂度**: 🟢 中等 — TTS 引擎配置 + 简体中文语言包
- **竞争风险**: 🟢 极低（竞争分 100，极新 issue）
- **人工确认需求**: ✅ 需要确认 sponsor 是否有 $100 预算
- **结论**: 最佳候选，但需人工 gate 确认支付

### 🥈 home-assistant/core#170850 — 备份存储路径问题
- **赏金确定度**: 🟡 低（sponsor 推断 $100）
- **AI 适配度**: 🟢 较高（75分）
- **技术复杂度**: 🟡 中高 — 涉及 Home Assistant 备份系统和存储架构
- **竞争风险**: 🟢 极低
- **结论**: 可行但需要深入理解 HA 备份机制，排第二

### 🥉 home-assistant/core#170849 — Zigbee 网络拥塞（持续出现）
- **赏金确定度**: 🟡 低（sponsor 推断 $100）
- **AI 适配度**: 🟡 中等（75分但技术深度大）
- **技术复杂度**: 🔴 高 — Zigbee 协议栈、网络调试、制造商兼容性
- **竞争风险**: 🟢 极低（多次扫描仍未分配，可能因为难度）
- **结论**: 技术门槛高，不建议优先投入

**总体评估**: 三轮扫描（00:02, 06:30, 10:02）均显示管线枯竭。唯一真正 $250 的 issue 已分配。3 个赚钱候选均来自 home-assistant/core，赏金为推断值，实际 payout 不确定。建议人工关注 Expensify/App 是否有新的 $250 无 assignee issue 出现。

---

## 已知问题
1. **所有赚钱候选赏金为推断值**: home-assistant/core 无正式赏金计划，$100 基于 sponsor 标签推断
2. `gh` CLI 搜索查询引用错误 — calcom/cal.com, All-Hands-AI/OpenHands, Expensify/App, tscircuit/* 的复合查询失败，但不影响单独热区扫描结果
3. Algora/IssueHunt/OnlyDust/Huntr API 均不可用 — 持续依赖 GitHub 降级搜索
4. 管线连续三次扫描枯竭 — 需考虑扩大热区表或调整扫描策略

---

## 文件创建/修改
- `reports/candidates_2026-05-16.json` — 被本轮扫描覆盖更新
- `reports/scan-2026-05-16-midday.md` — 本报告（新创建）
