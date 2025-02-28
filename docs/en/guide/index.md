# Quick Start

::: tip
This guide will help you quickly set up and run the AIDA project. If you're a complete beginner, check out the [Beginner-Friendly Guide](./beginners.md) for more detailed instructions.
:::

## Prerequisites

Ensure your system has the following software installed:

- Git
- Node.js (v16+) and npm
- Python (v3.9+)
- MongoDB

## Clone the Project

```bash
git clone https://github.com/thevertexlab/aida.git
cd aida
```

## Install Dependencies

Install all dependencies with a single command:

```bash
npm run setup:all
```

## Configure Environment

1. Copy the `.env.example` file and rename it to `.env`
2. Modify the configuration as needed

## Import Test Data

```bash
npm run setup:mongodb
```

## Start the Project

```bash
npm run dev
```

After starting, you can access:

- Frontend application: http://localhost:3000
- Backend service: http://localhost:8000
- Project documentation: http://localhost:5173
- API documentation: http://localhost:8000/api/docs

## Next Steps

- Check out the [Architecture](./architecture.md) to understand the project structure
- Learn about the [Backend](./backend.md), [Frontend](./frontend.md), and [Scraper](./scraper.md) components
- Refer to the [Beginner-Friendly Guide](./beginners.md) for more detailed guidance 