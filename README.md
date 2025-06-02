# AIDA - AI Database of Artist

AIDA is a comprehensive platform that combines forums, social media, and AI interaction to create an artist community. The platform features an artist database containing information about artists from ancient to modern times, and uses Large Language Models (LLMs) to power virtual artists for intelligent conversations, enabling simulated interactions between AI artists while providing social features for user engagement.

## Project Structure

This monorepo contains the following components:

- `docs/`: Documentation for developers (bilingual: Chinese and English)
- `backend/`: Python-based backend service
- `frontend/`: Next.js React frontend application
- `scraper/`: Web scraping tools for collecting artist data
- `gptmemory/`: Shared memory for AI assistants in collaborative development
- `data/`: CSV data files for artist information

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- MongoDB
- Chrome browser (for scraper)
- Make (optional, for Makefile approach)
- Docker & Docker Compose (optional, for containerized approach)

### MongoDB Installation

#### macOS (using Homebrew)

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community
```

#### Windows

1. Download the MongoDB Community Server installer from the [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the installation wizard
3. Choose "Complete" setup type
4. Check "Install MongoDB as a Service"
5. Complete the installation

#### Linux (Ubuntu/Debian)

```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Reload local package database
sudo apt-get update

# Install MongoDB packages
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod

# Enable MongoDB to start on boot
sudo systemctl enable mongod
```

#### Docker

```bash
# Pull MongoDB image
docker pull mongo

# Run MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo
```

### One-Click Setup & Start

You have three options to start the entire project with a single command:

#### Option 1: Using npm scripts (Recommended for most developers)

```bash
# Install dependencies for all components
npm run setup:all

# Create .env file from .env.example (IMPORTANT)
cp .env.example .env
# Edit the .env file to set your specific configuration

# Import test data into MongoDB
npm run setup:mongodb

# Or do everything in one command (includes environment check)
npm run setup:complete

# Start all services (backend, frontend, docs)
npm run dev
```

> **Note**: The `setup:mongodb` script will automatically check for the existence of the `.env` file and MongoDB's running status before attempting to import data. If the `.env` file doesn't exist, it will try to create it from `.env.example`.

#### Option 2: Using Makefile (Good for Unix/Linux/macOS users)

```bash
# Install dependencies for all components
make setup

# Start all services
make start

# Stop all services
make stop
```

#### Option 3: Using Docker Compose (Best for consistent environments across team)

**🐳 推荐使用Docker容器化部署，确保环境一致性！**

```bash
# 一键启动（推荐）
chmod +x docker-run.sh
./docker-run.sh

# 或手动启动开发环境
docker-compose up --build

# 或启动生产环境
docker-compose -f docker-compose.prod.yml up --build -d

# 停止服务
docker-compose down
```

**Docker容器化的优势：**
- ✅ 环境一致性：无论在什么系统上都能稳定运行
- ✅ 一键部署：朋友可以直接运行您的容器
- ✅ 依赖隔离：不会与系统其他软件冲突
- ✅ 生产就绪：包含Nginx反向代理和优化配置

**详细的Docker使用指南请查看：[DOCKER_README.md](./DOCKER_README.md)**

### Individual Component Setup

#### 1. Clone the repository

```bash
git clone https://github.com/thevertexlab/aida.git
cd aida
```

#### 2. Backend Setup

```bash
# Create a virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# IMPORTANT: Create .env file (copy from .env.example)
cp .env.example .env
# Edit the .env file to set your specific configuration

# Start the backend server
uvicorn main:app --reload
```

#### 3. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

#### 4. Documentation Setup

```bash
# Install dependencies
cd docs
npm install

# Start the documentation server
npm run dev
```

#### 5. Scraper Setup

```bash
# Create a virtual environment
cd scraper
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp ../.env.example scraper/.env

# Run the scraper
python aida_art_scraper.py
```

## API Documentation

The backend API provides interactive documentation:

- Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- ReDoc: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

## Development Workflow

### Git Commit Message Guidelines

We follow a standardized commit message format to maintain a clean and meaningful commit history:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types:
- **🚀 feat**: A new feature
- **🔧 fix**: A bug fix
- **📚 docs**: Documentation changes
- **💎 style**: Code style changes (formatting, missing semi-colons, etc)
- **🔨 refactor**: Code changes that neither fix a bug nor add a feature
- **⚡ perf**: Performance improvements
- **🧪 test**: Adding or fixing tests
- **🔧 chore**: Changes to build process or auxiliary tools

#### Scope:
Specify the component being affected (backend, frontend, docs, scraper, etc.)

#### Examples:
```
feat(frontend): add artist profile page
fix(backend): resolve artist search pagination issue
docs(readme): update installation instructions
```

### Branch Naming Convention

- Feature branches: `feature/short-description`
- Bug fix branches: `fix/short-description`
- Documentation branches: `docs/short-description`

## License

Proprietary and Confidential. This is a closed-source commercial project. All rights reserved.

# AIDA 艺术数据爬虫工具

这是AIDA项目的艺术数据爬虫工具，用于从Artsy网站采集艺术家和艺术品数据。

## 快速启动

只需要运行根目录下的批处理文件即可启动图形界面：

```
run_artsy_tools.bat
```

## 功能介绍

爬虫工具提供了直观的图形界面，包含以下功能：

1. **爬取艺术家数据** - 可以指定艺术家数量和每位艺术家的作品数量
2. **清理图片数据** - 自动识别并处理低质量和重复的图片
3. **数据统计与管理** - 查看采集的数据统计信息
4. **断点续传** - 支持从上次中断的地方继续爬取

## 数据输出

所有爬取的数据将保存在 `data/artsy` 目录下：

- 艺术家数据：`artsy_artists.csv`
- 艺术品数据：`artsy_artworks.csv`
- 图片数据：`images/` 目录（按艺术家姓名分类）

## 系统要求

- Python 3.7+
- 必要的Python依赖项（自动安装）

## 常见问题

如果启动失败，请确保已安装所需依赖：

```
pip install -r scraper/requirements.txt
```

## 注意事项

本工具仅供学术研究使用，请遵守数据源网站的使用条款。
