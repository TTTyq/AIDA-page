from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Optional

from app.schemas.artwork import Artwork, ArtworkCreate, ArtworkUpdate, ArtworkResponse
from app.services.artwork_service import ArtworkService
from app.services.artist_service import ArtistService

router = APIRouter()

@router.get("/", response_model=List[Artwork])
async def get_artworks():
    """
    获取所有艺术品
    
    返回数据库中所有艺术品的列表
    """
    try:
        artworks = ArtworkService.get_all_artworks()
        return artworks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching artworks: {str(e)}")

@router.get("/import-test-data")
async def import_test_data():
    """
    导入测试数据
    
    从 test_artworks.csv 文件导入测试数据到 MongoDB
    """
    try:
        from app.utils.csv_handler import CSVHandler
        
        # 获取测试数据文件路径
        test_data_path = CSVHandler.get_test_data_path("test_artworks.csv")
        
        if not test_data_path:
            raise HTTPException(status_code=404, detail="Test data file not found")
        
        # 导入数据
        result = ArtworkService.import_from_csv(test_data_path)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail={"message": "Error importing test data", "errors": result["errors"]})
        
        # 返回自定义响应
        from fastapi.responses import JSONResponse
        return JSONResponse(content={
            "message": "Test artwork data import successful",
            "records_count": result["rows_processed"],
            "collection": ArtworkService.COLLECTION_NAME,
            "sample_records": result["sample_records"]
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing test data: {str(e)}")

@router.get("/{artwork_id}", response_model=Artwork)
async def get_artwork(artwork_id: int = Path(..., description="艺术品ID")):
    """
    获取特定艺术品
    
    根据ID获取特定艺术品的详细信息
    
    Args:
        artwork_id: 艺术品ID
    """
    try:
        artwork = ArtworkService.get_artwork_by_id(artwork_id)
        
        if not artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        return artwork
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching artwork: {str(e)}")

@router.post("/", response_model=Artwork, status_code=status.HTTP_201_CREATED)
async def create_artwork(artwork: ArtworkCreate):
    """
    创建艺术品
    
    创建新的艺术品记录
    
    Args:
        artwork: 艺术品数据
    """
    try:
        # 检查艺术家是否存在
        artist = ArtistService.get_artist_by_id(artwork.artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail=f"Artist with ID {artwork.artist_id} not found")
        
        # 获取最大ID
        all_artworks = ArtworkService.get_all_artworks()
        max_id = 0
        if all_artworks:
            max_id = max(artwork.get("id", 0) for artwork in all_artworks)
        
        # 创建艺术品
        artwork_data = artwork.dict()
        artwork_data["id"] = max_id + 1
        
        created_artwork = ArtworkService.create_artwork(artwork_data)
        return created_artwork
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating artwork: {str(e)}")

@router.put("/{artwork_id}", response_model=Artwork)
async def update_artwork(artwork_data: ArtworkUpdate, artwork_id: int = Path(..., description="艺术品ID")):
    """
    更新艺术品
    
    更新特定艺术品的信息
    
    Args:
        artwork_id: 艺术品ID
        artwork_data: 艺术品更新数据
    """
    try:
        # 检查艺术品是否存在
        existing_artwork = ArtworkService.get_artwork_by_id(artwork_id)
        if not existing_artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        # 如果更新了艺术家ID，检查艺术家是否存在
        if artwork_data.artist_id is not None:
            artist = ArtistService.get_artist_by_id(artwork_data.artist_id)
            if not artist:
                raise HTTPException(status_code=404, detail=f"Artist with ID {artwork_data.artist_id} not found")
        
        # 更新艺术品
        update_data = {k: v for k, v in artwork_data.dict().items() if v is not None}
        updated_artwork = ArtworkService.update_artwork(artwork_id, update_data)
        
        return updated_artwork
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating artwork: {str(e)}")

@router.delete("/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artwork(artwork_id: int = Path(..., description="艺术品ID")):
    """
    删除艺术品
    
    删除特定艺术品
    
    Args:
        artwork_id: 艺术品ID
    """
    try:
        # 检查艺术品是否存在
        existing_artwork = ArtworkService.get_artwork_by_id(artwork_id)
        if not existing_artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        # 删除艺术品
        success = ArtworkService.delete_artwork(artwork_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete artwork")
        
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting artwork: {str(e)}")

@router.get("/artist/{artist_id}", response_model=List[Artwork])
async def get_artworks_by_artist(artist_id: int = Path(..., description="艺术家ID")):
    """
    获取艺术家的艺术品
    
    根据艺术家ID获取其所有艺术品
    
    Args:
        artist_id: 艺术家ID
    """
    try:
        # 检查艺术家是否存在
        artist = ArtistService.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail=f"Artist with ID {artist_id} not found")
        
        # 获取艺术品
        artworks = ArtworkService.get_artworks_by_artist_id(artist_id)
        return artworks
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching artworks: {str(e)}") 