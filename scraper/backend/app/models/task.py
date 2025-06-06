from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Task(Base):
    """
    爬虫任务模型
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    config = Column(JSON, nullable=False)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)
    
    # 关联数据
    data_items = relationship("DataItem", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Task {self.id}: {self.name}>" 