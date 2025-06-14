# AIDA项目 - 爬虫工具开发记录

## 任务概述
- 在scraper目录下部署一个SAAS爬虫工具
- 要求是一个相对轻便的程序
- 需要提供前后端方案
- 内部使用工具，无需用户登录系统，简单易用为主

## 当前进度
- [x] 初始化工作记忆文件
- [x] 设计爬虫工具架构
- [x] 确定技术栈和依赖
- [x] 实现后端API基础结构
- [x] 实现前端界面基础结构
- [x] 创建前端视图组件
- [x] 创建数据库模型
- [x] 实现服务层
- [x] 更新API端点使用数据库
- [x] 创建启动程序
- [x] 创建纯英文批处理文件
- [x] 添加网站管理功能
- [x] 改进批处理文件，避免打开多个窗口
- [ ] 完善爬虫引擎实现
- [ ] 完善前端交互
- [ ] 集成到AIDA项目中

## 工作记录
- 2023-07-01: 初始化工作记忆文件，开始规划爬虫工具架构
- 2023-07-01: 完成爬虫工具架构设计，确定技术栈和目录结构
- 2023-07-01: 根据反馈简化设计，移除用户系统，专注于爬虫功能
- 2023-07-01: 进一步简化技术栈，采用更轻量级的方案
- 2023-07-01: 创建项目基本目录结构
- 2023-07-01: 实现后端API基础结构，包括路由、爬虫引擎基类和实现
- 2023-07-01: 实现前端基础结构，包括Vue组件、路由和状态管理
- 2023-07-01: 创建项目README文件
- 2023-07-02: 创建前端视图组件，包括任务列表、任务详情和数据预览
- 2023-07-02: 创建数据库模型，包括任务模型和数据模型
- 2023-07-02: 实现服务层，包括任务服务、数据服务和爬虫服务
- 2023-07-02: 更新API端点，使用数据库模型
- 2023-07-03: 开始创建启动程序，用于同时启动前端和后端服务
- 2023-07-03: 创建了三种启动脚本：Windows批处理文件(.bat)、Linux/macOS Shell脚本(.sh)和跨平台Python脚本(.py)
- 2023-07-03: 创建了相应的停止脚本，用于停止爬虫工具的服务
- 2023-07-03: 更新了README.md，添加了有关启动脚本的说明
- 2023-07-03: 根据用户需求，创建了综合启动脚本run_scraper.bat，将启动、停止和安装功能整合到一个批处理文件中
- 2023-07-03: 按照用户要求，将综合启动脚本中所有中文内容替换为英文，并删除了其他多余的启动/停止脚本，仅保留一个英文版的run_scraper.bat
- 2023-07-04: 添加了网站管理功能，包括添加、编辑、删除和测试网站配置
- 2023-07-04: 改进了批处理文件，避免打开多个命令窗口，改为单窗口模式并显示运行状态
- 2023-07-04: 创建了基于JSON文件的配置存储系统，无需使用数据库就能保存和管理网站配置

## 架构设计（轻量级版）

### 技术栈
- 后端：FastAPI + SQLite
- 前端：Vue.js + Element Plus + Vite
- 爬虫引擎：Requests + BeautifulSoup4 + Playwright（按需使用）
- 配置存储：JSON文件（无需数据库）

### 功能模块
1. **爬虫任务管理**：创建任务、配置规则、任务调度、监控
2. **数据处理**：数据清洗、转换、导出(CSV/JSON/Excel)、预览
3. **API接口**：RESTful API、批量数据获取
4. **网站管理**：添加、编辑、删除和测试爬虫目标网站

### 目录结构
```
scraper/
├── backend/           # 后端API服务
│   ├── data/          # 存储网站配置的JSON文件
├── frontend/          # 前端Web界面
├── run_scraper.bat    # 综合管理脚本（启动/停止/安装）
└── README.md          # 文档
```

### 后端目录结构（轻量级版）
```
backend/
├── app/
│   ├── api/           # API路由和端点
│   │   ├── endpoints/
│   │       ├── websites.py  # 网站管理API
│   ├── core/          # 核心配置
│   ├── db/            # 数据库连接
│   ├── models/        # 数据模型
│   │   ├── website.py # 网站配置模型
│   ├── scrapers/      # 爬虫实现
│   │   ├── base.py    # 基础爬虫类
│   │   ├── html.py    # HTML爬虫
│   │   └── browser.py # 浏览器爬虫
│   ├── services/      # 服务层
│   │   ├── website_service.py # 网站配置服务
│   └── utils/         # 工具函数
├── data/              # 配置存储目录
│   ├── websites.json  # 网站配置数据
├── main.py            # 应用入口
└── requirements.txt   # 依赖列表
```

### 前端目录结构（轻量级版）
```
frontend/
├── public/            # 静态资源
├── src/
│   ├── assets/        # 资源文件
│   ├── components/    # Vue组件
│   │   ├── layout/    # 布局组件
│   │   ├── tasks/     # 任务相关组件
│   │   └── results/   # 结果展示组件
│   ├── views/         # 页面视图
│   │   ├── WebsiteList.vue # 网站管理页面
│   ├── router/        # 路由配置
│   ├── store/         # 状态管理
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
├── index.html         # HTML模板
├── package.json       # 依赖配置
└── vite.config.js     # Vite配置
```

## 下一步计划
1. ~~创建启动程序，用于同时启动前端和后端服务~~
2. ~~创建纯英文批处理文件，符合项目规范~~
3. ~~添加网站管理功能，方便添加和删除爬虫目标网站~~
4. ~~改进批处理文件，避免打开多个命令窗口~~
5. 完善爬虫引擎实现，添加对网站配置的支持
6. 完善前端交互和数据可视化
7. 添加更多数据导出格式支持（如CSV、Excel）
8. 编写详细的使用文档
9. 集成到AIDA项目中 