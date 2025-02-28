# Scraper

::: info
This document introduces the AIDA project's scraper system, used for collecting artist and artwork data.
:::

## Technology Stack

The AIDA scraper system uses the following technologies:

- **Python**: Programming language
- **BeautifulSoup**: HTML parsing library
- **Selenium**: Web automation tool
- **Requests**: HTTP request library
- **Pandas**: Data processing library

## Directory Structure

The scraper code is located in the `/scraper` folder in the project root directory, with the following main structure:

```
scraper/
├── main.py              # Scraper entry point
├── config/              # Configuration files
├── spiders/             # Scraper implementations for various websites
├── processors/          # Data processors
├── utils/               # Utility functions
└── tests/               # Test code
```

## Supported Data Sources

The scraper system currently supports collecting artist information from the following data sources:

1. **WikiArt**: Collects basic artist information and works
2. **MoMA**: Museum of Modern Art artist data
3. **Artsy**: Contemporary art platform data
4. **National Galleries**: Artist data from national galleries of various countries

## Data Collection Process

The scraper system's data collection process is as follows:

1. **Initialization**: Set up scraper parameters and target website
2. **Page Fetching**: Use Requests or Selenium to get web page content
3. **Data Parsing**: Use BeautifulSoup to parse HTML and extract data
4. **Data Cleaning**: Process and normalize the extracted data
5. **Data Storage**: Save data to CSV files or write directly to the database
6. **Deduplication and Merging**: Handle duplicate data from different sources

## Usage Guide

### Setting Up the Development Environment

1. Ensure Python 3.9+ is installed
2. Install dependencies:
   ```bash
   cd scraper
   pip install -r requirements.txt
   ```
3. If using Selenium, install the appropriate browser driver

### Running the Scraper

Basic usage:

```bash
cd scraper
python main.py --source wikiart --limit 100
```

Parameter description:
- `--source`: Data source name (wikiart, moma, artsy, etc.)
- `--limit`: Limit the number of artists to collect
- `--output`: Output file path (default is `../data/artists.csv`)

### Data Import

After collecting data, you can use the following command to import the data into MongoDB:

```bash
cd scraper
python import_to_db.py --file ../data/artists.csv
```

Or use the one-click import command from the project root directory:

```bash
npm run import:data
```

## Best Practices

1. **Respect Website Rules**: Honor robots.txt and website terms of use
2. **Control Request Rate**: Add appropriate delays to avoid putting pressure on target websites
3. **Error Handling**: Properly handle network errors and parsing exceptions
4. **Data Validation**: Ensure collected data conforms to expected formats
5. **Incremental Updates**: Support updating only new data to avoid duplicate collection

## Development Plans

Future development plans for the scraper system include:

- Adding more art data sources
- Implementing distributed scraper architecture
- Adding automated scheduling functionality
- Improving data cleaning and matching algorithms
- Implementing automatic classification of art styles and movements

::: warning Note
The scraper documentation is still being refined. More detailed content will be added in future updates.
::: 