import os
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from tqdm import tqdm
from dotenv import load_dotenv
import pandas as pd
import logging
import sys
import re
import pickle
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"artsy_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("artsy_scraper")

# Configuration
# Use the data directory in the project root
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "artsy")
CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, "checkpoints")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

class ArtsyScraper:
    def __init__(self):
        self.setup_browser()
        self.artists = []
        self.artworks = []
        self.base_url = "https://www.artsy.net"
        self.artists_url = f"{self.base_url}/artists"
        self.artists_scraped = 0
        self.artworks_scraped = 0
        self.max_retries = 3
        self.checkpoint_interval = 10  # Save data every 10 artists
        self.scroll_pause_time = 2.5    # Time to pause between scrolls
        self.max_scrolls = 1000         # Maximum number of scrolls to perform
        self.important_artists_categories = [
            "top-selling", "trending", "blue-chip", "critically-acclaimed",
            "established", "famous", "influential", "master", "pioneering"
        ]
        self.load_checkpoint()
        
    def load_checkpoint(self):
        """Load checkpoint if exists."""
        checkpoint_file = os.path.join(CHECKPOINT_DIR, "scraper_checkpoint.pkl")
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'rb') as f:
                    checkpoint = pickle.load(f)
                    self.artists = checkpoint.get('artists', [])
                    self.artworks = checkpoint.get('artworks', [])
                    self.artists_scraped = checkpoint.get('artists_scraped', 0)
                    self.artworks_scraped = checkpoint.get('artworks_scraped', 0)
                    logger.info(f"Loaded checkpoint: {self.artists_scraped} artists, {self.artworks_scraped} artworks")
            except Exception as e:
                logger.error(f"Error loading checkpoint: {e}")
                
    def save_checkpoint(self):
        """Save checkpoint."""
        checkpoint_file = os.path.join(CHECKPOINT_DIR, "scraper_checkpoint.pkl")
        try:
            checkpoint = {
                'artists': self.artists,
                'artworks': self.artworks,
                'artists_scraped': self.artists_scraped,
                'artworks_scraped': self.artworks_scraped
            }
            with open(checkpoint_file, 'wb') as f:
                pickle.dump(checkpoint, f)
            logger.info(f"Saved checkpoint: {self.artists_scraped} artists, {self.artworks_scraped} artworks")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")
        
    def setup_browser(self):
        """Set up the Selenium browser with appropriate options."""
        ua = UserAgent()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={ua.random}")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        
        # Use ChromeDriver path from environment variable if available
        chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
        if chrome_driver_path and os.path.exists(chrome_driver_path):
            service = Service(chrome_driver_path)
        else:
            service = Service(ChromeDriverManager().install())
            
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        
    def _wait_for_element(self, by, selector, timeout=10):
        """Wait for an element to appear on the page."""
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timed out waiting for element: {selector}")
            return None
            
    def _random_delay(self, min_sec=1.5, max_sec=4.5):
        """Random delay to avoid detection."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        
    def scrape_artists_by_category(self, category, max_artists=1000, max_artworks=10):
        """Scrape artists by a specific category like 'top-selling', 'blue-chip', etc."""
        logger.info(f"Scraping artists from category: {category}, max: {max_artists}")
        category_url = f"{self.base_url}/collections/artists/{category}"
        
        try:
            self.browser.get(category_url)
            self._random_delay(3, 5)
            
            # Accept cookies if the dialog appears
            self._accept_cookies()
            
            # Scroll to load more artists
            artist_urls = self._scroll_and_collect_artist_urls(max_artists)
            
            logger.info(f"Found {len(artist_urls)} artist URLs in category {category}. Starting to scrape individual artists...")
            
            # Process each artist
            for i, artist_url in enumerate(tqdm(artist_urls, desc=f"Scraping {category} artists")):
                full_url = f"{self.base_url}{artist_url}" if not artist_url.startswith("http") else artist_url
                self.scrape_artist_details(full_url, max_artworks=max_artworks, category=category)
                self.artists_scraped += 1
                
                # Save data periodically
                if self.artists_scraped % self.checkpoint_interval == 0:
                    self.save_data()
                    self.save_checkpoint()
                
        except Exception as e:
            logger.error(f"Error scraping artists from category {category}: {str(e)}", exc_info=True)
            
    def scrape_multiple_categories(self, max_artists_per_category=200, max_artworks=10):
        """Scrape artists from multiple categories based on importance."""
        for category in self.important_artists_categories:
            logger.info(f"Starting to scrape category: {category}")
            self.scrape_artists_by_category(category, max_artists=max_artists_per_category, max_artworks=max_artworks)
            # Short break between categories
            self._random_delay(10, 20)
        
    def scrape_artists_list(self, max_artists=1000, max_artworks=10):
        """Scrape the list of artists from Artsy's artists page."""
        logger.info(f"Starting to scrape up to {max_artists} artists from Artsy main list")
        
        try:
            # Navigate to the artists page
            self.browser.get(self.artists_url)
            self._random_delay(3, 5)
            
            # Accept cookies if the dialog appears
            self._accept_cookies()
            
            # Get artist URLs by scrolling
            artist_urls = self._scroll_and_collect_artist_urls(max_artists)
            
            logger.info(f"Found {len(artist_urls)} artist URLs. Starting to scrape individual artists...")
            
            # Process each artist
            for artist_url in tqdm(artist_urls, desc="Scraping artists"):
                full_url = f"{self.base_url}{artist_url}" if not artist_url.startswith("http") else artist_url
                self.scrape_artist_details(full_url, max_artworks=max_artworks)
                self.artists_scraped += 1
                
                # Save data periodically
                if self.artists_scraped % self.checkpoint_interval == 0:
                    self.save_data()
                    self.save_checkpoint()
                    
        except Exception as e:
            logger.error(f"Error during artist list scraping: {str(e)}", exc_info=True)
            
        finally:
            # Save final data
            self.save_data()
            self.save_checkpoint()
    
    def _accept_cookies(self):
        """Accept cookies if the dialog appears."""
        try:
            cookie_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Cookie')]")
            cookie_button.click()
            self._random_delay()
        except NoSuchElementException:
            logger.info("No cookie consent dialog found.")
            
    def _scroll_and_collect_artist_urls(self, max_artists):
        """Scroll down the page and collect artist URLs."""
        artist_urls = []
        scroll_count = 0
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        
        while len(artist_urls) < max_artists and scroll_count < self.max_scrolls:
            # Scroll down
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for page to load
            self._random_delay(self.scroll_pause_time, self.scroll_pause_time + 1)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            
            # Extract artist links from the current page
            try:
                soup = BeautifulSoup(self.browser.page_source, "lxml")
                artist_links = soup.select("a[href*='/artist/']")
                
                # Add unique artist URLs to our list
                for link in artist_links:
                    href = link.get('href')
                    if href and '/artist/' in href and href not in artist_urls:
                        artist_urls.append(href)
                
                if len(artist_urls) >= max_artists:
                    break
                
                # If heights are the same, we've reached the end of the page
                if new_height == last_height:
                    # Try one more time to make sure it's not a temporary issue
                    self._random_delay(2, 3)
                    new_height = self.browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        logger.info("Reached the end of the page")
                        break
                        
                last_height = new_height
                scroll_count += 1
                if scroll_count % 5 == 0:
                    logger.info(f"Scroll {scroll_count}/{self.max_scrolls}: Found {len(artist_urls)} artist URLs so far")
            
            except (StaleElementReferenceException, Exception) as e:
                logger.error(f"Error during scrolling: {str(e)}")
                scroll_count += 1
                continue
        
        # Limit to max_artists
        result = artist_urls[:max_artists]
        logger.info(f"Found {len(result)} artist URLs after {scroll_count} scrolls")
        return result
                
    def scrape_artist_details(self, artist_url, max_artworks=10, category=None):
        """Scrape detailed information about an artist."""
        logger.info(f"Scraping artist details from: {artist_url}")
        
        for attempt in range(self.max_retries):
            try:
                self.browser.get(artist_url)
                self._random_delay(2, 4)
                
                # Parse the page
                soup = BeautifulSoup(self.browser.page_source, "lxml")
                
                # Get artist name
                name_elem = soup.select_one("h1")
                name = name_elem.text.strip() if name_elem else "Unknown Artist"
                
                # Get bio/about text
                bio_elem = soup.select_one("div[data-test='biography']") or soup.select_one("[data-test='artist-bio']")
                bio = bio_elem.text.strip() if bio_elem else ""
                
                # Get birth/death years
                years_elem = soup.select_one("div:contains('born') span") or soup.select_one("div:contains('Born')") 
                years_text = years_elem.text.strip() if years_elem else ""
                
                birth_year = None
                death_year = None
                
                if years_text:
                    # Try to extract years using regex or string manipulation
                    import re
                    years_match = re.search(r'(\d{4})\s*-?\s*(\d{4})?', years_text)
                    if years_match:
                        birth_year = int(years_match.group(1)) if years_match.group(1) else None
                        death_year = int(years_match.group(2)) if years_match.group(2) else None
                
                # Get nationality
                nationality_elem = soup.select_one("div:contains('Nationality') span") or soup.select_one("div:contains('nationality')")
                nationality = nationality_elem.text.strip() if nationality_elem else ""
                
                # Get art movement
                movement_elem = soup.select_one("div:contains('Movement') span") or soup.select_one("a[href*='gene']")
                art_movement = movement_elem.text.strip() if movement_elem else ""
                
                # Get additional metrics for importance
                followers_count = 0
                works_count = 0
                exhibitions_count = 0
                
                # Try to find follower count
                followers_elem = soup.select_one("span:contains('follower')")
                if followers_elem:
                    followers_text = followers_elem.text
                    followers_match = re.search(r'(\d+)', followers_text)
                    if followers_match:
                        followers_count = int(followers_match.group(1))
                
                # Try to find exhibitions count
                exhibitions_elem = soup.select_one("div:contains('exhibition')")
                if exhibitions_elem:
                    exhibitions_text = exhibitions_elem.text
                    exhibitions_match = re.search(r'(\d+)', exhibitions_text)
                    if exhibitions_match:
                        exhibitions_count = int(exhibitions_match.group(1))
                
                # Create artist object
                artist = {
                    "name": name,
                    "bio": bio,
                    "birth_year": birth_year,
                    "death_year": death_year,
                    "nationality": nationality,
                    "art_movement": art_movement,
                    "followers_count": followers_count,
                    "exhibitions_count": exhibitions_count,
                    "category": category,
                    "source_url": artist_url
                }
                
                # Append to the list
                self.artists.append(artist)
                logger.info(f"Successfully scraped artist: {name}")
                
                # Try to find artwork links
                self._scrape_artist_artworks(artist_url, name, max_artworks)
                
                # Successful scrape, break the retry loop
                break
                
            except Exception as e:
                logger.error(f"Error scraping artist details (attempt {attempt+1}/{self.max_retries}): {str(e)}", exc_info=True)
                self._random_delay(5, 10)  # Longer delay between retries
                
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to scrape artist after {self.max_retries} attempts")
    
    def _scrape_artist_artworks(self, artist_url, artist_name, max_artworks=10):
        """Scrape artwork information for an artist."""
        try:
            # Navigate to the artist's works page
            works_url = f"{artist_url}/works-for-sale"
            self.browser.get(works_url)
            self._random_delay(2, 4)
            
            # Find artwork links
            soup = BeautifulSoup(self.browser.page_source, "lxml")
            artwork_links = soup.select("a[href*='/artwork/']")[:max_artworks]
            
            logger.info(f"Found {len(artwork_links)} artworks for {artist_name}")
            
            # Process each artwork
            for link in artwork_links:
                href = link.get('href')
                if href:
                    artwork_url = f"{self.base_url}{href}" if not href.startswith("http") else href
                    self._scrape_artwork_details(artwork_url, artist_name)
                    self.artworks_scraped += 1
                    self._random_delay()
                    
        except Exception as e:
            logger.error(f"Error scraping artworks for {artist_name}: {str(e)}", exc_info=True)
    
    def _scrape_artwork_details(self, artwork_url, artist_name):
        """Scrape details about an artwork."""
        try:
            self.browser.get(artwork_url)
            self._random_delay(2, 3)
            
            soup = BeautifulSoup(self.browser.page_source, "lxml")
            
            # Get artwork title
            title_elem = soup.select_one("h1")
            title = title_elem.text.strip() if title_elem else "Untitled"
            
            # Get artwork date
            date_elem = soup.select_one("div:contains('Date') span") or soup.select_one("div:contains('Created')") 
            date = date_elem.text.strip() if date_elem else ""
            
            # Get medium
            medium_elem = soup.select_one("div:contains('Medium') span") or soup.select_one("div:contains('materials')")
            medium = medium_elem.text.strip() if medium_elem else ""
            
            # Get dimensions
            dimensions_elem = soup.select_one("div:contains('Dimensions') span") or soup.select_one("div:contains('Size')")
            dimensions = dimensions_elem.text.strip() if dimensions_elem else ""
            
            # 修改图片选择器，更精确地选择艺术品图片并获取更高分辨率
            # 先尝试找主图片，通常是最大的或主要展示的图片
            image_url = ""
            # 尝试多种选择器找到正确的图片
            img_selectors = [
                "div[role='img'] img", # 角色为img的div中的img
                "img.Image__StyledImage-sc-o114fg-0", # 主要的图片类
                "img[data-reactid*='image']", # 带特定data属性的img
                "img[sizes*='100vw']", # 大尺寸图片
                "img[src*='d32dm0rphc51dk'][src*='/normalized/']", # 高清artsy CDN图片
                "img[src*='artsy.net'][src*='/larger/']", # 大尺寸艺术品图片
                "img[src*='artsy.net'][src*='/large/']", # 大尺寸艺术品图片
                "img[src*='/larger/']", # 包含larger路径的图片
                "img[src*='/large/']", # 包含large路径的图片
                "img[alt*='Artwork']", # 带Artwork alt的图片
            ]
            
            for selector in img_selectors:
                img_elem = soup.select_one(selector)
                if img_elem and img_elem.get('src'):
                    image_url = img_elem.get('src')
                    # 尝试获取更高分辨率版本的图片URL
                    if "/medium/" in image_url:
                        image_url = image_url.replace("/medium/", "/larger/")
                    elif "/small/" in image_url:
                        image_url = image_url.replace("/small/", "/larger/")
                    elif "/large/" in image_url:
                        image_url = image_url.replace("/large/", "/larger/")
                    elif "/thumbnail/" in image_url:
                        image_url = image_url.replace("/thumbnail/", "/larger/")
                    # 找到了合适的图片，跳出循环
                    break
            
            # 如果上面的选择器都失败了，回退到最基本的图片选择
            if not image_url:
                # 查找页面源码中的图片URL
                all_scripts = soup.select("script")
                for script in all_scripts:
                    script_text = script.string
                    if script_text and ('"imageUrl"' in script_text or '"image_url"' in script_text or 'imageUrl' in script_text):
                        # 使用正则表达式查找图片URL
                        url_matches = re.findall(r'https?://[^"\'\s]+\.(jpg|jpeg|png|webp)', script_text)
                        for match in url_matches:
                            candidate_url = match[0]
                            if 'artsy' in candidate_url or 'd32dm0rphc51dk' in candidate_url:
                                # 选择更高分辨率的版本
                                if "/medium/" in candidate_url:
                                    candidate_url = candidate_url.replace("/medium/", "/larger/")
                                elif "/small/" in candidate_url:
                                    candidate_url = candidate_url.replace("/small/", "/larger/")
                                elif "/large/" in candidate_url:
                                    candidate_url = candidate_url.replace("/large/", "/larger/")
                                elif "/thumbnail/" in candidate_url:
                                    candidate_url = candidate_url.replace("/thumbnail/", "/larger/")
                                image_url = candidate_url
                                break
                
                # 如果上述方法都失败，尝试所有图片，排除图标和logo
                if not image_url:
                    all_images = soup.select("img")
                    largest_img = {"area": 0, "url": ""}
                    
                    for img in all_images:
                        src = img.get('src', '')
                        if src and ('artsy' in src or 'd32dm0rphc51dk' in src) and not ('logo' in src.lower() or 'icon' in src.lower()):
                            # 尝试提取图片尺寸，选择最大的图片
                            width = img.get('width')
                            height = img.get('height')
                            
                            if width and height:
                                try:
                                    width = int(width)
                                    height = int(height)
                                    area = width * height
                                    
                                    if area > largest_img["area"]:
                                        largest_img = {"area": area, "url": src}
                                except (ValueError, TypeError):
                                    pass
                            
                            if not width or not height:
                                # 如果没有尺寸信息，则查看其他属性判断是否是主图
                                if img.get('alt') and ('artwork' in img.get('alt').lower() or artist_name.lower() in img.get('alt').lower()):
                                    largest_img = {"area": 999999, "url": src}  # 给予高优先级
                    
                    if largest_img["url"]:
                        image_url = largest_img["url"]
                        # 尝试获取更高分辨率版本
                        if "/medium/" in image_url:
                            image_url = image_url.replace("/medium/", "/larger/")
                        elif "/small/" in image_url:
                            image_url = image_url.replace("/small/", "/larger/")
                        elif "/large/" in image_url:
                            image_url = image_url.replace("/large/", "/larger/")
                        elif "/thumbnail/" in image_url:
                            image_url = image_url.replace("/thumbnail/", "/larger/")
            
            # Get price if available
            price = ""
            price_elem = soup.select_one("div:contains('Price') span") or soup.select_one("span:contains('$')")
            if price_elem:
                price = price_elem.text.strip()
            
            # Create artwork object
            artwork = {
                "title": title,
                "artist_name": artist_name,
                "date": date,
                "medium": medium,
                "dimensions": dimensions,
                "price": price,
                "image_url": image_url,
                "source_url": artwork_url
            }
            
            # Append to the list
            self.artworks.append(artwork)
            logger.info(f"Successfully scraped artwork: {title} by {artist_name}")
            
            # Download image if available
            if image_url:
                self._download_image(image_url, artist_name, title)
                
        except Exception as e:
            logger.error(f"Error scraping artwork details: {str(e)}", exc_info=True)
    
    def _download_image(self, image_url, artist_name, artwork_title):
        """Download artwork image."""
        try:
            # Create directory for artist
            artist_dir = os.path.join(OUTPUT_DIR, "images", self._clean_filename(artist_name))
            os.makedirs(artist_dir, exist_ok=True)
            
            # 创建更独特的文件名，包含作品标题和URL的一部分哈希
            url_hash = str(hash(image_url))[-8:] # 使用URL的部分哈希避免重复
            artwork_title_clean = self._clean_filename(artwork_title)
            filename = f"{artwork_title_clean}_{url_hash}.jpg"
            filepath = os.path.join(artist_dir, filename)
            
            # Check if file already exists with same hash part
            existing_files = [f for f in os.listdir(artist_dir) 
                             if f.endswith(f"_{url_hash}.jpg")]
            
            if existing_files:
                logger.info(f"Image with same URL hash already exists: {existing_files[0]}")
                return
            
            # 添加更多header模拟真实浏览器请求
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.artsy.net/",
                "sec-ch-ua": '"Google Chrome";v="91", " Not;A Brand";v="99"',
                "sec-ch-ua-mobile": "?0"
            }
            
            # Download image with headers
            response = requests.get(image_url, stream=True, timeout=30, headers=headers)
            if response.status_code == 200:
                # 检查是否是图片内容
                content_type = response.headers.get('Content-Type', '')
                if not content_type.startswith('image/'):
                    logger.warning(f"Downloaded content is not an image: {content_type}, URL: {image_url}")
                    return
                    
                # 保存图片
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                logger.info(f"Downloaded image: {filepath}")
                
                # 验证文件大小，如果太小可能不是真正的图片
                file_size = os.path.getsize(filepath)
                if file_size < 5000:  # 小于5KB的图片可能有问题
                    logger.warning(f"Downloaded image is suspiciously small ({file_size} bytes): {filepath}")
            else:
                logger.warning(f"Failed to download image: {image_url} - Status code: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}", exc_info=True)
    
    def _clean_filename(self, name):
        """Clean a string to be used as a filename."""
        return "".join(c if c.isalnum() or c in [' ', '.', '-'] else '_' for c in name).strip()
    
    def save_data(self):
        """Save the scraped data to JSON and CSV files."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save artists data
        if self.artists:
            # Save to JSON
            json_path = os.path.join(OUTPUT_DIR, f"artsy_artists_{timestamp}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.artists, f, ensure_ascii=False, indent=2)
            
            # Save to CSV
            csv_path = os.path.join(OUTPUT_DIR, f"artsy_artists_{timestamp}.csv")
            df = pd.DataFrame(self.artists)
            df.to_csv(csv_path, index=False, encoding="utf-8")
            
            # Standard filename
            standard_csv_path = os.path.join(OUTPUT_DIR, "artsy_artists.csv")
            df.to_csv(standard_csv_path, index=False, encoding="utf-8")
            
            # 为每位艺术家创建单独的信息文档
            self._create_individual_artist_docs()
            
            logger.info(f"Saved {len(self.artists)} artists to:")
            logger.info(f"  - {json_path}")
            logger.info(f"  - {csv_path}")
            logger.info(f"  - {standard_csv_path}")
        
        # Save artworks data
        if self.artworks:
            # Save to JSON
            json_path = os.path.join(OUTPUT_DIR, f"artsy_artworks_{timestamp}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.artworks, f, ensure_ascii=False, indent=2)
            
            # Save to CSV
            csv_path = os.path.join(OUTPUT_DIR, f"artsy_artworks_{timestamp}.csv")
            df = pd.DataFrame(self.artworks)
            df.to_csv(csv_path, index=False, encoding="utf-8")
            
            # Standard filename
            standard_csv_path = os.path.join(OUTPUT_DIR, "artsy_artworks.csv")
            df.to_csv(standard_csv_path, index=False, encoding="utf-8")
            
            logger.info(f"Saved {len(self.artworks)} artworks to:")
            logger.info(f"  - {json_path}")
            logger.info(f"  - {csv_path}")
            logger.info(f"  - {standard_csv_path}")
    
    def _create_individual_artist_docs(self):
        """为每位艺术家创建单独的Markdown文档，包含完整信息和作品列表"""
        # 创建艺术家文档目录
        docs_dir = os.path.join(OUTPUT_DIR, "artist_docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        # 获取艺术家的作品映射
        artist_artworks = {}
        for artwork in self.artworks:
            artist_name = artwork.get("artist_name")
            if artist_name:
                if artist_name not in artist_artworks:
                    artist_artworks[artist_name] = []
                artist_artworks[artist_name].append(artwork)
        
        # 为每位艺术家创建文档
        for artist in self.artists:
            artist_name = artist.get("name")
            if not artist_name:
                continue
                
            # 清理文件名
            clean_name = self._clean_filename(artist_name)
            doc_path = os.path.join(docs_dir, f"{clean_name}.md")
            
            # 获取艺术家作品
            artist_artwork_list = artist_artworks.get(artist_name, [])
            
            try:
                with open(doc_path, "w", encoding="utf-8") as f:
                    # 写入艺术家信息
                    f.write(f"# {artist_name}\n\n")
                    
                    # 基本信息
                    if artist.get("nationality"):
                        f.write(f"**Nationality:** {artist['nationality']}\n\n")
                    
                    birth_year = artist.get("birth_year")
                    death_year = artist.get("death_year")
                    if birth_year:
                        birth_death_text = f"{birth_year}"
                        if death_year:
                            birth_death_text += f" - {death_year}"
                        f.write(f"**Years:** {birth_death_text}\n\n")
                    
                    if artist.get("art_movement"):
                        f.write(f"**Movement:** {artist['art_movement']}\n\n")
                    
                    # 简历
                    if artist.get("bio"):
                        f.write("## Biography\n\n")
                        f.write(f"{artist['bio']}\n\n")
                    
                    # 艺术家特征和指标
                    metrics_written = False
                    
                    if artist.get("followers_count") or artist.get("exhibitions_count"):
                        f.write("## Metrics\n\n")
                        metrics_written = True
                        
                        if artist.get("followers_count"):
                            f.write(f"**Followers:** {artist['followers_count']}\n\n")
                        
                        if artist.get("exhibitions_count"):
                            f.write(f"**Exhibitions:** {artist['exhibitions_count']}\n\n")
                    
                    # 分类信息
                    if artist.get("category"):
                        if not metrics_written:
                            f.write("## Metrics\n\n")
                        f.write(f"**Category:** {artist['category']}\n\n")
                    
                    # 作品列表
                    if artist_artwork_list:
                        f.write(f"## Artworks ({len(artist_artwork_list)})\n\n")
                        
                        for i, artwork in enumerate(artist_artwork_list):
                            title = artwork.get("title", "Untitled")
                            date = artwork.get("date", "")
                            medium = artwork.get("medium", "")
                            dimensions = artwork.get("dimensions", "")
                            
                            f.write(f"### {title} {date}\n\n")
                            
                            if medium:
                                f.write(f"**Medium:** {medium}\n\n")
                            
                            if dimensions:
                                f.write(f"**Dimensions:** {dimensions}\n\n")
                            
                            # 相对路径到图片
                            clean_title = self._clean_filename(title)
                            image_dir = os.path.join(OUTPUT_DIR, "images", clean_name)
                            
                            # 查找相关图片文件
                            image_found = False
                            if os.path.exists(image_dir):
                                image_files = [f for f in os.listdir(image_dir) if f.startswith(clean_title)]
                                if image_files:
                                    relative_path = f"../images/{clean_name}/{image_files[0]}"
                                    f.write(f"![{title}]({relative_path})\n\n")
                                    image_found = True
                            
                            if not image_found and artwork.get("image_url"):
                                f.write(f"*Image URL:* {artwork['image_url']}\n\n")
                            
                            if artwork.get("source_url"):
                                f.write(f"*Source:* [{title} on Artsy]({artwork['source_url']})\n\n")
                            
                            if i < len(artist_artwork_list) - 1:
                                f.write("---\n\n")
                    
                    # 来源信息
                    if artist.get("source_url"):
                        f.write(f"\n*Artist information from [Artsy]({artist['source_url']})*\n")
                
                logger.info(f"Created artist document: {doc_path}")
            
            except Exception as e:
                logger.error(f"Error creating document for {artist_name}: {str(e)}")
    
    def close(self):
        """Close the browser."""
        if hasattr(self, "browser"):
            self.browser.quit()

def main():
    scraper = ArtsyScraper()
    try:
        # Get number of artists from environment variable or use default
        num_artists = int(os.getenv("SCRAPER_NUM_ARTISTS", "2000"))
        max_artworks = int(os.getenv("SCRAPER_MAX_ARTWORKS", "20"))
        
        # Scrape important artist categories first
        scraper.scrape_multiple_categories(max_artists_per_category=300, max_artworks=max_artworks)
        
        # Scrape general artist list
        scraper.scrape_artists_list(max_artists=num_artists, max_artworks=max_artworks)
    finally:
        scraper.save_data()
        scraper.save_checkpoint()
        scraper.close()

if __name__ == "__main__":
    main() 