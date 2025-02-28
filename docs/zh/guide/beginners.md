# 宝宝也能看懂的开始开发指南

::: tip 提示
本指南专为完全没有全栈开发经验的新手设计，从零开始指导你如何安装必要工具、配置环境，并运行 AIDA 项目。
:::

## 目录

- [第一部分：环境准备](#第一部分-环境准备)
  - [安装基础工具](#安装基础工具)
  - [获取项目代码](#获取项目代码)
  - [配置项目环境](#配置项目环境)
- [第二部分：项目运行与理解](#第二部分-项目运行与理解)
  - [启动项目](#启动项目)
  - [理解项目结构](#理解项目结构)
- [第三部分：开发工作流](#第三部分-开发工作流)
  - [Git 工作流程](#git-工作流程)
  - [使用 GPT Memory](#使用-gpt-memory)
- [第四部分：AI 辅助开发](#第四部分-ai-辅助开发)
  - [AI 助手使用基础](#ai-助手使用基础)
  - [高级 AI 辅助开发实践](#高级-ai-辅助开发实践)
- [第五部分：常见问题与进阶](#第五部分-常见问题与进阶)
  - [常见问题解答](#常见问题解答)
  - [下一步学习](#下一步学习)

## 第一部分：环境准备

### 安装基础工具

在开始开发之前，我们需要安装一些基础工具。不要担心，我们会一步一步地引导你完成这个过程！

#### 安装 Git

Git 是一个版本控制系统，它可以帮助我们管理代码的变更。

::: details open Windows 用户
1. 访问 [Git 官网](https://git-scm.com/download/win)
2. 下载 Windows 版本的 Git 安装程序
3. 运行安装程序，使用默认设置一路点击"下一步"即可
4. 安装完成后，打开"命令提示符"或"PowerShell"，输入 `git --version` 确认安装成功
:::

::: details open macOS 用户
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

#### 安装 Cursor 编辑器

Cursor 是一个基于 AI 的代码编辑器，它可以帮助你更高效地编写代码。

1. 访问 [Cursor 官网](https://cursor.sh/)
2. 下载适合你操作系统的版本
3. 安装并启动 Cursor
4. 注册或登录 Cursor 账号

#### 安装 Node.js 和 npm

Node.js 是一个 JavaScript 运行环境，npm 是 Node.js 的包管理器，我们需要它们来运行前端代码。

::: details open Windows 用户
1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载并安装 LTS（长期支持）版本
3. 安装时使用默认设置
4. 安装完成后，打开命令提示符或 PowerShell，输入 `node --version` 和 `npm --version` 确认安装成功
:::

::: details open macOS 用户
1. 首先，我们需要安装 Homebrew（这是 macOS 上的一个包管理器，类似于手机上的应用商店，可以帮助你安装各种软件）：
   - 打开"终端"应用（可以在"应用程序 > 实用工具"中找到，或者使用 Spotlight 搜索"终端"）
   - 复制以下命令，粘贴到终端中，然后按回车键：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - 按照屏幕上的提示完成安装（可能需要输入你的电脑密码）
   - 安装完成后，终端会显示一些后续步骤，请按照这些步骤操作

2. 然后，使用 Homebrew 安装 Node.js：
   ```bash
   brew install node
   ```
3. 安装完成后，在终端中输入 `node --version` 和 `npm --version` 确认安装成功
:::

#### 安装 Python

Python 是一种编程语言，我们的后端使用 Python 开发。

::: details open Windows 用户
1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载最新的 Python 安装程序（选择 3.9 或更高版本）
3. 运行安装程序，**务必勾选"Add Python to PATH"**
4. 点击"Install Now"开始安装
5. 安装完成后，打开命令提示符或 PowerShell，输入 `python --version` 确认安装成功
:::

::: details open macOS 用户
1. macOS 通常已预装 Python，但可能不是最新版本
2. 使用 Homebrew 安装最新版本的 Python：
   ```bash
   brew install python
   ```
3. 安装完成后，在终端中输入 `python3 --version` 确认安装成功
:::

#### 安装 MongoDB

MongoDB 是一个文档数据库，我们用它来存储项目数据。

::: details open Windows 用户
1. 访问 [MongoDB 官网](https://www.mongodb.com/try/download/community)
2. 下载 MongoDB Community Server
3. 运行安装程序，选择"Complete"安装类型
4. 勾选"Install MongoDB as a Service"
5. 完成安装后，MongoDB 服务应该已经自动启动
6. 你也可以安装 [MongoDB Compass](https://www.mongodb.com/try/download/compass)，这是一个图形化的 MongoDB 管理工具
:::

::: details open macOS 用户
1. 使用我们之前安装的 Homebrew 来安装 MongoDB：
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

### 获取项目代码

现在我们已经安装了所有必要的工具，接下来获取项目代码。

#### 克隆 GitHub 仓库

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

#### 使用 Cursor 打开项目

1. 打开 Cursor 编辑器
2. 点击"File" > "Open Folder"
3. 导航到你刚才克隆的 aida 项目目录并打开

### 配置项目环境

现在我们需要配置项目环境，安装依赖并设置必要的配置文件。

#### 创建环境变量文件

1. 在项目根目录中，找到 `.env.example` 文件
2. 复制这个文件并重命名为 `.env`
3. 打开 `.env` 文件，根据需要修改配置（对于初次使用，默认配置通常就足够了）

#### 安装项目依赖

在 Cursor 中打开终端（Terminal > New Terminal），然后运行以下命令：

```bash
npm run setup:all
```

这个命令会安装前端、后端和文档系统所需的所有依赖。这可能需要几分钟时间，请耐心等待。

#### 导入测试数据

安装完依赖后，我们需要导入一些测试数据到 MongoDB：

```bash
npm run setup:mongodb
```

这个命令会检查你的环境配置，确保 MongoDB 正在运行，然后导入测试数据。

## 第二部分：项目运行与理解

### 启动项目

现在我们已经完成了所有配置，可以启动项目了！

#### 一键启动所有服务

在终端中运行：

```bash
npm run dev
```

这个命令会同时启动前端、后端和文档服务。你会看到一个漂亮的输出，显示所有服务的访问地址。

#### 访问各个服务

启动成功后，你可以通过以下地址访问各个服务：

- **前端应用**：http://localhost:3000
- **后端服务**：http://localhost:8000
- **项目文档**：http://localhost:5173
- **API 文档**：http://localhost:8000/api/docs

### 理解项目结构

现在你已经成功运行了项目，让我们来了解一下项目的基本结构。

#### 项目目录结构

- `frontend/`：前端代码，使用 Next.js 框架
- `backend/`：后端代码，使用 FastAPI 框架
- `docs/`：项目文档，使用 VitePress
- `scraper/`：数据爬虫，用于收集艺术家信息
- `data/`：存放数据文件
- `scripts/`：各种实用脚本
- `gptmemory/`：AI 助手的共享记忆

#### 理解后端 API

后端 API 可以理解为一组函数，它们通过 HTTP 请求被调用。例如：

- 当你访问 `http://localhost:8000/api/artists` 时，后端会返回所有艺术家的列表
- 当你访问 `http://localhost:8000/api/artists/123` 时，后端会返回 ID 为 123 的艺术家信息

你可以通过访问 API 文档 `http://localhost:8000/api/docs` 来查看所有可用的 API 端点及其详细说明。

## 第三部分：开发工作流

### Git 工作流程

在 AIDA 项目中，我们使用 Git 进行版本控制。以下是基本的 Git 工作流程：

#### 创建新分支

在开始新功能或修复 bug 前，应该创建一个新分支：

```bash
git checkout -b feature/your-feature-name
```

#### 提交更改

1. 查看你的更改：
   ```bash
   git status
   ```

2. 添加更改的文件到暂存区：
   ```bash
   git add .  # 添加所有更改
   # 或者
   git add path/to/specific/file  # 添加特定文件
   ```

3. **使用 Cursor 生成提交信息**：
   - 在 Cursor 中，点击左侧的源代码控制图标（Source Control）
   - 在提交信息框旁边，点击 "⭐⭐" 图标（Generate Commit Message）
   - Cursor 的 AI 会分析你的更改并生成一个合适的提交信息
   - 你可以根据需要编辑这个信息

4. 提交更改：
   - 在 Cursor 的源代码控制面板中，点击 "✓" 图标（Commit）
   - 或者在终端中使用：
     ```bash
     git commit -m "你的提交信息"
     ```

5. 推送到远程仓库：
   ```bash
   git push origin feature/your-feature-name
   ```

#### 创建拉取请求（Pull Request）

当你完成功能开发后，可以创建一个拉取请求：

1. 访问 GitHub 上的项目仓库
2. 点击 "Pull requests" 标签
3. 点击 "New pull request" 按钮
4. 选择你的分支和目标分支（通常是 main 或 master）
5. 填写拉取请求的标题和描述
6. 点击 "Create pull request" 按钮

### 使用 GPT Memory

AIDA 项目使用 GPT Memory 系统来帮助 AI 助手（如 Cursor 中的 AI）理解项目上下文和规范。

#### 了解 GPT Memory 文件

项目中的 `gptmemory/` 目录包含以下重要文件：

- `project_standards.md`：项目规范和标准
- `project_context.md`：项目的核心概念和架构概述
- `working_memory_[username].md`：每个开发者的工作记忆

#### 首次使用 AI 助手

当你在 Cursor 中首次使用 AI 助手时，应该让它阅读这些文件，这样它才能理解项目的规范和上下文。在 Cursor 中打开一个文件，然后在底部的聊天框中输入：

```
请阅读 gptmemory/project_standards.md 和 gptmemory/project_context.md 以了解项目规范和上下文
```

#### 创建个人工作记忆

你不需要手动创建工作记忆文件，可以让 AI 助手帮你创建：

1. 在 Cursor 的聊天框中输入：
   ```
   请参考 @working_memory_dim.md 帮我创建一个 working_memory_[你的名字].md
   ```

2. AI 助手会帮你创建一个新的工作记忆文件，并根据 Dim 的工作记忆格式进行设置

3. 当你开始新任务时，在每次对话的开始，都应该引用你的工作记忆文件：
   ```
   @working_memory_[你的名字].md 我正在开始一个新任务，[描述你的任务]
   ```

## 第四部分：AI 辅助开发

### AI 助手使用基础

在 AIDA 项目中，我们使用 AI 助手（如 Cursor 中的 AI）来提高开发效率。以下是一些有用的技巧：

#### 基本引用规则

每次与 AI 助手对话时，应该引用相关的文件，这样 AI 才能理解上下文：

```
@README.md @working_memory_[你的名字].md 我想了解如何实现[某个功能]
```

#### 常用对话模式

1. **请求解释代码**：
   ```
   @frontend/app/page.tsx 请解释这个文件中的代码是如何工作的
   ```

2. **请求实现功能**：
   ```
   @working_memory_[你的名字].md 我需要实现一个艺术家列表页面，要求能够分页显示并支持搜索
   ```

3. **请求修复错误**：
   ```
   @backend/main.py 我遇到了以下错误，请帮我修复：[错误信息]
   ```

4. **请求代码审查**：
   ```
   @frontend/components/ArtistCard.tsx 请审查这段代码，看是否有改进空间
   ```

5. **学习项目架构**：
   ```
   @project_context.md 请解释 AIDA 项目的整体架构和各组件之间的关系
   ```

#### 高级 Prompt 技巧

1. **提供足够上下文**：
   ```
   @working_memory_[你的名字].md @frontend/app/artists/page.tsx 我正在开发艺术家列表页面。
   目前已经完成了基本布局，现在需要实现分页功能。后端 API 支持通过 ?page=1&limit=10 参数进行分页。
   请帮我实现前端分页组件和相应的数据获取逻辑。
   ```

2. **分步骤引导 AI**：
   ```
   @backend/models/artist.py 我需要创建艺术家模型。请按以下步骤帮我：
   1. 首先，分析艺术家需要哪些字段
   2. 然后，创建 Pydantic 模型
   3. 最后，添加必要的验证和方法
   ```

3. **使用角色扮演提高质量**：
   ```
   @frontend/components/ArtistDetail.tsx 请以资深 React 开发者的角度，审查这个组件的性能和最佳实践
   ```

4. **请求多种方案**：
   ```
   @project_standards.md 我需要实现用户认证功能，请提供 3 种不同的实现方案，并分析各自的优缺点
   ```

记住，AI 助手是你的协作伙伴，而不是替代品。它可以帮助你理解代码、生成代码片段、解决问题，但最终的决策和代码质量控制仍然需要你来负责。

### 高级 AI 辅助开发实践

除了基本的对话模式，Cursor 的 AI 助手还可以帮助你完成更复杂的开发任务。以下是一些高级实践：

#### 实现新需求

当你需要实现一个新功能时，可以按照以下步骤使用 AI 助手：

1. **明确需求**：
   ```
   @working_memory_[你的名字].md 我需要实现一个新功能：艺术家作品展示页面。
   这个页面需要：
   1. 显示艺术家的基本信息
   2. 以网格形式展示艺术家的所有作品
   3. 点击作品可以查看大图和详细信息
   4. 支持按时间、风格筛选作品
   ```

2. **获取实现建议**：
   ```
   请帮我规划实现这个功能的步骤，包括需要创建哪些组件、如何组织数据流、需要哪些 API 等
   ```

3. **逐步实现**：
   ```
   现在我们开始实现第一步：创建艺术家作品列表组件。请帮我设计这个组件的结构和样式
   ```

4. **代码审查**：
   ```
   @frontend/components/ArtistWorks.tsx 我已经实现了作品列表组件，请帮我审查代码，看是否有改进空间
   ```

#### 调试问题

当你遇到 bug 或错误时，可以这样使用 AI 助手：

1. **描述问题**：
   ```
   @frontend/app/artist/[id]/page.tsx 我在访问艺术家详情页时遇到了错误：
   "TypeError: Cannot read properties of undefined (reading 'name')"
   ```

2. **提供上下文**：
   ```
   这个错误发生在加载艺术家数据时。我使用了 SWR 来获取数据，但似乎在数据加载完成前就尝试访问了数据属性
   ```

3. **请求解决方案**：
   ```
   请帮我分析这个问题的原因，并提供解决方案。我希望能够优雅地处理数据加载状态
   ```

4. **实施修复**：
   ```
   你的解决方案看起来不错，请帮我修改代码来实现这个修复
   ```

#### 重构代码

当你需要改进现有代码时：

1. **说明重构目标**：
   ```
   @backend/routes/artist.py 这个文件变得越来越大，难以维护。我想将它重构为更小的模块，遵循单一职责原则
   ```

2. **请求重构计划**：
   ```
   请帮我分析这个文件，并提出一个重构计划，包括如何拆分模块、如何组织代码结构
   ```

3. **逐步实施**：
   ```
   我们先实现第一步：将艺术家 CRUD 操作拆分到单独的文件中。请帮我编写新的代码结构
   ```

#### 学习新技术

当你需要学习项目中使用的新技术时：

1. **请求技术概述**：
   ```
   @project_context.md 我注意到项目使用了 Jotai 进行状态管理。请给我介绍 Jotai 的基本概念和使用方法
   ```

2. **请求示例**：
   ```
   请给我一个在 AIDA 项目中使用 Jotai 的简单示例，包括如何创建原子、如何在组件中使用它们
   ```

3. **应用到实际问题**：
   ```
   我现在需要实现一个功能：用户可以将艺术家添加到收藏夹。请帮我设计如何使用 Jotai 来管理收藏夹状态
   ```

#### 生成测试

当你需要为代码编写测试时：

1. **请求测试策略**：
   ```
   @backend/models/artist.py 我需要为这个艺术家模型编写单元测试。请帮我设计测试策略，包括需要测试哪些场景
   ```

2. **生成测试代码**：
   ```
   请帮我为 create_artist 函数编写单元测试，包括正常情况和各种边缘情况
   ```

记住，AI 助手是强大的工具，但它不能替代你的思考和判断。始终审查 AI 生成的代码，确保它符合项目标准和最佳实践。

## 第五部分：常见问题与进阶

### 常见问题解答

#### MongoDB 无法连接怎么办？

1. 确保 MongoDB 服务正在运行
2. 检查 `.env` 文件中的连接字符串是否正确
3. 尝试使用 MongoDB Compass 连接数据库，确认连接信息正确

#### 如何停止所有服务？

在运行服务的终端窗口中按 `Ctrl+C`。

#### 如何更新项目代码？

在终端中运行：
```bash
git pull
```

然后重新安装依赖：
```bash
npm run setup:all
```

#### 如何查看项目的最新变更？

在终端中运行：
```bash
git log --oneline -n 10
```

这将显示最近的 10 次提交记录。

### 下一步学习

恭喜你完成了 AIDA 项目的初始设置和运行！接下来，你可以：

1. 探索项目文档，了解更多技术细节
2. 查看前端和后端代码，理解它们是如何工作的
3. 尝试修改一些代码，看看会发生什么变化
4. 学习更多关于 Next.js、FastAPI 和 MongoDB 的知识

记住，学习编程是一个循序渐进的过程。不要害怕犯错，每个错误都是学习的机会！

如果你有任何问题，可以查阅项目文档或向团队成员寻求帮助。祝你编程愉快！ 