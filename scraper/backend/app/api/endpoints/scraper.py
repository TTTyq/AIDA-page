from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List, Dict, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services import ScraperService, TaskService

router = APIRouter()

# 爬虫配置模型
class ScraperConfig(BaseModel):
    url: str
    selector: str = None
    use_browser: bool = False
    wait_time: int = 0
    pagination: bool = False
    max_pages: int = 1

# 爬虫结果模型
class ScraperResult(BaseModel):
    success: bool
    data: List[Dict[str, Any]] = []
    error: str = None

@router.post("/run", response_model=ScraperResult)
async def run_scraper(config: ScraperConfig):
    """
    运行爬虫并返回结果
    """
    try:
        results = await ScraperService.run_scraper(config.url, config.dict())
        return ScraperResult(
            success=True,
            data=results
        )
    except Exception as e:
        return ScraperResult(
            success=False,
            error=str(e)
        )

@router.post("/run-task/{task_id}", response_model=ScraperResult)
async def run_task(
    task_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    运行特定任务的爬虫
    """
    try:
        # 检查任务是否存在
        task = await TaskService.get_task_by_id(db, task_id)
        if not task:
            return ScraperResult(
                success=False,
                error=f"Task not found: {task_id}"
            )
        
        # 运行爬虫任务
        results = await ScraperService.run_task(db, task_id)
        
        return ScraperResult(
            success=True,
            data=results
        )
    except Exception as e:
        return ScraperResult(
            success=False,
            error=str(e)
        )

@router.get("/test/{url:path}")
async def test_scraper(url: str):
    """
    测试URL是否可访问
    """
    try:
        result = await ScraperService.test_url(url)
        if result:
            return {"status": "ok", "url": url}
        else:
            return {"status": "error", "url": url, "message": "URL可能无法访问"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 