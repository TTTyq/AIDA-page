from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseScraper(ABC):
    """
    爬虫基类，定义爬虫的通用接口
    """
    
    def __init__(self, url: str, config: Optional[Dict[str, Any]] = None):
        self.url = url
        self.config = config or {}
        self.results = []
    
    @abstractmethod
    async def scrape(self) -> List[Dict[str, Any]]:
        """
        执行爬取操作，返回爬取结果
        """
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """
        测试URL是否可访问
        """
        pass
    
    def get_results(self) -> List[Dict[str, Any]]:
        """
        获取爬取结果
        """
        return self.results 