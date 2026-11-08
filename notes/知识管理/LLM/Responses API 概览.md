# Responses API 概览：它能干什么

> 整理日期：2026-11-08
> 定位：OpenAI 新一代统一接口，用来取代 **Chat Completions** 与 **Assistants API**。
> 注意：Responses API 仍在快速迭代，具体工具 `type` 名称和参数**以官方文档为准**。
> 官方文档：https://platform.openai.com/docs/api-reference/responses

---

## 一、一句话理解

> **Responses API 是一个端点（`POST /v1/responses`），把「对话、工具调用、内置工具、多模态、状态管理、结构化输出」全部收进同一个请求/响应模型里。**

以前你要在 Chat Completions 和 Assistants 之间权衡；现在一个 API 覆盖两类需求。

---

## 二、它想解决什么问题

| 旧方案的痛点 | Responses 的改进 |
|---|---|
| Chat Completions 只能「一问一答」，工具和多模态要自己拼 | 工具、图片、文件、结构化输出都是一等公民 |
| Assistants 有 Thread / Message / Run 一堆对象，还要轮询 Run | 一次调用直接返回；需要多轮时用 `previous_response_id` |
| 内置工具（联网、检索、代码、绘画）要自己实现 | 直接声明 `tools`，模型自己调 |
| 各家接口对象结构不一致 | 统一成 `input` → `output` 的 item 列表 |

---

## 三、核心概念（先建立心智模型）

```
请求 input  ──►  [ 模型 + 工具 ]  ──►  响应 output
（字符串或 item 数组）                  （item 数组：消息/工具调用/推理...）
```

| 概念 | 含义 |
|---|---|
| **Response** | 一次调用的完整结果，带 `id`、`status`、`output`、`usage` |
| **input** | 你传进去的内容：字符串，或 item 数组（消息、图片、文件、工具结果） |
| **output** | 模型产出的 item 数组：`message`、`function_call`、`reasoning`、`web_search_call` 等 |
| **instructions** | 系统级指令（相当于 system prompt） |
| **tools** | 工具声明：自定义函数 or 内置工具 |
| **previous_response_id** | 指向上一轮 Response，实现多轮续接（服务端存历史） |
| **store** | 是否把这次 Response 存到服务端（默认存，供续接/检索） |

> **重要**：output 是「item 列表」，不是一段纯文本。工具调用、推理过程都是独立的 item。取纯文本可以用 SDK 的 `response.output_text` 便捷属性。

---

## 四、能力清单

| 能力 | 怎么用 | 说明 |
|---|---|---|
| **文本对话** | `input` + `model` | 最基础 |
| **多轮对话** | `previous_response_id` | 服务端存历史并自动续接 |
| **会话分组** | Conversations API | 把多个 Response 归到一个会话 |
| **流式输出** | `stream=True` | 逐 token 推送，改善感知等待 |
| **自定义工具（Function Calling）** | `tools=[{type:"function",...}]` | 模型返回 `function_call`，你执行后回传 |
| **联网搜索** | `tools=[{type:"web_search"}]` | 内置，无需自己爬 |
| **文件检索（RAG）** | `tools=[{type:"file_search", vector_store_ids:[...]}]` | 挂向量库 |
| **代码解释器** | `tools=[{type:"code_interpreter",...}]` | 跑 Python、画图、处理文件 |
| **图像生成** | `tools=[{type:"image_generation"}]` | 直接出图 |
| **计算机操作** | `tools=[{type:"computer_use_preview"}]` | 控制浏览器/界面（预览） |
| **MCP 工具** | `tools=[{type:"mcp",...}]` | 接外部 MCP server |
| **结构化输出** | `text={"format":{...json_schema...}}` | 强制输出符合 JSON Schema |
| **多模态输入** | `input` 里放 `input_image` / `input_file` | 图片、PDF 等 |
| **推理控制** | `reasoning={"effort": ...}` | 对推理模型控制思考强度 |
| **后台模式** | `background=True` | 长任务异步跑，轮询取结果 |

---

## 五、和 Chat Completions、Assistants 对比

| 维度 | Chat Completions | Assistants API（已弃用） | **Responses API** |
|---|---|---|---|
| 端点 | `/v1/chat/completions` | 多个对象 + Runs | `/v1/responses` |
| 输入 | `messages` | Thread + Message | `input` |
| 输出 | `choices[].message` | 轮询 Run → 取 Message | `output` item 列表 |
| 工具 | 手写 function calling | Run `requires_action` 回传 | `tools` 一等公民 |
| 内置工具 | 无 | code/file search | 联网/检索/代码/绘画/MCP |
| 状态 | 自己重发历史 | 服务端 Thread | 默认存 + `previous_response_id` |
| 多模态 | 部分支持 | 有限 | 原生图片/文件 |
| 推荐度 | 仍可用，适合简单场景 | **弃用，别新用** | **新项目首选** |

> **结论**：新项目直接用 Responses；只在需要「最简、最便宜的一问一答」或兼容旧代码时继续用 Chat Completions。

---

## 六、关键参数速查（`responses.create`）

| 参数 | 作用 |
|---|---|
| `model` | 模型名，如 `gpt-4o-mini` |
| `input` | 字符串或 item 数组 |
| `instructions` | 系统指令 |
| `tools` / `tool_choice` | 工具声明 / 强制或自动选择 |
| `stream` | 是否流式 |
| `previous_response_id` | 续接上一轮 |
| `store` | 是否服务端存储（多轮续接需要） |
| `max_output_tokens` | 输出 Token 上限（注意不是 `max_tokens`） |
| `text` | 结构化输出格式（JSON Schema） |
| `reasoning` | 推理强度/摘要（推理模型） |
| `background` | 后台异步模式 |
| `truncation` | 上下文超长时如何截断 |
| `metadata` | 自定义元数据 |

---

## 七、什么时候选 Responses

- ✅ **要工具调用 / Agent**：首选。
- ✅ **要联网、文件检索、代码执行、出图**：首选（内置）。
- ✅ **要多轮但不想自己管历史**：`previous_response_id`。
- ✅ **要结构化 JSON 输出**：`text` + JSON Schema。
- ⚠️ **只要极简一问一答、极低兼容要求**：Chat Completions 也够用。
- ❌ **还在用 Assistants 写新代码**：不建议，官方已弃用。

---

## 关联

- [[Responses API 实战]]（安装、代码、工具闭环、迁移对照）
- [[LLM 服务栈与 API 设计]]（模型 / API / OpenAI 的分层与状态本质）
- [[应用开发 知识点总结]]（Assistants API 旧口径，考试用）
