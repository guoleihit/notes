# LLM 服务栈与 API 设计（模型 · API · OpenAI）

> 整理日期：2026-11-08
> 主题：澄清「大模型 / API / OpenAI」三者的关系，以及 Assistants API → Responses API 的演进。

---

## 一、先分清三个东西

| 名称 | 是什么 | 会不会「说话」 |
|---|---|---|
| **大模型** | 一堆浮点权重文件，本质是函数 `f(tokens) → 下一个 token 的概率分布` | 不会，不懂 HTTP，没有 IP |
| **API** | 把模型包装成网络服务的接口层（`/v1/chat/completions`、`/v1/responses`） | 会，但背后不是「裸模型」 |
| **OpenAI** | 同时运营权重、GPU 集群、编排逻辑、API 网关的公司 | —— |

核心认知：**模型 ≠ API ≠ OpenAI。「通过 API 调用模型」= 通过一整套服务栈间接调用模型。**

---

## 二、分层架构（拓扑）

```
┌──────────────────────────────────────────────┐
│ 你的代码 / 应用                                 │
└───────────────────┬──────────────────────────┘
                    │  HTTPS + JSON
┌───────────────────▼──────────────────────────┐
│ ① API 网关层   /v1/chat/completions, /v1/responses │
│    鉴权 · 限流 · 路由 · 计费 · 日志 · 滥用检测      │
└───────────────────┬──────────────────────────┘
                    │  (内部 RPC)
┌───────────────────▼──────────────────────────┐
│ ② 产品编排层  Assistants / Responses / Agents   │
│    存 Thread · 拼上下文 · 挂工具 · RAG · 安全审查   │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│ ③ 推理服务层  推理引擎 + 调度                    │
│    KV cache · continuous batching · 多副本负载均衡 │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│ ④ 模型权重层  GPU 集群上的神经网络                │
│    纯函数: token 序列 → 下一个 token 的概率分布     │
└──────────────────────────────────────────────┘
```

### 各层职责

- **④ 模型权重层**：就是几 GB～几百 GB 的权重文件。它是数学函数，不会鉴权、不会说 HTTP。
- **③ 推理服务层**：把权重加载到 GPU 高效计算。vLLM / SGLang / TensorRT-LLM 这类引擎负责 KV cache、continuous batching（把几百个用户请求打包进同一块 GPU）。**你从来不是独占一个模型，你的请求在和无数陌生人拼单。**
- **② 产品编排层**：Assistants / Responses / Agents 所在层。存会话、重放历史、注入 system prompt、调用工具、跑安全过滤。
- **① API 网关层**：唯一对外说 HTTP 的地方。校验 Key、限流、路由到某个 GPU 副本、记账单。

**「API」这个词只存在于第 ① 层；模型在第 ④ 层，中间隔了两层你接触不到的东西。**

---

## 三、一次请求的真实生命周期

```
你 POST /v1/responses { input: "你好" }
        ↓
① 网关: 校验 API Key → 查额度 → 选一个副本
        ↓
② 编排: 取历史消息 + 系统提示 → 拼成完整 prompt
         （还要过 moderation 安全审查）
        ↓
③ 推理: tokenize → 放进某个 GPU 的 batch → 逐 token 生成
        ↓
② 编排: 输出再过一遍安全过滤 / 判断是否该调工具
        ↓
① 网关: 封装 JSON / 流式 SSE → 回给你，记一次账
```

几个「你以为在和模型对话，其实不是」的点：

- **系统提示是平台偷偷加的**，你看到的不是完整 prompt。
- **安全审查在你之前、之后都跑过**，可能改写或拒绝。
- **输出是流式的**，一个字一个字吐，因为推理本来就逐 token 生成。

---

## 四、模型无状态，为什么 API 有状态？

**状态不在模型里，在 API 的存储层。**

大模型每次推理只看到「本次请求里传进去的 token」，请求之间没有任何记忆。所谓「有状态」，是服务商在模型外面加了一层**数据库 + 上下文重放（replay）**：

```
createThread()            → 数据库建一条 thread 记录
createMessage(thread)     → message 表插一行，外键指向 thread
createRun(thread)         → 服务器执行：
      1. 读出该 thread 下所有 message（+ instructions、文件、工具记录）
      2. 拼成 messages 数组塞进上下文窗口
      3. 调用【无状态】模型
      4. 把输出写回 message 表
      5. 更新 run 状态 → 你轮询拿结果
```

**类比**：模型 = 无状态后端；Thread = Redis/DB 里的 session；每次 Run = 读历史 → 拼请求 → 调后端 → 写回。

**推论**：`previous_response_id` / Conversations API **同样是有状态的**——一样是「服务器存历史 + 下次重放」，只是变成显式、可选的一层。从没有什么「有状态的模型」，只有「要不要让 API 帮你存历史并自动重放」的选择。

---

## 五、Assistants API vs Responses API

### 废弃背景

OpenAI 于 2025 年宣布 **Assistants API 进入弃用流程**（计划 2026 年停止服务），统一推荐 **Responses API**。原因是 Thread / Message / Run 这套有状态抽象太重、难扩展；Responses 用一个端点同时覆盖 Chat Completions 和 Assistants 的能力，并原生集成更丰富的工具。

### 结构差异

| 维度 | Assistants API | Responses API |
|---|---|---|
| 核心对象 | Assistant、Thread、Message、Run、RunStep | Response（输入 `input` / 输出 `output`） |
| 消息模型 | Message 是独立资源，有 create/list/update/delete | 没有独立 Message 资源，直接传 `input` 数组 |
| 状态 | 服务端持久化 Thread（默认有状态） | 默认无状态，靠 `previous_response_id` 或 Conversations API 续接 |
| 执行 | 创建 Run 后**轮询**状态 | 单次调用直接返回（可流式） |
| 工具 | code interpreter、file search、function calling | 上述 + web search、computer use、image generation 等 |

### Message 的定位变化

- **Assistants**：Message 是独立资源。`create` 往 Thread 加一条消息，`update` 只能改 `metadata`（**改不了正文**），还要 `list` / `delete` 管理。
- **Responses**：没有「Message 资源」这一层。上下文作为 `input` 传入（字符串或消息数组），回复在 `response.output`；多轮靠 `previous_response_id` 或新的 **Conversations API** 持久化。

### 迁移对应关系

```
Assistants 流程                         Responses 流程
─────────────────────────────────────  ─────────────────────────────
create Assistant                →      每次请求带 model + instructions
create Thread                   →      (可选) previous_response_id / Conversations
create Message (user)           →      放进 input
create Run + 轮询                →      一次 responses.create()，直接拿 output
```

---

## 六、结论

> **模型是一个无状态的数学函数（一堆权重文件）；API 是把它包装成网络服务的接口层；OpenAI 是同时运营权重、推理集群、编排逻辑和网关的公司。**

「大模型以 API 方式提供服务」的完整版应是：**OpenAI 用一整套后端栈（网关 + 编排 + 引擎 + 调度）把模型包起来，只暴露一个 HTTP 接口，你通过它间接地、分时共享地、被审查和记账地调用那个模型。** 你调用的从来不是模型本身，而是「模型 + 平台外壳」。

---

## 关联

- [[简介]]（大模型 / Transformer / 注意力机制）
- [[KV Cache]]（推理服务层的关键优化）
- [[Responses API 概览]]（新一代统一接口能干什么）
- [[Responses API 实战]]（安装、代码、工具闭环、迁移）
