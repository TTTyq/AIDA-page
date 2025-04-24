# AIDA 艺术数据爬虫模块

这个目录包含了AIDA项目的艺术数据爬虫组件，主要用于从各大艺术网站采集艺术家和艺术品信息。

## 主要文件

- `artsy_scraper_app.py`: 爬虫GUI应用程序，整合了所有爬虫功能
- `artsy_scraper.py`: 核心爬虫类，提供基础爬取功能
- `simple_artsy_scraper.py`: 简单爬虫脚本，适合少量数据测试
- `mass_artsy_scraper.py`: 大规模爬虫脚本，适合大量数据采集
- `cleanup.py`: 数据清理工具，处理低质量和重复图片

## 使用方法

### 图形界面（推荐）

使用图形界面是最简单的方法，它整合了所有功能：

```bash
python scraper/artsy_scraper_app.py
```

或者使用项目根目录下的批处理文件：

```
run_artsy_tools.bat
```

然后选择 "启动GUI工具"。

### 命令行使用

如果需要命令行使用，可以直接调用相应的脚本：

#### 简单爬虫

```bash
python scraper/simple_artsy_scraper.py --num-artists 100 --max-artworks 10 --use-categories
```

#### 大规模爬虫

```bash
python scraper/mass_artsy_scraper.py --num-artists 2000 --max-artworks 30 --checkpoint-interval 10
```

#### 数据清理

```bash
python cleanup_data.py --min-size 15 --min-width 400 --min-height 400
```

## 输出数据

所有爬取的数据将保存在项目根目录的 `data/artsy` 文件夹下：

- `artsy_artists.csv`: 艺术家数据
- `artsy_artworks.csv`: 艺术品数据
- `images/`: 艺术品图片，按艺术家名称分类
- `images/low_quality/`: 低质量图片
- `images/duplicates/`: 重复图片
- `checkpoints/`: 检查点数据

## 开发说明

### 依赖安装

```bash
pip install -r scraper/requirements.txt
```

### 添加新爬虫源

如需添加新的数据源，建议继承 `ArtsyScraper` 类并实现相应的方法。

### 性能优化

- 对于大规模爬取，建议增加随机延迟避免被封禁
- 定期使用检查点保存进度
- 使用多线程可以提高图片下载速度

## 注意事项

- 请遵守数据源的使用条款和robots.txt规则
- 避免频繁高速爬取同一网站，以免IP被封
- 大规模爬取建议使用代理IP
- 定期备份重要数据 