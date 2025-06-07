# AIDA Scraper Tool

A lightweight web scraper tool for AIDA project data collection, with specialized support for Artsy.net.

## Features

- Web scraping with configurable settings
- Support for both static HTML and JavaScript-rendered pages
- **Specialized Artsy.net scraper** for artists and artworks data
- Data export in various formats (JSON, CSV)
- User-friendly web interface
- RESTful API with background task support

## Quick Start

### Using the Management Script

We provide a comprehensive script `run_scraper.bat` that integrates all functionality in a single file:

```
run_scraper.bat           # Start the scraper tool (default)
run_scraper.bat install   # Install dependencies only
run_scraper.bat stop      # Stop running services
run_scraper.bat help      # Show help information
```

### Using the Artsy Scraper

For Artsy.net specifically, use the dedicated Artsy scraper script:

```
run_artsy_scraper.bat     # Interactive Artsy scraper tool
```

This script provides options to:
1. Run example scraping (recommended for first time)
2. Start scraper API server
3. Test connection to Artsy.net

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

## Artsy Scraper Usage

### 1. Using the Python API

```python
import asyncio
from app.scrapers.artsy_scraper import ArtsyScraper

async def scrape_artists():
    # Configuration
    config = {
        'type': 'artists',           # 'artists', 'artworks', or 'both'
        'max_artists': 50,           # Number of artists to scrape
        'max_artworks_per_artist': 10, # Artworks per artist
        'delay': 2.0                 # Delay between requests (seconds)
    }
    
    # Create scraper
    scraper = ArtsyScraper(config)
    
    # Test connection
    if await scraper.test_connection():
        print("Connected to Artsy.net")
        
        # Start scraping
        results = await scraper.scrape()
        
        # Get specific data
        artists = scraper.get_artists_data()
        artworks = scraper.get_artworks_data()
        
        # Save to file
        scraper.save_to_json("artsy_data.json")
        
        return results

# Run the scraper
asyncio.run(scrape_artists())
```

### 2. Using the REST API

Start the API server:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### API Endpoints:

- **POST** `/api/artsy/start` - Start scraping task
- **GET** `/api/artsy/status/{task_id}` - Get task status
- **GET** `/api/artsy/results/{task_id}` - Get scraping results
- **GET** `/api/artsy/tasks` - List all tasks
- **POST** `/api/artsy/test-connection` - Test Artsy connection
- **GET** `/api/artsy/sample` - Get sample data

#### Example API Usage:

```bash
# Start scraping
curl -X POST "http://localhost:8000/api/artsy/start" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "artists",
    "max_artists": 20,
    "delay": 1.5
  }'

# Check status
curl "http://localhost:8000/api/artsy/status/{task_id}"

# Get results
curl "http://localhost:8000/api/artsy/results/{task_id}"
```

### 3. Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | string | "artists" | Scraping type: "artists", "artworks", or "both" |
| `max_artists` | int | 50 | Maximum number of artists to scrape |
| `max_artworks` | int | 100 | Maximum number of artworks to scrape |
| `max_artworks_per_artist` | int | 10 | Artworks to collect per artist |
| `delay` | float | 2.0 | Delay between requests (seconds) |
| `save_to_file` | bool | true | Whether to save results to JSON file |

### 4. Data Structure

#### Artist Data:
```json
{
  "type": "artist",
  "name": "Leonardo da Vinci",
  "dates": "1452-1519",
  "nationality": "Italian",
  "bio": "Renaissance polymath...",
  "image_url": "https://...",
  "artworks_count": "15 works",
  "url": "https://www.artsy.net/artist/leonardo-da-vinci",
  "source": "artsy.net"
}
```

#### Artwork Data:
```json
{
  "type": "artwork",
  "title": "Mona Lisa",
  "artist": "Leonardo da Vinci",
  "date": "1503-1519",
  "medium": "Oil on poplar panel",
  "dimensions": "77 cm × 53 cm",
  "image_url": "https://...",
  "url": "https://www.artsy.net/artwork/leonardo-da-vinci-mona-lisa",
  "source": "artsy.net"
}
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

3. **Artsy Connection Issues**:
   - Check your internet connection
   - Verify that Artsy.net is accessible from your location
   - Try increasing the delay between requests if you get rate limited

4. **Port Conflicts**: If ports 8000 or 5173 are already in use, modify the port numbers in the startup commands.

5. **Database Errors**: Check that SQLite is properly configured and the database file is accessible.

6. **Startup Script Issues**:
   - If the script doesn't work, try running it from a command prompt
   - Make sure you have administrative privileges if needed

### Rate Limiting and Best Practices

- The scraper includes built-in delays between requests to respect Artsy's servers
- Default delay is 2 seconds, but you can adjust it based on your needs
- For large scraping jobs, consider running during off-peak hours
- Always test with small amounts of data first

### For More Help

Refer to the documentation in the `docs` directory or contact the AIDA project team.

## License

This project is part of the AIDA platform and follows its licensing terms. 