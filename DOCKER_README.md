# AIDA项目 Docker容器化指南

本指南将帮助您使用Docker快速部署AIDA项目，确保在任何环境中都能稳定运行。

## 🚀 快速开始

### 前置要求

- Docker (版本 20.10+)
- Docker Compose (版本 2.0+)
- 至少 4GB 可用内存
- 至少 10GB 可用磁盘空间

### 一键启动

1. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd aida
   ```

2. **运行启动脚本**
   ```bash
   chmod +x docker-run.sh
   ./docker-run.sh
   ```

3. **配置环境变量**
   - 脚本会自动创建 `.env` 文件
   - 编辑 `.env` 文件，设置您的 OpenAI API 密钥：
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

4. **选择运行模式**
   - 开发模式：支持热重载，适合开发调试
   - 生产模式：优化构建，适合正式部署

## 📋 服务说明

### 开发模式服务

| 服务 | 端口 | 描述 |
|------|------|------|
| 前端 | 3000 | Next.js React应用 |
| 后端 | 8000 | FastAPI Python服务 |
| 文档 | 5173 | VitePress文档站点 |
| 数据库 | 27017 | MongoDB数据库 |

### 生产模式服务

| 服务 | 端口 | 描述 |
|------|------|------|
| Nginx | 80/443 | 反向代理和负载均衡 |
| 前端 | 内部 | 优化构建的React应用 |
| 后端 | 内部 | 生产环境FastAPI服务 |
| 文档 | 内部 | 静态文档站点 |
| 数据库 | 27017 | MongoDB数据库 |

## 🔧 手动操作

### 开发模式

```bash
# 启动开发环境
docker-compose up --build

# 后台运行
docker-compose up --build -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f
```

### 生产模式

```bash
# 启动生产环境
docker-compose -f docker-compose.prod.yml up --build -d

# 停止服务
docker-compose -f docker-compose.prod.yml down

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

## 🗄️ 数据管理

### 数据持久化

- MongoDB数据存储在Docker卷 `mongo-data` 中
- 数据在容器重启后会保持

### 数据备份

```bash
# 备份MongoDB数据
docker exec -it aida_mongo_1 mongodump --out /backup

# 从容器复制备份文件
docker cp aida_mongo_1:/backup ./mongodb-backup
```

### 数据恢复

```bash
# 复制备份文件到容器
docker cp ./mongodb-backup aida_mongo_1:/restore

# 恢复数据
docker exec -it aida_mongo_1 mongorestore /restore
```

## 🔍 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   lsof -i :3000
   lsof -i :8000
   lsof -i :27017
   
   # 修改docker-compose.yml中的端口映射
   ```

2. **内存不足**
   ```bash
   # 检查Docker内存限制
   docker system df
   docker system prune
   ```

3. **构建失败**
   ```bash
   # 清理Docker缓存
   docker builder prune
   docker system prune -a
   ```

4. **环境变量问题**
   ```bash
   # 检查.env文件
   cat .env
   
   # 重新创建.env文件
   cp env.example .env
   ```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongo

# 实时跟踪日志
docker-compose logs -f backend
```

### 容器调试

```bash
# 进入容器
docker exec -it aida_backend_1 /bin/bash
docker exec -it aida_frontend_1 /bin/sh
docker exec -it aida_mongo_1 /bin/bash

# 检查容器状态
docker ps
docker stats
```

## 🔒 安全配置

### 生产环境安全

1. **修改默认密码**
   ```bash
   # 在.env文件中设置强密码
   MONGO_INITDB_ROOT_PASSWORD=your_strong_password
   ```

2. **使用HTTPS**
   - 将SSL证书放在 `nginx/ssl/` 目录
   - 修改nginx配置启用HTTPS

3. **网络隔离**
   - 生产模式使用独立网络
   - 只暴露必要端口

## 📊 性能优化

### 资源限制

在docker-compose文件中添加资源限制：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

### 缓存优化

- 使用多阶段构建减少镜像大小
- 启用nginx gzip压缩
- 配置静态资源缓存

## 🤝 分享给朋友

### 打包分发

1. **导出镜像**
   ```bash
   # 构建所有镜像
   docker-compose -f docker-compose.prod.yml build
   
   # 导出镜像
   docker save -o aida-images.tar aida_backend aida_frontend aida_docs
   ```

2. **创建分发包**
   ```bash
   # 创建分发目录
   mkdir aida-distribution
   cp docker-compose.prod.yml aida-distribution/
   cp env.example aida-distribution/
   cp docker-run.sh aida-distribution/
   cp DOCKER_README.md aida-distribution/
   cp -r nginx aida-distribution/
   cp -r scripts aida-distribution/
   
   # 打包
   tar -czf aida-distribution.tar.gz aida-distribution/
   ```

### 朋友使用步骤

1. 解压分发包
2. 导入镜像：`docker load -i aida-images.tar`
3. 运行：`./docker-run.sh`
4. 配置环境变量
5. 访问应用

## 📞 支持

如果遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查GitHub Issues
3. 联系项目维护者

---

**注意**: 首次运行可能需要较长时间下载依赖和构建镜像，请耐心等待。 