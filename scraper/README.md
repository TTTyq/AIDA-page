# AIDA Scraper Tool

A lightweight web scraper tool for AIDA project data collection.

## Features

- Web scraping with configurable settings
- Support for both static HTML and JavaScript-rendered pages
- Data export in various formats
- User-friendly web interface
- RESTful API

## Quick Start

### Using the Management Script

We provide a comprehensive script `run_scraper.bat` that integrates all functionality in a single file:

```
run_scraper.bat           # Start the scraper tool (default)
run_scraper.bat install   # Install dependencies only
run_scraper.bat stop      # Stop running services
run_scraper.bat help      # Show help information
```

This script automatically checks the environment, installs dependencies only when necessary, and checks if services are already running to avoid duplicate starts.

### Manual Setup

If you prefer to start the services manually:

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Accessing the Application

- Frontend UI: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Troubleshooting

### Common Issues

1. **Frontend Dependencies Installation Fails**:
   - Make sure you have Node.js 16+ installed
   - Try clearing npm cache with `npm cache clean --force`
   - Increase Node.js memory limit with `set NODE_OPTIONS=--max_old_space_size=4096`
   - Try running `npm install` manually in the frontend directory

2. **Backend Dependencies Installation Fails**:
   - Make sure you have Python 3.9+ installed
   - Try installing dependencies manually with `pip install -r requirements.txt`

3. **Port Conflicts**: If ports 8000 or 5173 are already in use, modify the port numbers in the startup commands.

4. **Database Errors**: Check that SQLite is properly configured and the database file is accessible.

5. **Startup Script Issues**:
   - If the script doesn't work, try running it from a command prompt
   - Make sure you have administrative privileges if needed

### For More Help

Refer to the documentation in the `docs` directory or contact the AIDA project team.

## License

This project is part of the AIDA platform and follows its licensing terms. 