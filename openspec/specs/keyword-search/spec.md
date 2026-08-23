# keyword-search Specification

## Purpose
为个人学习知识库提供基于关键词匹配的检索能力，使用户无需精确记起笔记内容，即可快速定位包含指定关键词的笔记与命中片段。

## Requirements

### Requirement: 关键词检索
系统 SHALL 根据用户给定的关键词，在 `notes/` 下的所有 Markdown 笔记中查找匹配的笔记。

#### Scenario: 关键词命中笔记
- **WHEN** 用户输入一个关键词
- **THEN** 系统返回所有包含该关键词的笔记，并标明命中的片段或行

#### Scenario: 多关键词检索
- **WHEN** 用户输入多个关键词
- **THEN** 系统返回与这些关键词相关的笔记，命中更多关键词的笔记排在前面

#### Scenario: 无命中
- **WHEN** 用户输入的关键词在所有笔记中都不存在
- **THEN** 系统明确提示没有找到匹配结果
