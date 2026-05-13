"""Opportunity Radar - 打分引擎

EV = 奖金 × 接受概率 × 支付概率 / 预估小时数 - 风险成本

Score 权重:
  26% 支付确定性
  22% 可验证性
  18% AI适配度
  12% 维护者活跃度
   7% 上下文复用
  15% 竞争强度
  - 风险惩罚
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import yaml
import json
from pathlib import Path


class RiskType(Enum):
    NONE = 0
    LOW = -5
    MEDIUM = -15
    HIGH = -25


class PaymentType(Enum):
    ESCROW = "escrow"              # 平台托管，pay-on-merge
    PLATFORM = "platform"          # 平台赏金，有争议机制
    TIPPING = "tipping"            # Algora tipping / GitHub Sponsors
    SPONSOR = "sponsor"            # OpenCollective / 社区 grant
    IMPLIED = "implied"            # 隐性，维护者可能打赏
    NONE = "none"                  # 无明确支付


@dataclass
class Candidate:
    """候选任务"""
    source: str                       # 来源平台
    repo: str                         # owner/repo
    issue_number: int
    title: str
    url: str
    labels: list[str] = field(default_factory=list)
    bounty_amount: float = 0.0        # 美元
    payment_type: PaymentType = PaymentType.NONE
    has_repro_steps: bool = False     # 有复现步骤
    has_failing_test: bool = False    # 有失败测试
    has_acceptance_criteria: bool = False  # 有验收标准
    is_local_modifiable: bool = False     # 可局部修改
    has_test_suite: bool = False          # 有测试套件可跑
    maintainer_merged_ext_pr_30d: int = 0   # 近30天合并外部PR数
    maintainer_merged_ext_pr_90d: int = 0   # 近90天
    maintainer_response_days: float = 7.0   # 平均响应天数
    repo_in_whitelist: bool = False    # 是否在白名单
    is_familiar_repo: bool = False     # 是否已熟悉
    estimated_hours: float = 2.0       # 预估小时数
    is_security: bool = False          # 是否安全任务
    has_poc: bool = False              # 安全任务是否有PoC
    has_scope: bool = False            # 安全任务是否有授权范围
    has_sponsors: bool = False         # repo 是否有赞助/打赏渠道
    bounty_history: float = 0.0        # 历史赏金/打赏金额
    issue_age_days: float = 0.0       # 距离最后更新的天数
    preflight_flags: list[str] = field(default_factory=list)
    description: str = ""
    open_pr_count: int = 0            # 引用此 issue 的开放 PR 数量（竞争强度用）
    assignee_count: int = 0           # 被指派者数量（竞争强度用）


def payment_certainty_score(
    payment_type: PaymentType,
    has_sponsors: bool = False,
    bounty_history: float = 0.0,
) -> float:
    """支付确定性 0-100"""
    scores = {
        PaymentType.ESCROW: 95,
        PaymentType.PLATFORM: 85,
        PaymentType.TIPPING: 70,
        PaymentType.SPONSOR: 68,
        PaymentType.IMPLIED: 42,
        PaymentType.NONE: 5,
    }
    score = scores.get(payment_type, 5)

    if has_sponsors:
        score += 8
    if bounty_history > 0:
        score += min(10, bounty_history / 500)

    return min(score, 100)


def verifiability_score(candidate: Candidate) -> float:
    """可验证性 0-100"""
    score = 0.0
    if candidate.has_repro_steps:
        score += 35
    if candidate.has_failing_test:
        score += 30
    if candidate.has_acceptance_criteria:
        score += 35
    return min(score, 100)


def ai_fitness_score(candidate: Candidate) -> float:
    """AI适配度 0-100"""
    score = 0.0
    if candidate.is_local_modifiable:
        score += 40
    if candidate.has_test_suite:
        score += 35
    # 标签加分
    fit_labels = {"bug", "good first issue", "help wanted", "documentation",
                  "test", "testing", "migration", "tech-debt", "chore"}
    label_match = len(set(l.lower() for l in candidate.labels) & fit_labels)
    score += min(label_match * 10, 25)
    return min(score, 100)


def maintainer_activity_score(candidate: Candidate) -> float:
    """维护者活跃度 0-100"""
    score = 0.0
    # 近30天合并外部PR
    if candidate.maintainer_merged_ext_pr_30d >= 5:
        score += 40
    elif candidate.maintainer_merged_ext_pr_30d >= 2:
        score += 25
    elif candidate.maintainer_merged_ext_pr_30d >= 1:
        score += 15

    # 近90天
    if candidate.maintainer_merged_ext_pr_90d >= 10:
        score += 30
    elif candidate.maintainer_merged_ext_pr_90d >= 5:
        score += 20
    elif candidate.maintainer_merged_ext_pr_90d >= 2:
        score += 10

    # 响应速度
    if candidate.maintainer_response_days <= 2:
        score += 30
    elif candidate.maintainer_response_days <= 5:
        score += 20
    elif candidate.maintainer_response_days <= 10:
        score += 10

    return min(score, 100)


def context_reuse_score(candidate: Candidate) -> float:
    """上下文复用 0-100"""
    score = 0.0
    if candidate.repo_in_whitelist:
        score += 50
    if candidate.is_familiar_repo:
        score += 50
    return min(score, 100)


def competition_intensity_score(candidate: Candidate) -> float:
    """
    竞争强度评分 0-100
    通过 open PR 数量 + assignees 数量判断竞争激烈程度
    0 个竞争者 → 高分 (100)  无竞争，黄金机会
    1 个竞争者 → 中分 (50)   轻度竞争
    >=2 个竞争者 → 低分 (20)  激烈竞争
    """
    total = candidate.open_pr_count + candidate.assignee_count
    if total == 0:
        return 100.0
    elif total == 1:
        return 50.0
    else:
        return 20.0


def risk_penalty(candidate: Candidate) -> float:
    """风险惩罚 0 到 -25"""
    penalty = 0.0

    # 安全任务风险
    if candidate.is_security:
        if not candidate.has_poc:
            penalty -= 15  # 无PoC，curl教训
        if not candidate.has_scope:
            penalty -= 10  # 无授权范围
        if candidate.has_poc and candidate.has_scope:
            penalty -= 2   # 即使有PoC和scope，安全仍有固有风险

    # 维护者冷漠
    if candidate.maintainer_response_days > 14:
        penalty -= 5
    if candidate.maintainer_merged_ext_pr_90d == 0:
        penalty -= 8

    # 支付模糊
    if candidate.payment_type in (PaymentType.IMPLIED, PaymentType.NONE):
        if candidate.bounty_amount > 0:
            penalty -= 3   # 标了金额但没有支付机制

    # 陈旧 issue 惩罚：越旧越难被处理
    if candidate.issue_age_days > 180:
        penalty -= 12
    elif candidate.issue_age_days > 90:
        penalty -= 8
    elif candidate.issue_age_days > 30:
        penalty -= 4

    return max(penalty, -25)


@dataclass
class ScoredCandidate:
    """打分结果"""
    candidate: Candidate
    total_score: float
    payment_score: float
    verifiability_score: float
    ai_fitness_score: float
    maintainer_score: float
    context_score: float
    competition_score: float
    risk_penalty: float
    expected_value: float
    needs_human_approval: bool
    lane: str = "practice"
    selection_reason: str = ""
    blocked_reason: str = ""
    skip_reason: Optional[str] = None


def score_candidate(candidate: Candidate, weights: dict | None = None) -> ScoredCandidate:
    """对候选任务打分"""
    if weights is None:
        weights = {
            "payment_certainty": 0.26,
            "verifiability": 0.22,
            "ai_fitness": 0.18,
            "maintainer_activity": 0.12,
            "context_reuse": 0.07,
            "competition_intensity": 0.15,
        }

    p = payment_certainty_score(
        candidate.payment_type,
        has_sponsors=candidate.has_sponsors,
        bounty_history=candidate.bounty_history,
    )
    v = verifiability_score(candidate)
    a = ai_fitness_score(candidate)
    m = maintainer_activity_score(candidate)
    c = context_reuse_score(candidate)
    comp = competition_intensity_score(candidate)
    r = risk_penalty(candidate)

    total = (
        weights["payment_certainty"] * p
        + weights["verifiability"] * v
        + weights["ai_fitness"] * a
        + weights["maintainer_activity"] * m
        + weights["context_reuse"] * c
        + weights["competition_intensity"] * comp
        + r
    )

    # 期望收益
    accept_prob = min(total / 100, 1.0)
    pay_prob = p / 100
    freshness_factor = 1.0
    if candidate.issue_age_days > 180:
        freshness_factor = 0.55
    elif candidate.issue_age_days > 90:
        freshness_factor = 0.7
    elif candidate.issue_age_days > 30:
        freshness_factor = 0.85

    ev = ((candidate.bounty_amount * freshness_factor) * accept_prob * pay_prob / max(candidate.estimated_hours, 0.5)) + (r / 10)

    # 安全任务必须人工审批
    needs_approval = candidate.is_security

    # 跳过条件
    skip_reason = None
    blocked_reason = ""
    selection_reason = ""
    lane = "practice"
    if candidate.is_security and not candidate.has_poc:
        skip_reason = "安全任务无PoC，不提交（curl教训）"
    elif candidate.is_security and not candidate.has_scope:
        skip_reason = "安全任务无授权范围，不提交"
    elif candidate.maintainer_merged_ext_pr_90d == 0 and candidate.maintainer_response_days > 30:
        skip_reason = "维护者不活跃，无外部PR合并"

    if skip_reason:
        blocked_reason = skip_reason
    elif candidate.bounty_amount > 0 or candidate.payment_type != PaymentType.NONE:
        lane = "money"
        selection_reason = "有明确支付路径或赏金"
    else:
        selection_reason = "适合练手，但暂无明确收益"

    return ScoredCandidate(
        candidate=candidate,
        total_score=round(total, 2),
        payment_score=p,
        verifiability_score=v,
        ai_fitness_score=a,
        maintainer_score=m,
        context_score=c,
        competition_score=comp,
        risk_penalty=r,
        expected_value=round(ev, 2),
        needs_human_approval=needs_approval,
        lane=lane,
        selection_reason=selection_reason,
        blocked_reason=blocked_reason,
        skip_reason=skip_reason,
    )


def batch_score(candidates: list[Candidate], weights: dict | None = None) -> list[ScoredCandidate]:
    """批量打分，返回按总分降序排列"""
    scored = [score_candidate(c, weights) for c in candidates]
    scored.sort(key=lambda s: s.total_score, reverse=True)
    return scored


def load_weights_from_config(config_path: str = "config.yaml") -> dict:
    """从配置文件加载打分权重"""
    p = Path(config_path)
    if p.exists():
        with open(p) as f:
            cfg = yaml.safe_load(f)
        s = cfg.get("scoring", {})
        return {
            "payment_certainty": (s.get("payment_certainty", 26)) / 100,
            "verifiability": (s.get("verifiability", 22)) / 100,
            "ai_fitness": (s.get("ai_fitness", 18)) / 100,
            "maintainer_activity": (s.get("maintainer_activity", 12)) / 100,
            "context_reuse": (s.get("context_reuse", 7)) / 100,
            "competition_intensity": (s.get("competition_intensity", 15)) / 100,
        }
    return None


if __name__ == "__main__":
    # Demo
    c = Candidate(
        source="algora",
        repo="vercel/next.js",
        issue_number=12345,
        title="Fix hydration mismatch in nested layouts",
        url="https://github.com/vercel/next.js/issues/12345",
        labels=["bug", "good first issue"],
        bounty_amount=500,
        payment_type=PaymentType.ESCROW,
        has_repro_steps=True,
        has_failing_test=True,
        has_acceptance_criteria=True,
        is_local_modifiable=True,
        has_test_suite=True,
        maintainer_merged_ext_pr_30d=8,
        maintainer_merged_ext_pr_90d=25,
        maintainer_response_days=2,
        repo_in_whitelist=True,
        is_familiar_repo=False,
        estimated_hours=3,
        is_security=False,
    )

    result = score_candidate(c)
    print(f"Score: {result.total_score} | EV: ${result.expected_value}/hr")
    print(f"  Payment: {result.payment_score} | Verify: {result.verifiability_score}")
    print(f"  AI Fit: {result.ai_fitness_score} | Maintainer: {result.maintainer_score}")
    print(f"  Context: {result.context_score} | Competition: {result.competition_score}")
    print(f"  Risk: {result.risk_penalty}")
    print(f"  Needs approval: {result.needs_human_approval}")
