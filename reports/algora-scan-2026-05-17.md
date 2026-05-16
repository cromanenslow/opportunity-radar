# Algora 赏金快速扫描报告

**任务**: Heartbeat 109 — Algora 赏金快速扫描  
**日期**: 2026-05-17 01:34 CST  
**扫描方式**: 直接 API + 降级策略  

---

## 1. Algora API 可用性检查

| 端点 | 结果 |
|------|------|
| `https://algora.io/api/bounties?status=open` | ⚠️ 返回 HTML (Phoenix LiveView) |
| `https://algora.io/api/v1/bounties` | ⚠️ 返回 HTML |
| `https://algora.io/api/open-bounties` | ❌ 400 Not Acceptable |
| `https://api.algora.io/v1/bounties?status=open&limit=20` | ❌ 301 Moved → 最终 406 Not Acceptable |
| `https://algora.io/api/graphql` | ❌ 404 Not Found |

**结论**: 🔴 **Algora 公开 REST API 不可用。** 平台已迁移到 Phoenix LiveView 架构，数据通过 WebSocket 实时加载，无 HTTP API 可用于抓取。

---

## 2. 降级策略扫描

通过 GitHub GraphQL API 搜索已知在 Algora 上发布赏金的仓库（`label:bounty is:open`）：

| 仓库 | 结果 |
|------|------|
| `tscircuit/schematic-trace-solver` | 0 个开放式 bounty issue |
| `tscircuit/tscircuit-autorouter` | 0 个开放式 bounty issue |
| `calcom/cal.com` | 0 个开放式 bounty issue |
| `keephq/keep` | 0 个开放式 bounty issue |

**降级扫描结果**: **0 个新赏金 issue。**

---

## 3. 现有候选管线 $100+ 扫描

通过 GitHub 搜索验证现有候选状态（2026-05-17 01:34）：

| 候选 | 上一次 | 状态 | $金额 | 变化 |
|------|--------|------|-------|------|
| vitejs/vite#22456 | 🟢 OPEN/无人 | 🟢 **OPEN/无人** | $100 | ↔ 无变化 |
| home-assistant/core#170880 | 🟢 OPEN/无人 | 🟢 **OPEN/无人** | $100 | ↔ 无变化 |
| home-assistant/core#170914 | 🆕 新候选 | 🟢 **OPEN/无人** | $100 (推断) | 🆕 新增 |
| strapi/strapi#26346 | 🆕 新候选 | 🟢 **OPEN/无人** | $75 (推断) | 🆕 新增 |
| strapi/strapi#26345 | 🆕 新候选 | 🟢 **OPEN/无人** | $75 (推断) | ⚠️ PR冲突风险 |
| Expensify/App (5x $250) | 🔴 全部有 assignee | 🔴 **全部有 assignee** | $250 | ↔ 无变化 |

---

## 4. 结论

### 🚫 无新的 Algora $100+ 可做候选

- Algora API 不可访问，降级策略也未找到新 bounty
- 现有最佳候选仍为 **vite#22456 ($100/推断)** 和 **HA#170880 ($100/推断)**
- 新候选 **HA#170914 ($100/推断)** 已在深度预检中评估

### 下次扫描建议

- Algora 扫描频率：保持每 6h 一次（API 短期内不太可能恢复公开访问）
- 考虑扩展降级搜索的已知仓库列表（添加更多使用 Algora 的仓库）
- 可尝试通过 Algora WebSocket 抓取（但需要深入逆向工程，暂不建议）

---

*报告结束。Algora API 不可用，降级扫描 0 新结果，管线无新增可做候选。*
