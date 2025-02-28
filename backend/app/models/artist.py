from typing import Optional, Dict, Any, List
import pandas as pd

class Artist:
    """
    艺术家数据模型
    
    用于表示艺术家的基本信息和相关数据
    """
    
    def __init__(
        self,
        id: int,
        name: str,
        birth_year: Optional[int] = None,
        death_year: Optional[int] = None,
        nationality: Optional[str] = None,
        bio: Optional[str] = None,
        art_movement: Optional[str] = None,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year
        self.nationality = nationality
        self.bio = bio
        self.art_movement = art_movement
        
        # 存储其他可能的字段
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artist':
        """
        从字典创建艺术家实例
        
        Args:
            data: 包含艺术家数据的字典
            
        Returns:
            Artist: 艺术家实例
        """
        # 确保 id 字段存在
        if 'id' not in data:
            raise ValueError("Artist data must contain 'id' field")
        
        # 处理 NaN 值
        for key, value in data.items():
            if isinstance(value, float) and pd.isna(value):
                data[key] = None
                
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将艺术家实例转换为字典
        
        Returns:
            Dict[str, Any]: 包含艺术家数据的字典
        """
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')  # 排除私有属性
        }
    
    @staticmethod
    def validate_csv_data(df: pd.DataFrame) -> List[str]:
        """
        验证 CSV 数据是否符合艺术家模型要求
        
        Args:
            df: 包含艺术家数据的 DataFrame
            
        Returns:
            List[str]: 验证错误列表，如果没有错误则为空列表
        """
        errors = []
        
        # 检查必填字段
        if 'id' not in df.columns:
            errors.append("Missing required column: 'id'")
        if 'name' not in df.columns:
            errors.append("Missing required column: 'name'")
            
        # 检查 id 字段类型
        if 'id' in df.columns and not pd.api.types.is_numeric_dtype(df['id']):
            errors.append("Column 'id' must contain numeric values")
            
        # 检查 id 唯一性
        if 'id' in df.columns and df['id'].duplicated().any():
            errors.append("Column 'id' contains duplicate values")
            
        return errors 