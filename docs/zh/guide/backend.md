# 后端

::: info 信息
本文档介绍 AIDA 项目的后端架构、API 设计和开发指南。
:::

## 技术栈

AIDA 后端使用以下技术：

- **FastAPI**：高性能的 Python Web 框架
- **MongoDB**：文档数据库
- **Pydantic**：数据验证和设置管理
- **Motor**：MongoDB 的异步 Python 驱动
- **Pytest**：测试框架

## 目录结构

后端代码位于项目根目录的 `/backend` 文件夹中，主要结构如下：

```
backend/
├── main.py              # 应用入口点
├── config/              # 配置文件
├── models/              # 数据模型
├── routes/              # API 路由
├── services/            # 业务逻辑
├── utils/               # 工具函数
└── tests/               # 测试代码
```

## API 设计

AIDA 后端 API 遵循 RESTful 设计原则，主要端点包括：

### 艺术家 API

- `GET /api/artists`：获取艺术家列表，支持分页和筛选
- `GET /api/artists/{id}`：获取特定艺术家详情
- `POST /api/artists`：创建新艺术家
- `PUT /api/artists/{id}`：更新艺术家信息
- `DELETE /api/artists/{id}`：删除艺术家

### 作品 API

- `GET /api/works`：获取作品列表
- `GET /api/works/{id}`：获取特定作品详情
- `GET /api/artists/{id}/works`：获取特定艺术家的所有作品

## 数据模型

### 艺术家模型

```python
class Artist(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None
    styles: List[str] = []
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 作品模型

```python
class Artwork(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    artist_id: str
    year: Optional[int] = None
    medium: Optional[str] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## 开发指南

### 设置开发环境

1. 确保已安装 Python 3.9+
2. 安装依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. 确保 MongoDB 服务正在运行

### 启动后端服务

```bash
cd backend
uvicorn main:app --reload
```

或者使用项目根目录的一键启动命令：

```bash
npm run dev:backend
```

### 访问 API 文档

启动后端服务后，可以通过以下地址访问自动生成的 API 文档：

- Swagger UI：http://localhost:8000/api/docs
- ReDoc：http://localhost:8000/api/redoc

## 测试

运行后端测试：

```bash
cd backend
pytest
```

## 最佳实践

1. **使用异步**：尽可能使用 FastAPI 的异步特性
2. **数据验证**：使用 Pydantic 模型进行数据验证
3. **依赖注入**：利用 FastAPI 的依赖注入系统
4. **错误处理**：统一处理异常和错误响应
5. **文档**：为 API 端点添加详细的文档注释

::: warning 注意
后端文档仍在完善中，更多详细内容将在后续更新。
::: 