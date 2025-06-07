import requests
import json
import time
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from .html import HTMLScraper

class ArtsyScraper(HTMLScraper):
    """
    Artsy.net website scraper for artists and artworks data
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # Artsy base URL
        base_url = "https://www.artsy.net"
        super().__init__(base_url, config)
        
        # Artsy specific headers
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Configuration
        self.max_artists = self.config.get('max_artists', 50)
        self.max_artworks_per_artist = self.config.get('max_artworks_per_artist', 10)
        self.delay_between_requests = self.config.get('delay', 2)
        self.scrape_type = self.config.get('type', 'artists')  # 'artists', 'artworks', 'both'
        
        # Data storage
        self.artists_data = []
        self.artworks_data = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def scrape(self) -> List[Dict[str, Any]]:
        """
        Main scraping method
        """
        self.logger.info(f"Starting Artsy scraping - Type: {self.scrape_type}")
        
        try:
            if self.scrape_type in ['artists', 'both']:
                await self._scrape_artists()
            
            if self.scrape_type in ['artworks', 'both']:
                await self._scrape_artworks()
            
            # Combine results
            self.results = []
            if self.artists_data:
                self.results.extend(self.artists_data)
            if self.artworks_data:
                self.results.extend(self.artworks_data)
                
            self.logger.info(f"Scraping completed. Total items: {len(self.results)}")
            return self.results
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {str(e)}")
            return []

    async def _scrape_artists(self):
        """
        Scrape artists from Artsy
        """
        self.logger.info("Starting artists scraping...")
        
        # Start from artists browse page
        artists_url = "https://www.artsy.net/artists"
        page = 1
        collected_artists = 0
        collected_urls = set()  # Track visited URLs to avoid duplicates
        
        while collected_artists < self.max_artists:
            try:
                # Add pagination parameter
                url = f"{artists_url}?page={page}"
                self.logger.info(f"Scraping artists page {page}: {url}")
                
                response = requests.get(url, headers=self.headers, timeout=30)
                if response.status_code != 200:
                    self.logger.error(f"Failed to fetch page {page}: {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Find artist links - Artsy uses specific CSS classes
                artist_links = soup.select('a[href*="/artist/"]')
                
                if not artist_links:
                    self.logger.info("No more artist links found")
                    break
                
                for link in artist_links:
                    if collected_artists >= self.max_artists:
                        break
                    
                    artist_url = urljoin(self.url, link.get('href'))
                    
                    # Skip if already processed
                    if artist_url in collected_urls:
                        continue
                    
                    collected_urls.add(artist_url)
                    artist_data = await self._scrape_single_artist(artist_url)
                    
                    if artist_data:
                        self.artists_data.append(artist_data)
                        collected_artists += 1
                        self.logger.info(f"Collected artist {collected_artists}/{self.max_artists}: {artist_data.get('name', 'Unknown')}")
                    
                    # Delay between requests
                    time.sleep(self.delay_between_requests)
                
                page += 1
                time.sleep(self.delay_between_requests)
                
            except Exception as e:
                self.logger.error(f"Error scraping artists page {page}: {str(e)}")
                break

    async def _scrape_single_artist(self, artist_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape individual artist page
        """
        try:
            response = requests.get(artist_url, headers=self.headers, timeout=30)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract artist information
            artist_data = {
                'type': 'artist',
                'url': artist_url,
                'source': 'artsy.net'
            }
            
            # Extract artist ID from URL
            artist_slug = artist_url.split('/artist/')[-1].split('?')[0]
            artist_data['artist_id'] = artist_slug
            
            # Artist name
            name_elem = soup.select_one('h1[data-test="artistName"], h1.artist-name, h1')
            if name_elem:
                artist_data['name'] = name_elem.get_text(strip=True)
            
            # Artist bio/description
            bio_elem = soup.select_one('[data-test="artistBio"], .artist-bio, .artist-description')
            if bio_elem:
                artist_data['bio'] = bio_elem.get_text(strip=True)
            
            # Birth/death dates
            dates_elem = soup.select_one('[data-test="artistDates"], .artist-dates')
            if dates_elem:
                artist_data['dates'] = dates_elem.get_text(strip=True)
            
            # Nationality
            nationality_elem = soup.select_one('[data-test="artistNationality"], .artist-nationality')
            if nationality_elem:
                artist_data['nationality'] = nationality_elem.get_text(strip=True)
            
            # Artist image - Try multiple selectors
            img_elem = soup.select_one('img[alt*="artist"], img.artist-image, .artist-header img, img[src*="artist"], .artist-photo img, .profile-image img')
            if img_elem:
                artist_data['image_url'] = urljoin(artist_url, img_elem.get('src', ''))
            else:
                # Try to find any image in the artist header/profile section
                header_section = soup.select_one('.artist-header, .artist-profile, .profile-section')
                if header_section:
                    header_img = header_section.select_one('img')
                    if header_img:
                        artist_data['image_url'] = urljoin(artist_url, header_img.get('src', ''))
            
            # Get artist avatar/profile image from meta tags
            if 'image_url' not in artist_data:
                meta_img = soup.select_one('meta[property="og:image"], meta[name="twitter:image"]')
                if meta_img:
                    artist_data['image_url'] = meta_img.get('content', '')
            
            # Artworks count
            artworks_count_elem = soup.select_one('[data-test="artworksCount"], .artworks-count')
            if artworks_count_elem:
                artist_data['artworks_count'] = artworks_count_elem.get_text(strip=True)
            
            # Extract some artworks if configured
            if self.scrape_type == 'both':
                artworks = await self._scrape_artist_artworks(
                    soup, artist_url, 
                    artist_data.get('artist_id'), 
                    artist_data.get('name')
                )
                artist_data['artworks'] = artworks
                # Also add artworks to global collection
                self.artworks_data.extend(artworks)
            
            return artist_data
            
        except Exception as e:
            self.logger.error(f"Error scraping artist {artist_url}: {str(e)}")
            return None

    async def _scrape_artist_artworks(self, soup: BeautifulSoup, artist_url: str, artist_id: str = None, artist_name: str = None) -> List[Dict[str, Any]]:
        """
        Scrape artworks from artist page with enhanced functionality
        """
        artworks = []
        
        try:
            self.logger.info(f"Scraping artworks for artist: {artist_name or 'Unknown'}")
            
            # Find artwork links on artist page - try multiple selectors
            artwork_links = soup.select('a[href*="/artwork/"]')
            
            # Also try to find artwork links in specific sections
            artwork_sections = soup.select('.artist-artworks, .artworks-grid, .works-section')
            for section in artwork_sections:
                section_links = section.select('a[href*="/artwork/"]')
                artwork_links.extend(section_links)
            
            # Remove duplicates
            unique_links = {}
            for link in artwork_links:
                href = link.get('href')
                if href:
                    unique_links[href] = link
            
            artwork_links = list(unique_links.values())[:self.max_artworks_per_artist]
            
            self.logger.info(f"Found {len(artwork_links)} artwork links for {artist_name}")
            
            for i, link in enumerate(artwork_links, 1):
                artwork_url = urljoin(artist_url, link.get('href'))
                artwork_data = await self._scrape_single_artwork(artwork_url)
                
                if artwork_data:
                    # Add artist context to artwork
                    artwork_data['artist_id'] = artist_id
                    artwork_data['artist_name'] = artist_name
                    artwork_data['artist_page_url'] = artist_url
                    artworks.append(artwork_data)
                    
                    self.logger.info(f"Collected artwork {i}/{len(artwork_links)} for {artist_name}: {artwork_data.get('title', 'Unknown')}")
                
                time.sleep(self.delay_between_requests)
        
        except Exception as e:
            self.logger.error(f"Error scraping artworks for artist {artist_name}: {str(e)}")
        
        return artworks

    async def _scrape_artworks(self):
        """
        Scrape artworks from Artsy browse pages
        """
        self.logger.info("Starting artworks scraping...")
        
        artworks_url = "https://www.artsy.net/collect"
        page = 1
        collected_artworks = 0
        max_artworks = self.config.get('max_artworks', 100)
        collected_artwork_urls = set()  # Track visited URLs to avoid duplicates
        
        while collected_artworks < max_artworks:
            try:
                url = f"{artworks_url}?page={page}"
                self.logger.info(f"Scraping artworks page {page}: {url}")
                
                response = requests.get(url, headers=self.headers, timeout=30)
                if response.status_code != 200:
                    break
                
                soup = BeautifulSoup(response.text, 'lxml')
                artwork_links = soup.select('a[href*="/artwork/"]')
                
                if not artwork_links:
                    break
                
                for link in artwork_links:
                    if collected_artworks >= max_artworks:
                        break
                    
                    artwork_url = urljoin(self.url, link.get('href'))
                    
                    # Skip if already processed
                    if artwork_url in collected_artwork_urls:
                        continue
                    
                    collected_artwork_urls.add(artwork_url)
                    artwork_data = await self._scrape_single_artwork(artwork_url)
                    
                    if artwork_data:
                        self.artworks_data.append(artwork_data)
                        collected_artworks += 1
                        self.logger.info(f"Collected artwork {collected_artworks}/{max_artworks}: {artwork_data.get('title', 'Unknown')}")
                    
                    time.sleep(self.delay_between_requests)
                
                page += 1
                time.sleep(self.delay_between_requests)
                
            except Exception as e:
                self.logger.error(f"Error scraping artworks page {page}: {str(e)}")
                break

    async def _scrape_single_artwork(self, artwork_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape individual artwork page
        """
        try:
            response = requests.get(artwork_url, headers=self.headers, timeout=30)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            artwork_data = {
                'type': 'artwork',
                'url': artwork_url,
                'source': 'artsy.net'
            }
            
            # Artwork title
            title_elem = soup.select_one('h1[data-test="artworkTitle"], h1.artwork-title, h1')
            if title_elem:
                artwork_data['title'] = title_elem.get_text(strip=True)
            
            # Artist name and info
            artist_elem = soup.select_one('[data-test="artistName"], .artist-name, a[href*="/artist/"]')
            if artist_elem:
                artwork_data['artist'] = artist_elem.get_text(strip=True)
                if artist_elem.get('href'):
                    artwork_data['artist_url'] = urljoin(artwork_url, artist_elem.get('href'))
                    # Extract artist ID from URL for better linking
                    artist_slug = artist_elem.get('href').split('/artist/')[-1].split('?')[0]
                    artwork_data['artist_id'] = artist_slug
            
            # Artwork image - Enhanced image extraction
            img_elem = soup.select_one('img[data-test="artworkImage"], .artwork-image img, .artwork img, .artwork-main-image img')
            if img_elem:
                artwork_data['image_url'] = urljoin(artwork_url, img_elem.get('src', ''))
            else:
                # Try alternative image sources
                main_img = soup.select_one('.main-artwork-image img, .primary-image img, .hero-image img')
                if main_img:
                    artwork_data['image_url'] = urljoin(artwork_url, main_img.get('src', ''))
                else:
                    # Try meta tags for artwork image
                    meta_img = soup.select_one('meta[property="og:image"], meta[name="twitter:image"]')
                    if meta_img:
                        artwork_data['image_url'] = meta_img.get('content', '')
            
            # Get high-resolution image if available
            if 'image_url' in artwork_data:
                img_url = artwork_data['image_url']
                # Try to get larger version from Artsy CDN
                if 'cloudfront.net' in img_url and 'large.jpg' in img_url:
                    artwork_data['image_url_large'] = img_url
                elif 'cloudfront.net' in img_url:
                    # Try to construct large version URL
                    artwork_data['image_url_large'] = img_url.replace('medium.jpg', 'large.jpg').replace('small.jpg', 'large.jpg')
            
            # Date
            date_elem = soup.select_one('[data-test="artworkDate"], .artwork-date')
            if date_elem:
                artwork_data['date'] = date_elem.get_text(strip=True)
            
            # Medium
            medium_elem = soup.select_one('[data-test="artworkMedium"], .artwork-medium')
            if medium_elem:
                artwork_data['medium'] = medium_elem.get_text(strip=True)
            
            # Dimensions
            dimensions_elem = soup.select_one('[data-test="artworkDimensions"], .artwork-dimensions')
            if dimensions_elem:
                artwork_data['dimensions'] = dimensions_elem.get_text(strip=True)
            
            # Price (if available)
            price_elem = soup.select_one('[data-test="artworkPrice"], .artwork-price, .price')
            if price_elem:
                artwork_data['price'] = price_elem.get_text(strip=True)
            
            # Description
            description_elem = soup.select_one('[data-test="artworkDescription"], .artwork-description')
            if description_elem:
                artwork_data['description'] = description_elem.get_text(strip=True)
            
            return artwork_data
            
        except Exception as e:
            self.logger.error(f"Error scraping artwork {artwork_url}: {str(e)}")
            return None

    async def test_connection(self) -> bool:
        """
        Test connection to Artsy.net
        """
        try:
            response = requests.head("https://www.artsy.net", headers=self.headers, timeout=10)
            return 200 <= response.status_code < 300
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False

    def get_artists_data(self) -> List[Dict[str, Any]]:
        """
        Get collected artists data
        """
        return self.artists_data

    def get_artworks_data(self) -> List[Dict[str, Any]]:
        """
        Get collected artworks data
        """
        return self.artworks_data

    def save_to_json(self, filename: str = None):
        """
        Save scraped data to JSON file
        """
        if not filename:
            filename = f"artsy_data_{int(time.time())}.json"
        
        data = {
            'scrape_info': {
                'timestamp': time.time(),
                'type': self.scrape_type,
                'total_items': len(self.results),
                'artists_count': len(self.artists_data),
                'artworks_count': len(self.artworks_data)
            },
            'artists': self.artists_data,
            'artworks': self.artworks_data
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save data: {str(e)}") 