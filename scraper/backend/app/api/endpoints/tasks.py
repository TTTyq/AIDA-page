from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# 任务模型
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: str
    config: dict

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 模拟数据存储
tasks_db = [
    {
        "id": 1,
        "name": "测试任务",
        "description": "这是一个测试任务",
        "url": "https://example.com",
        "config": {"selector": "div.content", "use_browser": False},
        "status": "completed",
        "created_at": datetime.now(),
        "updated_at": None
    }
]

@router.get("/", response_model=List[Task])
async def list_tasks():
    """
    获取所有任务
    """
    return tasks_db

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate):
    """
    创建新任务
    """
    new_task = task.dict()
    new_task.update({
        "id": len(tasks_db) + 1,
        "status": "pending",
        "created_at": datetime.now(),
        "updated_at": None
    })
    tasks_db.append(new_task)
    return new_task

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0)):
    """
    获取特定任务
    """
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}")
async def delete_task(task_id: int = Path(..., gt=0)):
    """
    删除任务
    """
    for i, task in enumerate(tasks_db):
        if task["id"] == task_id:
            del tasks_db[i]
            return {"message": f"Task {task_id} deleted"}
    raise HTTPException(status_code=404, detail="Task not found") 