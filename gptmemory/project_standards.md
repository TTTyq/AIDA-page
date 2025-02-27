# AIDA 项目规范

本文档定义了 AI Artist Database (AIDA) 项目的开发规范和标准。所有团队成员必须遵循这些规范以确保代码质量和一致性。

## 代码规范

### Python (后端 & 爬虫)

- 遵循 PEP 8 风格指南
- 使用类型注解 (Python 3.9+)
- 使用 docstring 记录函数和类的用途
- 模块导入顺序: 标准库 > 第三方库 > 本地模块
- 变量和函数使用 snake_case
- 类名使用 PascalCase

### TypeScript/JavaScript (前端)

- 使用 ESLint 和 Prettier 进行代码格式化
- 使用 TypeScript 类型定义
- 函数和变量使用 camelCase
- 组件使用 PascalCase
- 使用函数组件和 React Hooks
- 避免直接操作 DOM

### 文档

- 使用 Markdown 格式编写文档
- 中英文档同步更新
- 代码示例应当可以直接运行
- API 文档需包含参数说明和返回值

## Git 工作流

### 分支命名

- 功能分支: `feature/short-description`
- 修复分支: `fix/short-description`
- 文档分支: `docs/short-description`

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **类型**:
  - feat: 新功能
  - fix: 错误修复
  - docs: 文档变更
  - style: 代码格式变更
  - refactor: 代码重构
  - perf: 性能优化
  - test: 测试相关
  - chore: 构建过程或辅助工具变更

- **范围**: 指定变更影响的组件 (backend, frontend, docs, scraper)

- **主题**: 简洁描述变更内容，不超过50个字符

### 代码审查

- 所有代码必须经过至少一名团队成员的审查
- 确保所有自动化测试通过
- 遵循项目规范和架构设计

## 部署流程

- 开发环境: 本地开发和测试
- 测试环境: 合并到 develop 分支后自动部署
- 生产环境: 从 main 分支手动部署

## 安全规范

- 不在代码中硬编码敏感信息
- 使用环境变量存储密钥和凭证
- API 端点需进行适当的权限验证
- 定期更新依赖包以修复安全漏洞 