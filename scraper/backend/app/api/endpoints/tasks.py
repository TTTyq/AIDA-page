from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services import TaskService

router = APIRouter()

# 任务模型
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: str
    config: dict

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    config: Optional[dict] = None
    status: Optional[str] = None

class Task(TaskBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

@router.get("/", response_model=List[Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """
    获取所有任务
    """
    return await TaskService.get_all_tasks(db)

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    创建新任务
    """
    return await TaskService.create_task(db, task.dict())

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    """
    获取特定任务
    """
    task = await TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_update: TaskUpdate, 
    task_id: int = Path(..., gt=0), 
    db: AsyncSession = Depends(get_db)
):
    """
    更新任务
    """
    task = await TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_task = await TaskService.update_task(db, task_id, update_data)
    return updated_task

@router.delete("/{task_id}")
async def delete_task(task_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    """
    删除任务
    """
    task = await TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted = await TaskService.delete_task(db, task_id)
    if deleted:
        return {"message": f"Task {task_id} deleted"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete task") 