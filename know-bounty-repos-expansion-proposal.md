# 机会雷达 - 已知赏金仓库热区表扩充提案

> **日期**: 2026-05-14
> **当前热区表**: 29 个已验证赏金仓库
> **建议新增**: 20 个仓库
> **目标**: 弥补「赚钱真空」，优先 $500+ 且竞争低的仓库
> **KYC 约束**: 优选无需 KYC 的支付渠道（GitHub Sponsors / Algora / OpenCollective）

---

## 一、当前热区表分析

### 现有 29 个仓库分布

| 类别 | 数量 | 代表仓库 |
|------|------|----------|
| TypeScript / JS | 21 | Expensify/App, tscircuit/*, calcom/cal.com, supabase/supabase, twentyhq/twenty, n8n-io/n8n, appwrite/appwrite, plasmic-hq/plasmic, vercel/ai 等 |
| Python | 8 | oppia/oppia, apache/apisix, home-assistant/core, mattermost/mattermost, zama-ai/bounty-program 等 |

### 主要缺口

1. **Web3/DeFi 完全缺失** — 链上赏金（OnlyDust、Gitcoin）未覆盖
2. **大型安全赏金项目缺失** — VS Code、Electron、Grafana 等有正式赏金计划未收录
3. **前端/UI 框架类不足** — 仅 plasmic-hq/plasmic，ant-design、mermaid 等缺失
4. **AI/ML 社区项目缺失** — huggingface/transformers、dify 等有赞助赏金
5. **低竞争中型项目缺失** — immich、directus、appsmith 等活跃且竞争低

---

## 二、新增仓库提案（20 个）

### 2.1 TypeScript / JS — Web3 / DeFi（4 个）

```yaml
  # ==================== Web3 / DeFi (新增) ====================

  # Hardhat - 以太坊开发环境，Immunefi 赏金 + 开发赏金
  - repo: NomicFoundation/hardhat
    language: typescript
    labels: ["bounty", "help wanted", "bug"]
    bounty_type: "security"
    bounty_source: "immunefi"
    expected_bounty_range: [500, 50000]
    tags: ["web3", "defi", "high-value", "competitive"]
    competition: "high"
    notes: "Immunefi bug bounty $500-$50k。开发赏金通过 GitHub issues 发布。注意 KYC 门槛，但小型 bug 赏金可走 crypto。"

  # MetaMask - 最流行的加密钱包，Immunefi 赏金
  - repo: MetaMask/metamask-extension
    language: typescript
    labels: ["bounty", "help wanted", "bug"]
    bounty_type: "security"
    bounty_source: "immunefi"
    expected_bounty_range: [1000, 50000]
    tags: ["web3", "wallet", "high-value", "high-profile"]
    competition: "high"
    notes: "Immunefi bounty $1k-$50k。MetaMask 团队反应积极。KYC required for payout，但中型赏金 ($1k-$5k) 可通过 crypto 结算。"

  # Uniswap interface - 最大 DEX 前端，Immunefi 赏金
  - repo: Uniswap/interface
    language: typescript
    labels: ["bug", "help wanted"]
    bounty_type: "security"
    bounty_source: "immunefi"
    expected_bounty_range: [500, 25000]
    tags: ["web3", "defi", "frontend"]
    competition: "medium"
    notes: "Uniswap 前端 bug bounty $500-$25k。TypeScript/React 项目。适合前端安全研究者。Immunefi 平台需注意 KYC。"

  # Safe (Gnosis Safe) - 智能合约钱包，Immunefi 赏金
  - repo: safe-global/safe-contracts
    language: typescript
    labels: ["bug", "help wanted"]
    bounty_type: "security"
    bounty_source: "immunefi"
    expected_bounty_range: [1000, 100000]
    tags: ["web3", "defi", "smart-contracts"]
    competition: "high"
    notes: "Safe 多重签名钱包。高额 bug bounty。Solidity 合约 + TypeScript SDK。Immunefi 平台 KYC required。"
```

### 2.2 TypeScript / JS — 大型开源赏金项目（4 个）

```yaml
  # ==================== 大型开源赏金项目 (新增) ====================

  # VS Code - Microsoft 官方 Bug Bounty
  - repo: microsoft/vscode
    language: typescript
    labels: ["bug", "help wanted", "good first issue"]
    bounty_type: "security"
    bounty_source: "microsoft-bounty"
    expected_bounty_range: [5000, 15000]
    tags: ["microsoft", "high-profile", "editor"]
    competition: "medium"
    notes: "Microsoft Bug Bounty 计划 $5k-$15k。TypeScript 项目。虽需 KYC 但赏金高。另外有大量 help-wanted issues 可作为练手。"

  # Electron - 桌面框架安全赏金
  - repo: electron/electron
    language: typescript
    labels: ["bug", "security", "help wanted"]
    bounty_type: "security"
    bounty_source: "electron-bounty"
    expected_bounty_range: [1000, 20000]
    tags: ["framework", "desktop", "security"]
    competition: "low"
    notes: "Electron 官方赏金 $1k-$20k。TypeScript/C++ 混合。竞争相对低因为需要深入理解 Chromium/Node.js。KYC required。"

  # Grafana - 监控平台 HackerOne 赏金
  - repo: grafana/grafana
    language: typescript
    labels: ["bug", "security", "help wanted"]
    bounty_type: "security"
    bounty_source: "hackerone"
    expected_bounty_range: [500, 10000]
    tags: ["monitoring", "high-profile", "bug-bounty"]
    competition: "medium"
    notes: "Grafana HackerOne pgrogram $500-$10k。TypeScript/Go 项目。有安全研究团队响应积极。大量 Dashboard/Frontend 相关的 issue。KYC required for HackerOne payout。"

  # Discourse - 论坛软件 HackerOne 赏金
  - repo: discourse/discourse
    language: typescript
    labels: ["bug", "security", "help wanted"]
    bounty_type: "security"
    bounty_source: "hackerone"
    expected_bounty_range: [500, 5000]
    tags: ["forum", "bug-bounty", "well-established"]
    competition: "low"
    notes: "Discourse HackerOne pgrogram $500-$5k。Ruby/JS 混合但前端是 Ember.js。竞争低的细分市场。HackerOne KYC required。"
```

### 2.3 TypeScript / JS — 框架与库（6 个）

```yaml
  # ==================== 框架与库赏金项目 (新增) ====================

  # Directus - 无头 CMS，有 Algora 赏金
  - repo: directus/directus
    language: typescript
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "algora"
    expected_bounty_range: [50, 1000]
    tags: ["cms", "algora", "active", "low-competition"]
    competition: "low"
    notes: "Directus 使用 Algora 平台发放赏金。有 'bounty' 标签。TypeScript/Node 全栈项目。KYC not required (Algora)。非常适合 AI 编码。"

  # Appsmith - 内部工具构建器，明确赏金标签
  - repo: appsmithorg/appsmith
    language: typescript
    labels: ["💰 Bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [50, 500]
    tags: ["low-code", "active", "proven-payer", "low-competition"]
    competition: "low"
    notes: "Appsmith 有明确 '💰 Bounty' 标签。TypeScript/Java 混合。团队积极支付赏金。低竞争，适合批量完成任务。"

  # Payload CMS - 无头 CMS，有 bounty 标签
  - repo: payloadcms/payload
    language: typescript
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [100, 1000]
    tags: ["cms", "active", "growing"]
    competition: "low"
    notes: "Payload CMS 的 'bounty' 标签 issue。$100-$1000。TypeScript 全栈。高代码质量，测试充分。竞争低因为相对较新。"

  # Immich - 开源照片管理，活跃赞助赏金
  - repo: immich-app/immich
    language: typescript
    labels: ["bounty", "help wanted", "good first issue", "sponsor"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [50, 500]
    tags: ["photo", "active", "high-volume", "mobile"]
    competition: "low"
    notes: "Immich 是增长最快的开源项目之一。使用 GitHub Sponsors 发放赏金。TypeScript/Dart 混合。大量 good first issues。AI 友好的任务多。"

  # Mermaid - 图表生成，bounty 标签
  - repo: mermaid-js/mermaid
    language: typescript
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [50, 500]
    tags: ["diagram", "visualization", "active"]
    competition: "low"
    notes: "Mermaid 是流行的图表工具。有 'bounty' 标签 issue。TypeScript 项目。解析器/渲染器任务适合 AI。低竞争。"

  # Standard Notes - 加密笔记应用，赞助赏金
  - repo: standardnotes/app
    language: typescript
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [50, 500]
    tags: ["encryption", "notes", "active"]
    competition: "low"
    notes: "Standard Notes 端到端加密笔记。TypeScript/React 项目。GitHub Sponsors 支付赏金。有 'bounty' 标签 issue。代码架构清晰。"
```

### 2.4 TypeScript / JS — 其他活跃赏金项目（2 个）

```yaml
  # ==================== 其他活跃赏金项目 (新增) ====================

  # Strapi - 最流行无头 CMS 之一，赞助赏金
  - repo: strapi/strapi
    language: typescript
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [100, 1000]
    tags: ["cms", "high-profile", "proven-payer"]
    competition: "medium"
    notes: "Strapi 65k+ stars。GitHub Sponsors 赞助赏金。TypeScript/Node 全栈。有 'bounty' 标签。插件系统适合模块化任务。竞争中等。"

  # Documenso - 开源 DocuSign，Algora 赏金
  - repo: documenso/documenso
    language: typescript
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "algora"
    expected_bounty_range: [50, 500]
    tags: ["algora", "e-signature", "active", "low-competition"]
    competition: "low"
    notes: "Documenso 是开源电子签名平台。TypeScript/Next.js 项目。Algora 平台赏金。增长快速，竞争低。AI 编码友好。"
```

### 2.5 Python — 活跃赏金项目（4 个）

```yaml
  # ==================== Python 活跃赏金项目 (新增) ====================

  # Hugging Face Transformers - AI/ML，赞助赏金
  - repo: huggingface/transformers
    language: python
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [100, 2000]
    tags: ["ai", "ml", "high-profile", "high-volume"]
    competition: "medium"
    notes: "Hugging Face 是目前最活跃的 ML 项目。GitHub Sponsors 赞助。大量 good first issues。文档/测试/新模型支持任务。"💰 Bounty" 标签清晰。中等竞争但任务量大。"

  # Pydantic - 数据验证库，赞助赏金
  - repo: pydantic/pydantic
    language: python
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [100, 1000]
    tags: ["validation", "active", "well-maintained"]
    competition: "low"
    notes: "Pydantic V2 重写后持续活跃。有 GitHub Sponsors 赞助。Python 类型系统专家可做。低竞争但需要较深理解。"

  # ApeWorX/ape - Web3 开发框架，赞助赏金
  - repo: ApeWorX/ape
    language: python
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "github-sponsors"
    expected_bounty_range: [100, 3000]
    tags: ["web3", "python", "active", "growing"]
    competition: "low"
    notes: "Ape 是 Python 生态系统中的 Web3 开发框架。GitHub Sponsors 赞助。有明确 bounty 标签。竞争极低因为 niche。以太坊/Python 双技能要求。"

  # Celery - 分布式任务队列，OpenCollective 赏金
  - repo: celery/celery
    language: python
    labels: ["bounty", "help wanted", "good first issue"]
    bounty_type: "$bounty"
    bounty_source: "opencollective"
    expected_bounty_range: [50, 500]
    tags: ["task-queue", "established", "opencollective"]
    competition: "low"
    notes: "Celery 是成熟的分布式任务队列。OpenCollective 赞助。有 'bounty' 标签 issue。Python 后端任务。代码库大但模块化好。低竞争。"
```

---

## 三、新增仓库总览

| # | 仓库 | 类型 | 赏金类型 | 预计范围 | 竞争 | KYC | 推荐优先级 |
|---|------|------|----------|----------|------|-----|-----------|
| 1 | NomicFoundation/hardhat | web3/defi | security | $500-$50k | 🔴 high | ⚠️ 需要 | ⭐⭐⭐ |
| 2 | MetaMask/metamask-extension | web3/defi | security | $1k-$50k | 🔴 high | ⚠️ 需要 | ⭐⭐ |
| 3 | Uniswap/interface | web3/defi | security | $500-$25k | 🟡 medium | ⚠️ 需要 | ⭐⭐⭐ |
| 4 | safe-global/safe-contracts | web3/defi | security | $1k-$100k | 🔴 high | ⚠️ 需要 | ⭐⭐ |
| 5 | microsoft/vscode | large/msft | security | $5k-$15k | 🟡 medium | ⚠️ 需要 | ⭐⭐⭐ |
| 6 | electron/electron | large/framework | security | $1k-$20k | 🟢 low | ⚠️ 需要 | ⭐⭐⭐⭐ |
| 7 | grafana/grafana | large/monitoring | security | $500-$10k | 🟡 medium | ⚠️ 需要 | ⭐⭐⭐ |
| 8 | discourse/discourse | large/forum | security | $500-$5k | 🟢 low | ⚠️ 需要 | ⭐⭐⭐ |
| 9 | directus/directus | cms/framework | $bounty | $50-$1k | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐⭐ |
| 10 | appsmithorg/appsmith | low-code | $bounty | $50-$500 | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐⭐ |
| 11 | payloadcms/payload | cms | $bounty | $100-$1k | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐⭐ |
| 12 | immich-app/immich | photo/app | $bounty | $50-$500 | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐⭐ |
| 13 | mermaid-js/mermaid | diagram | $bounty | $50-$500 | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐ |
| 14 | standardnotes/app | notes | $bounty | $50-$500 | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐ |
| 15 | strapi/strapi | cms | $bounty | $100-$1k | 🟡 medium | ✅ 无需 | ⭐⭐⭐ |
| 16 | documenso/documenso | e-sign | $bounty | $50-$500 | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐ |
| 17 | huggingface/transformers | ai/ml | $bounty | $100-$2k | 🟡 medium | ✅ 无需 | ⭐⭐⭐⭐ |
| 18 | pydantic/pydantic | validation | $bounty | $100-$1k | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐ |
| 19 | ApeWorX/ape | web3/py | $bounty | $100-$3k | 🟢 low | ✅ 无需 | ⭐⭐⭐⭐ |
| 20 | celery/celery | task-queue | $bounty | $50-$500 | 🟢 low | ✅ 无需 | ⭐⭐⭐ |

**竞争程度**: 🟢 low = 适合切入 | 🟡 medium = 有竞争但可获胜 | 🔴 high = 需实力

---

## 四、重点推荐（Top 5 Immediate Picks）

按"低竞争 + 无需 KYC + $500+ 潜力"排序：

1. **🥇 directus/directus** — Algora 平台，$50-$1000 赏金，TypeScript，低竞争，无需 KYC
2. **🥇 appsmithorg/appsmith** — 明确 💰 Bounty 标签，$50-$500，TypeScript，低竞争，AI 友好
3. **🥇 payloadcms/payload** — Bounty 标签，$100-$1000，TypeScript，代码质量高，竞争力低
4. **🥇 immich-app/immich** — 赞助赏金，$50-$500，TypeScript/Dart，极低竞争，高频发布
5. **🥈 electron/electron** — 安全赏金 $1k-$20k，低竞争，TypeScript/C++，需 KYC 但收益高

---

## 五、配置建议

### Scanner 更新
新增仓库后，建议调整 `config.yaml`：
```yaml
known_bounty_scan_limit: 30  # 从 10 提升到 30，覆盖更多热区
```
或者保持 10 但利用 `tags` 中的优先级排序，优先扫描带 `algora` / `low-competition` 标签的仓库。

### 搜索策略增强
针对新增的 Web3/DeFi 和安全仓库，建议添加搜索：
```yaml
- 'is:issue is:open label:"💰 Bounty" no:assignee'
- 'is:issue is:open label:immunefi no:assignee'
```

---

## 六、风险提示

1. **Web3/DeFi 安全赏金**：大部分通过 Immunefi 需要 KYC。小型赏金（<$5k）可通过 crypto 结算。大型赏金需要人工审批。
2. **Microsoft/HackerOne 赏金**：需要 W-8BEN 或类似税务表单。配置 `filter_required_kyc: true` 时会自动过滤。
3. **竞争变化**：新增仓库发布后 1-2 周内竞争可能快速上升。建议每 30 天 review 一次竞争程度。
4. **支付确认**：对于新加入的仓库，建议先完成一个小型 issue 验证支付，再投入时间在大任务上。
