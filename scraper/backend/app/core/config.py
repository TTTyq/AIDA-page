import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    应用配置
    """
    # 应用信息
    APP_NAME: str = "AIDA Scraper"
    APP_VERSION: str = "0.1.0"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./scraper.db"
    
    # API配置
    API_PREFIX: str = "/api"
    
    # 爬虫配置
    DEFAULT_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    DEFAULT_TIMEOUT: int = 30
    MAX_CONCURRENT_TASKS: int = 5
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置对象
settings = Settings()

# 确保数据目录存在
os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", "")), exist_ok=True) 