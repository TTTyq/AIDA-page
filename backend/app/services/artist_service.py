from typing import List, Dict, Any, Optional
import pandas as pd
from bson import json_util
import json

from app.db.mongodb import get_collection
from app.models.artist import Artist

class ArtistService:
    """
    艺术家服务类
    
    提供艺术家数据的CRUD操作和其他相关功能
    """
    
    COLLECTION_NAME = "test_table"  # 集合名称
    
    @classmethod
    def get_all_artists(cls) -> List[Dict[str, Any]]:
        """
        获取所有艺术家
        
        Returns:
            List[Dict[str, Any]]: 艺术家列表
        """
        collection = get_collection(cls.COLLECTION_NAME)
        artists = list(collection.find())
        
        # 处理 MongoDB ObjectId 和 NaN 值
        for artist in artists:
            if "_id" in artist:
                del artist["_id"]
            
            # 转换 NaN 值为 None
            for key, value in artist.items():
                if isinstance(value, float) and pd.isna(value):
                    artist[key] = None
            
            # 确保返回 art_movement 字段
            if "primary_style" in artist and "art_movement" not in artist:
                artist["art_movement"] = artist["primary_style"]
        
        return artists
    
    @classmethod
    def get_artist_by_id(cls, artist_id: int) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取艺术家
        
        Args:
            artist_id: 艺术家 ID
            
        Returns:
            Optional[Dict[str, Any]]: 艺术家数据，如果不存在则返回 None
        """
        collection = get_collection(cls.COLLECTION_NAME)
        artist = collection.find_one({"id": artist_id})
        
        if not artist:
            return None
        
        # 处理 MongoDB ObjectId 和 NaN 值
        if "_id" in artist:
            del artist["_id"]
        
        # 转换 NaN 值为 None
        for key, value in artist.items():
            if isinstance(value, float) and pd.isna(value):
                artist[key] = None
        
        return artist
    
    @classmethod
    def create_artist(cls, artist_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建艺术家
        
        Args:
            artist_data: 艺术家数据
            
        Returns:
            Dict[str, Any]: 创建的艺术家数据
        """
        collection = get_collection(cls.COLLECTION_NAME)
        
        # 确保 ID 唯一
        if "id" in artist_data:
            existing = collection.find_one({"id": artist_data["id"]})
            if existing:
                raise ValueError(f"Artist with ID {artist_data['id']} already exists")
        else:
            # 自动生成 ID
            max_id = collection.find_one(sort=[("id", -1)])
            artist_data["id"] = 1 if not max_id else max_id["id"] + 1
        
        # 插入数据
        collection.insert_one(artist_data)
        
        # 返回创建的艺术家数据
        return cls.get_artist_by_id(artist_data["id"])
    
    @classmethod
    def update_artist(cls, artist_id: int, artist_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新艺术家
        
        Args:
            artist_id: 艺术家 ID
            artist_data: 要更新的艺术家数据
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的艺术家数据，如果不存在则返回 None
        """
        collection = get_collection(cls.COLLECTION_NAME)
        
        # 检查艺术家是否存在
        existing = collection.find_one({"id": artist_id})
        if not existing:
            return None
        
        # 更新数据
        collection.update_one({"id": artist_id}, {"$set": artist_data})
        
        # 返回更新后的艺术家数据
        return cls.get_artist_by_id(artist_id)
    
    @classmethod
    def delete_artist(cls, artist_id: int) -> bool:
        """
        删除艺术家
        
        Args:
            artist_id: 艺术家 ID
            
        Returns:
            bool: 是否成功删除
        """
        collection = get_collection(cls.COLLECTION_NAME)
        
        # 删除艺术家
        result = collection.delete_one({"id": artist_id})
        
        # 返回是否成功删除
        return result.deleted_count > 0
    
    @classmethod
    def import_from_csv(cls, csv_path: str) -> Dict[str, Any]:
        """
        从 CSV 文件导入艺术家数据
        
        Args:
            csv_path: CSV 文件路径
            
        Returns:
            Dict[str, Any]: 导入结果
        """
        # 读取 CSV 文件
        df = pd.read_csv(csv_path)
        
        # 验证数据
        errors = Artist.validate_csv_data(df)
        if errors:
            return {
                "status": "error",
                "errors": errors,
                "rows_processed": 0
            }
        
        # 转换为记录列表
        records = df.to_dict('records')
        
        # 获取集合
        collection = get_collection(cls.COLLECTION_NAME)
        
        # 清除现有数据（可选）
        collection.delete_many({})
        
        # 插入记录
        if records:
            collection.insert_many(records)
        
        # 返回结果
        return {
            "status": "success",
            "rows_processed": len(records),
            "sample_records": json.loads(json_util.dumps(records[:3] if len(records) > 3 else records))
        } 