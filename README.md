# AIDA - AI Artist Database

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

```bash
# Build and start all services
docker-compose up

# Stop all services
docker-compose down
```

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
python main.py
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
