# 深度预检报告：home-assistant/core#170683

**Issue**: Ha 2026.5 the damper state is unknow and not closed.
**URL**: https://github.com/home-assistant/core/issues/170683
**预检日期**: 2026-05-15
**评估人**: Hermes Agent (自动预检)

---

## 1. Issue 基本信息

| 字段 | 值 |
|------|-----|
| **赏金** | ❌ 无确认赏金（无标签、无 bounty 平台匹配） |
| **类型** | Bug（用户报告） |
| **状态** | OPEN |
| **创建时间** | 2026-05-14T16:08Z（距今约 12 小时） |
| **标签** | 无 |
| **Assignee** | 无 |
| **评论数** | 0 |
| **提案/PR 数** | 0 |

### 用户提供的信息（翻译自意大利语）

用户只贴出了实体的属性片段：
```
14 maggio 2026 alle ore 18:02:50
Attributi
Is closed Sconosciuto       ← "Sconosciuto" = "Unknown"
Device class damper
Friendly name PERGOLA
Supported features 11
```

- **版本**: HA 2026.5（Home Assistant OS）
- **集成**: 未指定（关键信息缺失）
- **日志**: 未提供
- **诊断信息**: 未提供
- **最后正常版本**: 未提供
- **复现步骤**: 未提供

---

## 2. 赏金确认

### 2.1 Issue 本体检查
- ❌ 无 `bounty`/`sponsor`/`hackathon` 标签
- ❌ Issue body 中无任何赏金提及
- ❌ 无 `💰`/`$`/`Bounty` 标记

### 2.2 仓库政策检查
- **CONTRIBUTING.md**: 标准开源贡献指南，无赏金政策
- **SECURITY.md**: 不存在（404）
- **README.rst**: 未提及赏金
- **GitHub Sponsors**: home-assistant 组织有 Sponsors 页面，但这是一般性赞助（贡献认可），非按 issue 付费

### 2.3 赏金平台检查
| 平台 | 结果 |
|------|------|
| **Algora** | ❌ 404 — home-assistant/core 无悬赏 |
| **IssueHunt** | ❌ 未找到相关记录 |
| **OnlyDust** | ❌ 未找到相关记录 |

### 2.4 结论：❌ 无确认赏金
与 KNOWLEDGE.md 标注一致（"无确认赏金"）。Home Assistant 项目没有官方 Bug Bounty 计划，贡献通过 GitHub Sponsors（组织级别）获得认可，不针对单个 issue 支付。

---

## 3. 技术分析

### 3.1 问题理解

用户报告在升级到 HA 2026.5 后，一个 **damper**（风门/阻尼器）设备状态显示为 "unknown" 而非 "closed"。

**设备特征分析（从属性推断）：**
- `device_class: damper` — 设备类为风门
- `friendly_name: PERGOLA` — 用户命名为 "PERGOLA"（凉棚/遮阳篷，可能是电动遮阳篷）
- `supported_features: 11` — 二进制：`OPEN(1) + CLOSE(2) + STOP(8)`，**不支持 SET_POSITION(4)**
- `is_closed: Sconosciuto` — `is_closed` 返回 `None`，导致 cover state 为 `None` → HA 显示 "unknown"

### 3.2 根因分析

**核心技术路径：**

```python
# homeassistant/components/cover/__init__.py
class CoverEntity(Entity):
    @property
    @final
    def state(self) -> str | None:
        if (closed := self.is_closed) is None:
            return None  # ← 这就是 "unknown" 的来源
        return CoverState.CLOSED if closed else CoverState.OPEN
```

**问题本质**：`is_closed` 返回 `None`，导致 `state` 返回 `None` → HA 显示 "unknown"。

**最常见的可能导致 `is_closed=None` 的场景：**

1. **Overkiz 集成（Somfy/RTS 生态）** ⭐ 最可能
   - HA 2026.5 包含 Overkiz 的 Cover 平台重构 PR #141330
   - 重构后，`is_closed` 通过 `is_closed_state` 状态值判断
   - 如果设备状态返回 `unknown`，则 `is_closed` 返回 `None`
   - 已知类似问题：PR #170130 修复了 DynamicGate 的 `is_closed` 问题（同样是重构导致的回归）
   - Overkiz 的 `UIClass.PERGOLA` 使用 `CORE_SLATS_OPEN_CLOSED` 状态，若该状态为 "unknown" 则出问题
   - **但是**: Overkiz 的 PERGOLA 使用 device_class `AWNING` 而非 `DAMPER`，除非用户手动覆盖

2. **MQTT Cover**（用户自配置）
   - 无状态主题时设 `_attr_is_closed = None`
   - 如果 MQTT 消息格式在 HA 2026.5 中解析异常，可能导致状态丢失

3. **Template Cover**（用户自配置）
   - `is_closed` 依赖 `current_cover_position`
   - 如果 position 为 `None`，则 `is_closed` 返回 `None`

4. **deCONZ/ZHA/Z-Wave 集成**
   - deCONZ 使用 `LEVEL_CONTROLLABLE_OUTPUT` 映射到 DAMPER 类
   - deCONZ 覆盖了 `is_closed` 属性，通常能正常工作

### 3.3 HA 2026.4 → 2026.5 变更分析

| 组件 | 变更 | 影响评估 |
|------|------|----------|
| `cover/__init__.py` | 移除 `bind_hass` 导入和装饰器 | 🟢 无影响（仅模块级函数） |
| `blebox/cover.py` | 位置计算修复 | 🟢 不影响其他集成 |
| `abode/cover.py` | 内部重构 | 🟢 不影响其他集成 |
| `entity.py` | 无变更 | N/A |
| `propcache` | 版本不变（0.4.1） | N/A |

**结论：核心 Cover 平台在 2026.5 中没有引入会导致 damper 状态变为 unknown 的变更。** 问题很可能出在特定集成（如 Overkiz）的重构中。

### 3.4 修复方向

**如果是 Overkiz 集成的问题：**
```python
# Overkiz is_closed 当前逻辑（简化）：
def is_closed(self) -> bool | None:
    if is_closed_state := self.entity_description.is_closed_state:
        if state := self.device.states.get(is_closed_state):
            if state.value == OverkizCommandParam.UNKNOWN:
                return None  # 问题在这里！
            return state.value == OverkizCommandParam.CLOSED
    ...
    return None

# 修复方案：当状态为 UNKNOWN 时，fallback 到 position
def is_closed(self) -> bool | None:
    if is_closed_state := self.entity_description.is_closed_state:
        if state := self.device.states.get(is_closed_state):
            if state.value == OverkizCommandParam.UNKNOWN:
                # Fall through to position check
                pass
            else:
                return state.value == OverkizCommandParam.CLOSED
    
    # Fallback: use position
    if (position := self.current_cover_position) is not None:
        return position == 0
    if (tilt_position := self.current_cover_tilt_position) is not None:
        return tilt_position == 0
    
    return None
```

**如果其他集成的问题：** 需要用户提供集成名称，分析对应集成代码。

### 3.5 代码量估计
- **如果修复 Overkiz**: ~10-20 行（修改 `is_closed` 逻辑 + 测试）
- **如果修复其他集成**: 取决于具体集成，通常 10-50 行
- **如果是核心 Cover 修复**: 可能涉及 `cover/__init__.py` 的 `state` 属性改进，~20 行

---

## 4. AI 可行性评估

### 4.1 复现难度：🔴 高

| 因素 | 评估 |
|------|------|
| **集成未知** | 用户未指定集成名称，需要猜测 |
| **设备未知** | 需要 Somfy/Overkiz 设备或特定 Zigbee/Z-Wave 设备 |
| **环境依赖** | 需要 Home Assistant OS 2026.5 + 具体硬件 |
| **日志缺失** | 无错误日志，无诊断信息 |

### 4.2 模拟方案

| 方案 | 可行性 | 说明 |
|------|--------|------|
| **Overkiz mock** | ⚠️ 中等 | 可以使用 Overkiz 测试夹具 + pyoverkiz mock |
| **MQTT mock** | ✅ 高 | 可以使用 MQTT 客户端模拟设备 |
| **Template mock** | ✅ 高 | 无需外部设备 |
| **ZHA/deCONZ mock** | ❌ 低 | 需要 Zigbee 硬件或完整模拟器 |
| **完整 HA 环境** | ⚠️ 中等 | 需要搭建 HA 开发环境 + 大量依赖 |

### 4.3 验证方案
- 修改后需要通过 `pytest tests/components/<integration>/` 测试套件
- 需要编写新的测试用例覆盖 `is_closed=None` 的边缘情况
- Overkiz 的测试套件需要 pyoverkiz mock 数据

### 4.4 可行性总分：⚠️ 有条件可行
- 如果能确定用户使用的集成（大概率 Overkiz），AI 可以完成修复
- 修复本身代码量小、逻辑简单
- 但需要用户配合确认集成信息，当前 issue 信息不足以独立工作

---

## 5. 竞争评估

| 维度 | 状态 |
|------|------|
| **Assignee** | 无 |
| **评论** | 0 |
| **PR** | 0 |
| **其他提案** | 0 |
| **竞争强度** | 🟢 无（全新 issue） |

**竞争分析**: 该 issue 创建仅 12 小时，无人认领，零讨论。但由于信息不完整，其他开发者也可能因缺少信息而暂时搁置。

**注意**: Overkiz 的维护者 @nyroDev 刚刚合并了 #170130（DynamicGate 修复），可能已经注意到 Overkiz 的同类问题，存在被抢先修复的风险。

---

## 6. 综合结论

### ❌ 不推荐投入

| 评估维度 | 分数 | 说明 |
|----------|------|------|
| **赏金确定性** | 0/10 | 无任何形式的赏金或支付承诺 |
| **可验证性** | 3/10 | 缺少关键信息（集成、日志），难以验证 |
| **AI 适配度** | 4/10 | 修复逻辑简单，但需要猜使用场景 |
| **维护者活跃度** | 7/10 | Home Assistant 项目活跃，但 issue 无标签 = 未 triage |
| **上下文复用** | 2/10 | 只能学到 Overkiz 覆盖类的特定知识 |
| **竞争强度** | 9/10 | 零竞争，但这是信息不完整导致的 |

### 核心否决理由

1. **🔴 无赏金**: Home Assistant 没有 bug bounty 计划，该 issue 无任何支付承诺
2. **🔴 信息严重缺失**: 用户未指定集成、未提供日志、未提供诊断信息、未提供复现步骤
3. **🔴 非核心 Bug**: 问题出在特定集成的状态处理，不是 HA 核心平台的普遍问题
4. **🟡 修复范围模糊**: 即使修复也需要用户交互确认集成，无法独立完成
5. **🟡 可替代性低**: 即使提交 PR，无金钱回报，仅获得贡献记录

### 建议策略

**如果目标是赚钱**：❌ 跳过。无赏金，不投入。

**如果目标是社区声誉建设**：⚠️ 暂缓。可以等用户补充信息后再评估，届时：
1. 用户确认集成类型（Overkiz、MQTT、Template 等）
2. 提供具体日志或诊断信息
3. 有明确的是 2026.4→2026.5 回归的证据

**如果条件变化**：当且仅当以下条件满足时重新评估：
1. 维护者在该 issue 添加了 `bug` 标签（表示已 triage 并确认）
2. 用户补充了集成名称和日志
3. 意外发现该 issue 有赏金（可能性极低）

---

## 附录：关键技术参考

### Cover 状态流转
```
self.is_closed 属性
  → None → state = None → "unknown"（问题状态）
  → True → state = "closed"
  → False → state = "open"
```

### Overkiz PERGOLA 描述（cover.py）
```python
OverkizCoverDescription(
    key=UIClass.PERGOLA,
    device_class=CoverDeviceClass.AWNING,
    open_command=OverkizCommand.OPEN,
    close_command=OverkizCommand.CLOSE,
    stop_command=OverkizCommand.STOP,
    is_closed_state=OverkizState.CORE_SLATS_OPEN_CLOSED,
    ...
)
```

### 已知类似修复
- PR #170130: Fix is_closed state for DynamicGate covers in Overkiz（2026-05-08 合并）
  - 同样模式：Overkiz 重构后 `is_closed_state` 不匹配导致 `is_closed=None`
  - 该 PR 的修复思路可参考用于本 issue

---

*报告结束。本预检由 Hermes Agent 自动完成，仅供参考。*
