from typing import Dict, List, Any, Optional
import logging
import asyncio
from playwright.async_api import async_playwright
from .base import BaseScraper

class BrowserScraper(BaseScraper):
    """
    基于Playwright的浏览器爬虫，用于处理JavaScript渲染的页面
    """
    
    def __init__(self, url: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(url, config)
        self.selector = self.config.get('selector', 'body')
        self.wait_time = self.config.get('wait_time', 0)
        self.pagination = self.config.get('pagination', False)
        self.max_pages = self.config.get('max_pages', 1)
    
    async def test_connection(self) -> bool:
        """
        测试URL是否可访问
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                response = await page.goto(self.url, wait_until="domcontentloaded")
                await browser.close()
                return response.ok
        except Exception as e:
            logging.error(f"连接测试失败: {str(e)}")
            return False
    
    async def scrape(self) -> List[Dict[str, Any]]:
        """
        执行爬取操作，返回爬取结果
        """
        self.results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                current_url = self.url
                current_page = 1
                
                while current_page <= self.max_pages:
                    logging.info(f"爬取页面: {current_url}")
                    
                    # 导航到页面
                    await page.goto(current_url, wait_until="networkidle")
                    
                    # 等待指定时间
                    if self.wait_time > 0:
                        await asyncio.sleep(self.wait_time)
                    
                    # 等待选择器
                    try:
                        await page.wait_for_selector(self.selector, timeout=5000)
                    except Exception:
                        logging.warning(f"选择器未找到: {self.selector}")
                    
                    # 提取数据
                    elements = await page.query_selector_all(self.selector)
                    
                    for element in elements:
                        data = await self._extract_data(element, page)
                        if data:
                            self.results.append(data)
                    
                    # 处理分页
                    if self.pagination and current_page < self.max_pages:
                        next_url = await self._get_next_page(page)
                        if not next_url or next_url == current_url:
                            break
                        current_url = next_url
                    else:
                        break
                    
                    current_page += 1
                
                await browser.close()
                
        except Exception as e:
            logging.error(f"爬取错误: {str(e)}")
        
        return self.results
    
    async def _extract_data(self, element, page) -> Dict[str, Any]:
        """
        从元素中提取数据
        """
        try:
            # 获取文本
            text = await element.text_content()
            
            # 获取HTML
            html = await element.evaluate("el => el.outerHTML")
            
            # 获取链接
            links = await element.evaluate("""
                element => {
                    const anchors = element.querySelectorAll('a');
                    return Array.from(anchors).map(a => a.href);
                }
            """)
            
            # 获取图片
            images = await element.evaluate("""
                element => {
                    const imgs = element.querySelectorAll('img');
                    return Array.from(imgs).map(img => img.src);
                }
            """)
            
            return {
                "text": text.strip() if text else "",
                "links": links,
                "images": images,
                "html": html
            }
        except Exception as e:
            logging.error(f"数据提取错误: {str(e)}")
            return {}
    
    async def _get_next_page(self, page) -> Optional[str]:
        """
        获取下一页的URL
        """
        try:
            # 尝试查找常见的下一页按钮
            next_selectors = [
                'a.next', 
                'a[rel="next"]', 
                'a:has-text("下一页")', 
                'a:has-text("Next")',
                'button:has-text("下一页")',
                'button:has-text("Next")'
            ]
            
            for selector in next_selectors:
                next_element = await page.query_selector(selector)
                if next_element:
                    # 如果找到了下一页按钮，点击它
                    await next_element.click()
                    # 等待导航完成
                    await page.wait_for_load_state("networkidle")
                    return page.url
            
            return None
        except Exception as e:
            logging.error(f"获取下一页错误: {str(e)}")
            return None 