# AIDA 开发者文档

欢迎访问 AIDA（AI 艺术家数据库）开发者文档。本指南提供了关于 AIDA 平台的架构、组件和开发工作流程的全面信息。

## 概述

AIDA 是一个综合平台，结合论坛、社交媒体和 AI 交互，创建艺术家社区。该平台包含一个艺术家数据库，存储从古至今的艺术家信息，并通过大语言模型（LLM）驱动虚拟艺术家进行智能对话。

## 快速开始

- [宝宝也能看懂的开发指南](/zh/guide/beginners) 👶 **新手必读！**
- [架构概述](/zh/guide/architecture)
- [后端开发](/zh/guide/backend)
- [前端开发](/zh/guide/frontend)
- [爬虫开发](/zh/guide/scraper)

## 组件

AIDA 平台由四个主要组件组成：

1. **后端**：FastAPI Python 应用，使用 MongoDB
2. **前端**：Next.js React 应用，使用 Mantine、Jotai 和 Less
3. **文档**：双语开发者文档（本站）
4. **爬虫**：用于收集艺术家信息的数据采集工具 