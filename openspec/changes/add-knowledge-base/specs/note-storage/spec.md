## Purpose

为个人学习知识库提供笔记的持久化存储，以纯文本 Markdown 保存本地笔记，支持增量添加与内容修改，并通过版本控制防止数据丢失。

## ADDED Requirements

### Requirement: 以 Markdown 存储笔记
系统 SHALL 将每篇笔记作为独立的纯文本 Markdown 文件存储，不依赖任何专有格式或数据库。

#### Scenario: 添加新笔记
- **WHEN** 用户创建一篇新笔记
- **THEN** 系统将其保存为一个 Markdown 文件，内容可用任意文本编辑器直接读取

#### Scenario: 笔记可迁移
- **WHEN** 用户将笔记文件复制或移动到其他工具或目录
- **THEN** 笔记内容完整保留，无需任何导出或转换

### Requirement: 修改已有笔记
系统 SHALL 支持修改已有笔记的内容，并在保存后保留最新内容。

#### Scenario: 修改并保存
- **WHEN** 用户编辑一篇已有笔记并保存
- **THEN** 系统将该 Markdown 文件更新为最新内容

### Requirement: 版本化与防丢失
系统 SHALL 通过版本控制保存笔记的修改历史，允许回看和恢复历史版本。

#### Scenario: 恢复历史版本
- **WHEN** 用户需要找回某篇笔记的早期内容
- **THEN** 系统能提供该笔记的历史版本供恢复
