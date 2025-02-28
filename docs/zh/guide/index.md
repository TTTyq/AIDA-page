# 快速开始

::: tip 提示
本指南将帮助你快速设置和运行 AIDA 项目。如果你是完全的新手，建议查看[宝宝也能看懂的开发指南](./beginners.md)获取更详细的说明。
:::

## 前提条件

确保你的系统已安装以下软件：

- Git
- Node.js (v16+) 和 npm
- Python (v3.9+)
- MongoDB

## 克隆项目

```bash
git clone https://github.com/thevertexlab/aida.git
cd aida
```

## 安装依赖

一键安装所有依赖：

```bash
npm run setup:all
```

## 配置环境

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 根据需要修改配置

## 导入测试数据

```bash
npm run setup:mongodb
```

## 启动项目

```bash
npm run dev
```

启动后，你可以访问：

- 前端应用：http://localhost:3000
- 后端服务：http://localhost:8000
- 项目文档：http://localhost:5173
- API 文档：http://localhost:8000/api/docs

## 下一步

- 查看[架构](./architecture.md)了解项目结构
- 了解[后端](./backend.md)、[前端](./frontend.md)和[爬虫](./scraper.md)组件
- 参考[宝宝也能看懂的开发指南](./beginners.md)获取更详细的入门指导 