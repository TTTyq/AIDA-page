# AIDA 爬虫工具

这是一个轻量级的爬虫工具，用于AIDA项目数据采集。

## 功能特点

- 简单易用的Web界面
- 支持HTML和JavaScript渲染页面的爬取
- 支持分页爬取
- 数据预览和导出
- 任务管理和监控

## 技术栈

### 后端
- FastAPI
- SQLite
- Beautiful Soup 4
- Playwright

### 前端
- Vue.js 3
- Element Plus
- Vuex
- Vue Router

## 快速开始

### 安装依赖

#### 后端

```bash
cd backend
pip install -r requirements.txt
```

#### 前端

```bash
cd frontend
npm install
```

### 启动服务

#### 后端

```bash
cd backend
python main.py
```

后端服务将在 http://localhost:8000 上运行。

#### 前端

```bash
cd frontend
npm run dev
```

前端服务将在 http://localhost:3000 上运行。

## 使用说明

1. 访问 http://localhost:3000
2. 创建新的爬虫任务
3. 配置爬虫参数
4. 运行爬虫任务
5. 查看和导出数据

## API文档

启动后端服务后，可以访问 http://localhost:8000/docs 查看API文档。

## 目录结构

```
scraper/
├── backend/           # 后端API服务
│   ├── app/
│   │   ├── api/       # API路由和端点
│   │   ├── core/      # 核心配置
│   │   ├── db/        # 数据库连接
│   │   ├── models/    # 数据模型
│   │   ├── scrapers/  # 爬虫实现
│   │   └── utils/     # 工具函数
│   ├── main.py        # 应用入口
│   └── requirements.txt # 依赖列表
└── frontend/          # 前端Web界面
    ├── public/        # 静态资源
    ├── src/
    │   ├── assets/    # 资源文件
    │   ├── components/ # Vue组件
    │   ├── views/     # 页面视图
    │   ├── router/    # 路由配置
    │   ├── store/     # 状态管理
    │   ├── App.vue    # 根组件
    │   └── main.js    # 入口文件
    ├── index.html     # HTML模板
    ├── package.json   # 依赖配置
    └── vite.config.js # Vite配置
``` 