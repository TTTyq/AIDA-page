# GPT Memory

这个目录用于存储 AI 助手（如 Cursor、Windsurf 等 LLM IDE）在多人协作环境中共享的记忆和上下文信息。通过维护这些共享记忆文件，可以确保不同开发者使用的 AI 助手能够保持一致的理解和行为。

## 目录结构

- `project_standards.md` - 项目规范和标准，包括代码风格、Git 提交规范、文档要求等
- `project_context.md` - 项目的核心概念和架构的简明概述，高信息密度，便于 AI 快速理解项目
- `working_memory_[username].md` - 每个开发者的当前工作记忆，记录正在进行的任务和进度

## 使用指南

1. **初次使用 AI 助手时**：请先让 AI 阅读 `project_standards.md` 和 `project_context.md`，以获取项目的基本理解。

   ```
   请阅读 gptmemory/project_standards.md 和 gptmemory/project_context.md 以了解项目规范和上下文
   ```

2. **开始新任务时**：更新您的个人工作记忆文件，描述您正在进行的任务。

   ```
   我正在开始一个新任务，请查看 gptmemory/working_memory_[您的用户名].md
   ```

3. **完成任务后**：更新您的工作记忆文件，记录完成的内容和下一步计划。

4. **项目变更时**：及时更新 `project_context.md`，确保它反映最新的项目状态。

## 最佳实践

- 保持文件简洁，信息密度高，避免冗余内容
- 定期更新工作记忆文件，确保其反映当前状态
- 在提交代码前，确保您的更改符合 `project_standards.md` 中的规范
- 如发现 AI 助手行为不一致，请检查共享记忆文件是否需要更新 