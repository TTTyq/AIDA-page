from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional
import logging

from app.scrapers import create_scraper
from app.services.task_service import TaskService
from app.services.data_service import DataService

class ScraperService:
    """
    爬虫服务，处理爬虫相关的业务逻辑
    """
    
    @staticmethod
    async def test_url(url: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        测试URL是否可访问
        """
        try:
            scraper = create_scraper(url, config)
            return await scraper.test_connection()
        except Exception as e:
            logging.error(f"测试URL失败: {str(e)}")
            return False
    
    @staticmethod
    async def run_scraper(url: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        运行爬虫
        """
        try:
            scraper = create_scraper(url, config)
            results = await scraper.scrape()
            return results
        except Exception as e:
            logging.error(f"运行爬虫失败: {str(e)}")
            raise
    
    @staticmethod
    async def run_task(db: AsyncSession, task_id: int) -> List[Dict[str, Any]]:
        """
        运行任务
        """
        # 获取任务
        task = await TaskService.get_task_by_id(db, task_id)
        if not task:
            raise ValueError(f"任务不存在: {task_id}")
        
        # 更新任务状态为运行中
        await TaskService.update_task_status(db, task_id, "running")
        
        try:
            # 运行爬虫
            results = await ScraperService.run_scraper(task.url, task.config)
            
            # 清除旧数据
            await DataService.delete_data_by_task_id(db, task_id)
            
            # 保存新数据
            if results:
                await DataService.create_many_data(db, task_id, results)
            
            # 更新任务状态为完成
            await TaskService.update_task_status(db, task_id, "completed")
            
            return results
        except Exception as e:
            # 更新任务状态为失败
            await TaskService.update_task_status(db, task_id, "failed")
            logging.error(f"任务运行失败: {str(e)}")
            raise 