from typing import List, Dict, Any, Optional
import pandas as pd
from bson import json_util
import json
import os
from pymongo.collection import Collection

from app.db.mongodb import get_database
from app.models.artwork import Artwork

class ArtworkService:
    """
    艺术品服务
    
    提供艺术品数据的CRUD操作
    """
    
    COLLECTION_NAME = "artworks"
    
    @classmethod
    def get_collection(cls) -> Collection:
        """
        获取艺术品集合
        
        Returns:
            Collection: MongoDB 集合对象
        """
        db = get_database()
        return db[cls.COLLECTION_NAME]
    
    @classmethod
    def get_all_artworks(cls) -> List[Dict[str, Any]]:
        """
        获取所有艺术品
        
        Returns:
            List[Dict[str, Any]]: 艺术品列表
        """
        collection = cls.get_collection()
        artworks = list(collection.find())
        
        # 将 MongoDB 的 _id 转换为字符串
        for artwork in artworks:
            if '_id' in artwork:
                artwork['_id'] = str(artwork['_id'])
                
        return artworks
    
    @classmethod
    def get_artwork_by_id(cls, artwork_id: int) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取艺术品
        
        Args:
            artwork_id: 艺术品 ID
            
        Returns:
            Optional[Dict[str, Any]]: 艺术品数据，如果不存在则返回 None
        """
        collection = cls.get_collection()
        artwork = collection.find_one({"id": artwork_id})
        
        if artwork and '_id' in artwork:
            artwork['_id'] = str(artwork['_id'])
            
        return artwork
    
    @classmethod
    def get_artworks_by_artist_id(cls, artist_id: int) -> List[Dict[str, Any]]:
        """
        根据艺术家 ID 获取艺术品
        
        Args:
            artist_id: 艺术家 ID
            
        Returns:
            List[Dict[str, Any]]: 艺术品列表
        """
        collection = cls.get_collection()
        artworks = list(collection.find({"artist_id": artist_id}))
        
        # 将 MongoDB 的 _id 转换为字符串
        for artwork in artworks:
            if '_id' in artwork:
                artwork['_id'] = str(artwork['_id'])
                
        return artworks
    
    @classmethod
    def create_artwork(cls, artwork_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建艺术品
        
        Args:
            artwork_data: 艺术品数据
            
        Returns:
            Dict[str, Any]: 创建的艺术品数据
        """
        collection = cls.get_collection()
        
        # 验证数据
        artwork = Artwork.from_dict(artwork_data)
        
        # 插入数据
        result = collection.insert_one(artwork.to_dict())
        
        # 获取插入的数据
        inserted_artwork = cls.get_artwork_by_id(artwork.id)
        
        return inserted_artwork
    
    @classmethod
    def update_artwork(cls, artwork_id: int, artwork_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新艺术品
        
        Args:
            artwork_id: 艺术品 ID
            artwork_data: 艺术品数据
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的艺术品数据，如果不存在则返回 None
        """
        collection = cls.get_collection()
        
        # 检查艺术品是否存在
        existing_artwork = cls.get_artwork_by_id(artwork_id)
        if not existing_artwork:
            return None
        
        # 更新数据
        collection.update_one(
            {"id": artwork_id},
            {"$set": artwork_data}
        )
        
        # 获取更新后的数据
        updated_artwork = cls.get_artwork_by_id(artwork_id)
        
        return updated_artwork
    
    @classmethod
    def delete_artwork(cls, artwork_id: int) -> bool:
        """
        删除艺术品
        
        Args:
            artwork_id: 艺术品 ID
            
        Returns:
            bool: 是否成功删除
        """
        collection = cls.get_collection()
        
        # 检查艺术品是否存在
        existing_artwork = cls.get_artwork_by_id(artwork_id)
        if not existing_artwork:
            return False
        
        # 删除数据
        result = collection.delete_one({"id": artwork_id})
        
        return result.deleted_count > 0
    
    @classmethod
    def import_from_csv(cls, csv_path: str) -> Dict[str, Any]:
        """
        从 CSV 文件导入艺术品数据
        
        Args:
            csv_path: CSV 文件路径
            
        Returns:
            Dict[str, Any]: 导入结果
        """
        try:
            # 读取 CSV 文件
            df = pd.read_csv(csv_path)
            
            # 验证数据
            errors = Artwork.validate_csv_data(df)
            if errors:
                return {
                    "status": "error",
                    "errors": errors
                }
            
            # 转换为字典列表
            records = df.to_dict(orient="records")
            
            # 清空集合
            collection = cls.get_collection()
            collection.delete_many({})
            
            # 插入数据
            artwork_objects = [Artwork.from_dict(record).to_dict() for record in records]
            collection.insert_many(artwork_objects)
            
            # 获取样本记录
            sample_records = cls.get_all_artworks()[:3]
            
            return {
                "status": "success",
                "rows_processed": len(records),
                "sample_records": sample_records
            }
        except Exception as e:
            return {
                "status": "error",
                "errors": [str(e)]
            } 