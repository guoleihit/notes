# draft-publish Specification

## Purpose
为个人学习知识库提供草稿与发布机制，用独立的草稿区暂存未完成的灵感，发布后将草稿转为正式笔记进入检索。

## Requirements

### Requirement: 草稿区隔离
系统 SHALL 将草稿存放在独立的 `drafts/` 目录，检索与整理仅作用于 `notes/` 下的正式笔记。

#### Scenario: 草稿不参与检索
- **WHEN** 用户在 `drafts/` 下存放草稿
- **THEN** 关键词检索与整理命令不会命中这些草稿

### Requirement: 发布草稿
系统 SHALL 支持将草稿从 `drafts/` 移动到 `notes/`，转为正式笔记。

#### Scenario: 发布到正式笔记
- **WHEN** 用户发布一篇草稿
- **THEN** 该草稿被移动到 `notes/` 目录，成为可检索的正式笔记

#### Scenario: 发布到子目录
- **WHEN** 用户指定目标子目录发布草稿
- **THEN** 草稿被移动到 `notes/` 下的该子目录，子目录不存在时自动创建

### Requirement: 发布冲突保护
系统 SHALL 在发布目标已存在同名笔记时拒绝覆盖并提示。

#### Scenario: 目标已存在
- **WHEN** 用户发布草稿到已存在同名笔记的位置
- **THEN** 系统拒绝覆盖并提示目标已存在
