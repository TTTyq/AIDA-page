# AIAD Scraper

This component provides web scraping tools for collecting artist data from various online sources for the AI Artist Database (AIAD) project.

## Technology Stack

- **BeautifulSoup4**: HTML parsing library
- **Selenium**: Browser automation for dynamic content
- **Requests**: HTTP library for static content
- **Pandas**: Data manipulation and analysis
- **MongoDB**: Database for storing scraped data

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Chrome browser (required for Selenium)

4. Create a `.env` file with the following variables:
   ```
   MONGODB_URI=mongodb://localhost:27017/aiad
   ```

## Usage

Run the main scraper:

```bash
python main.py
```

This will:
1. Scrape artist data from WikiArt
2. Save the data to JSON and CSV files in the `data` directory
3. (When configured) Store the data in MongoDB

## Available Scrapers

- **WikiArt Scraper**: Collects artist information from WikiArt
- More scrapers will be added for other art websites and databases

## Data Format

The scraped artist data follows this structure:

```json
{
  "name": "Artist Name",
  "bio": "Artist biography text",
  "birth_year": 1900,
  "death_year": 1980,
  "nationality": "Country",
  "art_movement": "Art Movement",
  "source_url": "https://source-website.com/artist"
}
```

## Legal Considerations

Please ensure you comply with the terms of service of any website you scrape. This tool is intended for educational and research purposes only. Always respect rate limits and robots.txt directives. 