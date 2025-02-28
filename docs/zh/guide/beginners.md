# 宝宝也能看懂的开始开发指南

::: tip 提示
本指南专为完全没有全栈开发经验的新手设计，从零开始指导你如何安装必要工具、配置环境，并运行 AIDA 项目。
:::

## 第一步：安装基础工具

在开始开发之前，我们需要安装一些基础工具。不要担心，我们会一步一步地引导你完成这个过程！

### 安装 Git

Git 是一个版本控制系统，它可以帮助我们管理代码的变更。

::: details Windows 用户
1. 访问 [Git 官网](https://git-scm.com/download/win)
2. 下载 Windows 版本的 Git 安装程序
3. 运行安装程序，使用默认设置一路点击"下一步"即可
4. 安装完成后，打开"命令提示符"或"PowerShell"，输入 `git --version` 确认安装成功
:::

::: details macOS 用户
1. 如果你已经安装了 Xcode，Git 已经包含在内
2. 如果没有 Xcode，可以通过终端安装 Git：
   - 打开"终端"应用
   - 输入 `xcode-select --install` 并按回车
   - 按照提示完成安装
3. 或者，你可以使用 Homebrew 安装 Git：
   - 安装 Homebrew（如果尚未安装）：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - 安装 Git：`brew install git`
4. 安装完成后，在终端中输入 `git --version` 确认安装成功
:::

### 安装 Cursor 编辑器

Cursor 是一个基于 AI 的代码编辑器，它可以帮助你更高效地编写代码。

1. 访问 [Cursor 官网](https://cursor.sh/)
2. 下载适合你操作系统的版本
3. 安装并启动 Cursor
4. 注册或登录 Cursor 账号

### 安装 Node.js 和 npm

Node.js 是一个 JavaScript 运行环境，npm 是 Node.js 的包管理器，我们需要它们来运行前端代码。

::: details Windows 用户
1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载并安装 LTS（长期支持）版本
3. 安装时使用默认设置
4. 安装完成后，打开命令提示符或 PowerShell，输入 `node --version` 和 `npm --version` 确认安装成功
:::

::: details macOS 用户
1. 使用 Homebrew 安装 Node.js：
   ```bash
   brew install node
   ```
2. 安装完成后，在终端中输入 `node --version` 和 `npm --version` 确认安装成功
:::

### 安装 Python

Python 是一种编程语言，我们的后端使用 Python 开发。

::: details Windows 用户
1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载最新的 Python 安装程序（选择 3.9 或更高版本）
3. 运行安装程序，**务必勾选"Add Python to PATH"**
4. 点击"Install Now"开始安装
5. 安装完成后，打开命令提示符或 PowerShell，输入 `python --version` 确认安装成功
:::

::: details macOS 用户
1. macOS 通常已预装 Python，但可能不是最新版本
2. 使用 Homebrew 安装最新版本的 Python：
   ```bash
   brew install python
   ```
3. 安装完成后，在终端中输入 `python3 --version` 确认安装成功
:::

### 安装 MongoDB

MongoDB 是一个文档数据库，我们用它来存储项目数据。

::: details Windows 用户
1. 访问 [MongoDB 官网](https://www.mongodb.com/try/download/community)
2. 下载 MongoDB Community Server
3. 运行安装程序，选择"Complete"安装类型
4. 勾选"Install MongoDB as a Service"
5. 完成安装后，MongoDB 服务应该已经自动启动
6. 你也可以安装 [MongoDB Compass](https://www.mongodb.com/try/download/compass)，这是一个图形化的 MongoDB 管理工具
:::

::: details macOS 用户
1. 使用 Homebrew 安装 MongoDB：
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   ```
2. 启动 MongoDB 服务：
   ```bash
   brew services start mongodb-community
   ```
3. 你也可以安装 MongoDB Compass：
   ```bash
   brew install --cask mongodb-compass
   ```
:::

## 第二步：获取项目代码

现在我们已经安装了所有必要的工具，接下来获取项目代码。

### 克隆 GitHub 仓库

1. 打开命令提示符（Windows）或终端（macOS）
2. 导航到你想要存放项目的目录，例如：
   ```bash
   cd Documents
   ```
3. 克隆项目仓库：
   ```bash
   git clone https://github.com/thevertexlab/aida.git
   ```
4. 进入项目目录：
   ```bash
   cd aida
   ```

### 使用 Cursor 打开项目

1. 打开 Cursor 编辑器
2. 点击"File" > "Open Folder"
3. 导航到你刚才克隆的 aida 项目目录并打开

## 第三步：配置项目环境

现在我们需要配置项目环境，安装依赖并设置必要的配置文件。

### 创建环境变量文件

1. 在项目根目录中，找到 `.env.example` 文件
2. 复制这个文件并重命名为 `.env`
3. 打开 `.env` 文件，根据需要修改配置（对于初次使用，默认配置通常就足够了）

### 安装项目依赖

在 Cursor 中打开终端（Terminal > New Terminal），然后运行以下命令：

```bash
npm run setup:all
```

这个命令会安装前端、后端和文档系统所需的所有依赖。这可能需要几分钟时间，请耐心等待。

### 导入测试数据

安装完依赖后，我们需要导入一些测试数据到 MongoDB：

```bash
npm run setup:mongodb
```

这个命令会检查你的环境配置，确保 MongoDB 正在运行，然后导入测试数据。

## 第四步：启动项目

现在我们已经完成了所有配置，可以启动项目了！

### 一键启动所有服务

在终端中运行：

```bash
npm run dev
```

这个命令会同时启动前端、后端和文档服务。你会看到一个漂亮的输出，显示所有服务的访问地址。

### 访问各个服务

启动成功后，你可以通过以下地址访问各个服务：

- **前端应用**：http://localhost:3000
- **后端服务**：http://localhost:8000
- **项目文档**：http://localhost:5173
- **API 文档**：http://localhost:8000/api/docs

## 第五步：理解项目结构

现在你已经成功运行了项目，让我们来了解一下项目的基本结构。

### 项目目录结构

- `frontend/`：前端代码，使用 Next.js 框架
- `backend/`：后端代码，使用 FastAPI 框架
- `docs/`：项目文档，使用 VitePress
- `scraper/`：数据爬虫，用于收集艺术家信息
- `data/`：存放数据文件
- `scripts/`：各种实用脚本
- `gptmemory/`：AI 助手的共享记忆

### 理解后端 API

后端 API 可以理解为一组函数，它们通过 HTTP 请求被调用。例如：

- 当你访问 `http://localhost:8000/api/artists` 时，后端会返回所有艺术家的列表
- 当你访问 `http://localhost:8000/api/artists/123` 时，后端会返回 ID 为 123 的艺术家信息

你可以通过访问 API 文档 `http://localhost:8000/api/docs` 来查看所有可用的 API 端点及其详细说明。

## 第六步：使用 GPT Memory

AIDA 项目使用 GPT Memory 系统来帮助 AI 助手（如 Cursor 中的 AI）理解项目上下文和规范。

### 了解 GPT Memory 文件

项目中的 `gptmemory/` 目录包含以下重要文件：

- `project_standards.md`：项目规范和标准
- `project_context.md`：项目的核心概念和架构概述
- `working_memory_[username].md`：每个开发者的工作记忆

### 首次使用 AI 助手

当你在 Cursor 中首次使用 AI 助手时，可以让它阅读这些文件：

```
请阅读 gptmemory/project_standards.md 和 gptmemory/project_context.md 以了解项目规范和上下文
```

### 创建个人工作记忆

你可以创建自己的工作记忆文件：

1. 在 `gptmemory/` 目录中创建一个名为 `working_memory_你的用户名.md` 的文件
2. 在文件中记录你正在进行的任务和进度
3. 当你使用 AI 助手时，可以让它查看你的工作记忆：
   ```
   我正在开始一个新任务，请查看 gptmemory/working_memory_你的用户名.md
   ```

## 常见问题解答

### MongoDB 无法连接怎么办？

1. 确保 MongoDB 服务正在运行
2. 检查 `.env` 文件中的连接字符串是否正确
3. 尝试使用 MongoDB Compass 连接数据库，确认连接信息正确

### 如何停止所有服务？

在运行服务的终端窗口中按 `Ctrl+C`。

### 如何更新项目代码？

在终端中运行：
```bash
git pull
```

然后重新安装依赖：
```bash
npm run setup:all
```

### 如何查看项目的最新变更？

在终端中运行：
```bash
git log --oneline -n 10
```

这将显示最近的 10 次提交记录。

## 下一步学习

恭喜你完成了 AIDA 项目的初始设置和运行！接下来，你可以：

1. 探索项目文档，了解更多技术细节
2. 查看前端和后端代码，理解它们是如何工作的
3. 尝试修改一些代码，看看会发生什么变化
4. 学习更多关于 Next.js、FastAPI 和 MongoDB 的知识

记住，学习编程是一个循序渐进的过程。不要害怕犯错，每个错误都是学习的机会！

如果你有任何问题，可以查阅项目文档或向团队成员寻求帮助。祝你编程愉快！ 