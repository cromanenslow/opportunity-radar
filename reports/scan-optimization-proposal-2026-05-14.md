# 扫描配置优化方案：提升 money 候选发现率

> **日期**: 2026-05-14
> **当前状态**: money 候选 ~0.1/天 (79 原始 → 1 money → pre-check 后暂缓)
> **目标**: 提升至 ≥1.0 money 候选/天

---

## 当前问题诊断

| 环节 | 问题 | 影响程度 |
|------|------|----------|
| **搜索策略** | 14 个策略中仅 2 个搜索 bounty/reward，其余为 help-wanted/good-first-issue | 🔴 核心瓶颈 |
| **天轮换制** | 每日仅运行 6/14 策略，赏金搜索可能几天才跑一次 | 🟡 中等 |
| **平台扫描** | 平台 API 可能失效或数据稀疏；algora-github 仅搜 org:algora-io | 🟡 中等 |
| **赏金解析** | 只在 title 中搜 `$`，body 中的赏金信息大量遗漏 | 🟡 中等 |
| **白名单覆盖** | 100 个 repo 多为明星项目（React/Vue/Django），极少有现金赏金 | 🔴 核心瓶颈 |
| **优先级扫描** | 每天只扫 ≤5 个有赞助的 repo，覆盖面太窄 | 🟡 中等 |
| **money 门槛** | require_payment_for_top=true 过滤掉有 bounty_history 但无明确支付的候选 | 🟢 低 |

---

## 优化建议

---

### 建议 1：新增定向赏金搜索策略（最高回报 / 最低风险）

**问题**：当前 14 个搜索策略主要命中无赏金的 help-wanted / good-first-issue，这是 79:1 比例的根本原因。

**修改方式**：在 `config.yaml` 的 `scanner.github_searches` 中添加以下高精度搜索：

```yaml
github_searches:
  # ... 保留现有搜索
  
  # 新增：显式赏金 issue（金额在标题中）
  - 'is:issue is:open "$" bounty no:assignee updated:>=2026-05-01'
  - 'is:issue is:open "$" reward no:assignee updated:>=2026-05-01'
  
  # 新增：Expensify 风格的外部赏金
  - 'is:issue is:open "External" "bounty" no:assignee updated:>=2026-04-01'
  - 'is:issue is:open label:"$" no:assignee updated:>=2026-04-01'
  
  # 新增：安全赏金（不依赖平台扫描）
  - 'is:issue is:open label:security label:bounty no:assignee updated:>=2026-04-01'
  - 'is:issue is:open label:sponsor no:assignee updated:>=2026-04-01'
  
  # 新增：开源基金会/支持机构的 bounty
  - 'is:issue is:open "bounty" "funded" no:assignee updated:>=2026-04-01'
  - 'is:issue is:open "bounty" "grant" no:assignee updated:>=2026-04-01'
```

同时在 `scanner/github.py` 的 `SEARCH_STRATEGIES` 中也添加对应的策略，确保这些搜索每天都运行（不依赖轮换）。

**预期效果**：
- 赏金搜索直接从每天运行的策略中产出，不再受 6/14 轮换影响
- 预计每天多发现 3-5 个带 `$` 或 bounty 标签的 issue
- 其中 ~1-2 个可能通过打分进入 money 候选

**风险**：极低。只是增加搜索请求，不会影响现有逻辑。

**具体实现**：编辑 `config.yaml` 和 `scanner/github.py` 两处。

---

### 建议 2：建立「已知赏金仓库」热区扫描表（高回报 / 低风险）

**问题**：白名单 100 个 repo 虽然 star 多在 10-50000，但极少有现金赏金。已知的赏金活跃仓库（Expensify/App, tscircuit/*, crosscompute/* 等）不在白名单中，只能靠通用搜索偶尔命中。

**修改方式**：

1. 在 `whitelist/initial_whitelist.py` 中新增 10-15 个确认有赏金历史的仓库（或单独建 `BOUNTY_HOTLIST`）：

```python
# 已知现金赏金活跃仓库（不依赖通用搜索，直接每日扫描）
BOUNTY_HOT_REPOS = [
    WhitelistRepo("Expensify/App", "typescript", 38000, ..., bounty_history=50000,
                  has_algora_tipping=True, priority=2),
    WhitelistRepo("tscircuit/schematic-trace-solver", "typescript", 600, ..., bounty_history=5000,
                  has_algora_tipping=True, priority=2),
    WhitelistRepo("tscircuit/tscircuit-autorouter", "typescript", 300, ..., bounty_history=3000,
                  has_algora_tipping=True, priority=2),
    # ... 更多已知赏金仓库
]
```

2. 在 `radar.py` 的 `cmd_scan` 中，修改 priority_repos 扫描逻辑：

当前代码（第 443 行）：
```python
priority_repos = [repo for repo in whitelist if repo.has_sponsors or repo.has_algora_tipping or repo.has_opencollective]
scan_limit = min(5, len(priority_repos))
```

改为每日扫描更多仓库（如 20 个），并优先扫描 bounty_history > 0 的仓库：

```python
# 按 bounty_history 排序，优先扫描有赏金历史/打赏渠道的仓库
bounty_repos = sorted(
    [repo for repo in whitelist if repo.bounty_history > 0 or repo.has_algora_tipping or repo.has_sponsors],
    key=lambda r: r.bounty_history,
    reverse=True
)
scan_limit = min(20, len(bounty_repos))  # 从 5 -> 20
```

3. 并且对 bounty_history > 0 的 repo，不仅搜 `help wanted`，还应额外搜 `bounty` 和 `$` label 的 issue。

**预期效果**：
- 已知赏金仓库每天覆盖更全，不错过新发布的赏金 issue
- 白名单扩充到 110-115 个仓库，赏金信号密度更高
- 预计每天多发现 2-3 个 money 候选

**风险**：低。需要维护热区列表，但不需要修改打分逻辑。

---

### 建议 3：增强 bounty 金额解析与支付信号检测（中等回报 / 低风险）

**问题**：`github_issue_to_candidate()` 中赏金解析逻辑太弱：
- 只在 title 中搜 `$`（line 142），很多赏金只在 body 中标明
- 非 `$` 格式（如 "250 USD", "bounty: 250"）遗漏
- `has_bounty_signal` 只检查 "bounty"/"reward"/"$" 关键词
- Algora-github 的金额字段始终为 0（line 228 in platforms.py）

**修改方式**：

1. 在 `radar.py` 的 `github_issue_to_candidate()` 中增强金额提取（约 142-149 行）：

```python
# 当前
title_amounts = re.findall(r"\$(\d+)", title)
body_amounts = re.findall(r"\$(\d+)", body)

# 增强为
import re
# $ 前缀金额
title_amounts = re.findall(r"\$(\d+(?:,\d{3})*(?:\.\d+)?)", title)
body_amounts = re.findall(r"\$(\d+(?:,\d{3})*(?:\.\d+)?)", body)
# "X USD" / "X USDC" 格式
body_usd = re.findall(r"(\d+)\s*(?:USD|USDC|USDT)\b", body, re.IGNORECASE)
# "bounty: X" / "reward: X" / "prize: X" 格式
body_bounty = re.findall(r"(?:bounty|reward|prize|amount)[:\s]+\$?(\d+(?:,\d{3})*)", body, re.IGNORECASE)

all_amounts = []
for amounts in [title_amounts, body_amounts, body_usd, body_bounty]:
    all_amounts.extend(int(a.replace(",", "")) for a in amounts if int(a.replace(",", "")) > 0)
```

2. 在 `has_bounty_signal` 检查中增加更多信号词：
```python
has_bounty_signal = (
    "bounty" in label_names_lower 
    or "bounty" in combined 
    or "reward" in combined 
    or "$" in title
    or "external" in combined  # Expensify 风格
    or "usd" in combined
    or "bounty" in combined
    or "funded" in combined
    or "grant" in combined
)
```

3. 在 `scanner/platforms.py` 的 `fetch_algora_github_bounties()` 中从 body 解析金额：
```python
# 当前 amount=0
# 改为从 body 中解析
import re
body_text = item.get("body", "") or ""
amount_matches = re.findall(r"\$(\d+(?:,\d{3})*)", body_text)
amount = int(amount_matches[0].replace(",", "")) if amount_matches else 0
```

**预期效果**：
- body 中标注 $250 但没有写入 title 的 issue 也能被正确识别为有赏金
- 当前这类 issue 被识别为 $0 bounty、PaymentType.NONE，直接降至 practice lane
- 预计可多捕获 20-30% 的实际有赏金 issue
- 每天可能多 1-2 个 money 候选

**风险**：极低。纯解析增强，不影响现有数据流。

---

### 建议 4：降低 money lane 门槛，启用「隐性支付」通道（中等回报 / 中等风险）

**问题**：`require_payment_for_top: true` 导致即使 repo 有 bounty_history（曾给过钱），但如果当前 issue 没明确标注 $，仍然归入 practice。

**修改方式**：在 `config.yaml` 中调整：

```yaml
scanner:
  require_payment_for_top: false    # 改为 false
  min_expected_value: 1.0          # 但提高 EV 门槛
```

在 `radar.py` 的 `_candidate_to_row()`（第 337-343 行），将降级逻辑改为更精细的判断：

```python
# 当前：无明确支付就降级
if lane == "money":
    if require_payment_for_top and not payment_ready:
        lane = "practice"

# 改为：有 bounty_history 或 sponsor 的 repo 即使当前 issue 无显式 $ 也保留 money lane
if lane == "money":
    if not payment_ready:
        # 但 repo 有打赏历史，仍然保留赚钱赛道
        if scored.candidate.bounty_history > 200 or scored.candidate.has_sponsors:
            pass  # 留在 money lane，靠 bounty_history 推断支付概率
        else:
            lane = "practice"
            selection_reason = "暂无明确支付路径，转入练手池"
```

**预期效果**：
- 来自 known-payer repo 的 issue 即使没写 `$` 也能进入 money lane
- 这些 repo 的评分因 payment_type=IMPLIED/SPONSOR 本身较低，但 EV 可能仍为正
- 预计每天增加 0.5-1 个 money 候选

**风险**：中等。可能引入一些假阳性（repo 有历史但拒绝支付），需要配合人工审批过滤。

---

### 建议 5：新增 Polar.sh 赏金平台源（中等回报 / 低风险）

**问题**：当前 5 个平台中 Algora 可能 API 变化、IssueHunt 可能数据稀疏。Polar.sh 是目前活跃的开源赏金平台。

**修改方式**：在 `scanner/platforms.py` 中添加 Polar.sh 抓取器：

```python
def fetch_polar_bounties() -> list[PlatformBounty]:
    """抓取 Polar.sh 公开赏金"""
    bounties = []
    data = _curl_json("https://api.polar.sh/api/v1/bounties?status=open&limit=50")
    if not data:
        return bounties
    items = data if isinstance(data, list) else data.get("data", [])
    for item in items:
        try:
            bounties.append(PlatformBounty(
                platform="polar",
                repo=item.get("repository_full_name", ""),
                issue_number=item.get("issue_number", 0),
                title=item.get("title", ""),
                url=item.get("issue_url", ""),
                amount=float(item.get("amount", item.get("reward", 0))),
                currency="USD",
                labels=[l.get("name", "") for l in item.get("labels", [])],
                payment_type="escrow" if item.get("escrow_enabled") else "platform",
            ))
        except (ValueError, TypeError):
            continue
    return bounties
```

并在 `PLATFORM_FETCHERS` 和 `config.yaml` 的 `platforms` 中注册。

**预期效果**：
- 新增一个活跃赏金源，Polar.sh 上有不少 TS/Python 项目的赏金
- 预计每天多 1-3 个平台赏金候选

**风险**：低。API 变化时静默失败，不影响现有流程。

---

## 优先级排序

| 优先级 | 建议 | 预期每日新增 money 候选 | 实施难度 | 风险 | 投入产出比 |
|--------|------|------------------------|----------|------|-----------|
| 🥇 1 | **定向赏金搜索策略** | +1~2 | 低 (30min) | 极低 | ⭐⭐⭐⭐⭐ |
| 🥇 2 | **已知赏金仓库热区表** | +1~2 | 低 (1h) | 低 | ⭐⭐⭐⭐⭐ |
| 🥈 3 | **bounty 金额解析增强** | +1~2 | 低 (30min) | 极低 | ⭐⭐⭐⭐ |
| 🥉 4 | **降低 money lane 门槛** | +0.5~1 | 中 (1h+测试) | 中 | ⭐⭐⭐ |
| 5 | **新增 Polar.sh 平台源** | +1~3 | 中 (1h) | 低 | ⭐⭐⭐ |

## 投资回报估算

如果优化后达到 **2-3 个 money 候选/天**（从 0.1 提升 20-30 倍）：

| 指标 | 当前 | 优化后（预估） |
|------|------|---------------|
| money 候选/天 | 0.1 | 2.5 |
| 周 money 候选 | ~0.7 | ~17 |
| 月 money 候选 | ~3 | ~75 |
| 假设通过率 15% | ~0.45/月 | ~11/月 |
| 平均赏金 $150 | $67.5/月 | $1,650/月 |

---

## 实施步骤

### 今天可立即做的（30 分钟）：

1. **编辑 `config.yaml`** — 添加 8 条新的 github_searches（见建议 1）
2. **编辑 `radar.py`** — 增强 bounty 金额解析（见建议 3 第 1 点）
3. **编辑 `scanner/platforms.py`** — algora-github 金额解析修复

### 本周内做的：

4. **编辑 `whitelist/initial_whitelist.py`** — 新增 10-15 个已知赏金仓库（建议 2）
5. **编辑 `radar.py`** — 扩大 priority_repos 每日扫描量至 20 个（建议 2）
6. **编辑 `scanner/platforms.py`** — 新增 Polar.sh 抓取器（建议 5）

### 需谨慎评估的：

7. **降低 money lane 门槛**（建议 4）— 需要在测试环境验证不影响现有 practice 池质量

---

## 最终建议

**最优起步路径**：先做建议 1 + 建议 3（共约 1 小时），两者均为纯配置/解析增强，零风险。预期可将 money 候选发现率从 0.1/天 提升至 1~3/天。运行 3-5 天后评估效果，再决定是否需要实施建议 2 和 5。
