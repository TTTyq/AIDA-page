from fastapi import APIRouter
from app.api.endpoints import scraper, tasks, data, websites

# 创建主路由
api_router = APIRouter(prefix="/api")
 
# 包含各个端点的路由
api_router.include_router(scraper.router, prefix="/scraper", tags=["scraper"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(websites.router, prefix="/websites", tags=["websites"]) 