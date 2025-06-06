from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class WebsiteBase(BaseModel):
    """Base model for website configuration"""
    name: str
    url: str
    description: Optional[str] = None
    type: str = "html"  # "html" or "api"
    active: bool = True
    

class WebsiteCreate(WebsiteBase):
    """Model for creating a website configuration"""
    selectors: Optional[Dict[str, str]] = None
    config: Optional[Dict[str, Any]] = None


class WebsiteUpdate(BaseModel):
    """Model for updating a website configuration"""
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = None
    selectors: Optional[Dict[str, str]] = None
    config: Optional[Dict[str, Any]] = None


class Website(WebsiteBase):
    """Complete website model with all fields"""
    id: str
    selectors: Optional[Dict[str, str]] = None
    config: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 