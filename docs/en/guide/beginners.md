# Beginner-Friendly Development Guide

::: tip Note
This guide is designed for complete beginners with no full-stack development experience. We'll guide you step by step on how to install necessary tools, configure your environment, and run the AIDA project.
:::

## Step 1: Install Basic Tools

Before we start development, we need to install some basic tools. Don't worry, we'll guide you through this process step by step!

### Install Git

Git is a version control system that helps us manage code changes.

::: details Windows Users
1. Visit the [Git website](https://git-scm.com/download/win)
2. Download the Git installer for Windows
3. Run the installer, using default settings by clicking "Next" throughout the process
4. After installation, open "Command Prompt" or "PowerShell" and type `git --version` to confirm successful installation
:::

::: details macOS Users
1. If you have Xcode installed, Git is already included
2. If you don't have Xcode, you can install Git via Terminal:
   - Open the "Terminal" application
   - Type `xcode-select --install` and press Enter
   - Follow the prompts to complete the installation
3. Alternatively, you can use Homebrew to install Git:
   - Install Homebrew (if not already installed): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Install Git: `brew install git`
4. After installation, type `git --version` in the terminal to confirm successful installation
:::

### Install Cursor Editor

Cursor is an AI-powered code editor that helps you write code more efficiently.

1. Visit the [Cursor website](https://cursor.sh/)
2. Download the version suitable for your operating system
3. Install and launch Cursor
4. Register or log in to your Cursor account

### Install Node.js and npm

Node.js is a JavaScript runtime environment, and npm is the Node.js package manager. We need them to run the frontend code.

::: details Windows Users
1. Visit the [Node.js website](https://nodejs.org/)
2. Download and install the LTS (Long Term Support) version
3. Use default settings during installation
4. After installation, open Command Prompt or PowerShell and type `node --version` and `npm --version` to confirm successful installation
:::

::: details macOS Users
1. Use Homebrew to install Node.js:
   ```bash
   brew install node
   ```
2. After installation, type `node --version` and `npm --version` in the terminal to confirm successful installation
:::

### Install Python

Python is a programming language that our backend is developed with.

::: details Windows Users
1. Visit the [Python website](https://www.python.org/downloads/)
2. Download the latest Python installer (choose version 3.9 or higher)
3. Run the installer, **make sure to check "Add Python to PATH"**
4. Click "Install Now" to begin installation
5. After installation, open Command Prompt or PowerShell and type `python --version` to confirm successful installation
:::

::: details macOS Users
1. macOS usually comes with Python pre-installed, but it might not be the latest version
2. Use Homebrew to install the latest version of Python:
   ```bash
   brew install python
   ```
3. After installation, type `python3 --version` in the terminal to confirm successful installation
:::

### Install MongoDB

MongoDB is a document database that we use to store project data.

::: details Windows Users
1. Visit the [MongoDB website](https://www.mongodb.com/try/download/community)
2. Download MongoDB Community Server
3. Run the installer, select "Complete" installation type
4. Check "Install MongoDB as a Service"
5. After installation, the MongoDB service should start automatically
6. You can also install [MongoDB Compass](https://www.mongodb.com/try/download/compass), a graphical MongoDB management tool
:::

::: details macOS Users
1. Use Homebrew to install MongoDB:
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   ```
2. Start the MongoDB service:
   ```bash
   brew services start mongodb-community
   ```
3. You can also install MongoDB Compass:
   ```bash
   brew install --cask mongodb-compass
   ```
:::

## Step 2: Get the Project Code

Now that we have installed all the necessary tools, let's get the project code.

### Clone the GitHub Repository

1. Open Command Prompt (Windows) or Terminal (macOS)
2. Navigate to the directory where you want to store the project, for example:
   ```bash
   cd Documents
   ```
3. Clone the project repository:
   ```bash
   git clone https://github.com/thevertexlab/aida.git
   ```
4. Enter the project directory:
   ```bash
   cd aida
   ```

### Open the Project in Cursor

1. Open the Cursor editor
2. Click "File" > "Open Folder"
3. Navigate to the aida project directory you just cloned and open it

## Step 3: Configure the Project Environment

Now we need to configure the project environment, install dependencies, and set up necessary configuration files.

### Create Environment Variables File

1. In the project root directory, find the `.env.example` file
2. Copy this file and rename it to `.env`
3. Open the `.env` file and modify the configuration as needed (for first-time use, the default configuration is usually sufficient)

### Install Project Dependencies

Open a terminal in Cursor (Terminal > New Terminal), then run the following command:

```bash
npm run setup:all
```

This command will install all dependencies required for the frontend, backend, and documentation system. This may take a few minutes, please be patient.

### Import Test Data

After installing dependencies, we need to import some test data into MongoDB:

```bash
npm run setup:mongodb
```

This command will check your environment configuration, ensure MongoDB is running, and then import test data.

## Step 4: Start the Project

Now we have completed all configurations and can start the project!

### Start All Services with One Command

In the terminal, run:

```bash
npm run dev
```

This command will start the frontend, backend, and documentation services simultaneously. You will see a nice output displaying the access addresses for all services.

### Access the Services

After successful startup, you can access the various services at the following addresses:

- **Frontend Application**: http://localhost:3000
- **Backend Service**: http://localhost:8000
- **Project Documentation**: http://localhost:5173
- **API Documentation**: http://localhost:8000/api/docs

## Step 5: Understand the Project Structure

Now that you have successfully run the project, let's understand the basic structure of the project.

### Project Directory Structure

- `frontend/`: Frontend code, using the Next.js framework
- `backend/`: Backend code, using the FastAPI framework
- `docs/`: Project documentation, using VitePress
- `scraper/`: Data crawler, used to collect artist information
- `data/`: Store data files
- `scripts/`: Various utility scripts
- `gptmemory/`: Shared memory for AI assistants

### Understanding Backend APIs

Backend APIs can be understood as a set of functions that are called via HTTP requests. For example:

- When you visit `http://localhost:8000/api/artists`, the backend will return a list of all artists
- When you visit `http://localhost:8000/api/artists/123`, the backend will return information about the artist with ID 123

You can view all available API endpoints and their detailed descriptions by visiting the API documentation at `http://localhost:8000/api/docs`.

## Step 6: Using GPT Memory

The AIDA project uses the GPT Memory system to help AI assistants (such as the AI in Cursor) understand project context and specifications.

### Understanding GPT Memory Files

The `gptmemory/` directory in the project contains the following important files:

- `project_standards.md`: Project specifications and standards
- `project_context.md`: Overview of the project's core concepts and architecture
- `working_memory_[username].md`: Working memory for each developer

### First-time Using AI Assistant

When you first use the AI assistant in Cursor, you can have it read these files:

```
Please read gptmemory/project_standards.md and gptmemory/project_context.md to understand the project specifications and context
```

### Create Personal Working Memory

You can create your own working memory file:

1. Create a file named `working_memory_your-username.md` in the `gptmemory/` directory
2. Record your current tasks and progress in the file
3. When using the AI assistant, you can have it check your working memory:
   ```
   I'm starting a new task, please check gptmemory/working_memory_your-username.md
   ```

## Frequently Asked Questions

### What if I can't connect to MongoDB?

1. Make sure the MongoDB service is running
2. Check if the connection string in the `.env` file is correct
3. Try connecting to the database using MongoDB Compass to confirm the connection information is correct

### How do I stop all services?

Press `Ctrl+C` in the terminal window where the services are running.

### How do I update the project code?

Run in the terminal:
```bash
git pull
```

Then reinstall dependencies:
```bash
npm run setup:all
```

### How do I view the latest changes to the project?

Run in the terminal:
```bash
git log --oneline -n 10
```

This will display the 10 most recent commit records.

## Next Steps for Learning

Congratulations on completing the initial setup and running of the AIDA project! Next, you can:

1. Explore the project documentation to learn more technical details
2. Look at the frontend and backend code to understand how they work
3. Try modifying some code to see what changes occur
4. Learn more about Next.js, FastAPI, and MongoDB

Remember, learning programming is a gradual process. Don't be afraid to make mistakes; each error is an opportunity to learn!

If you have any questions, you can refer to the project documentation or seek help from team members. Happy coding! 