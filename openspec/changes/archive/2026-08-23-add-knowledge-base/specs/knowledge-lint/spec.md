## Purpose

为个人学习知识库提供按需整理能力，通过 lint 命令发现可关联但未链接的笔记与孤立笔记，增量处理并记录档案。

## ADDED Requirements

### Requirement: 发现可关联的笔记
系统 SHALL 在 lint 时找出语义或关键词上相关、但尚未建立链接的笔记，并输出关联建议。

#### Scenario: 发现相关笔记对
- **WHEN** 用户运行 lint 命令
- **THEN** 系统输出可能存在关联的笔记对列表

#### Scenario: 发现孤立笔记
- **WHEN** 用户运行 lint 命令
- **THEN** 系统输出没有任何关联的孤立笔记

### Requirement: 增量处理与档案记录
系统 SHALL 记录已 lint 的文档及其内容指纹，仅对新增或变更的笔记重新 lint，并保存每次 lint 的结果档案。

#### Scenario: 仅处理变更笔记
- **WHEN** 用户再次运行 lint 且仅新增或修改了少量笔记
- **THEN** 系统只处理这些变更的笔记，其余笔记不重复处理

#### Scenario: 档案可追溯
- **WHEN** 用户查看 lint 结果
- **THEN** 系统能说明每次 lint 处理了哪些文档
