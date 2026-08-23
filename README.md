# my-kb 使用说明

一个个人学习知识库：笔记是纯文本 Markdown，用**关键词检索 + 大模型问答**代替繁重的分类整理。

## 一句话理解

你只管把笔记**分类好、随手丢进 `notes/` 目录**，剩下的（检索、问答、找关联）交给 `kb` 命令。不用 embedding、不用向量库、不花额外 API 钱。

## 核心流程：grep 找，大模型答

```
① 记笔记              ② 检索               ③ 问答 / 整理
   │                     │                    │
   ▼                     ▼                    ▼
notes/ 下按目录      kb grep "关键词"     kb ask "问题"
分类写 Markdown      （grep 关键词命中）    （命中文档→GLM→答案）
                                          kb lint（找关联/孤立）
```

**为什么不是"语义搜索"？** 语义搜索要 embedding（额外 API 成本 + 本地高配置）。改用 grep 关键词匹配，零成本、可解释、实时。代价是"说法不同"会漏，靠**良好目录分类 + 命名**弥补。

## 一次性配置

1. 装了 Python 3.11+，安装依赖：

   ```
   pip install -e .
   ```

2. 在项目根目录创建 `.env`（已存在则直接改），填你的 **OpenCode Go** API key（在 [opencode.ai/auth](https://opencode.ai/auth) 获取）：

   ```
   KB_LLM_BASE_URL=https://opencode.ai/zen/go/v1
   KB_LLM_API_KEY=你的Go key
   KB_LLM_MODEL=glm-5.2
   ```

   这里复用的是你已有的 Go 订阅（GLM 聊天模型），零额外成本。想换别的 OpenAI 兼容服务，改这三行即可（智谱、本地 Ollama 等）。

## 日常使用

### 记笔记

在 `notes/` 下按目录分类写 Markdown（推荐 Obsidian 打开 `notes/` 目录当编辑器）。**文件名和标题起得清楚点**——它们是 grep 检索的关键。

### 草稿与发布

灵感来了先丢 `drafts/`（不参与 grep/ask/lint），想清楚了再发布：

```
kb publish "临时灵感"           # 移到 notes/
kb publish "临时灵感" -t 主题A   # 移到 notes/主题A/
```

- 草稿文件名可省略 `.md`
- 目标已有同名文件时会拒绝覆盖
- 草稿区在 Obsidian 里和 notes 同 vault，随手拖拽也行

### 检索：kb grep

```
kb grep 向量 检索
```

按关键词命中排序，输出命中的笔记和片段：

```
向量检索.md  (命中 2 词, 10 次)
  1: # 向量检索（Vector Search）
  5: 把文本转成高维向量……
```

命中更多关键词的排在前面；没命中会明确提示。

### 问答：kb ask

```
kb ask "什么是向量检索，和关键词检索有什么区别" -k 向量 检索
```

流程：用 `-k` 的关键词 grep 命中笔记 → 把命中的笔记内容 + 你的问题交给 GLM → 返回答案。

- `-k` 可省略，省略时从问题里自动提取词。
- `-n 3` 控制喂给模型的笔记篇数（默认 3）。
- 没找到相关笔记时，会提示而非编造。

### 整理：kb lint

```
kb lint
```

按需整理知识库，输出：

- **关联建议**：内容相关、但还没互相链接的笔记对（建议你补 `[[双链]]`）
- **孤立笔记**：跟谁都关联不上的笔记

它是**增量**的：结果记在 `.kb_cache/lint.json`，下次只处理新增/改动的笔记，不重复劳动。

- `--threshold 2` 判定相关的特征重叠数（默认 2，越小越敏感，可能误报越多）。
- `-n 5` 每篇笔记显示的关联条数（默认 5）。

## 命令速查

| 命令 | 作用 |
|------|------|
| `kb grep "词1" "词2"` | 关键词检索，列命中文档与片段 |
| `kb ask "问题" -k 词1 词2` | 检索命中 → 大模型回答 |
| `kb lint` | 找关联建议 + 孤立笔记（增量） |
| `kb publish "草稿" -t 子目录` | 把草稿从 drafts/ 发布到 notes/ |

## 项目结构

```
my-kb/
├── notes/        ← 正式笔记（纯 Markdown，进入检索/问答/lint，git 管理）
├── drafts/       ← 草稿区（快速记灵感，不参与检索，发布后进 notes/）
├── kb/           ← 检索/问答/整理/发布的 Python 代码
├── .kb_cache/    ← 缓存（lint 档案，可删，会自动重建）
├── .env          ← LLM 配置（含 key，已被 gitignore）
└── openspec/     ← 变更管理（可忽略）
```

## 常见问题

**笔记会丢吗？** 不会。笔记就是 `notes/` 下的纯文本 Markdown，配合 git 版本化。删掉 `.kb_cache/` 不影响笔记，`kb lint` 会重建档案。

**`kb grep` 和 `kb ask` 的关系？** `grep` 是纯检索（不用大模型，免费）；`ask` 是检索 + 回答（用 Go 的 GLM，按需调）。不确定关键词时先用 `grep` 探路。

**想换大模型？** 改 `.env` 三行，例如切本地 Ollama：`KB_LLM_BASE_URL=http://localhost:11434/v1` + 对应模型名。

**关联不够准？** 先用零成本的 `kb lint`；将来需要更准的语义关联，可以再引入 embedding（升级路径开放）。
