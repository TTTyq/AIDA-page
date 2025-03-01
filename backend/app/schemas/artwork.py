from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ArtworkBase(BaseModel):
    """艺术品基础模式"""
    title: str
    artist_id: int
    year: Optional[int] = None
    medium: Optional[str] = None
    dimensions: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class ArtworkCreate(ArtworkBase):
    """创建艺术品模式"""
    pass

class ArtworkUpdate(BaseModel):
    """更新艺术品模式"""
    title: Optional[str] = None
    artist_id: Optional[int] = None
    year: Optional[int] = None
    medium: Optional[str] = None
    dimensions: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class Artwork(ArtworkBase):
    """艺术品完整模式"""
    id: int
    
    class Config:
        from_attributes = True

class ArtworkResponse(BaseModel):
    """艺术品响应模式"""
    data: List[Artwork]
    total: int
    page: int = 1
    page_size: int = 10
    
class ArtworkDetail(Artwork):
    """艺术品详情模式"""
    artist_name: Optional[str] = None
    related_artworks: Optional[List[Dict[str, Any]]] = None 