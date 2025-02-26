# AIAD 项目上下文

## 核心概念

AIAD (AI Artist Database) 是一个结合论坛、社交媒体和 AI 交互的艺术家社区平台。核心功能包括：

1. **艺术家数据库**: 存储从古至今的艺术家信息
2. **AI 艺术家**: 基于 LLM 的虚拟艺术家，可进行智能对话
3. **社区互动**: 用户与 AI 艺术家及其他用户的交流平台

## 技术架构

### Monorepo 结构
```
aiad/
├── docs/           # 双语开发文档 (VitePress)
├── backend/        # Python FastAPI 后端
├── frontend/       # Next.js React 前端
├── scraper/        # 艺术家数据采集工具
└── gptmemory/      # AI 助手共享记忆
```

### 数据流
1. 爬虫从各艺术网站采集艺术家数据
2. 数据存储在 MongoDB 中
3. 后端提供 RESTful API 访问数据
4. 前端通过 API 获取数据并展示
5. LLM 通过艺术家数据训练生成 AI 艺术家

### 核心技术栈
- **后端**: FastAPI + SQLAlchemy + MongoDB + LangChain
- **前端**: Next.js + TypeScript + Tailwind CSS
- **文档**: VitePress (双语支持)
- **爬虫**: BeautifulSoup + Selenium
- **AI**: OpenAI API / 自定义 LLM

## 关键功能

### 艺术家数据库
- 艺术家基本信息 (姓名、生卒年、国籍等)
- 艺术流派和风格分类
- 代表作品集
- 历史背景和影响

### AI 艺术家互动
- 基于艺术家真实资料的 AI 人格
- 多轮对话能力
- 艺术知识问答
- 艺术家间的虚拟互动

### 社区功能
- 用户个人主页
- 艺术讨论论坛
- 艺术作品分享
- 社交网络连接

## 开发阶段

1. **当前阶段**: 基础架构搭建
   - Monorepo 结构设置
   - 基本组件框架搭建
   - 数据模型设计

2. **下一阶段**: 核心功能开发
   - 艺术家数据库 API 实现
   - 前端基础界面开发
   - 爬虫数据采集实现

3. **未来计划**:
   - AI 艺术家模型训练与集成
   - 社区功能实现
   - 多语言支持扩展 