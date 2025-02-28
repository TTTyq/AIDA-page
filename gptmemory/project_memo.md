# AIDA项目备忘录 - LLM指南

## 备忘录使用说明
本文档为LLM/GPT模型提供AIDA项目的关键信息。格式设计原则：1)信息高度压缩，减少换行；2)使用简洁关键词；3)优先使用二级标题(##)确保在VitePress TOC中可见；4)三四级标题仅在必要时使用；5)代码块使用```标记；6)重要信息使用**加粗**；7)列表项使用短横线并保持在同一行；8)更新时保持格式一致性，添加日期标记。

## 项目概述
AIDA(AI Artist Database)是艺术家社区平台，结合论坛、社交媒体和AI交互。核心功能：1)艺术家数据库-存储从古至今的艺术家信息；2)AI艺术家-基于LLM的虚拟艺术家，可进行智能对话；3)社区互动-用户与AI艺术家及其他用户的交流平台。

## 技术架构
### Monorepo结构
```
aida/
├── docs/           # 双语开发文档(VitePress)
├── backend/        # Python FastAPI后端
├── frontend/       # Next.js React前端
├── scraper/        # 艺术家数据采集工具
└── gptmemory/      # AI助手共享记忆
```

### 数据流
爬虫从艺术网站采集数据→数据存储MongoDB→后端提供RESTful API→前端通过API获取数据→LLM通过艺术家数据训练生成AI艺术家。

### 核心技术栈
后端:FastAPI+SQLAlchemy+MongoDB+LangChain；前端:Next.js+TypeScript+Tailwind CSS；文档:VitePress(双语)；爬虫:BeautifulSoup+Selenium；AI:OpenAI API/自定义LLM。

## 代码规范
### Python规范
遵循PEP 8；使用类型注解(Python 3.9+)；使用docstring；模块导入顺序:标准库>第三方库>本地模块；变量函数snake_case；类名PascalCase。

### TypeScript规范
使用ESLint和Prettier；使用TypeScript类型定义；函数变量camelCase；组件PascalCase；使用函数组件和React Hooks；避免直接操作DOM。

### CSS框架规范
**优先使用Tailwind CSS**；只有必要时才使用Less；使用MUI组件库时优先通过Tailwind类调整样式；全局样式在globals.css；特定组件复杂样式在styles目录。

### 文档规范
使用Markdown；中英文档同步；代码示例可直接运行；API文档包含参数说明和返回值。

## VitePress文档结构
### 侧边栏导航限制
VitePress侧边栏默认只显示二级标题(##)，不显示三级标题(###)。解决方案：1)将重要三级标题提升为二级标题；2)调整文档结构，使二级目录更详细全面；3)保持扁平化结构有利于导航。

### 文档目录规划
每个主要功能模块应有独立二级标题；相关子功能归类在同一二级标题下；避免过多一级标题；保持文档结构清晰。

## Git工作流
### 分支命名
功能分支:feature/short-description；修复分支:fix/short-description；文档分支:docs/short-description。

### 提交信息格式
```
<type>(<scope>): <subject>
<body>
<footer>
```
类型:feat(新功能)、fix(错误修复)、docs(文档)、style(格式)、refactor(重构)、perf(优化)、test(测试)、chore(构建)；范围:指定变更影响组件；主题:简洁描述，不超过50字符。

### 代码审查
所有代码必须经过至少一名团队成员审查；确保自动化测试通过；遵循项目规范和架构设计。

## 部署流程
开发环境:本地开发测试；测试环境:合并develop分支后自动部署；生产环境:main分支手动部署。

## 安全规范
不硬编码敏感信息；使用环境变量存储密钥；API端点进行权限验证；定期更新依赖包修复漏洞。

## 关键功能
### 艺术家数据库
艺术家基本信息(姓名、生卒年、国籍等)；艺术流派和风格分类；代表作品集；历史背景和影响。

### AI艺术家互动
基于艺术家真实资料的AI人格；多轮对话能力；艺术知识问答；艺术家间虚拟互动。

### 社区功能
用户个人主页；艺术讨论论坛；艺术作品分享；社交网络连接。

## 开发阶段
当前阶段:基础架构搭建(Monorepo结构、基本组件框架、数据模型设计)；下一阶段:核心功能开发(艺术家数据库API、前端基础界面、爬虫数据采集)；未来计划:AI艺术家模型训练与集成、社区功能实现、多语言支持扩展。

## Cursor AI使用技巧
### 基础功能
打开AI聊天:Cmd+L(macOS)/Ctrl+L(Windows)；切换Agent模式:聊天界面右上角下拉菜单；快速编辑代码:选中代码后Ctrl+K；终端命令生成:终端中Ctrl+K。

### 高级引用技巧
文件引用:@文件名；代码引用:@引用特定代码片段；文件夹引用:@文件夹名；网络搜索:@Web触发联网搜索(例:@Web如何在Next.js中实现SSR?)。

### 文件长度限制
Cursor AI编辑功能对文件长度有限制(250-400行)；超过限制的文件应拆分为多个模块；使用@引用其他文件可在跨文件编辑时保持上下文。

### 团队协作提示
使用.cursorrules文件在项目根目录设置全局AI规则；这些规则会自动应用于所有团队成员的Cursor AI提示；适合定义代码风格、项目特定约定等。

### 模型选择
复杂任务优先使用claude-3.5-sonnet模型；需要深度思考的任务可尝试o1-mini模型；注意不同模型的费用差异，合理选择。

## 常见问题
MongoDB连接问题:确保服务已启动，检查连接字符串；Git合并冲突:经常拉取最新代码，避免长时间不同步；依赖版本不一致:使用package.json锁定版本，定期更新；跨平台兼容性:注意Windows/macOS路径分隔符差异 