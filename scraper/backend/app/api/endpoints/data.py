from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json

router = APIRouter()

# 数据模型
class DataItem(BaseModel):
    id: int
    task_id: int
    content: Dict[str, Any]

# 模拟数据存储
data_db = [
    {
        "id": 1,
        "task_id": 1,
        "content": {
            "title": "示例标题",
            "url": "https://example.com",
            "text": "这是一个示例内容"
        }
    },
    {
        "id": 2,
        "task_id": 1,
        "content": {
            "title": "另一个标题",
            "url": "https://example.com/page2",
            "text": "这是另一个示例内容"
        }
    }
]

@router.get("/", response_model=List[DataItem])
async def list_data(task_id: Optional[int] = Query(None)):
    """
    获取所有数据，可选按任务ID过滤
    """
    if task_id is not None:
        return [item for item in data_db if item["task_id"] == task_id]
    return data_db

@router.get("/{data_id}", response_model=DataItem)
async def get_data(data_id: int = Path(..., gt=0)):
    """
    获取特定数据项
    """
    for item in data_db:
        if item["id"] == data_id:
            return item
    raise HTTPException(status_code=404, detail="Data not found")

@router.get("/export/{task_id}")
async def export_data(task_id: int = Path(..., gt=0), format: str = Query("json")):
    """
    导出特定任务的数据
    """
    data = [item["content"] for item in data_db if item["task_id"] == task_id]
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this task")
    
    if format.lower() == "json":
        return JSONResponse(content=data)
    else:
        # 未来可以支持更多格式
        raise HTTPException(status_code=400, detail="Unsupported format") 