from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.task import Task

class TaskService:
    """
    任务服务，处理任务相关的数据库操作
    """
    
    @staticmethod
    async def get_all_tasks(db: AsyncSession) -> List[Task]:
        """
        获取所有任务
        """
        result = await db.execute(select(Task).order_by(Task.created_at.desc()))
        return result.scalars().all()
    
    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[Task]:
        """
        根据ID获取任务
        """
        result = await db.execute(select(Task).filter(Task.id == task_id))
        return result.scalars().first()
    
    @staticmethod
    async def create_task(db: AsyncSession, task_data: Dict[str, Any]) -> Task:
        """
        创建新任务
        """
        task = Task(**task_data)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task
    
    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, task_data: Dict[str, Any]) -> Optional[Task]:
        """
        更新任务
        """
        # 更新任务数据
        task_data["updated_at"] = datetime.now()
        await db.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(**task_data)
        )
        await db.commit()
        
        # 返回更新后的任务
        return await TaskService.get_task_by_id(db, task_id)
    
    @staticmethod
    async def update_task_status(db: AsyncSession, task_id: int, status: str) -> Optional[Task]:
        """
        更新任务状态
        """
        return await TaskService.update_task(db, task_id, {"status": status})
    
    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int) -> bool:
        """
        删除任务
        """
        result = await db.execute(delete(Task).where(Task.id == task_id))
        await db.commit()
        return result.rowcount > 0 