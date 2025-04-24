#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单版Artsy爬虫 - 基于测试文件的执行方式

这个脚本直接参考test_scraper.py的执行方式，简单直接地执行爬虫，
没有复杂的错误处理和信号处理，专注于基本功能。
"""

import os
import sys
import time
import logging
import argparse
from artsy_scraper import ArtsyScraper

# 配置日志 - 直接输出到标准输出，避免编码问题
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("simple_scraper")

def run_scraper(num_artists, max_artworks, use_categories=True):
    """
    运行简单爬虫 - 基于test_scraper.py的模式
    
    参数:
        num_artists (int): 要爬取的艺术家数量
        max_artworks (int): 每位艺术家最多爬取的作品数量
        use_categories (bool): 是否使用分类爬取
    """
    logger.info(f"开始爬取，目标: {num_artists}位艺术家，每位最多{max_artworks}件作品")
    start_time = time.time()
    
    # 创建爬虫实例
    scraper = ArtsyScraper()
    scraper.checkpoint_interval = 10  # 每10个艺术家保存一次检查点
    
    try:
        # 根据参数决定是爬取分类还是主列表
        if use_categories:
            logger.info("使用分类模式爬取...")
            scraper.scrape_multiple_categories(
                max_artists_per_category=min(300, num_artists // 10),
                max_artworks=max_artworks
            )
        else:
            logger.info("使用主列表模式爬取...")
            scraper.scrape_artists_list(
                max_artists=num_artists,
                max_artworks=max_artworks
            )
        
        # 计算统计信息
        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # 打印结果
        logger.info(f"爬取完成！共爬取了 {len(scraper.artists)} 位艺术家，{len(scraper.artworks)} 件艺术品")
        logger.info(f"耗时: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
        
        if scraper.artists:
            logger.info(f"首位艺术家: {scraper.artists[0]['name']}")
        
        if scraper.artworks:
            logger.info(f"第一件艺术品: {scraper.artworks[0]['title']} by {scraper.artworks[0]['artist_name']}")
        
        # 保存数据
        scraper.save_data()
        
        return True
    
    except Exception as e:
        logger.error(f"爬取过程中出错: {str(e)}", exc_info=True)
        return False
    
    finally:
        # 确保关闭资源
        scraper.close()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='简单版Artsy爬虫')
    parser.add_argument('--num-artists', type=int, default=6000,
                      help='要爬取的艺术家数量，默认6000')
    parser.add_argument('--max-artworks', type=int, default=10,
                      help='每位艺术家最多爬取的作品数量，默认10')
    parser.add_argument('--use-categories', action='store_true',
                      help='使用分类模式爬取（推荐）')
    parser.add_argument('--test', action='store_true',
                      help='测试模式，只爬取少量数据')
    
    args = parser.parse_args()
    
    # 测试模式
    if args.test:
        logger.info("启动测试模式")
        num_artists = 2
        max_artworks = 2
    else:
        num_artists = args.num_artists
        max_artworks = args.max_artworks
    
    # 运行爬虫
    success = run_scraper(
        num_artists, 
        max_artworks, 
        use_categories=args.use_categories
    )
    
    if success:
        logger.info("✅ 爬虫成功完成!")
        sys.exit(0)
    else:
        logger.error("❌ 爬虫未成功完成!")
        sys.exit(1)

if __name__ == "__main__":
    # 确保数据目录存在
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "artsy")
    os.makedirs(os.path.join(data_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "checkpoints"), exist_ok=True)
    
    main() 