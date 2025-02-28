import os
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from tqdm import tqdm
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Configuration
# Use the data directory in the project root
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class ArtistScraper:
    def __init__(self):
        self.setup_browser()
        self.artists = []
        
    def setup_browser(self):
        """Set up the Selenium browser with appropriate options."""
        ua = UserAgent()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={ua.random}")
        
        # Use ChromeDriver path from environment variable if available
        chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
        if chrome_driver_path and os.path.exists(chrome_driver_path):
            service = Service(chrome_driver_path)
        else:
            service = Service(ChromeDriverManager().install())
            
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
    
    def scrape_wikiart(self, num_artists=10):
        """Scrape artist data from WikiArt."""
        print(f"Scraping {num_artists} artists from WikiArt...")
        
        # Example: Scrape artists from WikiArt
        url = "https://www.wikiart.org/en/artists-by-century/all"
        self.browser.get(url)
        time.sleep(3)  # Wait for page to load
        
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        artist_links = soup.select(".artists-list-row a")[:num_artists]
        
        for link in tqdm(artist_links, desc="Scraping artists"):
            artist_url = f"https://www.wikiart.org{link['href']}"
            self.browser.get(artist_url)
            time.sleep(random.uniform(1, 3))  # Random delay to avoid detection
            
            artist_soup = BeautifulSoup(self.browser.page_source, "lxml")
            
            try:
                name = artist_soup.select_one("h1").text.strip()
                bio_elem = artist_soup.select_one(".wiki-layout-artist-info p")
                bio = bio_elem.text.strip() if bio_elem else ""
                
                # Extract years (birth-death)
                years_elem = artist_soup.select_one(".wiki-layout-artist-info .wiki-layout-artist-years")
                years = years_elem.text.strip() if years_elem else ""
                
                birth_year = None
                death_year = None
                if years:
                    years_parts = years.replace("(", "").replace(")", "").split("-")
                    if len(years_parts) > 0:
                        try:
                            birth_year = int(years_parts[0].strip())
                            if len(years_parts) > 1 and years_parts[1].strip():
                                death_year = int(years_parts[1].strip())
                        except ValueError:
                            pass
                
                # Extract nationality and art movement
                info_items = artist_soup.select(".wiki-layout-artist-info .wiki-layout-artist-item")
                nationality = ""
                art_movement = ""
                
                for item in info_items:
                    label = item.select_one(".wiki-layout-artist-item-label")
                    value = item.select_one(".wiki-layout-artist-item-value")
                    
                    if label and value:
                        label_text = label.text.strip().lower()
                        value_text = value.text.strip()
                        
                        if "nationality" in label_text:
                            nationality = value_text
                        elif "movement" in label_text:
                            art_movement = value_text
                
                # Create artist object
                artist = {
                    "name": name,
                    "bio": bio,
                    "birth_year": birth_year,
                    "death_year": death_year,
                    "nationality": nationality,
                    "art_movement": art_movement,
                    "source_url": artist_url
                }
                
                self.artists.append(artist)
                print(f"Scraped: {name}")
                
            except Exception as e:
                print(f"Error scraping artist: {e}")
    
    def save_data(self):
        """Save the scraped data to JSON and CSV files."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save to JSON
        json_path = os.path.join(OUTPUT_DIR, f"artists_{timestamp}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.artists, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        csv_path = os.path.join(OUTPUT_DIR, f"artists_{timestamp}.csv")
        df = pd.DataFrame(self.artists)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        
        # Also save to a standard filename for easy access
        standard_csv_path = os.path.join(OUTPUT_DIR, "artists.csv")
        df.to_csv(standard_csv_path, index=False, encoding="utf-8")
        
        print(f"Saved {len(self.artists)} artists to:")
        print(f"  - {json_path}")
        print(f"  - {csv_path}")
        print(f"  - {standard_csv_path}")
    
    def close(self):
        """Close the browser."""
        if hasattr(self, "browser"):
            self.browser.quit()

def main():
    scraper = ArtistScraper()
    try:
        # Get number of artists from environment variable or use default
        num_artists = int(os.getenv("SCRAPER_NUM_ARTISTS", "20"))
        scraper.scrape_wikiart(num_artists=num_artists)
        scraper.save_data()
    finally:
        scraper.close()

if __name__ == "__main__":
    main() 