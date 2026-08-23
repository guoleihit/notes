# RAG 入门

## 是什么

RAG（Retrieval-Augmented Generation，检索增强生成）是一种让大模型在回答前先检索外部知识的技术。

## 流程

1. 检索：从知识库中查找相关文档
2. 增强：把检索到的文档作为上下文
3. 生成：大模型基于上下文生成回答

## 检索方式

常用 vector search（向量检索）来找相关文档：

- 用 embedding 把文档转成向量
- 用余弦相似度（cosine similarity）比较向量
- 向量索引（如 HNSW）加速搜索

## 关联

- 向量检索
- Embedding
