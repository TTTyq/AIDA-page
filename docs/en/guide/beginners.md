# Beginner-Friendly Development Guide

::: tip Note
This guide is designed for complete beginners with no full-stack development experience. We'll guide you step by step on how to install necessary tools, configure your environment, and run the AIDA project.
:::

::: info AI Assistant is Your Helper
Throughout this guide, you'll see many "Let AI Help You" tip boxes. The AIDA project encourages using AI assistants (like the AI in Cursor) to improve development efficiency. Don't hesitate to ask AI questions! Whether it's environment configuration, code writing, or troubleshooting, AI can provide valuable assistance.
:::

## Table of Contents

- [Environment Setup](#environment-setup)
  - [Installing Basic Tools](#installing-basic-tools)
  - [Getting the Project Code](#getting-the-project-code)
  - [Configuring the Project Environment](#configuring-the-project-environment)
- [Running and Understanding the Project](#running-and-understanding-the-project)
  - [Starting the Project](#starting-the-project)
  - [Understanding the Project Structure](#understanding-the-project-structure)
  - [Understanding Backend APIs](#understanding-backend-apis)
- [Development Workflow](#development-workflow)
  - [Git Workflow](#git-workflow)
  - [Using GPT Memory](#using-gpt-memory)
- [AI-Assisted Development](#ai-assisted-development)
  - [AI Assistant Basics](#ai-assistant-basics)
  - [Advanced AI-Assisted Development Practices](#advanced-ai-assisted-development-practices)
  - [Implementing New Requirements](#implementing-new-requirements)
  - [Debugging Issues](#debugging-issues)
  - [Using Chrome DevTools for Debugging](#using-chrome-devtools-for-debugging)
  - [Using Swagger UI and ReDoc to Understand APIs](#using-swagger-ui-and-redoc-to-understand-apis)
  - [Understanding HTTP Request Methods](#understanding-http-request-methods)
  - [Refactoring Code](#refactoring-code)
  - [Learning New Technologies](#learning-new-technologies)
  - [Generating Tests](#generating-tests)
- [Common Issues and Next Steps](#common-issues-and-next-steps)
  - [Frequently Asked Questions](#frequently-asked-questions)
  - [Next Steps for Learning](#next-steps-for-learning)

## Environment Setup

### Installing Basic Tools

Before we start development, we need to install some basic tools. Don't worry, we'll guide you through this process step by step!

### Installing Cursor Editor

Cursor is an AI-powered code editor that helps you write code more efficiently. This is the first tool we'll install because once you have Cursor, you can use its AI assistant to help you install and configure all the other tools!

1. Visit the [Cursor website](https://cursor.sh/)
2. Download the version suitable for your operating system
3. Install and launch Cursor
4. Register or log in to your Cursor account
   - **Important note**: In the AIDA project, we use the team shared account `work@thevertexlab.com` (ask for the password in the team chat)
   - Using the team account allows sharing subscription benefits and quotas, which is a team perk

::: info Relationship Between Cursor and VSCode
Cursor is actually an enhanced editor built on VSCode. It retains all the excellent features of VSCode (such as the extension system, debugging tools, Git integration, etc.) while integrating powerful AI capabilities. This means:
- If you're familiar with VSCode, you'll immediately be familiar with Cursor's interface and basic operations
- You can use most VSCode extensions
- All VSCode keyboard shortcuts work in Cursor
- But Cursor additionally provides powerful AI code generation, code explanation, automatic refactoring, and other features

You can think of Cursor as a combination of VSCode + AI assistant, giving you powerful AI support in a familiar environment!
:::

::: warning 🎉 New Era of Programming!
After completing this step, you can say goodbye to cold code and complicated command lines! You only need to remember a few commands, and most of the time you just need to use natural language to talk to AI to complete programming tasks. Imagine just saying "help me implement a login page," and AI generates the code for you! Isn't that super cool?! This is the revolutionary change brought by AI-assisted programming!
:::

### Cursor Usage Tips

Before you start using Cursor for development, here are some important usage tips:

1. **Open the AI chat interface**:
   - Use the shortcut `Cmd+I` (macOS) or `Ctrl+I` (Windows) to open the chat interface at the bottom
   - Or click the chat icon in the bottom right corner of the editor

2. **Switch to Agent mode**:
   - In the chat interface, click the dropdown menu in the top right corner and select "Agent" mode
   - In Agent mode, AI can automatically perform multiple operations, such as searching code, reading files, editing code, etc.
   - Note: Agent mode will automatically stop after executing a maximum of 25 commands to prevent infinite loops

::: warning Mode Selection Alert
Make sure you've correctly switched to Agent mode! If you notice the AI is only answering questions but not performing any actions (like reading files, modifying code, etc.), it's likely because you're still in Ask mode. Most development tasks should be done in Agent mode unless you're just asking a simple question. Get in the habit of checking your mode every time you start a new conversation.
:::

3. **About command execution**:
   - When AI suggests executing command line commands, it will display a "Run Command" button
   - You need to manually click this button to execute the command; AI will not automatically execute command line operations

4. **Handling code application issues**:
   - Sometimes AI-generated code changes may not be automatically applied to files
   - If you see AI outputting code in the dialog box instead of directly modifying the file, look for and click the "Apply" button
   - If there's no "Apply" button, you can manually copy the code and paste it into the appropriate file

5. **Understanding curl commands executed by Cursor**:
   - When you see Cursor AI automatically executing `curl` commands, don't worry - this is AI retrieving network resources
   - `curl` is a command-line tool for transferring data that Cursor uses to fetch information from the web, check API responses, etc.
   - These commands are generally safe and are executed by the AI assistant to better help you
   - If you have questions about a curl command, you can directly ask the AI: "What was that curl command you just executed for?"

6. **Installing mongosh for MongoDB debugging**:
   - `mongosh` is MongoDB's command-line tool that helps you interact directly with the database
   - Installation methods:
     - Windows: Download and install from the [MongoDB website](https://www.mongodb.com/try/download/shell)
     - macOS: Install using Homebrew: `brew install mongosh`
   - After installation, you can type `mongosh` in the terminal to connect to your local MongoDB
   - Cursor AI can help you execute database queries, modify data structures, etc. through mongosh
:::

::: info 💡 Tip
If AI seems stuck or behaving abnormally, try refreshing the page or restarting Cursor. Sometimes a simple restart can solve most problems!
:::

::: warning Important Note
Please note that during the Cursor installation process, you don't have an AI assistant to ask questions yet. But once you've installed and logged in successfully, you can use Cursor's AI assistant to help you install and configure all subsequent tools! That's why we put installing Cursor as the first step.
:::

### Using Cursor AI Web Search

Cursor AI has powerful web search capabilities that can help you get the latest information:

1. **Trigger web search**: Type `@` in the chat box and select the `Web` option, or directly type `@Web`
2. **Search syntax**: `@Web your search question`, for example: `@Web How to implement SSR in Next.js?`
3. **Search advantages**:
   - Get the latest technical documentation and tutorials
   - Solve dependency issues for specific versions
   - Find best practices in the community
   - Learn about technology trends and updates

4. **Web search use cases**:
   - **Learning new frameworks or libraries**: `@Web React Server Components best practices`
   - **Solving specific errors**: `@Web Next.js 14 TypeError: Cannot read properties of undefined`
   - **Finding API documentation**: `@Web MongoDB aggregation pipeline operators documentation`
   - **Understanding technology trends**: `@Web 2024 frontend development trends`

5. **Processing search results**:
   - Cursor will return summaries of multiple relevant web pages
   - Results usually include original links for further viewing of complete content
   - AI will provide comprehensive answers based on search results

::: tip Let AI Help You
When you need to learn about the latest technical information, you can use the web search feature:

> @Web Please find information about Next.js 14 new features and migration guide

AI will search the web and provide the latest Next.js 14 related information.
:::

::: warning Notes
Web search functionality is particularly useful in the following situations:
1. Querying the latest released technologies or versions
2. Finding solutions for specific errors
3. Learning about the latest community developments and best practices
4. Getting the latest API changes from official documentation

But remember, the quality of search results depends on your query description, so try to use accurate and specific keywords.
:::

### Installing Git

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

::: tip Let AI Help You
Now that you've installed Cursor, you can use its AI assistant to help you install Git:

> I need to install Git on my computer. Please guide me through the installation process. I'm using [your operating system].

AI will provide detailed installation steps based on your operating system and can even generate the necessary commands.
:::

### Installing Node.js and npm

Node.js is a JavaScript runtime environment, and npm is the Node.js package manager. We need them to run the frontend code.

::: details Windows Users
1. Visit the [Node.js website](https://nodejs.org/)
2. Download and install the LTS (Long Term Support) version
3. Use default settings during installation
4. After installation, open Command Prompt or PowerShell and type `node --version` and `npm --version` to confirm successful installation
:::

::: details macOS Users
1. First, we need to install Homebrew (a package manager for macOS, similar to an app store on your phone, which helps you install various software):
   - Open the "Terminal" application (you can find it in "Applications > Utilities" or use Spotlight to search for "Terminal")
   - Copy the following command, paste it into the terminal, and press Enter:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Follow the prompts on the screen to complete the installation (you may need to enter your computer password)
   - After installation, the terminal will display some follow-up steps; please follow these steps

2. Then, use Homebrew to install Node.js:
   ```bash
   brew install node
   ```
3. After installation, type `node --version` and `npm --version` in the terminal to confirm successful installation
:::

::: tip Let AI Help You
Use Cursor's AI assistant to help you install Node.js and npm:

> Please help me install Node.js and npm on [your operating system], and ensure they are correctly configured.

AI will provide detailed installation guides, including download links, installation commands, and verification steps.
:::

### Installing Python

Python is a programming language; our backend is developed using Python.

::: details Windows Users
1. Visit the [Python website](https://www.python.org/downloads/)
2. Download the latest Python installer (choose version 3.9 or higher)
3. Run the installer, **be sure to check "Add Python to PATH"**
4. Click "Install Now" to start installation
5. After installation, open Command Prompt or PowerShell and type `python --version` to confirm successful installation
:::

::: details macOS Users
1. macOS usually comes with Python pre-installed, but it may not be the latest version
2. Use Homebrew to install the latest version of Python:
   ```bash
   brew install python
   ```
3. After installation, type `python3 --version` in the terminal to confirm successful installation
:::

::: tip Let AI Help You
Let Cursor's AI assistant help you install and configure Python:

> I need to install Python for the AIDA project. Please guide me on how to install Python 3.9 or higher on [your operating system], and ensure it's correctly added to PATH.

AI will provide detailed installation steps for your operating system and help you solve any issues you might encounter.
:::

### Installing MongoDB

MongoDB is a document database that we use to store project data.

::: details Windows Users
1. Visit the [MongoDB website](https://www.mongodb.com/try/download/community)
2. Download MongoDB Community Server
3. Run the installer, select "Complete" installation type
4. Check "Install MongoDB as a Service"
5. After installation is complete, the MongoDB service should start automatically
6. You can also install [MongoDB Compass](https://www.mongodb.com/try/download/compass), which is a graphical MongoDB management tool
:::

::: details macOS Users
1. Use Homebrew (which we installed earlier) to install MongoDB:
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

::: tip Let AI Help You
MongoDB installation and configuration can be complex. Let Cursor's AI assistant help you complete this process:

> Please help me install and configure MongoDB on [your operating system], including how to start the service and verify that the installation is successful.

AI will provide detailed installation guides, including common issues and solutions you might encounter.
:::

## Getting the Project Code

Now that we've installed all the necessary tools, let's get the project code.

### Cloning the GitHub Repository

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

### Opening the Project in Cursor

1. Open the Cursor editor
2. Click "File" > "Open Folder"
3. Navigate to the aida project directory you just cloned and open it

### Configuring the Project Environment

Now we need to configure the project environment, install dependencies, and set up necessary configuration files.

### Creating Environment Variables File

1. In the project root directory, find the `.env.example` file
2. Copy this file and rename it to `.env`
3. Open the `.env` file and modify the configuration as needed (for first-time use, the default configuration is usually sufficient)

### Installing Project Dependencies

Open a terminal in Cursor (Terminal > New Terminal), then run the following command:

```bash
npm run setup:all
```

This command will install all dependencies required for the frontend, backend, and documentation system. This may take a few minutes, please be patient.

::: info 💡 Tip
Don't worry about these complex commands! This might be one of the few commands you need to manually input. Remember, with the AI assistant, you can always ask "What command should I run now?" and AI will tell you the correct approach. It's like having an experienced developer guiding you at all times!
:::

::: tip Let AI Help You
If you encounter errors during the installation process, you can directly ask the AI assistant:

> I encountered the following error while running npm run setup:all: [copy error message]. Please help me solve it.

AI will analyze the error and provide solutions.
:::

### Importing Test Data

After installing the dependencies, we need to import some test data into MongoDB:

```bash
npm run setup:mongodb
```

This command will check your environment configuration, ensure MongoDB is running, and then import test data.

::: tip Let AI Help You
If you're not sure whether MongoDB is correctly installed or running, you can ask the AI assistant:

> Please help me check if MongoDB is correctly installed and running. How can I verify?

AI will guide you to check the MongoDB service status and provide the appropriate commands.
:::

## Running and Understanding the Project

### Starting the Project

Now that we've completed all the configuration, we can start the project!

#### Starting All Services with One Command

In the terminal, run:

```bash
npm run dev
```

This command will start the frontend, backend, and documentation services simultaneously. You'll see a nice output displaying the access addresses for all services.

::: info 🚀 Achievement Moment!
Feeling a bit excited when you see all services successfully starting? This is a full-stack application that you've set up yourself! Although you just ran a simple command, you've successfully started a complete project with frontend, backend, and database. This used to require professional developers spending a lot of time to accomplish!
:::

### Accessing Various Services

After successful startup, you can access the various services through the following addresses:

- **Frontend application**: http://localhost:3000
- **Backend service**: http://localhost:8000
- **Project documentation**: http://localhost:5173
- **API documentation**: http://localhost:8000/api/docs

### Understanding the Project Structure

Now that you've successfully run the project, let's understand the basic structure of the project.

### Project Directory Structure

- `frontend/`: Frontend code, using the Next.js framework
- `backend/`: Backend code, using the FastAPI framework
- `docs/`: Project documentation, using VitePress
- `scraper/`: Data scraper, used to collect artist information
- `data/`: Stores data files
- `scripts/`: Various utility scripts
- `gptmemory/`: Shared memory for AI assistants

::: tip Let AI Help You
If you want to understand the detailed structure of a specific directory, you can ask the AI assistant:

> Please help me explain the structure of the frontend directory and the purpose of each file.

AI will explain the structure of the directory in detail and the purpose of each important file.
:::

### Understanding Backend APIs

Backend APIs can be understood as a set of functions that are called through HTTP requests. For example:

- When you visit `http://localhost:8000/api/artists`, the backend will return a list of all artists
- When you visit `http://localhost:8000/api/artists/123`, the backend will return information about the artist with ID 123

You can access the API documentation by visiting `http://localhost:8000/api/docs` to view all available API endpoints and their detailed descriptions.

## Development Workflow

### Git Workflow

In the AIDA project, we use Git for version control. Here's the basic Git workflow:

::: info 🧙‍♂️ Magic Moment
Git might seem a bit complex, but don't worry! Think of it as a time machine that lets you go back to any historical state of your code at any time. And with AI assistants, you don't even need to remember those complex Git commands — just tell the AI "I want to save my changes" or "I want to switch to a new branch," and the AI will tell you exactly what to do!
:::

### Creating a New Branch

Before starting a new feature or fixing a bug, you should create a new branch:

```bash
git checkout -b feature/your-feature-name
```

::: tip Let AI Help You
You can directly tell the AI assistant:

> I need to work on a new branch for development. Help me create and switch to a new branch. I'm Dim, and I'm working on the artist list feature.

AI might respond:
"You can use the following command to create and switch to a new branch:
```bash
git checkout -b feature/dim/artist-list
```
This branch name follows the project's naming convention: feature/developer-name/feature-description"
:::

### Committing Changes

1. Check your changes:
   ```bash
   git status
   ```

2. Add changed files to the staging area:
   ```bash
   git add .  # Add all changes
   # or
   git add path/to/specific/file  # Add specific file
   ```

3. **Use Cursor to generate commit messages**:
   - In Cursor, click the Source Control icon on the left
   - Click the "⭐⭐" icon (Generate Commit Message) next to the commit message box
   - Cursor's AI will analyze your changes and generate an appropriate commit message
   - You can edit this message as needed

::: tip Let AI Help You
You can also ask the AI assistant to help you generate a commit message:

> I modified the following files: [list modified files], mainly implementing pagination for the artist list. Please help me generate a commit message that follows the project standards.

AI will generate an appropriate commit message based on your description, such as:
"feat(artist-list): implement pagination for artist listing page"
:::

4. Commit your changes:
   - In Cursor's Source Control panel, click the "✓" icon (Commit)
   - Or use the terminal:
     ```bash
     git commit -m "Your commit message"
     ```

### Pushing and Pulling Changes

After committing changes, you need to push these changes to the remote repository or pull changes from others:

1. **Push changes to the remote repository**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Pull changes from the remote repository**:
   ```bash
   git pull origin main  # Pull changes from the main branch
   ```

#### Using Cursor Interface for Git Operations

Cursor provides a convenient graphical interface for Git operations:

1. **Using the status bar**:
   - In the status bar at the bottom left of the editor, you'll see an icon like `1↑/2↓`
   - `↑` indicates how many local commits you need to push to the remote repository
   - `↓` indicates how many remote commits you need to pull to your local repository
   - Click this icon to quickly perform push or pull operations

2. **Using the Source Control panel**:
   - Click the Source Control icon in the activity bar on the left (usually a branch icon)
   - In the panel that opens, you can see all changed files
   - The panel has buttons like "Push", "Pull", etc. at the top; click to perform the corresponding operation
   - You can also right-click on files to stage, unstage, or discard changes

::: info 💡 Tip
When you see `1↑` in the status bar, it means you have one local commit that needs to be pushed to the remote repository. Click it and select "Push" to do so.

Similarly, when you see `2↓`, it means there are two remote commits that need to be pulled to your local repository. Click it and select "Pull" to do so.
:::

::: tip Let AI Help You
If you're unsure how to handle Git push or pull operations, you can ask the AI assistant:

> I see 2↑/3↓ in the status bar. What does this mean? What should I do?

Or:

> I just committed my code and now need to push it to the remote repository. Please tell me the exact steps.

AI will provide detailed operational guidance to help you complete Git operations.
:::

### Resolving Merge Conflicts

- When you pull remote changes, you may encounter merge conflicts
- Cursor will display conflict areas in the file and provide options for resolving conflicts
- You can choose to keep your changes, keep others' changes, or manually edit the conflict area
- After resolving all conflicts, you need to commit these changes

::: warning 🚨 Tips to Avoid Conflicts
To reduce merge conflicts, develop good habits:
1. Pull the latest code before starting work (`git pull`)
2. Commit and push your changes frequently
3. Develop different features on different branches
4. Communicate and coordinate in advance if multiple people are modifying the same file
:::

### Creating Pull Requests

When you've completed feature development, you can create a pull request:

1. Visit the project repository on GitHub
2. Click the "Pull requests" tab
3. Click the "New pull request" button
4. Select your branch and the target branch (usually main or master)
5. Fill in the title and description of the pull request
6. Click the "Create pull request" button

### Using GPT Memory

The AIDA project uses the GPT Memory system to help AI assistants (like the AI in Cursor) understand project context and standards.

### Understanding GPT Memory Files

The `gptmemory/` directory in the project contains the following important files:

- `project_memo.md`: Project standards, context, and common pitfalls
- `working_memory_[username].md`: Working memory for each developer

### First-time Using AI Assistant

When you first use the AI assistant in Cursor, you should have it read these files so it can understand the project's standards and context. Open a file in Cursor, then type in the chat box at the bottom:

```
Please read gptmemory/project_memo.md to understand project standards and context
```

### Creating Personal Working Memory

You don't need to manually create a working memory file; you can let the AI assistant help you create one:

1. In Cursor's chat box, type:
   ```
   Please refer to @working_memory_dim.md and help me create a working_memory_[your name].md
   ```

2. The AI assistant will help you create a new working memory file and set it up based on Dim's working memory format

::: tip Let AI Help You
After creating a working memory file, you can ask the AI assistant to help you update it:

> Please help me update my working memory file, adding the task I'm working on: implementing pagination for the artist list page.

AI will help you edit the working memory file, adding the new task and maintaining consistent formatting.
:::

3. When you start a new task, at the beginning of each conversation, you should reference your working memory file:
   ```
   @working_memory_[your name].md I'm starting a new task, [describe your task]
   ```

## AI-Assisted Development

### AI Assistant Basics

In the AIDA project, we use AI assistants (like the AI in Cursor) to improve development efficiency. Here are some useful tips:

::: warning 🤯 Revolutionary Programming Approach!
This might be the most important part of this guide! Once you master how to efficiently collaborate with AI assistants, your programming efficiency will increase 10-fold! Imagine those problems that would take hours of searching on Stack Overflow can now be solved with just a sentence; those API usages that would require reading lengthy documentation can now be answered by simply asking AI. This isn't just a change in tools, but a revolution in programming thinking!
:::

### Tips for Efficient Collaboration with AI

1. **Use shortcuts to open chat**: Press `Cmd+I` (macOS) or `Ctrl+I` (Windows) anytime to open the AI chat interface
2. **Ensure you're in Agent mode**: For complex tasks, it's recommended to use Agent mode, which can automatically execute multiple steps
3. **Handle code application issues**: If AI-generated code isn't automatically applied, look for and click the "Apply" button
4. **Manually confirm command execution**: When AI suggests executing commands, remember to click the "Run Command" button
5. **When AI gets stuck**: If AI behaves abnormally or gets stuck, try refreshing the page or restarting Cursor

::: info 🔄 Handling Common Issues
- **AI-generated code isn't applied**: Click the "Apply" button in the dialog box, or manually copy the code to the appropriate file
- **AI stops responding**: Refresh the page or restart Cursor
- **Command isn't executed**: Confirm whether you clicked the "Run Command" button
- **AI generates incorrect code**: Tell AI the code has issues and describe the specific errors; AI will try to fix it
:::

### Using Cursor AI Web Search

Cursor AI has powerful web search capabilities that can help you get the latest information:

1. **Trigger web search**: Type `@` in the chat box and select the `Web` option, or directly type `@Web`
2. **Search syntax**: `@Web your search question`, for example: `@Web How to implement SSR in Next.js?`
3. **Search advantages**:
   - Get the latest technical documentation and tutorials
   - Solve dependency issues for specific versions
   - Find best practices in the community
   - Learn about technology trends and updates

4. **Web search use cases**:
   - **Learning new frameworks or libraries**: `@Web React Server Components best practices`
   - **Solving specific errors**: `@Web Next.js 14 TypeError: Cannot read properties of undefined`
   - **Finding API documentation**: `@Web MongoDB aggregation pipeline operators documentation`
   - **Understanding technology trends**: `@Web 2024 frontend development trends`

5. **Processing search results**:
   - Cursor will return summaries of multiple relevant web pages
   - Results usually include original links for further viewing of complete content
   - AI will provide comprehensive answers based on search results

::: tip Let AI Help You
When you need to learn about the latest technical information, you can use the web search feature:

> @Web Please find information about Next.js 14 new features and migration guide

AI will search the web and provide the latest Next.js 14 related information.
:::

::: warning Notes
Web search functionality is particularly useful in the following situations:
1. Querying the latest released technologies or versions
2. Finding solutions for specific errors
3. Learning about the latest community developments and best practices
4. Getting the latest API changes from official documentation

But remember, the quality of search results depends on your query description, so try to use accurate and specific keywords.
:::

### Common Conversation Patterns

1. **Request code explanation**:
   ```
   @frontend/app/page.tsx Please explain how the code in this file works
   ```

2. **Request feature implementation**:
   ```
   @working_memory_[your name].md I need to implement an artist list page that can display with pagination and support search
   ```

3. **Request error fixing**:
   ```
   @backend/main.py I encountered the following error, please help me fix it: [error message]
   ```

4. **Request code review**:
   ```
   @frontend/components/ArtistCard.tsx Please review this code and see if there's room for improvement
   ```

5. **Learn project architecture**:
   ```
   @project_memo.md Please explain the overall architecture of the AIDA project and the relationships between components
   ```

### Advanced Prompt Techniques

1. **Provide sufficient context**:
   ```
   @working_memory_[your name].md @frontend/app/artists/page.tsx I'm developing the artist list page.
   I've completed the basic layout and now need to implement pagination. The backend API supports pagination through ?page=1&limit=10 parameters.
   Please help me implement the frontend pagination component and corresponding data fetching logic.
   ```

2. **Guide AI step by step**:
   ```
   @backend/models/artist.py I need to create an artist model. Please help me with the following steps:
   1. First, analyze what fields an artist needs
   2. Then, create a Pydantic model
   3. Finally, add necessary validations and methods
   ```

3. **Use role-playing to improve quality**:
   ```
   @frontend/components/ArtistDetail.tsx From the perspective of a senior React developer, please review this component for performance and best practices
   ```

4. **Request multiple solutions**:
   ```
   @project_memo.md I need to implement user authentication. Please provide 3 different implementation approaches and analyze the pros and cons of each
   ```

### Handling AI Limitations

Despite being very powerful, AI also has some limitations. Understanding these can help you use it more effectively:

1. **Code application issues**:
   - Issue: Sometimes AI generates code in the dialog box instead of directly modifying files
   - Solution: Look for and click the "Apply" button, or manually copy the code to the appropriate file

2. **Command execution limitations**:
   - Issue: AI won't automatically execute command line commands
   - Solution: When AI suggests executing commands, manually click the "Run Command" button

3. **Operation count limitations**:
   - Issue: In Agent mode, AI will stop after automatically executing a maximum of 25 operations
   - Solution: If the task isn't complete, you can tell AI "Please continue," or break large tasks into smaller ones

4. **Context loss**:
   - Issue: After long conversations, AI might "forget" previous context
   - Solution: Use `@filename` to reference relevant files again, or start a new conversation

::: tip Let AI Help You
When AI-generated code isn't automatically applied to the file, you can say:

> I see you've generated code, but it hasn't been applied to the file. Please help me regenerate this code and ensure it's applied to the file.

Or directly ask:

> How should I apply this code to the file?
:::

### Implementing New Requirements

When you need to implement a new feature, you can follow these steps using the AI assistant:

1. **Clarify requirements**:
   ```
   @working_memory_[your name].md I need to implement a new feature: artist works showcase page.
   This page needs to:
   1. Display basic information about the artist
   2. Show all the artist's works in a grid format
   3. Allow clicking on a work to view a larger image and detailed information
   4. Support filtering works by time and style
   ```

::: tip Let AI Help You
When you're not sure how to start implementing a feature, you can directly seek help from the AI assistant:

> I need to implement an artist details page, but I don't know where to start. This page needs to display the artist's basic information and a list of works. Please help me plan the implementation steps and generate a basic code framework.

AI will provide detailed implementation steps and code examples to help you quickly start development.
:::

2. **Get implementation suggestions**:
   ```
   Please help me plan the steps to implement this feature, including which components to create, how to organize data flow, what APIs are needed, etc.
   ```

3. **Implement step by step**:
   ```
   Now let's start implementing the first step: creating the artist works list component. Please help me design the structure and style of this component
   ```

4. **Code review**:
   ```
   @frontend/components/ArtistWorks.tsx I've implemented the works list component. Please review the code and see if there's room for improvement
   ```

### Debugging Issues

When you encounter bugs or errors, you can use the AI assistant like this:

1. **Describe the problem**:
   ```
   @frontend/app/artist/[id]/page.tsx I encountered an error when visiting the artist details page:
   "TypeError: Cannot read properties of undefined (reading 'name')"
   ```

::: tip Let AI Help You
When you encounter errors, you can directly provide the error message and relevant code to the AI assistant:

> I encountered the following error when running the project: [error message]. Here's the relevant code: [code snippet]. Please help me analyze the problem and provide a solution.

AI will analyze the cause of the error and provide fix suggestions, sometimes even providing the fixed code directly.
:::

2. **Provide context**:
   ```
   This error occurs when loading artist data. I used SWR to fetch data, but it seems I tried to access data properties before the data finished loading
   ```

3. **Request solutions**:
   ```
   Please help me analyze the cause of this problem and provide a solution. I want to handle the data loading state elegantly
   ```

4. **Implement the fix**:
   ```
   Your solution looks good. Please help me modify the code to implement this fix
   ```

### Using Chrome DevTools for Debugging

Chrome DevTools is a powerful set of web development tools built into the Chrome browser. It's essential for debugging frontend issues, especially network-related ones. Here's how to effectively use the Network panel:

#### Opening Chrome DevTools Network Panel

1. Open your frontend application (http://localhost:3000) in Chrome browser
2. Press F12 or right-click on the page and select "Inspect" to open DevTools
3. Click on the "Network" tab to access the Network panel

#### Monitoring API Requests

The Network panel shows all network requests made by your application:

1. **Viewing requests**: Each row represents a network request (API calls, images, scripts, etc.)
2. **Request details**: Click on any request to see detailed information in the right panel
3. **Filter requests**: Use the filter bar to show only specific types of requests:
   - Type "fetch" or "xhr" to see only API requests
   - Type the endpoint path to find specific requests

#### Analyzing Request and Response Data

When you click on a request, you can examine:

1. **Headers**: View request and response headers, including authentication tokens
2. **Preview**: See a formatted view of the response data
3. **Response**: View the raw response data
4. **Timing**: Analyze how long different parts of the request took

#### Useful Debugging Techniques

1. **Copy as cURL**: Right-click on a request and select "Copy > Copy as cURL" to get a command you can:
   - Share with backend developers to reproduce issues
   - Run in terminal to test the API directly
   - Use in AI debugging by pasting the cURL command to the AI assistant

2. **Copy as fetch**: Right-click and select "Copy > Copy as fetch" to get JavaScript code that reproduces the request:
   - Paste in the Console tab to test the request
   - Use in your code to implement the same request

3. **Copy response**: Right-click and select "Copy > Copy response" to copy the API response data:
   - Analyze the data structure
   - Compare with what your application is displaying

4. **Copy as JSON**: For JSON responses, in the Preview tab, right-click on the object and select "Copy object" to get the JSON data:
   - Paste into your code for testing
   - Share with team members to analyze data issues

::: tip Let AI Help You
When debugging API issues, you can use Chrome DevTools with AI assistance:

> I copied this API request from Chrome DevTools: [paste cURL command]. The response shows [describe issue], but I expected [expected behavior]. Please help me understand what's wrong.

AI can analyze the request parameters, headers, and response data to identify issues in your API calls.
:::

#### Network Conditions Testing

You can simulate different network conditions to test how your app behaves:

1. Click the "Network conditions" tab (⚙️ icon or in the three-dot menu)
2. Disable cache to always get fresh responses
3. Select different connection speeds (3G, 4G, etc.) to test performance on slower connections

#### Best Practices for Beginners

1. **Always check the Network panel first** when API data isn't displaying correctly
2. **Look for red requests** (4xx or 5xx status codes) which indicate errors
3. **Compare request parameters** with what you expect to be sending
4. **Verify response data** matches what your application is trying to display
5. **Use the Preserve log option** (checkbox in Network panel) to keep requests visible when navigating between pages

These Chrome DevTools techniques will help you quickly identify and fix many common frontend issues without having to add numerous console.log statements to your code.

### Using Swagger UI and ReDoc to Understand APIs

During development, understanding backend APIs is key to frontend development. The AIDA project provides two API documentation tools: Swagger UI and ReDoc, which help you explore and test APIs.

#### Swagger UI Basics

Swagger UI is an interactive API documentation tool that not only displays the structure of APIs but also allows you to directly test API calls.

1. **Accessing Swagger UI**:
   - After starting the project, visit http://localhost:8000/api/docs
   - You'll see a complete list of APIs, grouped by functionality (such as artists, artworks, users, etc.)

2. **Exploring API Endpoints**:
   - Click on any API endpoint (like GET /api/artists) to expand detailed information
   - You can see:
     - Request parameters (path parameters, query parameters, request body, etc.)
     - Response schemas (possible response status codes and data structures)
     - Authentication requirements (if needed)

3. **Testing API Calls**:
   - Click the "Try it out" button
   - Fill in necessary parameters (if any)
   - Click "Execute" to make the request
   - View the actual response, including status code, response headers, and response body

4. **Using Swagger UI for Development**:
   - **Understanding Data Structures**: View JSON schemas for requests and responses to understand data formats
   - **Copying Request URLs**: After executing a request, you can copy the complete curl command or request URL
   - **Debugging Issues**: When the frontend encounters API problems, you can test the same request in Swagger UI

#### ReDoc Documentation

ReDoc provides a clearer, more readable view of API documentation, particularly suitable for learning and reference.

1. **Accessing ReDoc**:
   - After starting the project, visit http://localhost:8000/api/redoc
   - ReDoc provides a three-column view: left navigation, middle API description, right request/response examples

2. **Advantages of ReDoc**:
   - Clearer visual hierarchy
   - Better reading experience for long documentation
   - Response examples and schemas displayed side by side
   - Searchable API documentation

3. **When to Use ReDoc vs Swagger UI**:
   - Use **ReDoc** when you need to:
     - Learn and understand API structure
     - Find detailed parameter descriptions
     - Read lengthy API documentation
   - Use **Swagger UI** when you need to:
     - Test API calls
     - Debug frontend-backend integration issues
     - Explore actual API behavior

#### Relationship Between Frontend and APIs

Understanding how the frontend interacts with backend APIs is key to full-stack development:

1. **Data Flow**:
   - Frontend components call APIs when they need data
   - APIs return JSON data
   - Frontend parses and displays this data

2. **Frontend API Call Example**:
   ```typescript
   // Using fetch API to get a list of artists
   async function fetchArtists() {
     const response = await fetch('http://localhost:8000/api/artists');
     const data = await response.json();
     return data;
   }
   ```

3. **Mapping Between APIs and Frontend Components**:
   - Artist list page → GET /api/artists
   - Artist detail page → GET /api/artists/{id}
   - Create new artist → POST /api/artists
   - Update artist information → PUT /api/artists/{id}

### Understanding HTTP Request Methods

When using APIs, it's important to understand different HTTP request methods (also known as HTTP verbs). Each method has a specific purpose:

#### Common HTTP Methods

1. **GET**: Retrieve a resource
   - Used for reading data, should not modify any data
   - Example: `GET /api/artists` to get all artists
   - Parameters are typically passed in the URL query string: `GET /api/artists?page=1&limit=10`
   - Frontend example:
     ```javascript
     fetch('http://localhost:8000/api/artists?page=1&limit=10')
       .then(response => response.json())
       .then(data => console.log(data));
     ```

2. **POST**: Create a resource
   - Used for creating new data
   - Example: `POST /api/artists` to create a new artist
   - Data is passed in the request body (typically in JSON format)
   - Frontend example:
     ```javascript
     fetch('http://localhost:8000/api/artists', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({
         name: 'Picasso',
         birthYear: 1881,
         nationality: 'Spanish'
       })
     })
     .then(response => response.json())
     .then(data => console.log(data));
     ```

3. **PUT**: Update a resource (complete replacement)
   - Used to completely replace an existing resource
   - Example: `PUT /api/artists/123` to update all information for the artist with ID 123
   - Requires providing the complete data for the resource
   - Frontend example:
     ```javascript
     fetch('http://localhost:8000/api/artists/123', {
       method: 'PUT',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({
         name: 'Pablo Picasso',
         birthYear: 1881,
         deathYear: 1973,
         nationality: 'Spanish',
         movements: ['Cubism', 'Surrealism']
       })
     })
     .then(response => response.json())
     .then(data => console.log(data));
     ```

4. **PATCH**: Partially update a resource
   - Used for partially updating an existing resource
   - Example: `PATCH /api/artists/123` to update only certain fields of an artist
   - Only requires providing the fields to be updated
   - Frontend example:
     ```javascript
     fetch('http://localhost:8000/api/artists/123', {
       method: 'PATCH',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({
         name: 'Pablo Picasso' // Only updating the name
       })
     })
     .then(response => response.json())
     .then(data => console.log(data));
     ```

5. **DELETE**: Delete a resource
   - Used for deleting an existing resource
   - Example: `DELETE /api/artists/123` to delete the artist with ID 123
   - Typically doesn't require a request body
   - Frontend example:
     ```javascript
     fetch('http://localhost:8000/api/artists/123', {
       method: 'DELETE'
     })
     .then(response => {
       if (response.ok) {
         console.log('Artist deleted');
       }
     });
     ```

#### Testing Different HTTP Methods in Swagger UI

Swagger UI allows you to test all these HTTP methods:

1. Find the corresponding API endpoint (e.g., POST /api/artists)
2. Click "Try it out"
3. Fill in the necessary request body or parameters
4. Click "Execute"
5. View the response

#### Observing HTTP Requests in Chrome DevTools

You can observe these HTTP requests in the Network panel of Chrome DevTools:

1. Open Chrome DevTools (F12 or right-click > Inspect)
2. Switch to the Network tab
3. Perform an action in the frontend application (such as clicking a "Create Artist" button)
4. Observe the request sent in the Network panel
5. Click on the request to view detailed information, including request method, URL, headers, body, and response

::: tip Let AI Help You
If you're unsure which HTTP method to use, you can ask the AI assistant:

> I need to implement a feature that allows users to update part of an artist's information. Which HTTP method should I use? How do I implement this request in the frontend?

AI will explain that you should use the PATCH method and provide frontend implementation code examples.
:::

::: warning Common Errors
Using incorrect HTTP methods is a common source of API issues:
1. Using GET method to send a request body (not recommended, some servers may not accept it)
2. Using POST instead of PUT/PATCH for updates (may lead to creating duplicate resources)
3. Using PUT instead of PATCH for partial updates (requires sending complete resource data)
4. Forgetting to set the Content-Type header in POST/PUT/PATCH requests

When API calls fail, first check if you're using the correct HTTP method and data format!
:::

### Refactoring Code

When you need to improve existing code:

1. **Explain refactoring goals**:
   ```
   @backend/routes/artist.py This file is getting larger and harder to maintain. I want to refactor it into smaller modules, following the single responsibility principle
   ```

2. **Request a refactoring plan**:
   ```
   Please help me analyze this file and propose a refactoring plan, including how to split modules and how to organize the code structure
   ```

3. **Implement step by step**:
   ```
   Let's implement the first step: splitting artist CRUD operations into a separate file. Please help me write the new code structure
   ```

### Learning New Technologies

When you need to learn new technologies used in the project:

1. **Request technology overview**:
   ```
   @project_memo.md I noticed the project uses Jotai for state management. Please introduce me to the basic concepts and usage of Jotai
   ```

::: tip Let AI Help You
When you need to learn new technologies or frameworks, you can ask the AI assistant for tutorials and examples:

> I need to learn the Jotai state management library. Please give me a concise tutorial, including basic concepts and examples of using it in a Next.js project.

AI will provide customized tutorials to help you quickly master new technologies.
:::

2. **Request examples**:
   ```
   Please give me a simple example of using Jotai in the AIDA project, including how to create atoms and how to use them in components
   ```

3. **Apply to practical problems**:
   ```
   I now need to implement a feature: users can add artists to favorites. Please help me design how to use Jotai to manage the favorites state
   ```

### Generating Tests

When you need to write tests for your code:

1. **Request test strategy**:
   ```
   @backend/models/artist.py I need to write unit tests for this artist model. Please help me design a test strategy, including which scenarios need to be tested
   ```

2. **Generate test code**:
   ```
   Please help me write unit tests for the create_artist function, including normal cases and various edge cases
   ```

Remember, AI assistants are powerful tools, but they can't replace your thinking and judgment. Always review AI-generated code to ensure it meets project standards and best practices.

## Common Issues and Next Steps

### Frequently Asked Questions

#### What if MongoDB can't connect?

1. Make sure the MongoDB service is running
2. Check if the connection string in the `.env` file is correct
3. Try connecting to the database using MongoDB Compass to confirm the connection information is correct

::: tip Let AI Help You
If you encounter database connection issues, you can seek help from the AI assistant:

> My MongoDB connection failed with the error message: [error message]. My connection string is: [connection string]. Please help me diagnose the issue.

AI will analyze the connection problem and provide troubleshooting steps to help you restore the database connection.
:::

#### How to stop all services?

Press `Ctrl+C` in the terminal window where the services are running.

#### How to update the project code?

Run in the terminal:
```bash
git pull
```

Then reinstall dependencies:
```bash
npm run setup:all
```

#### How to view recent project changes?

Run in the terminal:
```bash
git log --oneline -n 10
```

This will display the 10 most recent commit records.

### Next Steps for Learning

Congratulations on completing the initial setup and running of the AIDA project! Next, you can:

1. Explore the project documentation to learn more technical details
2. Look at the frontend and backend code to understand how they work
3. Try modifying some code to see what changes occur
4. Learn more about Next.js, FastAPI, and MongoDB

::: warning 🎓 Journey from Beginner to Master
Remember that feeling of knowing nothing about programming when you first started? Look at you now! You've successfully set up a complete full-stack project, understood the basic development process, and even know how to use AI assistants to accelerate development. This is just the beginning of your programming journey. As you continue to practice and learn, you'll find that programming isn't actually difficult, especially with AI assistants by your side. In the near future, you might become the technical expert in your team, helping other beginners get started!
:::

::: tip Let AI Help You
When you want to dive deeper into the technologies used in the project, you can ask the AI assistant for a learning path:

> I want to learn Next.js in depth. Please create a learning plan for me, from basics to being able to independently develop features similar to those in the AIDA project.

AI will provide a personalized learning path and resource recommendations based on your needs and background.
:::

Remember, learning programming is a gradual process. Don't be afraid to make mistakes; each error is an opportunity to learn!

If you have any questions, you can refer to the project documentation or seek help from team members. Happy coding! 