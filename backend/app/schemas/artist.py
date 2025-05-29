from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ArtistBase(BaseModel):
    """艺术家基础模式"""
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None
    art_movement: Optional[str] = None
    image_url: Optional[str] = None

class ArtistCreate(ArtistBase):
    """创建艺术家模式"""
    pass

class ArtistUpdate(BaseModel):
    """更新艺术家模式"""
    name: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None
    art_movement: Optional[str] = None
    image_url: Optional[str] = None

class Artist(ArtistBase):
    """艺术家完整模式"""
    id: int
    
    class Config:
        from_attributes = True

class CSVUploadResponse(BaseModel):
    """CSV上传响应模式"""
    filename: str
    rows_processed: int
    status: str

class QueryParams(BaseModel):
    """查询参数模式"""
    name: Optional[str] = None
    nationality: Optional[str] = None
    style: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None

class ArtistResponse(BaseModel):
    """艺术家响应模式"""
    data: List[Artist]
    total: int
    page: int = 1
    page_size: int = 10
    
class ArtistDetail(Artist):
    """艺术家详情模式"""
    works: Optional[List[Dict[str, Any]]] = None
    exhibitions: Optional[List[Dict[str, Any]]] = None
    related_artists: Optional[List[Dict[str, Any]]] = None

class AIInteractionRequest(BaseModel):
    """AI交互请求模式"""
    message: str = Field(..., description="用户发送给AI艺术家的消息")
    artist_id: Optional[int] = Field(None, description="特定艺术家ID，如果为空则使用默认AI艺术家")
    
class AIInteractionResponse(BaseModel):
    """AI交互响应模式"""
    response: str = Field(..., description="AI艺术家的回复")
    artist_name: str = Field(..., description="回复的AI艺术家名称") 