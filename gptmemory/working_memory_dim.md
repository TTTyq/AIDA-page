# Dim 的工作记忆

## 当前任务

- [x] 创建 AIDA 项目的 monorepo 基础结构
  - [x] 设置文档组件 (VitePress, 中英双语)
  - [x] 设置后端组件 (FastAPI)
  - [x] 设置前端组件 (Next.js)
  - [x] 设置爬虫组件 (BeautifulSoup + Selenium)
  - [x] 更新主 README 添加综合指南
  - [x] 创建 gptmemory 目录用于 AI 助手共享记忆

## 进行中任务

- [ ] 完善项目文档
  - [ ] 添加架构图
  - [ ] 完善 API 文档
- [ ] 实现基础数据模型
  - [ ] 艺术家模型设计
  - [ ] 数据库连接配置
- [x] 实现一键启动全部项目组件
  - [x] 设计最佳启动方案
  - [x] 实现前后端、文档服务同时启动
  - [x] 添加开发环境配置自动化
- [x] 修复 VitePress ESM 模块问题
  - [x] 在 docs/package.json 中添加 "type": "module" 配置
- [x] 更新 .gitignore 文件
  - [x] 添加 VitePress 缓存目录 (docs/.vitepress/cache/, docs/.vitepress/.temp/)
  - [x] 添加 Next.js 环境声明文件 (next-env.d.ts)
  - [x] 添加 package-lock.json
- [x] 项目重命名 (AIAD → AIDA)
  - [x] 更新所有文件中的项目名称引用
  - [x] 更新 GitHub 仓库链接
  - [x] 更新数据库名称引用
  - [x] 更新包名称

## 下一步计划

- 实现艺术家数据 API 端点
- 开发前端艺术家列表和详情页面
- 配置爬虫采集初始数据集

## 注意事项

- 确保所有组件遵循项目规范
- 保持代码提交信息符合规范
- 更新文档时保持中英文同步
- VitePress 使用 ESM 模块，确保配置文件使用 ES 模块语法
- 定期检查 .gitignore 文件，确保不会提交不必要的文件 