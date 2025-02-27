# AIDA - AI Artist Database

AIDA is a comprehensive platform that combines forums, social media, and AI interaction to create an artist community. The platform features an artist database containing information about artists from ancient to modern times, and uses Large Language Models (LLMs) to power virtual artists for intelligent conversations, enabling simulated interactions between AI artists while providing social features for user engagement.

## Project Structure

This monorepo contains the following components:

- `docs/`: Documentation for developers (bilingual: Chinese and English)
- `backend/`: Python-based backend service
- `frontend/`: Next.js React frontend application
- `scraper/`: Web scraping tools for collecting artist data
- `gptmemory/`: Shared memory for AI assistants in collaborative development

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- MongoDB
- Chrome browser (for scraper)
- Make (optional, for Makefile approach)
- Docker & Docker Compose (optional, for containerized approach)

### One-Click Setup & Start

You have three options to start the entire project with a single command:

#### Option 1: Using npm scripts (Recommended for most developers)

```bash
# Install dependencies for all components
npm run setup:all

# Start all services (backend, frontend, docs)
npm run dev
```

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

# Create .env file
echo "DATABASE_URL=mongodb://localhost:27017/aida
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_jwt_secret" > .env

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

# Create .env file
echo "MONGODB_URI=mongodb://localhost:27017/aida" > .env

# Run the scraper
python main.py
```

## Development Workflow

### Git Commit Message Guidelines

We follow a standardized commit message format to maintain a clean and meaningful commit history:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semi-colons, etc)
- **refactor**: Code changes that neither fix a bug nor add a feature
- **perf**: Performance improvements
- **test**: Adding or fixing tests
- **chore**: Changes to build process or auxiliary tools

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
