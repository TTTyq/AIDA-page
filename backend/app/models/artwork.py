from typing import Optional, Dict, Any, List
import pandas as pd

class Artwork:
    """
    艺术品数据模型
    
    用于表示艺术品的基本信息和相关数据
    """
    
    def __init__(
        self,
        id: int,
        title: str,
        artist_id: int,
        year: Optional[int] = None,
        medium: Optional[str] = None,
        dimensions: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        **kwargs
    ):
        self.id = id
        self.title = title
        self.artist_id = artist_id
        self.year = year
        self.medium = medium
        self.dimensions = dimensions
        self.location = location
        self.description = description
        self.image_url = image_url
        
        # 存储其他可能的字段
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artwork':
        """
        从字典创建艺术品实例
        
        Args:
            data: 包含艺术品数据的字典
            
        Returns:
            Artwork: 艺术品实例
        """
        # 确保 id 字段存在
        if 'id' not in data:
            raise ValueError("Artwork data must contain 'id' field")
        
        # 确保 title 字段存在
        if 'title' not in data:
            raise ValueError("Artwork data must contain 'title' field")
            
        # 确保 artist_id 字段存在
        if 'artist_id' not in data:
            raise ValueError("Artwork data must contain 'artist_id' field")
        
        # 处理 NaN 值
        for key, value in data.items():
            if isinstance(value, float) and pd.isna(value):
                data[key] = None
                
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将艺术品实例转换为字典
        
        Returns:
            Dict[str, Any]: 包含艺术品数据的字典
        """
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')  # 排除私有属性
        }
    
    @staticmethod
    def validate_csv_data(df: pd.DataFrame) -> List[str]:
        """
        验证 CSV 数据是否符合艺术品模型要求
        
        Args:
            df: 包含艺术品数据的 DataFrame
            
        Returns:
            List[str]: 验证错误列表，如果没有错误则为空列表
        """
        errors = []
        
        # 检查必填字段
        if 'id' not in df.columns:
            errors.append("Missing required column: 'id'")
        if 'title' not in df.columns:
            errors.append("Missing required column: 'title'")
        if 'artist_id' not in df.columns:
            errors.append("Missing required column: 'artist_id'")
            
        # 检查 id 字段类型
        if 'id' in df.columns and not pd.api.types.is_numeric_dtype(df['id']):
            errors.append("Column 'id' must contain numeric values")
            
        # 检查 artist_id 字段类型
        if 'artist_id' in df.columns and not pd.api.types.is_numeric_dtype(df['artist_id']):
            errors.append("Column 'artist_id' must contain numeric values")
            
        # 检查 id 唯一性
        if 'id' in df.columns and df['id'].duplicated().any():
            errors.append("Column 'id' contains duplicate values")
            
        return errors 