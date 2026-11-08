# Responses API 实战：怎么干

> 整理日期：2026-11-08
> 配套：[[Responses API 概览]]
> 说明：示例使用 OpenAI 官方 Python SDK（`openai>=1.x`）。模型名可替换为你账号可用的模型。工具 `type` 名称随版本变化，**以官方文档为准**。
> 官方参考：https://platform.openai.com/docs/api-reference/responses

---

## 目录

- [0. 准备工作](#0-准备工作)
- [1. 最小调用](#1-最小调用)
- [2. 系统指令](#2-系统指令)
- [3. 多轮对话](#3-多轮对话)
- [4. 流式输出](#4-流式输出)
- [5. 结构化输出](#5-结构化输出)
- [6. 自定义工具（Function Calling）](#6-自定义工具function-calling)
- [7. 内置工具](#7-内置工具)
- [8. 多模态输入](#8-多模态输入)
- [9. 推理模型参数](#9-推理模型参数)
- [10. 后台模式](#10-后台模式)
- [11. 从旧 API 迁移](#11-从旧-api-迁移)
- [12. 常见坑](#12-常见坑)
- [13. 参考资料](#13-参考资料)

---

## 0. 准备工作

```bash
pip install --upgrade openai
```

```python
import os
from openai import OpenAI

client = OpenAI()  # 自动读取环境变量 OPENAI_API_KEY

# 国内兼容端点示例（百炼 / DashScope）：
# client = OpenAI(
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     api_key=os.environ["DASHSCOPE_API_KEY"],
# )
```

> 环境变量方式最安全，不要把 key 写进代码或提交到仓库。

---

## 1. 最小调用

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    input="用一句话解释什么是自回归。",
)
print(resp.output_text)
```

- 返回是一个 **Response 对象**，不是 `choices`。
- 取纯文本用 `resp.output_text`；要精细控制就遍历 `resp.output`。

**输出结构长这样：**

```
Response
├── id: "resp_..."
├── status: "completed"
├── output:
│   └── [ { type: "message", role: "assistant",
│            content: [ { type: "output_text", text: "..." } ] } ]
└── usage: { input_tokens, output_tokens, ... }
```

---

## 2. 系统指令

`instructions` 相当于 system prompt，优先级高、作用全局：

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    instructions="你是一名严谨的中文技术讲师，回答先给结论再解释。",
    input="解释 KV Cache。",
)
```

---

## 3. 多轮对话

### 方式 A：`previous_response_id`（最简单）

```python
r1 = client.responses.create(
    model="gpt-4o-mini",
    input="什么是自注意力机制？",
)

r2 = client.responses.create(
    model="gpt-4o-mini",
    input="再用一句大白话总结。",
    previous_response_id=r1.id,   # 自动带上上一轮上下文
)
print(r2.output_text)
```

> 前提：服务端要保存历史（默认 `store=True`）。若你设置 `store=False`，就无法用 `previous_response_id` 续接。

### 方式 B：自己维护历史（无状态）

```python
history = [{"role": "user", "content": "什么是自回归？"}]

resp = client.responses.create(model="gpt-4o-mini", input=history)
history.append({"role": "assistant", "content": resp.output_text})
history.append({"role": "user", "content": "举个例子"})

resp2 = client.responses.create(model="gpt-4o-mini", input=history)
```

### 方式 C：Conversations API（把多轮归到一个会话）

```python
conv = client.conversations.create()

r1 = client.responses.create(
    model="gpt-4o-mini", input="你好", conversation=conv.id)
r2 = client.responses.create(
    model="gpt-4o-mini", input="我刚说了什么？", conversation=conv.id)
```

> Conversations 用于「跨响应、跨设备」的会话归档；具体方法以官方文档为准。

---

## 4. 流式输出

```python
stream = client.responses.create(
    model="gpt-4o-mini",
    input="写一段 100 字的产品介绍。",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        print("\n[done]")
```

**常见事件类型**：

| 事件 | 含义 |
|---|---|
| `response.created` | 响应开始 |
| `response.output_text.delta` | 文本增量 |
| `response.function_call_arguments.delta` | 工具参数增量 |
| `response.completed` | 完成 |
| `response.failed` | 失败 |

> 流式**不减少总生成时间**，但能让用户更早看到首字，改善感知等待。

---

## 5. 结构化输出

用 JSON Schema 强制模型输出合法 JSON：

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    input="抽取信息：张三，28 岁，住在北京。",
    text={
        "format": {
            "type": "json_schema",
            "name": "person",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "city": {"type": "string"},
                },
                "required": ["name", "age", "city"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
)

import json
person = json.loads(resp.output_text)
print(person)
```

> `strict=True` 通常要求：所有字段列进 `required`、`additionalProperties: False`。

---

## 6. 自定义工具（Function Calling）

### 6.1 声明工具

Responses 的工具 schema 是**扁平**的（不像 Assistants 包在 `function` 里）：

```python
import json

tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "查询指定城市的实时天气",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}]
```

### 6.2 完整闭环

```python
def get_weather(city: str) -> dict:
    # 这里换成真实调用
    return {"city": city, "temp_c": 26, "condition": "晴"}

def run_with_tools(user_input: str):
    first = client.responses.create(
        model="gpt-4o-mini",
        input=user_input,
        tools=tools,
    )

    # 找出模型要求调用的工具
    tool_outputs = []
    for item in first.output:
        if item.type == "function_call":
            args = json.loads(item.arguments or "{}")
            result = get_weather(**args)
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result, ensure_ascii=False),
            })

    if not tool_outputs:
        return first.output_text

    # 把工具结果回传，接着生成
    second = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=first.id,
        input=tool_outputs,
    )
    return second.output_text

print(run_with_tools("北京现在天气怎么样？"))
```

**和旧 Assistant API 的对应**：

| 旧 Assistants | 新 Responses |
|---|---|
| Run 进入 `requires_action` | `output` 里出现 `function_call` item |
| `submit_tool_outputs` | 下一轮 `input` 传 `function_call_output` |
| `tool_call_id` | `call_id` |
| 轮询 Run 状态 | 直接拿 `response`，无需轮询 |

---

## 7. 内置工具

> 具体 `type` 名称与参数随账号/版本可能不同（如 `web_search` 与旧版 `web_search_preview`），**以官方文档为准**。

### 7.1 联网搜索

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input="今天北京的天气如何？",
)
print(resp.output_text)
```

### 7.2 文件检索（RAG）

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["vs_你的向量库ID"],
    }],
    input="根据知识库回答：KV Cache 是什么？",
)
```

### 7.3 代码解释器

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    input="计算 1 到 100 的和，并画出折线图。",
)
```

### 7.4 图像生成

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "image_generation"}],
    input="画一只在雪地里的橘猫。",
)
```

### 7.5 MCP 工具

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    tools=[{
        "type": "mcp",
        "server_label": "deepwiki",
        "server_url": "https://mcp.deepwiki.com/mcp",
        "require_approval": "never",
    }],
    input="介绍一下 openai-python 仓库的结构。",
)
```

---

## 8. 多模态输入

### 图片

```python
resp = client.responses.create(
    model="gpt-4o-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "这张图里是什么？"},
            {"type": "input_image", "image_url": "https://example.com/cat.jpg"},
        ],
    }],
)
```

### 文件（如 PDF）

```python
import base64

with open("report.pdf", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

resp = client.responses.create(
    model="gpt-4o-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "总结这份报告。"},
            {"type": "input_file", "filename": "report.pdf",
             "file_data": f"data:application/pdf;base64,{b64}"},
        ],
    }],
)
```

---

## 9. 推理模型参数

对 `o` 系列等推理模型，用 `reasoning` 控制思考强度：

```python
resp = client.responses.create(
    model="o4-mini",
    input="证明根号 2 是无理数。",
    reasoning={"effort": "high", "summary": "auto"},
)
print(resp.output_text)
```

> 推理模型通常不支持/忽略 `temperature` 等采样参数，按官方文档使用。

---

## 10. 后台模式

长任务用 `background=True` 异步执行，然后轮询：

```python
import time

resp = client.responses.create(
    model="gpt-4o-mini",
    input="写一篇 3000 字的行业分析。",
    background=True,
)

while resp.status in ("queued", "in_progress"):
    time.sleep(2)
    resp = client.responses.retrieve(resp.id)

print(resp.status, resp.output_text if resp.status == "completed" else resp.error)
```

---

## 11. 从旧 API 迁移

### Chat Completions → Responses

```python
# 旧
# resp = client.chat.completions.create(model="gpt-4o-mini", messages=[...])
# text = resp.choices[0].message.content

# 新
resp = client.responses.create(
    model="gpt-4o-mini",
    input=[{"role": "user", "content": "你好"}],
)
text = resp.output_text
```

### Assistants → Responses

| 旧 | 新 |
|---|---|
| `Assistants.create` | 每次请求带 `model` + `instructions` |
| `Threads.create` | `previous_response_id` / Conversations |
| `Messages.create` | `input` |
| `Messages.list` | `response.output` / `output_text` |
| `Runs.create` + 轮询 | 一次 `responses.create()` |
| `requires_action` + `submit_tool_outputs` | `function_call` item + 下一轮 `function_call_output` |

---

## 12. 常见坑

| 坑 | 正确做法 |
|---|---|
| 用 `messages` 参数 | Responses 用 `input` |
| 用 `max_tokens` | 用 `max_output_tokens` |
| 以为 `resp.output` 是字符串 | 它是 item 数组；纯文本用 `output_text` |
| 从 `choices[0]` 取结果 | Responses 没有 `choices` |
| `previous_response_id` 报错 | 检查是否 `store=False` 或 Response 已过期 |
| 工具结果用 `tool_call_id` | Responses 用 `call_id` |
| 结构化输出老是校验失败 | `strict=True` 时补齐 `required`、加 `additionalProperties: False` |
| 内置工具 `type` 报未知 | 名称可能带 `_preview` 或版本差异，查官方文档 |
| 把 key 写进代码 | 用环境变量 / `.env`，并确保被 gitignore |

---

## 13. 参考资料

- Responses API 参考：https://platform.openai.com/docs/api-reference/responses
- Function Calling 指南：https://platform.openai.com/docs/guides/function-calling
- 结构化输出：https://platform.openai.com/docs/guides/structured-outputs
- 流式事件：https://platform.openai.com/docs/guides/streaming-responses
- Python SDK：https://github.com/openai/openai-python
- 官方 Cookbook：https://cookbook.openai.com

---

## 关联

- [[Responses API 概览]]
- [[LLM 服务栈与 API 设计]]
- [[应用开发 知识点总结]]
