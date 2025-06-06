from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List, Optional, Dict, Any

from app.models.data import DataItem

class DataService:
    """
    数据服务，处理爬取数据相关的数据库操作
    """
    
    @staticmethod
    async def get_all_data(db: AsyncSession) -> List[DataItem]:
        """
        获取所有数据
        """
        result = await db.execute(select(DataItem).order_by(DataItem.created_at.desc()))
        return result.scalars().all()
    
    @staticmethod
    async def get_data_by_id(db: AsyncSession, data_id: int) -> Optional[DataItem]:
        """
        根据ID获取数据
        """
        result = await db.execute(select(DataItem).filter(DataItem.id == data_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_data_by_task_id(db: AsyncSession, task_id: int) -> List[DataItem]:
        """
        根据任务ID获取数据
        """
        result = await db.execute(
            select(DataItem)
            .filter(DataItem.task_id == task_id)
            .order_by(DataItem.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def create_data(db: AsyncSession, data_item: Dict[str, Any]) -> DataItem:
        """
        创建新数据项
        """
        data = DataItem(**data_item)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data
    
    @staticmethod
    async def create_many_data(db: AsyncSession, task_id: int, data_items: List[Dict[str, Any]]) -> List[DataItem]:
        """
        批量创建数据项
        """
        items = []
        for item in data_items:
            data = DataItem(task_id=task_id, content=item)
            db.add(data)
            items.append(data)
        
        await db.commit()
        for item in items:
            await db.refresh(item)
        
        return items
    
    @staticmethod
    async def delete_data(db: AsyncSession, data_id: int) -> bool:
        """
        删除数据
        """
        result = await db.execute(delete(DataItem).where(DataItem.id == data_id))
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def delete_data_by_task_id(db: AsyncSession, task_id: int) -> int:
        """
        删除任务相关的所有数据
        """
        result = await db.execute(delete(DataItem).where(DataItem.task_id == task_id))
        await db.commit()
        return result.rowcount 