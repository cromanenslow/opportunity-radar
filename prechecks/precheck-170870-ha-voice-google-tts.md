# Pre-check 分析报告：#170870 — HA VOICE PE sometimes don't response with Google AI TTS

**分析日期**: 2026-05-16  
**Issue URL**: https://github.com/home-assistant/core/issues/170870  
**仓库**: home-assistant/core  
**集成**: `tts` (Text-to-Speech), `assist_pipeline`, `google_generative_ai_conversation`, `esphome` (Voice PE)

---

## 1. Issue 摘要

用户报告 HA Voice PE（语音预览版硬件）在使用 Google AI TTS（Google Generative AI 语音合成）时，有时不响应。日志显示 Voice PE 在约 30 秒内尝试 6 次从 HAOS 获取 Google AI TTS 生成的 `.flac` 音频文件，全部失败（HTTP 状态码 -1，即连接超时/错误）。约 1 分 40 秒后，用户可以通过电脑正常下载该文件。

用户的建议：让 HA 先检查音频文件是否已创建，将 TTS 输出生成前的等待时间归入"思考"阶段。

---

## 2. Issue 健康度检查

| 检查项 | 状态 | 说明 |
|-------|------|------|
| **Assignee** | ❌ 无 | 无人认领 |
| **关联 PR** | ❌ 无 | 无关联 Pull Request |
| **标签** | 🔴 无 | 没有任何标签（无 `bug`/`integration: tts`/`help-wanted`） |
| **问题描述清晰度** | 🟡 一般 | 提供了详细日志，但问题描述较模糊——更像是一个 feature request（"能否让 HA 检查文件是否已创建"），而非明确的 bug 报告 |
| **可复现步骤** | ❌ 无 | 无明确、可复现的步骤；依赖 Google AI TTS 的响应延迟（可能因网络/API 负载而异） |
| **维护者回应** | ❌ 无 | 0 条评论，0 条回馈 |
| **社区反应** | 🔴 无 | 0 条回复，0 👍/👎，无讨论 |

**结论**: Issue 健康度**很低**。这是一个创建仅数小时的新 issue，没有任何标签、assignee、评论或社区互动。问题描述缺乏明确的根因分析和可复现步骤。

---

## 3. 技术复杂度评估

### 3.1 架构分析

整个 TTS 工作流如下：

```
┌─────────────────────────────────────────────────────────────┐
│ assist_pipeline/pipeline.py                                  │
│                                                              │
│ text_to_speech():                                            │
│   1. tts.async_create_stream() → 创建 ResultStream           │
│   2. async_set_message()      → 启动 TTS 生成（异步）        │
│   3. 立即发出 TTS_END 事件（含 URL）                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ TTS_END event with URL (/api/tts_proxy/{token})
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ esphome/assist_satellite.py                                  │
│                                                              │
│ _async_handle_event():                                       │
│   接到 TTS_END → 将 URL 发送给 ESPHome Voice PE 设备        │
└──────────────────────┬──────────────────────────────────────┘
                       │ Voice Assistant Event (URL)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ESPHome Voice PE 固件                                         │
│                                                              │
│ http_media_source 组件：                                      │
│   HTTP GET → /api/tts_proxy/{token}.flac                     │
│   超时默认 ~5 秒，重试 6 次 → 全部失败 (code=-1)           │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Request
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ tts/__init__.py — TextToSpeechView.get()                     │
│                                                              │
│ stream = token_to_stream[token]                              │
│ async for data in stream.async_stream_result():              │
│   # 阻塞等待 Google AI TTS 生成完毕                           │
│   prepare(request)  ← 只有等到数据后才发 HTTP 头             │
│   write(data)                                               │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 根本原因

时序竞争条件：

1. `text_to_speech()` 调用 `async_set_message()` 后**立即**发出 `TTS_END` 事件（含 URL）
2. `async_set_message()` 只是创建了 `TTSCache` 对象，**实际 TTS 生成**在后台任务 `_load_data_into_cache()` 中进行
3. Google AI TTS 调用可能耗时 30 秒到 2 分钟（取决于 API 响应速度、文本长度等）
4. Voice PE 收到 URL 后立即发起 HTTP 请求
5. `TextToSpeechView.get()` 在 `async_stream_result()` 处阻塞等待数据
6. Voice PE 的 HTTP 客户端在 ~5 秒后超时（`code = -1`）
7. 重试同样因数据尚未就绪而全部失败

**关键问题**: `TTS_END` 事件在音频可用之前发出，导致 Voice PE 过早获取 URL 并因超时而失败。

### 3.3 可能的修复方案

| 方案 | 修改位置 | 复杂度 | 优缺点 |
|------|---------|--------|--------|
| **A. 延迟 TTS_END** 直到音频就绪 | `assist_pipeline/pipeline.py` | ⭐⭐⭐ 中等 | ✅ 直接解决时序问题；❌ 增加管道延迟；需要设计"等待就绪"机制 |
| **B. 提前发送 HTTP 头** 立刻返回 200 + 流式传输 | `tts/__init__.py` - `TextToSpeechView.get()` | ⭐ 简单 (~10 行) | ✅ 快速修复；❌ 不确定 Voice PE HTTP 客户端是否支持长等待流式响应 |
| **C. 增加 Voice PE 超时** | ESPHome 固件（非 HA 仓库） | 不适用 | ❌ 不在 HA core 仓库范围内 |
| **D. 添加轮询/状态端点** | `tts/__init__.py` | ⭐⭐⭐ 较复杂 | 需要同时修改 HA 和 ESPHome 端 |

### 3.4 预估修改量

**方案 A（最可能被接受的方案）**:
- `assist_pipeline/pipeline.py` — `text_to_speech()` 方法：~30-50 行
- 可能需添加 ResultStream 的 `async_wait_for_data()` 方法：~20 行
- 总计：**~50-70 行，1-2 个文件**

**方案 B（最简单方案）**:
- `tts/__init__.py` — `TextToSpeechView.get()`：~10 行（移动 `prepare()` 到循环前）
- 总计：**~10 行，1 个文件**

---

## 4. AI 执行可行性

| 维度 | 评估 | 说明 |
|------|------|------|
| **有明确的重现步骤** | ❌ | 无明确步骤；依赖 Google AI TTS 的延迟，难以稳定复现 |
| **是否涉及外部硬件** | 🟡 | 推荐使用 Voice PE 测试，但可以通过模拟 HTTP 请求部分验证 |
| **是否有清晰的验收标准** | ❌ | 问题描述模糊（"sometimes don't response"），无明确预期行为 |
| **代码变更方向是否明确** | 🟡 | 方向合理但未经验证；需要确认 Voice PE 超时具体值、Google AI TTS 典型延迟 |
| **是否已有社区共识** | ❌ | 0 条评论，无维护者/贡献者参与讨论 |
| **是否可能被合并** | 🟡 | 可能被接受，但需要先在 issue 中与维护者确认方向 |

### 关键障碍

1. **Issue 质量极低**: 无标签、无 assignee、无评论、创建仅数小时。按 HA 项目的惯常节奏，此类 issue 可能数周都无人关注
2. **根因未确认**: HTTP code -1 可能是多种原因（超时、DNS 解析、网络中断），仅从用户日志不能 100% 确定是 TTS 生成延迟导致
3. **需要硬件测试**: 虽然可以通过 curl 模拟 Voice PE 的 HTTP 请求来验证部分修复，但完整验证需要 Voice PE 设备
4. **多方案选择**: 不同修复方案有不同 trade-off，需要维护者决策
5. **潜在 ESPHome 侧依赖**: 如果 ESPHome 端 HTTP 超时不可配置，需要在两侧协同修改

---

## 5. Pre-check 结论

### 🟡 需人工复核 — 不建议 AI 直接执行

**核心原因**:

1. **Issue 成熟度不足**: 这是一个创建于同一天的 issue（2026-05-16 04:39 UTC），没有任何标签、assignee、评论或社区互动。AI 直接提交 PR 风险极高。

2. **问题描述模糊**: 用户提供日志但未做根因分析，修复方向需要先在 issue 中与维护者讨论确认（方案 A vs B vs 其他）。

3. **修复方向未定**: 方案 A（延迟 TTS_END）和方案 B（提前发 HTTP 头）有不同的架构影响。方案 A 改变了 Assist Pipeline 的语义（TTS_END 代表"音频已就绪"而非"已提交生成"），可能需要 HA 核心维护者的 approval。

4. **测试依赖硬件**: 没有 Voice PE 设备无法进行完整的端到端验证。虽然可以 mock ESPHome 端请求，但无法确认修复后的用户体验。

5. **无维护者信号**: 没有代码所有者（`@balloob`, `@synesthesiam` 等 voice pipeline 维护者）参与，不确定他们对修复方向的偏好。

**建议路径**:
- 等待 issue 获得标签（至少 `integration: tts` 或 `bug`）和至少一个维护者回应
- 在 issue 中提出分析结果（根因分析 + 修复方案建议），引导社区讨论
- 如果维护者确认方向（例如选择方案 A 或 B），AI 可以高效执行代码修改
- 修复后需要用户验证（因为 AI 没有 Voice PE 硬件）

**追加观察**: 存在类似 issue #159537（TTS proxy 返回 404）和 #149882（语音助手在空闲后产生 404 URL），说明 TTS 代理的时序/缓存问题有一定普遍性。如果此 issue 被确认为同类型问题，可能有更根本的架构性修复需求。

---

## 6. 附：相关代码文件

| 文件 | 作用 | 可能的修改 |
|------|------|-----------|
| `homeassistant/components/assist_pipeline/pipeline.py` | Assist Pipeline TTS 阶段处理 | 延迟 TTS_END 事件直到音频就绪 |
| `homeassistant/components/tts/__init__.py` | TTS 管理器、代理视图、ResultStream | 提前发送 HTTP 头/添加就绪等待方法 |
| `homeassistant/components/esphome/assist_satellite.py` | Voice PE 事件处理 | 无需修改（但需确认事件流程） |
| `homeassistant/components/google_generative_ai_conversation/tts.py` | Google AI TTS 引擎实现 | 无需修改 |

---

*分析工具: GitHub API + 源码审计 (`assist_pipeline`, `tts`, `esphome`, `google_generative_ai_conversation`)*  
*分析日期: 2026-05-16*
