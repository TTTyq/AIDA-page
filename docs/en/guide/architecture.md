# Architecture

::: info
This document provides an overview of the AIDA project's overall architecture design and the relationships between its components.
:::

## System Architecture Overview

AIDA uses a modern full-stack architecture, consisting of the following main components:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │ ←→ │ Backend API  │ ←→ │ MongoDB DB   │
└─────────────┘     └─────────────┘     └─────────────┘
       ↑                   ↑                   ↑
       │                   │                   │
       └───────────┬───────┴───────────┬──────┘
                   │                   │
             ┌─────────────┐    ┌─────────────┐
             │   Scraper   │    │     Docs    │
             └─────────────┘    └─────────────┘
```

## Technology Stack

AIDA uses the following technology stack:

- **Frontend**: Next.js + React + Jotai + MUI + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: MongoDB
- **Scraper**: Python + BeautifulSoup + Selenium
- **Documentation**: VitePress (Vue.js)

## Component Interactions

### Data Flow

1. The **Scraper System** collects artist information and stores it in the MongoDB database
2. The **Backend API** reads data from the database and provides RESTful API interfaces
3. The **Frontend Application** fetches data via the API and presents it to users
4. User actions in the frontend are passed to the backend via the API, and the backend updates the database

### File Structure

The project uses a monorepo structure with the following main directories:

- `/frontend`: Frontend application code
- `/backend`: Backend API code
- `/scraper`: Scraper system code
- `/docs`: Project documentation
- `/data`: Data files
- `/scripts`: Utility scripts
- `/gptmemory`: AI assistant shared memory

## Design Principles

AIDA follows these design principles:

1. **Modularity**: Components are loosely coupled for independent development and testing
2. **Scalability**: Architecture designed with future expansion in mind
3. **Developer Experience**: One-click development environment setup and startup
4. **Documentation-Driven**: Comprehensive documentation to support development and maintenance

## Future Plans

- Add user authentication and authorization system
- Implement AI artist interaction features
- Optimize data models and query performance
- Enhance the scraper system's data collection capabilities

::: warning Note
The architecture documentation is still being refined. More detailed architecture diagrams and component descriptions will be added in future updates.
::: 