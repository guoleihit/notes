## 1. 笔记地基（note-storage）

- [x] 1.1 初始化笔记库结构：创建 `notes/` 目录与 `.gitignore`，提交初始 git 提交；验证 `git log` 含初始提交且 `.gitignore` 生效
- [x] 1.2 确定目录分类与命名约定，创建一篇示例学习笔记；验证该笔记是纯文本、任意文本编辑器可读
- [x] 1.3 用 Obsidian 打开 `notes/` 目录；验证笔记可编辑、保存后仍为纯文本 Markdown、迁移到其他目录内容不丢失

## 2. 关键词检索与问答（keyword-search + llm-answer）

- [x] 2.1 调整 Python 项目依赖：移除 numpy 与向量相关代码，保留 `openai`；验证 `python -c "import openai"` 成功
- [x] 2.2 实现 LLM 抽象层：OpenAI 兼容的 chat 接口，指向 OpenCode Go 的 GLM（`glm-5.2`）；验证能调用并返回回答
- [x] 2.3 实现关键词检索：在 `notes/` 下 grep 匹配，返回命中文档与片段；验证命中与片段正确
- [x] 2.4 实现 `kb grep` 命令；验证多关键词按命中数排序、无命中时明确提示
- [x] 2.5 实现 `kb ask` 命令：检索命中 → 喂 GLM → 返回答案；验证端到端问答，无候选文档时提示而非编造

## 3. 知识库整理（knowledge-lint）

- [x] 3.1 实现变更检测：内容 hash 对比 lint 档案，识别新增/变更的笔记；验证变更列表正确
- [x] 3.2 实现关联发现：关键词共现找出相关但未链接的笔记对，并识别孤立笔记；验证结果合理
- [x] 3.3 实现 lint 档案：记录已 lint 文档的 hash 与结果，仅对变更文档重新 lint；验证重复运行不重复处理
- [x] 3.4 实现 `kb lint` 命令输出整理报告；验证仅处理变更笔记、档案可追溯

## 4. 草稿与发布（draft-publish）

- [x] 4.1 创建 `drafts/` 草稿区，确保 grep/ask/lint 不扫描草稿；验证草稿不被检索命中
- [x] 4.2 实现 `kb publish` 命令：草稿移到 `notes/`（支持子目录、自动补 `.md`、冲突保护）；验证发布、子目录、冲突三种情况
