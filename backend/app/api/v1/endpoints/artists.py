from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Optional

from app.schemas.artist import Artist, ArtistCreate, ArtistUpdate, ArtistResponse
from app.services.artist_service import ArtistService

router = APIRouter()

@router.get("/", response_model=List[Artist])
async def get_artists():
    """
    获取所有艺术家
    
    返回数据库中所有艺术家的列表
    """
    try:
        artists = ArtistService.get_all_artists()
        return artists
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching artists: {str(e)}")

@router.get("/{artist_id}", response_model=Artist)
async def get_artist(artist_id: int = Path(..., description="艺术家ID")):
    """
    获取特定艺术家
    
    根据ID获取特定艺术家的详细信息
    
    Args:
        artist_id: 艺术家ID
    """
    try:
        artist = ArtistService.get_artist_by_id(artist_id)
        
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        
        return artist
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching artist: {str(e)}")

@router.post("/", response_model=Artist, status_code=status.HTTP_201_CREATED)
async def create_artist(artist: ArtistCreate):
    """
    创建艺术家
    
    创建新的艺术家记录
    
    Args:
        artist: 艺术家创建模式
    """
    try:
        created_artist = ArtistService.create_artist(artist.dict())
        return created_artist
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating artist: {str(e)}")

@router.put("/{artist_id}", response_model=Artist)
async def update_artist(
    artist_update: ArtistUpdate,
    artist_id: int = Path(..., description="艺术家ID")
):
    """
    更新艺术家
    
    更新特定艺术家的信息
    
    Args:
        artist_id: 艺术家ID
        artist_update: 艺术家更新模式
    """
    try:
        # 过滤掉 None 值，只更新提供的字段
        update_data = {k: v for k, v in artist_update.dict().items() if v is not None}
        
        updated_artist = ArtistService.update_artist(artist_id, update_data)
        
        if not updated_artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        
        return updated_artist
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating artist: {str(e)}")

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(artist_id: int = Path(..., description="艺术家ID")):
    """
    删除艺术家
    
    删除特定艺术家的记录
    
    Args:
        artist_id: 艺术家ID
    """
    try:
        success = ArtistService.delete_artist(artist_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Artist not found")
        
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting artist: {str(e)}")

@router.get("/search/", response_model=ArtistResponse)
async def search_artists(
    name: Optional[str] = Query(None, description="艺术家名称"),
    nationality: Optional[str] = Query(None, description="国籍"),
    style: Optional[str] = Query(None, description="艺术风格"),
    min_year: Optional[int] = Query(None, description="最小出生年份"),
    max_year: Optional[int] = Query(None, description="最大出生年份"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量")
):
    """
    搜索艺术家
    
    根据各种条件搜索艺术家
    
    Args:
        name: 艺术家名称
        nationality: 国籍
        style: 艺术风格
        min_year: 最小出生年份
        max_year: 最大出生年份
        page: 页码
        page_size: 每页数量
    """
    # TODO: 实现搜索功能
    # 目前返回所有艺术家
    try:
        artists = ArtistService.get_all_artists()
        
        # 简单分页
        start = (page - 1) * page_size
        end = start + page_size
        paginated_artists = artists[start:end]
        
        return {
            "data": paginated_artists,
            "total": len(artists),
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching artists: {str(e)}") 