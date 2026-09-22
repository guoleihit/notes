# RAG 知识点总结

> 归纳来源：`RAG 错题复习 2026-09-16 / 09-17 / 09-19 / 09-20 / 09-21 / 09-22` 六篇笔记
> 整理日期：2026-09-22（新增 09-21、09-22 错题）
> 说明：正文带「补充」标记的内容为错题之外的扩展知识，用于建立完整认知；文末附参考文献。

---

## 目录

- [0. 知识地图](#0-知识地图)
- [1. RAG 基础概念](#1-rag-基础概念)
- [2. 索引构建：加载与创建](#2-索引构建加载与创建)
  - [2.1 两个高频方法](#21-两个高频方法)
  - [2.2 `from_documents` 内部到底做了什么？](#22-from_documents-内部到底做了什么)
  - [2.3 索引的四个动作（极易混淆）](#23-索引的四个动作极易混淆)
  - [2.4 目录不存在 / 已存在，分别怎么做？](#24-目录不存在--已存在分别怎么做)
  - [2.5 加载本地索引可设置哪些参数？](#25-加载本地索引可设置哪些参数)
  - [2.6 查询引擎参数：similarity_top_k](#26-查询引擎参数similarity_top_k)
- [3. 文档切片（Chunking）](#3-文档切片chunking)
  - [3.1 什么时候该切得更小？](#31-什么时候该切得更小)
  - [3.2 各切片方法适用场景](#32-各切片方法适用场景)
  - [3.3 关键数据的「语义独立性与完整性」](#33-关键数据的语义独立性与完整性)
  - [3.4 基于语义的切片理念](#34-基于语义的切片理念)
- [4. 嵌入模型与向量化](#4-嵌入模型与向量化)
  - [4.1 大模型 vs Embedding 模型（分工必背）](#41-大模型-vs-embedding-模型分工必背)
  - [4.2 常见嵌入模型](#42-常见嵌入模型)
  - [4.3 `compare_embeddings` 函数](#43-compare_embeddings-函数)
  - [4.4 文本向量化的三个正确认识](#44-文本向量化的三个正确认识)
  - [4.5 `embedding_models` 字典的作用](#45-embedding_models-字典的作用)
- [5. 检索召回优化](#5-检索召回优化)
  - [5.1 相似度阈值与召回数量](#51-相似度阈值与召回数量)
  - [5.2 标签增强检索（Metadata Filtering）](#52-标签增强检索metadata-filtering)
  - [5.3 多查询类技术辨析（高频易混）](#53-多查询类技术辨析高频易混)
  - [5.4 HyDE（Hypothetical Document Embeddings）](#54-hydehypothetical-document-embeddings)
  - [5.5 检索后减少无关信息](#55-检索后减少无关信息)
  - [5.6 提高知识索引/检索性能的技术](#56-提高知识索引检索性能的技术)
  - [5.7 扩充信息以提升召回（Query Expansion / 用户画像）](#57-扩充信息以提升召回query-expansion--用户画像)
- [6. 多轮对话与查询改写](#6-多轮对话与查询改写)
  - [6.1 `custom_chat_history` 的作用](#61-custom_chat_history-的作用)
  - [6.2 机制：问题改写（Query Rewriting）](#62-机制问题改写query-rewriting)
  - [6.3 问题改写：检索前还原真实意图](#63-问题改写检索前还原真实意图)
- [7. 复杂问题求解：分解与多步检索](#7-复杂问题求解分解与多步检索)
  - [7.1 核心框架：「分解 — 执行 — 合成」](#71-核心框架分解--执行--合成)
  - [7.2 常用框架与工具](#72-常用框架与工具)
  - [7.3 提示词关键要素](#73-提示词关键要素)
  - [7.4 检索召回阶段「思考并规划多次检索」](#74-检索召回阶段思考并规划多次检索)
  - [7.5 注意事项](#75-注意事项)
- [8. GraphRAG](#8-graphrag)
  - [8.1 它结合了哪两种技术？](#81-它结合了哪两种技术)
  - [8.2 优势](#82-优势)
  - [8.3 高级 RAG 课题](#83-高级-rag-课题)
- [9. 幻觉治理与噪声抑制](#9-幻觉治理与噪声抑制)
  - [9.1 减少幻觉的三层措施](#91-减少幻觉的三层措施)
  - [9.2 召回噪声：搜索「包子」却出现「书包」](#92-召回噪声搜索包子却出现书包)
  - [9.3 私域知识「直接塞进 Prompt」的问题](#93-私域知识直接塞进-prompt-的问题)
- [10. RAG 评估指标（RAGAS）](#10-rag-评估指标ragas)
  - [10.1 四大核心指标对比](#101-四大核心指标对比)
  - [10.2 各指标如何评判](#102-各指标如何评判)
  - [10.3 一个典型反例（帮助区分指标）](#103-一个典型反例帮助区分指标)
  - [10.4 指标归属：检索 / 生成 / 端到端](#104-指标归属检索--生成--端到端)
  - [10.5 AnswerCorrectness 计算细节与 answer_accuracy 对比](#105-answercorrectness-计算细节与-answer_accuracy-对比)
- [11. 工程架构与实践](#11-工程架构与实践)
  - [11.1 为什么优化后的答疑机器人不需要每次都走 RAG？](#111-为什么优化后的答疑机器人不需要每次都走-rag)
  - [11.2 知识库上传的单文档大小限制](#112-知识库上传的单文档大小限制)
  - [11.3 安全与合规：提示词注入与敏感词拦截](#113-安全与合规提示词注入与敏感词拦截)
  - [11.4 时效性问题与联网搜索](#114-时效性问题与联网搜索)
- [12. 高频易混点速查](#12-高频易混点速查)
- [13. 参考文献](#13-参考文献)
- [14. 关联](#14-关联)
- [附：基于错题的复习清单](#附基于错题的复习清单)

---

## 0. 知识地图

先用一张 RAG 主流程图，把后面所有知识点挂上去：

```
离线 / 索引阶段                                    在线 / 问答阶段
┌───────────────────────────────────────┐   ┌──────────────────────────────────────────────┐
│ 加载 → 切片 → 向量化 → 建索引 → 持久化   │   │ 问题改写 → 检索召回 → 重排/过滤 → 生成 → 评估 │
└───────────────────────────────────────┘   └──────────────────────────────────────────────┘
```

| 阶段 | 核心问题 | 对应章节 |
|---|---|---|
| 索引构建 | 文档怎么加载、怎么切、怎么存 | 2、3 |
| 向量化 | 用哪种嵌入模型、向量怎么比 | 4 |
| 检索召回 | 怎么找得全（召回率）、找得准（精确率） | 5 |
| 多轮 / 复杂问题 | 怎么理解带指代、多跳、复杂的问题 | 6、7 |
| GraphRAG | 全局理解与多跳推理 | 8 |
| 生成与治理 | 怎么少幻觉、少噪声 | 9 |
| 评估 | 怎么量化好坏 | 10 |
| 工程落地 | 怎么省资源、怎么控限制 | 11 |

---

## 1. RAG 基础概念

- **RAG（Retrieval-Augmented Generation，检索增强生成）**：让大模型回答前先检索外部知识，把检索结果作为上下文，再生成答案。三大步为**检索 → 增强 → 生成**。
- **价值**：把「模型参数里的记忆」换成「可更新、可溯源的外部知识」，缓解知识过时、私域知识缺失和幻觉。
- **补充**：RAG 的概念由 Lewis 等人于 2020 年提出；目前主流按「索引—检索—生成」三阶段再拆分为 Naive / Advanced / Modular 三种范式（见 Gao 等人的综述）。

**关联**：[[RAG入门]]

---

## 2. 索引构建：加载与创建

### 2.1 两个高频方法

| 方法 | 角色 | 说明 |
|---|---|---|
| `SimpleDirectoryReader` | 数据加载 | 从本地目录读取文件，转换成 `Document` 对象 |
| `VectorStoreIndex.from_documents` | 构建索引 | 接收已加载的 `Document`，切分为 `Node`、生成向量、建立索引 |

### 2.2 `from_documents` 内部到底做了什么？

**只包含：文本分段（Chunking）+ 建立索引（Embedding/Indexing）。**

- **不包含「文档解析」**：解析发生在 `from_documents` **之前**——调用它时文档已经是被 `SimpleDirectoryReader` 封装好的 `Document` 对象，而不是原始文件。

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

documents = SimpleDirectoryReader("data").load_data()   # ① 加载 + 解析
index = VectorStoreIndex.from_documents(documents)      # ② 分段 + 建索引
```

### 2.3 索引的四个动作（极易混淆）

| 动作 | 方法 | 阶段 |
|---|---|---|
| 加载文档 | `SimpleDirectoryReader` | 创建索引的**起点** |
| 创建索引 | `VectorStoreIndex.from_documents` | 创建索引的**核心** |
| 查询 | `index.as_query_engine()` | 查询阶段，基于已建索引 |
| 持久化 | `index.storage_context.persist()` | 保存阶段，把索引落盘 |

> 结论：题目问「创建索引时用到哪些方法」，答案只选**加载 + 构建**，不含查询和持久化。

### 2.4 目录不存在 / 已存在，分别怎么做？

| 场景 | 做法 | 代码 |
|---|---|---|
| 存储目录**不存在** | 从原始文档重新读取并建索引 | `SimpleDirectoryReader(...)` + `VectorStoreIndex.from_documents(...)` |
| 存储目录**已存在** | 直接加载已持久化的索引 | `StorageContext.from_defaults(persist_dir=...)` + `load_index_from_storage(...)` |

```python
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### 2.5 加载本地索引可设置哪些参数？

- **存储路径**：必需，`StorageContext.from_defaults(persist_dir=...)`。
- **embedding 模型**：建议显式传入，且必须与建索引时一致（否则向量空间不匹配）。
- **API Key**：**不是** `load_index_from_storage` 的直接参数，而是初始化 embedding 模型的环境前置条件；课程若把它算作「加载流程中可设置的环节」，属于宽泛口径。

> 补充：`load_index_from_storage(..., embed_model=...)` 时若模型不一致，会导致检索质量骤降，这是线上常见事故点。

### 2.6 查询引擎参数：similarity_top_k

**召回文本段个数在创建查询引擎时设置**：

```python
query_engine = index.as_query_engine(
    similarity_top_k=3,        # 召回文本段数量，默认通常为 1 或 2
    response_mode="compact",   # 答案合成方式（compact / tree_summarize 等）
    verbose=True,
)
response = query_engine.query("你的问题")
```

| 选项 | 判断 | 说明 |
|---|---|---|
| `from_documents(similarity_top_k)` | ❌ | `from_documents` 用于**构建索引** |
| `as_query_engine(similarity_top_k)` | ✅ | 创建查询引擎时指定召回数量 |
| `query(similarity_top_k)` | ❌ | `query()` 只负责执行查询 |
| `print_response_stream(...)` | ❌ | 打印流式响应 |

> 易错点：`similarity_top_k` 设在**查询引擎创建阶段**，而不是查询执行阶段。

**「建立索引」阶段 vs 「查询」阶段**（高频判断题）：

| 阶段 | 处理对象 | 主要步骤 |
|---|---|---|
| 建立索引 | **文档** | 解析为纯文本 → 切分为小片段 → 片段向量化 → 存入向量库 |
| 查询 / 检索 | **用户问题** | 把用户问题转成向量 → 相似度检索 → 重排 → 生成 |

> 因此「**将用户问题转换为向量表示**」**不属于**建立索引阶段，而属于查询/检索阶段。

---

## 3. 文档切片（Chunking）

### 3.1 什么时候该切得更小？

**文档包含多个主题、信息量较大时。**

原因：多主题文档若整段向量化，语义会被「平均化」，单个主题的特征被稀释，检索精度下降。拆成小分块后，每块主题更聚焦。

### 3.2 各切片方法适用场景

| 切片方法 | 适合场景 | 不太适合 |
|---|---|---|
| 语义切片（Semantic） | **逻辑性强、内容专业**（技术文档、合同、医学文献） | 计算成本敏感的场景 |
| Token 切片 | 杂乱文本、快速处理、基线方案 | 专业文档、强逻辑文档 |
| 句子切片 | FAQ、短文本、细粒度检索 | 长逻辑段落 |
| 句子窗口切片 | 对话、叙述、需要上下文的场景 | 结构复杂的专业文档 |
| 标题 / 章节切片 | 结构清晰文档（Markdown、手册） | 无结构文本 |
| 递归切片 | 通用长文档、混合格式 | 规则设计复杂 |
| 表格 / 图片切片 | 多模态、结构化数据 | 纯文本简单场景 |

**口诀**：专业逻辑强 → **语义切片**；多主题大信息量 → **小分块**。

### 3.3 关键数据的「语义独立性与完整性」

- **正确做法**：每个语义单元有清晰边界与完整上下文；表格按行扩写并补上各级标题、表头字段说明；不同数据类型（文本/表格/图片）分别处理。
- **错误做法**：**把标题下的所有文本合成一个段落**——会混合多个子主题，破坏语义独立性。

> 补充：常见进阶策略还有「父子分块（Small-to-Big）」——用小块做检索、用其父块做生成，兼顾精度与上下文完整（LlamaIndex `SentenceWindowNodeParser`、`HierarchicalNodeParser` 等）。

### 3.4 基于语义的切片理念

题目：以下哪些做法符合「基于语义的文档切片」理念？**答案：B、D、E、F**。

| 选项 | 判断 | 说明 |
|---|---|---|
| A. 按固定长度切分 | ❌ | 机械切分，容易切断句子、段落和语义单元 |
| B. 按标题、段落、列表等结构切分 | ✅ | 结构与语义边界一致，尽量保持语义完整 |
| C. 表格每个单元格独立成 Chunk | ❌ | 破坏行列关系与整体语义，应保留表头、按行或整体切 |
| D. 在 Chunk 中添加上下文（标题、父级列表项等） | ✅ | 上下文增强，避免切片脱离原文后语义不清 |
| E. 用机器学习模型分析语义边界并切分 | ✅ | 最典型、最直接的「基于语义切片」 |
| F. 代码块单独切分并标注编程语言 | ✅ | 保持代码完整、保留语义，便于检索与生成 |

> 关键认识：**语义切片 ≠ 只靠模型**。按文档结构切分、给 Chunk 补上下文、代码块保持完整，都属于「保语义完整」的语义切片范畴；而「固定长度」「把表格单元格打散」属于机械切分。
> 补充：语义切片常用「相邻句子/段落向量相似度骤降处」作为切分点（LangChain `SemanticChunker` 思路）。

---

## 4. 嵌入模型与向量化

### 4.1 大模型 vs Embedding 模型（分工必背）

| 模型 | 负责 | 典型任务 |
|---|---|---|
| **大模型（LLM）** | 生成 / 理解 / 判断 / 推理 / 规划 | 提取观点、问题改写、判断事实一致性、生成答案 |
| **Embedding 模型** | 向量化 / 相似度 | 文档向量化、问题向量化、检索召回、聚类去重、语义相似度打分 |

**在 RAG 流程中的分工**：

1. 建索引：Embedding 模型把文档块向量化。
2. 检索：Embedding 模型把问题向量化并算相似度。
3. 生成：大模型依据召回内容生成答案。
4. 评估：大模型提取观点、判断正确性；Embedding 模型辅助算语义相似度。

### 4.2 常见嵌入模型

| 模型 | 归属 | 备注 |
|---|---|---|
| `text-embedding-3-small` | OpenAI | 便宜、够用 |
| `text-embedding-3-large` | OpenAI | 效果更好、成本更高 |
| `text-embedding-ada-002` | OpenAI | 早期模型 |
| `text-embedding-v2` / `text-embedding-v3` | 阿里云通义 | **不是 OpenAI 的** |
| BGE 系列 | 智源 BAAI | 一类先进文本嵌入模型，直接提升索引与检索质量 |

> 易错点：题目问「OpenAI 提供的 Embedding 模型」，只选 `text-embedding-3-small` / `text-embedding-3-large`（可加 ada-002）；`v2/v3` 是通义。

### 4.3 `compare_embeddings` 函数

- **用途**：在「切片向量化与存储」阶段接收查询与文档切片，用**多个嵌入模型**分别计算 embedding 并输出相似度对比，用于检查切片与向量化是否符合预期。
- **参数**：`query`（查询文本）、`chunks`（文档切片）、`embedding_models`（要对比的多个嵌入模型）。
- **不是参数**：`cosine_similarity`——它是内部使用的相似度计算方法。

> 另有一个 `compare_embedding_models`（带 ground_truth）在 LlamaIndex / RAGAS 官方文档中查无标准定义，很可能来自特定课程的自定义封装，**以课程材料为准**。

### 4.4 文本向量化的三个正确认识

题目：在文本向量化过程中，以下哪些描述正确？**答案：A、B、C**。

- **A. Embedding 模型把自然语言转化为数字形式**：核心作用就是把文本映射成数字向量，用数字表示语义。
- **B. 使用余弦相似度衡量向量相似度**：向量化后常用余弦相似度衡量语义相近程度，归一化后的 embedding 尤其常见。
- **C. Embedding 模型的训练包含对比学习**：现代文本 embedding（Sentence-BERT、SimCSE、BGE 等）训练中通常含对比学习，通过**拉近正样本、推远负样本**学习语义向量。

> 补充：余弦相似度 = 两向量夹角的余弦；向量归一化后，余弦相似度与点积等价。

### 4.5 `embedding_models` 字典的作用

在「切片向量化与存储」阶段，`embedding_models` 通常是**管理不同 embedding 模型实例的字典**。

**典型作用**：

- 注册 / 保存不同的 embedding 模型实例；
- 按模型名称或配置获取对应模型；
- 复用已初始化的模型，避免重复加载；
- 为切片批量生成向量：`embedding_models[model_name].embed_documents(texts)`；
- 支持多模型、多知识库、多集合切换。

**一般不属于它的作用**：存切片文本、存向量结果、存向量数据库连接 / 索引 / 集合、执行文档切片、保存检索结果或元数据。

> 速记：`embedding_models` 管的是「**模型实例**」，不是「**数据存储**」。

---

## 5. 检索召回优化

### 5.1 相似度阈值与召回数量

- 界面里的「检索片段数」是**上限（Top-K）**，不是必须返回的数量。
- 最终召回 = **通过相似度阈值过滤后的数量**。例：K=5，但高于阈值的只有 3 块 → 实际召回 **3** 块。
- 阈值越高，噪声越少但可能漏召回；阈值越低，召回多但噪声多。
- **案例一（召回太少）**：系统总是只检索到**一个无关切片** → 提高 Top-K，返回更多候选。换更大参数量的模型只影响生成，放弃知识库易产生幻觉，都不能解决问题。
- **案例二（阈值过高）**：阈值从 0.7 提到 0.95 → 过滤掉「相关但表述不同、相似度略低」的上下文 → 答案**准确但不全面**，部分问题答不好。**阈值不是越高越好**。

### 5.2 标签增强检索（Metadata Filtering）

**正确顺序：先标签过滤（约束候选集），再做向量相似度检索。**

- 索引阶段：从文档切片中抽取结构化标签（主题、类别、时间、来源等）。
- 检索阶段：从用户问题中识别标签，与索引标签匹配/过滤，缩小范围后做向量检索。
- **错误做法：先向量检索，再标签过滤**——先取 Top-K 再过滤，可能过滤后结果很少甚至为空，也让「标签缩小范围」的意义丧失。

> 补充：现代向量库普遍支持「元数据预过滤（pre-filter）」，与上述结论一致；部分实现会做混合策略，但考试语境下「先向量后过滤」通常被视为错误。

### 5.3 多查询类技术辨析（高频易混）

| 技术 | 核心做法 | 侧重点 |
|---|---|---|
| **Multi-Query 多路召回** | 生成**多个语义相关、表述不同**的查询，分别检索后合并 | 提高问题理解的**广度与深度** |
| **Step Back 问题摘要** | 把具体问题**抽象**成更上位的概念/原理再去检索 | 抽象与推理 |
| **Decomposition 问题分解** | 把复杂问题拆成若干子问题，分别检索后综合 | 化繁为简，解决**多跳**问题 |
| **RAG-Fusion** | 对多路召回结果做融合排序（如 RRF） | 与 Multi-Query 配合使用 |

> 记忆：「提出多个相关查询」这个动作本身 = **Multi-Query**；RAG-Fusion 是它的「结果融合」搭档。

### 5.4 HyDE（Hypothetical Document Embeddings）

**核心思路：先让大模型「编」一个假设答案，再用这个答案去检索真实文档。**

流程：

1. **生成假设文档**：LLM 根据问题生成一篇「假设答案」（可能含事实错误，但用词、风格、结构接近真实文档）。
2. **编码**：把假设文档转成向量（而非用原始问题转向量）。
3. **检索**：用该向量在知识库中找最相似的真实文档。
4. **生成**：把真实文档交给 LLM 生成最终答案。

**为什么需要**：用户提问通常短、口语化，知识库文档长、正式，两者在向量空间距离远，容易匹配不上；根本原因是**问题和答案的表述方式不一致**。

**关键点**：假设文档**不需要正确**，它只是**语义桥梁**；代价是**多一次 LLM 调用**，增加延迟与成本。

### 5.5 检索后减少无关信息

| 方法 | 作用 |
|---|---|
| **重排序（Rerank）** | 初步召回后重新打分排序，过滤低相关内容 |
| **滑动窗口检索** | 在长文档中定位最相关的一小段，只输出窗口内内容，减少无关信息进入生成 |

> 注：标准答案可能只把「重排序」算作检索后处理，但滑动窗口检索在长文档场景下同样能减少无关信息，**以课程答案为准**。
> 补充：还有 **CRAG（Corrective RAG）**、**Self-RAG** 等「检索质量自省/纠错」范式，会在检索后判断相关性，必要时触发互联网检索或重写。

### 5.6 提高知识索引/检索性能的技术

- **BGE 新嵌入模型**：直接提升向量化表示质量，属于「换更强的嵌入模型」。
- 其余多属**查询优化**（Decomposition、Step Back）或**检索策略**（CRAG 互联网检索），不涉及嵌入模型本身。

### 5.7 扩充信息以提升召回（Query Expansion / 用户画像）

题目：哪些方法通过**增加更多信息**让检索结果更全面？**答案：A、B**。

| 选项 | 判断 | 说明 |
|---|---|---|
| A. 问题扩写（Query Expansion） | ✅ | 在原始 query 中加入同义词、相关概念、背景信息，增加信息量，召回更全面 |
| B. 基于用户画像扩展上下文 | ✅ | 把用户偏好、历史行为、场景加入查询理解，增加个性化信息，优化召回范围 |
| C. 问题改写（Query Rewriting） | ❌ | 通常只是换表达（同义替换、纠错、规范化）或生成多个等价 query，**不一定增加新信息** |
| D. 重排序（Rerank） | ❌ | 召回之后的排序/精排，不增加信息，也不扩大召回集合 |

> 判断标准：**是否引入了原始 query 之外的新信息**。扩写 / 画像扩展 = 加信息；改写 = 换说法；重排序 = 只是重排。

---

## 6. 多轮对话与查询改写

### 6.1 `custom_chat_history` 的作用

**为 RAG 系统提供对话记忆，确保模型能理解并正确回应依赖上下文的后续提问。**

### 6.2 机制：问题改写（Query Rewriting）

多轮中后续问题常含指代或省略：

- 第 1 轮：「什么是任务分解？」
- 第 2 轮：「常见的做法有哪些？」←「做法」指什么？检索器不知道。

流程：

1. 将**聊天历史 + 最新问题**一起送入 LLM；
2. LLM 把问题改写成**不依赖历史的独立问题**；
3. 用改写后的问题检索知识库；
4. 获取真正相关的上下文，生成准确回答。

**辅助作用**：`custom_chat_history` 也会注入最终生成的 Prompt，使回答保持连贯。
**技术形式**：通常是含 `user`/`assistant` 的消息列表，可通过代码（如 LlamaIndex `CondenseQuestionChatEngine`）或 API 传递。

> 补充：常与「Query Rewriting / Condense Question」并用的还有多轮检索中保留「对话摘要」，避免历史过长挤占上下文窗口。

### 6.3 问题改写：检索前还原真实意图

题目：以下哪些方法用于在**检索前**还原用户真实意图？**答案：A、B、C**。

| 选项 | 判断 | 说明 |
|---|---|---|
| A. 用大模型扩充用户问题 | ✅ | 查询扩展/改写：补充同义表达、背景信息、潜在意图，更全面理解真实需求 |
| B. 将单一查询改写为多步骤查询 | ✅ | 查询分解/多步改写：把复杂 query 拆成子查询，更贴近真实意图，便于多路召回 |
| C. 用假设文档增强检索（HyDE） | ✅ | 生成假设文档再检索，缩小 query 与文档的语义差距，还原检索意图 |
| D. 重排序 | ❌ | 发生在召回**之后**，对已检索文档重排，不属于检索前改写，也不负责还原意图 |

> 对照记忆：**检索前**改 query（扩写 / 分解 / HyDE）；**检索后**重排结果（Rerank）。

---

## 7. 复杂问题求解：分解与多步检索

### 7.1 核心框架：「分解 — 执行 — 合成」

1. **分解（Decompose）**：LLM 判断复杂度，生成 1–3 个更简单的子问题。
2. **执行（Execute）**：对每个子问题独立检索并回答，得到中间答案。
3. **合成（Synthesize）**：汇总中间答案，生成最终回答。

### 7.2 常用框架与工具

| 框架/工具 | 作用 |
|---|---|
| LlamaIndex `SubQuestionQueryEngine` | 最直接方案：自动拆解复杂查询、分发执行、最后汇总 |
| LlamaIndex `MultiStepQueryEngine` + `StepDecomposeQueryTransform` | 面向**顺序依赖**的分解，后一子问题可能依赖前一答案，适合多跳推理 |
| LangChain / IterDRAG | 用 `decompose_prompt` 定义分解规则，`intermediate_prompt` 处理子问题，强调**迭代** |

### 7.3 提示词关键要素

- **定义复杂问题**：说明什么查询需要分解（比较、多条件、多跳）。
- **生成子问题**：要求输出格式化列表（如 `Follow up: [sub-question]`），便于程序解析。
- **包含示例（Few-shot）**：提供「复杂问题 → 子问题」样例，显著提升质量。
- **处理简单查询**：明确要求简单问题直接返回原问题 / 「无需分解」。

### 7.4 检索召回阶段「思考并规划多次检索」

- 对应「**思考并规划多次检索**」本身，属于多步检索策略。
- 易混：**问题改写**属查询优化；**重排序**属后处理；**增加训练数据**属模型训练层面。

### 7.5 注意事项

- **不要滥用**：简单事实查询强制分解会增加延迟并可能引入错误。
- **动态迭代优于一次性拆分**：迭代式（根据上一轮结果决定下一步）在多跳问答中通常更稳。

---

## 8. GraphRAG

### 8.1 它结合了哪两种技术？

**检索增强生成（RAG）+ 查询聚焦摘要（QFS，Query-Focused Summarization）。**

- **RAG**：从外部知识库检索相关信息交给大模型生成。
- **QFS**：针对某个查询，对大量文本做聚焦式摘要与归纳。
- **核心**：通过构建**知识图谱**组织实体、关系和社区摘要，在**全局理解**与**多跳推理**问题上优于传统 RAG。

### 8.2 优势

| 选项 | 判断 | 说明 |
|---|---|---|
| 准确回答具体问题 | ✅ | 利用图谱中的实体与关系提升准确性 |
| 处理需要深入理解的复杂查询 | ✅ | 核心优势，图结构支持多跳推理 |
| 提高模型训练速度 | ❌ | 不涉及，反而可能增加图构建开销 |

> 补充：GraphRAG 由微软于 2024 年提出，通过「社区检测 + 社区摘要」解决传统 RAG 难以回答「整体趋势/总结类」全局问题。

### 8.3 高级 RAG 课题

题目：构建 RAG 应用时，哪些高级 RAG 课题值得探索？**答案：A、B、C**。

| 选项 | 判断 | 说明 |
|---|---|---|
| A. GraphRAG 技术 | ✅ | 结合知识图谱、图检索与多跳推理，提升全局性、关联性问题的召回与回答 |
| B. 可视化工作流 | ✅ | 工程化课题：编排、调试、监控 RAG 流程（检索、路由、生成、评估） |
| C. 智能体编排（Agentic RAG） | ✅ | 智能体规划、工具调用、多步检索、反思与纠错 |
| D. LlamaIndex 组件 | ❌ | 偏具体框架的工具/组件，是**实现手段**，通常不算独立的高级 RAG 课题 |

> 一句话：高级 RAG = **GraphRAG（图）+ 可视化工作流（工程）+ Agentic RAG（智能体）**；框架组件是脚手架，不是课题本身。

---

## 9. 幻觉治理与噪声抑制

### 9.1 减少幻觉的三层措施

| 措施 | 作用层面 | 说明 |
|---|---|---|
| A. 提示词约束 | 生成**前** | 要求禁止虚构、只基于上下文、信息不足时拒答 |
| B. 引入知识库 | 生成**时**（知识补充） | 用真实资料约束生成，减少凭参数记忆胡编，是 RAG 的核心价值 |
| C. 后处理与验证 | 生成**后** | 检查一致性、二次检索交叉验证、过滤低置信度、必要时重生成或拒答 |

> 记忆：**生成前约束 → 生成时知识支撑 → 生成后校验**，三者组合效果最好。

### 9.2 召回噪声：搜索「包子」却出现「书包」

**问题根因在召回阶段已混入无关商品，应在召回阶段治理。**

| 选项 | 判断 | 原因 |
|---|---|---|
| A. 降低相似度阈值 | ❌ 反向 | 会让更多低相似文档进入，噪声更多 |
| B. 优化 prompt | ⚠️ 辅助 | 可减少最终输出无关项，但召回已脏，治标不治本 |
| C. 微调大模型 | ⚠️ 辅助 | 成本高、周期长，不解决召回根本问题 |

**正确方向**：适当**提高相似度阈值**、**去重**、**标签过滤**、**混合检索**、**重排序（Rerank）**。
- 提高阈值：直接有效，但过高可能误杀相关但表述不同的商品。
- 减少重复记录：提升结果多样性、降低无关占比，但不能阻止「书包」被召回。

### 9.3 私域知识「直接塞进 Prompt」的问题

**不能把全部私域参考信息直接塞进提示词。**

| 选项 | 判断 | 说明 |
|---|---|---|
| A. 提示词长度有限 | ✅ | 容易超出上下文窗口 |
| B. 模型处理效率降低 | ✅ | 输入越长推理开销越大 |
| C. 模型无法理解私域知识 | ❌ | 大模型通常能理解，问题是信息多、噪声大 |
| D. 模型生成内容不准确 | ✅ | 无关、矛盾信息干扰，导致不准确或幻觉 |

**结论**：私域知识应走 RAG 检索式注入，而非全量直塞。

---

## 10. RAG 评估指标（RAGAS）

### 10.1 四大核心指标对比

| 指标 | 关注点 | 典型反例场景 |
|---|---|---|
| **Context Precision（上下文精确率）** | 相关召回文本段**排名是否靠前** | 相关段落被排在末尾 |
| **Answer Relevancy（答案相关性）** | 答案是否**切题** | 问「如何退款」，答「退货政策历史」 |
| **Faithfulness / Groundedness（忠实度/接地性）** | 答案是否**忠于召回原文** | 答案含检索文本中不存在的信息（幻觉） |
| **Answer Correctness（答案正确性）** | 与标准参考答案的**事实与语义一致** | 事实错误或遗漏要点 |
| **整体回答质量** | 综合多维度 | 全面评估 |

### 10.2 各指标如何评判

**Faithfulness（忠实度）**
- 把答案拆成独立事实陈述，逐句检查能否从召回文本找到依据。
- 通常由 **LLM** 执行；高分 = 完全基于给定材料，低分 = 出现**幻觉**。

**Answer Relevancy（答案相关性）**
- 关注答案是否**直接、切题**，不关心是否忠于原文。
- 两种做法：**反向生成问题法**（RAGAS 常用，根据答案反向生成问题，再算与原始问题的语义相似度）；**直接打分法**（LLM 按 1–5 分或 0–1 分打分）。

**Context Precision（上下文精确率）**
- 衡量真正相关的文本段是否排在**更靠前**的位置，本质是**排序质量**指标。
- 判断 `context_i` 是否相关的依据：**question + ground_truth**。
- 计算三步骤：
  1. 按顺序读取 `contexts` 中的 `context_i`，判断其是否相关；
  2. 计算每个 context 的 precision 分；
  3. 对每个 context 的 precision 分求和，除以相关的 context 个数。
- 核心思想：越相关的结果排在越前面，分数越高。

**Answer Correctness（答案正确性）**
- 计算时使用两类模型：
  - **大模型**：提取 answer 与 ground_truth 的**观点列表**，并判断事实一致性；
  - **Embedding 模型**：计算答案与参考答案的**语义相似度**。
- 比较对象：**answer 的观点列表 vs ground_truth 的观点列表**。
- 优化措施（四项均可行）：优化 prompt、调低 `temperature`、换更强的大模型、领域微调。

**整体回答质量**
- 由一组指标综合衡量：**忠实度/接地性 → 答案正确性 → 答案完整性**。
- 评判逻辑：先看**是否忠于原文** → 再看**事实对不对** → 最后看**要点全不全**。

### 10.3 一个典型反例（帮助区分指标）

- 提问：GraphRAG 结合了哪两种技术？
- 检索文本：正确提到了 RAG 和 QFS。
- 生成答案：「GraphRAG 是一种基于知识图谱的检索方法，广泛应用于企业搜索。」

| 指标 | 表现 |
|---|---|
| Faithfulness | 高分（忠于原文） |
| Context Precision | 高分（相关文本排名靠前） |
| **Answer Relevancy** | **低分（没有回答问题）** |

> 结论：Answer Relevancy 评判答案的**切题程度**，独立于忠实度与检索质量。

### 10.4 指标归属：检索 / 生成 / 端到端

题目：`faithfulness`、`answer_relevancy`、`context_recall`、`context_precision` 中，哪个**仅评估生成阶段**？**答案：`faithfulness`**。

| 指标 | 归属阶段 |
|---|---|
| `context_precision` | **检索阶段**（检索上下文质量） |
| `context_recall` | **检索阶段**（检索上下文质量） |
| `faithfulness` | **生成阶段**（答案是否忠于上下文、有无幻觉） |
| `answer_correctness` | **端到端**（答案 vs 标准答案） |

> 记忆：`context_*` 属检索；`faithfulness` 属生成；`answer_correctness` 属端到端。做题先分清检索 / 生成 / 端到端三层。

### 10.5 AnswerCorrectness 计算细节与 answer_accuracy 对比

`answer_correctness` 是**端到端指标**，衡量生成答案与 `ground_truth` 的匹配程度，由「事实性」和「语义相似度」加权融合：

1. **事实性（Factual Correctness）**：把答案拆成事实陈述并分类——
   - **TP**：生成答案与标准答案都出现的事实；
   - **FP**：只在生成答案中出现的事实（幻觉 / 错误）；
   - **FN**：只在标准答案中出现、生成答案遗漏的事实。
   计算 F1 分数：`F1 = |TP| / (|TP| + 0.5 × (|FP| + |FN|))`。
2. **语义相似度（Semantic Similarity）**：生成答案与标准答案向量嵌入的余弦相似度。
3. **最终得分**：默认权重 `[0.75, 0.25]`，即事实性 75%、语义相似度 25%。

**与 `answer_accuracy` 的区别**：

| 指标 | 机制 | 特点 |
|---|---|---|
| `answer_correctness` | 陈述分解 + 分类，可解释性高 | 需 3 次 LLM 调用 |
| `answer_accuracy` | 双法官系统，2 次独立判断 | 可解释性较低 |

```python
from datasets import Dataset
from ragas.metrics import answer_correctness
from ragas import evaluate

data_samples = {
    "question": ["When was the first super bowl?"],
    "answer": ["The first superbowl was held on Jan 15, 1967"],
    "ground_truth": ["The first superbowl was held on January 15, 1967"],
}
dataset = Dataset.from_dict(data_samples)
score = evaluate(dataset, metrics=[answer_correctness])
print(score.to_pandas())
```

---

## 11. 工程架构与实践

### 11.1 为什么优化后的答疑机器人不需要每次都走 RAG？

**答案：节省资源，并避免知识库信息干扰大模型推理。**

加入**路由 / 意图判断**机制：

- 简单问题（寒暄、常识、固定话术）→ 直接由大模型回答。
- 需要知识库支撑的问题 → 才走 RAG 链路。

好处：① 省掉向量检索、重排、拼接上下文的开销，降低延迟与成本；② 避免不必要检索引入无关片段干扰推理。

**`ask_llm_route`：问题路由 / 意图分发器**

它根据用户问题判断任务类型并返回对应处理方式，**自身不直接回答问题**：

```python
def ask_llm_route(question):
    if is_review_question(question):
        return reviewed_prompt        # 提示词审查类
    elif is_translate_question(question):
        return translate_prompt       # 翻译类
    elif is_query_engine_question(question):
        return query_engine           # 查询引擎类
    else:
        return rag.ask                # 无法识别 / 通用问答 → 默认兜底
```

> 无法识别问题类型时，走**默认兜底分支**，交给通用 RAG 问答流程，即返回 `rag.ask`。

### 11.2 知识库上传的单文档大小限制

**没有统一标准，取决于平台。** 课程场景答案为 **100MB**（腾讯云 TCDataAgent 默认值）。

| 平台 | 单文档大小限制（默认） | 备注 |
|---|---|---|
| 腾讯云 TCDataAgent | **100MB** | PDF/Word/PPT；MD/TXT 仅 10MB，图片 20MB |
| 华为云盘古 | 128MB | 超过 60MB 建议用 API 上传 |
| RAGFlow | 128MB | Web UI 曾有 8–10MB 临时 Bug，现已移除 |
| Dify | 15MB | 可通过 `UPLOAD_FILE_SIZE_LIMIT` 调整 |
| 阿里云百炼 | 150MB | PDF/Word；TXT/Markdown 仅 10MB |
| 腾讯云（另一产品） | 200MB | 表格类文件为 20MB |

**实践建议**：查具体平台官方文档，或检查环境变量（如 `MAX_CONTENT_LENGTH`、`UPLOAD_FILE_SIZE_LIMIT`）。

### 11.3 安全与合规：提示词注入与敏感词拦截

**提示词注入获取知识库元数据 → 最有效的防护是系统层权限控制**：

| 选项 | 判断 | 说明 |
|---|---|---|
| A. 知识检索阶段严格限制数据访问权限 | ✅ | 只让应用访问当前用户有权查看的数据，元数据 / 非公开信息隔离，遵循最小权限 |
| B. 过滤「元数据」等关键词 | ❌ | 易被绕过（换词、编码、间接提问） |
| C. 让大模型避免回答这类问题 | ❌ | 软约束，注入可覆盖或绕过 |
| D. 避免列表形式输出 | ❌ | 与防止元数据泄露无关 |

**敏感词实时拦截（金融投顾场景）→ 在用户提问时实时检测**：

- 命中「内幕消息」等敏感词，立即返回预设合规话术，**不进入后续检索 / 生成**，响应最快、最可控。
- A 生成后二次审核有延迟；B 知识库预筛查管的是文档内容；D 微调只降低风险话题概率，都不能满足「立即返回固定话术」。

> 速记：**防注入靠权限隔离**（系统层 > 提示词过滤）；**敏感词靠输入前置拦截**。

### 11.4 时效性问题与联网搜索

题目：「总结今早的十大新闻」这类**强时效**需求，哪些方案可行？**答案：B、C**。

- A. 历史新闻库 + RAG ❌：知识库可能未更新到今早新闻，无法保证时效与完整。
- B. function call 调用搜索工具 ✅：实时获取最新新闻。
- C. 阿里云百炼 qwen-plus 设置 `enable_search=True` ✅：开启联网搜索，获取实时信息。

> 易错点：**RAG 知识库 ≠ 实时联网搜索**；历史库解决不了「今早」这种强时效问题。补充：这正是 Tool / Function Calling 的典型应用。

---

## 12. 高频易混点速查

| 易混对 | 一句话区分 |
|---|---|
| 文档解析 vs 文本分段 | 解析在 `from_documents` 之前，分段在它内部 |
| 创建索引 vs 查询 vs 持久化 | 创建 = 加载 + 构建；查询 = `as_query_engine`；持久化 = `persist` |
| 标签过滤 vs 向量检索顺序 | **先标签过滤，再向量检索** |
| Multi-Query vs RAG-Fusion | Multi-Query 负责「生成多个查询」；RAG-Fusion 负责「融合排序结果」 |
| Multi-Query vs Step Back | 前者扩展查询广度，后者把问题抽象成上位概念 |
| Decomposition vs 多步检索 | Decomposition 拆子问题；「思考并规划多次检索」是迭代式多步策略 |
| HyDE vs 普通检索 | HyDE 用「假答案」的向量去检索，桥接提问与文档的表述差异 |
| 大模型 vs Embedding 模型 | 生成/理解/判断用大模型；向量化/相似度/检索用 Embedding |
| Answer Relevancy vs Faithfulness | 前者问「切题吗」，后者问「有出处吗」 |
| Context Precision vs Context Recall | 前者看排序（相关项是否靠前），后者看是否把相关项都召回 |
| 问题扩写 vs 问题改写 | 扩写引入**新信息**（同义词/背景）；改写多为换表达，不一定加信息 |
| 检索前改写 vs 检索后重排序 | 前者改 query，后者对已召回结果重排 |
| 语义切片 vs 固定长度切片 | 前者按结构/语义边界，后者机械切分易断语义 |
| GraphRAG vs Agentic RAG | 前者靠知识图谱，后者靠智能体规划与工具调用 |
| 建立索引 vs 查询阶段 | 索引处理**文档**（解析/切分/向量化/入库）；查询才把**用户问题**向量化 |
| 提高 Top-K vs 提高相似度阈值 | 前者扩大候选（召回少时用），后者更严过滤（易漏召回，答案准确但不全面） |
| RAG 知识库 vs 联网搜索 | 历史库保证不了「今早」的时效性；强时效问题走 function call / 联网搜索 |
| faithfulness vs context_precision | 前者属生成阶段，后者属检索阶段 |

---

## 13. 参考文献

**经典论文**

1. Lewis et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020. arXiv:2005.11401
2. Gao et al. *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv:2312.10997
3. Es et al. *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. EACL 2024 (Demo). arXiv:2309.15217
4. Gao et al. *Precise Zero-Shot Dense Retrieval without Relevance Labels*（HyDE）. ACL 2023. arXiv:2212.10496
5. Edge et al. *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. arXiv:2404.16130
6. Xiao et al. *C-Pack: Packed Resources for General Chinese Embeddings*（BGE）. SIGIR 2024. arXiv:2309.07597
7. Rackauckas. *RAG-Fusion: A New Take on Retrieval-Augmented Generation*. arXiv:2402.03367
8. Zheng et al. *Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models*. arXiv:2310.06117
9. Zhou et al. *Least-to-Most Prompting Enables Complex Reasoning in Large Language Models*. arXiv:2205.10625
10. Yan et al. *Corrective Retrieval Augmented Generation*（CRAG）. arXiv:2401.15884
11. Asai et al. *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*. arXiv:2310.11511
12. Liu et al. *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172
13. Reimers & Gurevych. *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. EMNLP 2019. arXiv:1908.10084
14. Gao et al. *SimCSE: Simple Contrastive Learning of Sentence Embeddings*. EMNLP 2021. arXiv:2104.08821
15. Carpineto & Romano. *A Survey of Automatic Query Expansion in Information Retrieval*. ACM Computing Surveys, 44(1), 2012.
16. Singh et al. *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG*. arXiv:2501.09136

**官方文档**

17. LlamaIndex 官方文档：https://docs.llamaindex.ai
18. OpenAI Embeddings 指南：https://platform.openai.com/docs/guides/embeddings
19. 阿里云百炼 文本嵌入 API：https://help.aliyun.com/zh/model-studio/text-embedding-synchronous-api
20. RAGAS 官方文档：https://docs.ragas.io
21. OWASP Top 10 for LLM Applications（LLM01: Prompt Injection）：https://owasp.org/www-project-top-10-for-large-language-model-applications/
22. OpenAI Function Calling 指南：https://platform.openai.com/docs/guides/function-calling

---

## 14. 关联

- [[RAG入门]]
- [[向量检索]]

---

## 附：基于错题的复习清单

- [ ] RAG 三阶段：索引 → 检索 → 生成。
- [ ] `from_documents` = 文本分段 + 建索引，**不含文档解析**。
- [ ] 目录不存在 → `SimpleDirectoryReader` + `VectorStoreIndex`；已存在 → `load_index_from_storage`。
- [ ] 切片：专业逻辑强 → 语义切片；多主题大信息量 → 小分块。
- [ ] 大模型负责生成/判断，Embedding 负责向量化/相似度。
- [ ] 召回数量受相似度阈值限制，Top-K 只是上限。
- [ ] 标签增强检索：**先过滤，再向量检索**。
- [ ] Multi-Query / Step Back / Decomposition / RAG-Fusion 分清。
- [ ] HyDE：用假设文档搭语义桥梁，假设文档不需要正确。
- [ ] GraphRAG = RAG + QFS，优势在多跳推理与全局理解。
- [ ] 减少幻觉三层：生成前约束、生成时知识支撑、生成后校验。
- [ ] 召回噪声优先治**召回阶段**（阈值、过滤、混合检索、重排）。
- [ ] AnswerCorrectness：大模型提观点 + Embedding 算相似度。
- [ ] Context Precision：结合 question 与 ground_truth 判断相关性，按排序计算。
- [ ] 私域知识走 RAG 注入，不要全量直塞 Prompt。
- [ ] 语义切片理念：结构切分 + 上下文增强 + 模型语义边界 + 代码块完整；固定长度 / 表格打散不算。
- [ ] 文本向量化三认识：数字向量 + 余弦相似度 + 对比学习。
- [ ] 问题扩写增加**新信息**，问题改写不一定；重排序不增加信息。
- [ ] 高级 RAG 课题：GraphRAG、可视化工作流、Agentic RAG（框架组件不算）。
- [ ] `similarity_top_k` 在 `as_query_engine(...)` 创建时设置；用户问题向量化属查询阶段，不属建立索引。
- [ ] `embedding_models` 管模型实例，不管数据存储。
- [ ] 召回太少 → 提高 Top-K；阈值过高 → 召回不足、答案准确但不全面。
- [ ] 指标归属：`context_*` 检索、`faithfulness` 生成、`answer_correctness` 端到端。
- [ ] `answer_correctness` = 事实 F1（TP/FP/FN）+ 语义相似度，默认权重 0.75/0.25。
- [ ] 防提示词注入靠权限隔离；敏感词在输入阶段实时拦截。
- [ ] 强时效问题用联网搜索 / function call，历史 RAG 库不够。
- [ ] `ask_llm_route` 无法识别类型时默认走 `rag.ask`。
