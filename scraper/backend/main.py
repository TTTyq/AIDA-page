from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 导入路由
from app.api.router import api_router
from app.db.database import init_db

# 创建FastAPI应用
app = FastAPI(
    title="AIDA Scraper",
    description="轻量级爬虫工具，用于AIDA项目数据采集",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(api_router)

# 根路由
@app.get("/")
async def root():
    return {"message": "AIDA Scraper API"}

# 启动事件
@app.on_event("startup")
async def startup_event():
    logging.info("初始化数据库...")
    await init_db()
    logging.info("数据库初始化完成")

# 启动服务器
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 