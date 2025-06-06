import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import logging
from .base import BaseScraper

class HTMLScraper(BaseScraper):
    """
    基于Requests和BeautifulSoup的HTML爬虫
    """
    
    def __init__(self, url: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(url, config)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.selector = self.config.get('selector', 'body')
        self.pagination = self.config.get('pagination', False)
        self.max_pages = self.config.get('max_pages', 1)
    
    async def test_connection(self) -> bool:
        """
        测试URL是否可访问
        """
        try:
            response = requests.head(self.url, headers=self.headers, timeout=10)
            return 200 <= response.status_code < 300
        except Exception as e:
            logging.error(f"连接测试失败: {str(e)}")
            return False
    
    async def scrape(self) -> List[Dict[str, Any]]:
        """
        执行爬取操作，返回爬取结果
        """
        self.results = []
        current_url = self.url
        current_page = 1
        
        while current_page <= self.max_pages:
            try:
                logging.info(f"爬取页面: {current_url}")
                response = requests.get(current_url, headers=self.headers, timeout=30)
                
                if response.status_code != 200:
                    logging.error(f"HTTP错误: {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'lxml')
                elements = soup.select(self.selector)
                
                for element in elements:
                    # 提取数据
                    data = self._extract_data(element)
                    if data:
                        self.results.append(data)
                
                # 处理分页
                if self.pagination and current_page < self.max_pages:
                    next_url = self._get_next_page(soup)
                    if not next_url or next_url == current_url:
                        break
                    current_url = next_url
                else:
                    break
                
                current_page += 1
                
            except Exception as e:
                logging.error(f"爬取错误: {str(e)}")
                break
        
        return self.results
    
    def _extract_data(self, element) -> Dict[str, Any]:
        """
        从元素中提取数据
        可以根据需要在子类中重写此方法
        """
        try:
            # 默认提取文本、链接和图片
            text = element.get_text(strip=True)
            links = [a.get('href') for a in element.find_all('a') if a.get('href')]
            images = [img.get('src') for img in element.find_all('img') if img.get('src')]
            
            return {
                "text": text,
                "links": links,
                "images": images,
                "html": str(element)
            }
        except Exception as e:
            logging.error(f"数据提取错误: {str(e)}")
            return {}
    
    def _get_next_page(self, soup) -> Optional[str]:
        """
        获取下一页的URL
        可以根据需要在子类中重写此方法
        """
        # 默认查找常见的下一页链接
        next_link = soup.select_one('a.next, a[rel="next"], a:contains("下一页"), a:contains("Next")')
        if next_link and next_link.get('href'):
            # 处理相对URL
            next_url = next_link['href']
            if next_url.startswith('/'):
                from urllib.parse import urlparse
                parsed_url = urlparse(self.url)
                next_url = f"{parsed_url.scheme}://{parsed_url.netloc}{next_url}"
            return next_url
        return None 