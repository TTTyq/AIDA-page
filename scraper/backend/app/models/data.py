from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DataItem(Base):
    """
    数据项模型，用于存储爬取的数据
    """
    __tablename__ = "data_items"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(255), nullable=False)  # 数据来源
    type = Column(String(100), nullable=False)    # 数据类型 (artist, artwork, etc.)
    title = Column(String(500))                   # 标题
    url = Column(String(1000))                    # 原始URL
    data = Column(JSON)                           # JSON格式的数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DataItem(id={self.id}, type={self.type}, title={self.title})>" 