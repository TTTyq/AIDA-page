from .html import HTMLScraper
from .browser import BrowserScraper
from typing import Dict, Any, Optional

def create_scraper(url: str, config: Optional[Dict[str, Any]] = None):
    """
    爬虫工厂函数，根据配置创建适当的爬虫实例
    """
    config = config or {}
    use_browser = config.get('use_browser', False)
    
    if use_browser:
        return BrowserScraper(url, config)
    else:
        return HTMLScraper(url, config) 