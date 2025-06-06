from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.database import get_db
from app.services import DataService

router = APIRouter()

# 数据模型
class DataItemBase(BaseModel):
    task_id: int
    content: Dict[str, Any]

class DataItemCreate(DataItemBase):
    pass

class DataItem(DataItemBase):
    id: int

    class Config:
        orm_mode = True

@router.get("/", response_model=List[DataItem])
async def list_data(
    task_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有数据，可选按任务ID过滤
    """
    if task_id is not None:
        return await DataService.get_data_by_task_id(db, task_id)
    return await DataService.get_all_data(db)

@router.get("/{data_id}", response_model=DataItem)
async def get_data(
    data_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    获取特定数据项
    """
    data = await DataService.get_data_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@router.post("/", response_model=DataItem)
async def create_data(
    data_item: DataItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新数据项
    """
    return await DataService.create_data(db, data_item.dict())

@router.delete("/{data_id}")
async def delete_data(
    data_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    删除数据项
    """
    data = await DataService.get_data_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    deleted = await DataService.delete_data(db, data_id)
    if deleted:
        return {"message": f"Data {data_id} deleted"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete data")

@router.get("/export/{task_id}")
async def export_data(
    task_id: int = Path(..., gt=0),
    format: str = Query("json"),
    db: AsyncSession = Depends(get_db)
):
    """
    导出特定任务的数据
    """
    data_items = await DataService.get_data_by_task_id(db, task_id)
    
    if not data_items:
        raise HTTPException(status_code=404, detail="No data found for this task")
    
    # 提取内容数据
    data = [item.content for item in data_items]
    
    if format.lower() == "json":
        return JSONResponse(content=data)
    else:
        # 未来可以支持更多格式
        raise HTTPException(status_code=400, detail="Unsupported format") 