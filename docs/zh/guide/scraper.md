# 爬虫

::: info 信息
本文档介绍 AIDA 项目的爬虫系统，用于收集艺术家和作品数据。
:::

## 技术栈

AIDA 爬虫系统使用以下技术：

- **Python**：编程语言
- **BeautifulSoup**：HTML 解析库
- **Selenium**：Web 自动化工具
- **Requests**：HTTP 请求库
- **Pandas**：数据处理库

## 目录结构

爬虫代码位于项目根目录的 `/scraper` 文件夹中，主要结构如下：

```
scraper/
├── main.py              # 爬虫入口点
├── config/              # 配置文件
├── spiders/             # 各网站的爬虫实现
├── processors/          # 数据处理器
├── utils/               # 工具函数
└── tests/               # 测试代码
```

## 支持的数据源

爬虫系统目前支持从以下数据源收集艺术家信息：

1. **WikiArt**：收集艺术家基本信息和作品
2. **MoMA**：现代艺术博物馆艺术家数据
3. **Artsy**：当代艺术平台数据
4. **国家美术馆**：各国国家美术馆艺术家数据

## 数据收集流程

爬虫系统的数据收集流程如下：

1. **初始化**：设置爬虫参数和目标网站
2. **页面抓取**：使用 Requests 或 Selenium 获取网页内容
3. **数据解析**：使用 BeautifulSoup 解析 HTML 提取数据
4. **数据清洗**：处理和规范化提取的数据
5. **数据存储**：将数据保存到 CSV 文件或直接写入数据库
6. **去重和合并**：处理来自不同源的重复数据

## 使用指南

### 设置开发环境

1. 确保已安装 Python 3.9+
2. 安装依赖：
   ```bash
   cd scraper
   pip install -r requirements.txt
   ```
3. 如果使用 Selenium，需要安装相应的浏览器驱动

### 运行爬虫

基本用法：

```bash
cd scraper
python main.py --source wikiart --limit 100
```

参数说明：
- `--source`：数据源名称（wikiart, moma, artsy 等）
- `--limit`：限制收集的艺术家数量
- `--output`：输出文件路径（默认为 `../data/artists.csv`）

### 数据导入

收集完数据后，可以使用以下命令将数据导入 MongoDB：

```bash
cd scraper
python import_to_db.py --file ../data/artists.csv
```

或者使用项目根目录的一键导入命令：

```bash
npm run import:data
```

## 最佳实践

1. **遵守网站规则**：尊重 robots.txt 和网站使用条款
2. **控制请求频率**：添加适当的延迟，避免对目标网站造成压力
3. **错误处理**：妥善处理网络错误和解析异常
4. **数据验证**：确保收集的数据符合预期格式
5. **增量更新**：支持只更新新数据，避免重复收集

## 开发计划

爬虫系统的未来开发计划包括：

- 增加更多艺术数据源
- 实现分布式爬虫架构
- 添加自动化调度功能
- 改进数据清洗和匹配算法
- 实现艺术风格和流派的自动分类

::: warning 注意
爬虫文档仍在完善中，更多详细内容将在后续更新。
::: 