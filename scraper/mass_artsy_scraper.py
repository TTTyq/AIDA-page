#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
大规模Artsy爬虫 - 用于批量爬取艺术家数据

这个脚本基于simple_artsy_scraper.py但针对大规模爬取做了优化，
增加了检查点保存间隔设置，更好的日志记录和断点续传能力。
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime
from artsy_scraper import ArtsyScraper

# 配置日志
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"mass_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("mass_scraper")

def run_mass_scraper(num_artists, max_artworks, checkpoint_interval=10):
    """
    运行大规模爬虫 - 针对大量艺术家和作品
    
    参数:
        num_artists (int): 要爬取的艺术家数量
        max_artworks (int): 每位艺术家最多爬取的作品数量
        checkpoint_interval (int): 保存检查点的艺术家间隔
    """
    logger.info("="*80)
    logger.info(f"开始大规模爬取，目标: {num_artists}位艺术家，每位最多{max_artworks}件作品")
    logger.info(f"检查点保存间隔: 每{checkpoint_interval}位艺术家")
    logger.info("="*80)
    
    start_time = time.time()
    
    # 创建爬虫实例
    scraper = ArtsyScraper()
    scraper.checkpoint_interval = checkpoint_interval
    
    try:
        # 先爬取重要分类的艺术家
        logger.info("第1阶段: 爬取重要分类的艺术家...")
        categories_artists = min(num_artists // 3, 2000)  # 分配1/3的配额给分类，但最多2000
        per_category = max(10, categories_artists // len(scraper.important_artists_categories))
        
        scraper.scrape_multiple_categories(
            max_artists_per_category=per_category,
            max_artworks=max_artworks
        )
        
        phase1_artists = len(scraper.artists)
        logger.info(f"第1阶段完成: 已爬取{phase1_artists}位艺术家")
        
        # 然后爬取主艺术家列表，补足剩余的配额
        remaining_artists = max(0, num_artists - phase1_artists)
        if remaining_artists > 0:
            logger.info(f"第2阶段: 从主列表爬取剩余{remaining_artists}位艺术家...")
            
            scraper.scrape_artists_list(
                max_artists=remaining_artists,
                max_artworks=max_artworks
            )
        
        # 计算统计信息
        total_artists = len(scraper.artists)
        total_artworks = len(scraper.artworks)
        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # 打印结果
        logger.info("="*80)
        logger.info(f"爬取完成！共爬取了 {total_artists} 位艺术家，{total_artworks} 件艺术品")
        logger.info(f"平均每位艺术家 {total_artworks/total_artists:.1f} 件艺术品")
        logger.info(f"总耗时: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
        
        # 计算每分钟处理数量
        minutes_total = elapsed_time / 60
        artists_per_minute = total_artists / minutes_total if minutes_total > 0 else 0
        artworks_per_minute = total_artworks / minutes_total if minutes_total > 0 else 0
        
        logger.info(f"处理速度: {artists_per_minute:.1f} 艺术家/分钟, {artworks_per_minute:.1f} 艺术品/分钟")
        logger.info("="*80)
        
        # 保存最终数据
        scraper.save_data()
        
        return True
    
    except KeyboardInterrupt:
        logger.warning("检测到用户中断！正在保存已爬取的数据...")
        scraper.save_data()
        logger.info(f"已保存中断时的数据：{len(scraper.artists)}位艺术家，{len(scraper.artworks)}件艺术品")
        return False
    
    except Exception as e:
        logger.error(f"爬取过程中出错: {str(e)}", exc_info=True)
        # 尝试保存已爬取的数据
        try:
            scraper.save_data()
            logger.info(f"已保存错误前的数据：{len(scraper.artists)}位艺术家，{len(scraper.artworks)}件艺术品")
        except:
            logger.error("保存数据时出错", exc_info=True)
        return False
    
    finally:
        # 确保关闭资源
        scraper.close()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='大规模Artsy艺术家爬虫')
    parser.add_argument('--num-artists', type=int, default=10000,
                      help='要爬取的艺术家总数量，默认10000')
    parser.add_argument('--max-artworks', type=int, default=30,
                      help='每位艺术家最多爬取的作品数量，默认30')
    parser.add_argument('--checkpoint-interval', type=int, default=10,
                      help='每爬取多少位艺术家保存一次检查点，默认10')
    parser.add_argument('--test', action='store_true',
                      help='测试模式，只爬取少量数据')
    
    args = parser.parse_args()
    
    # 测试模式
    if args.test:
        logger.info("启动测试模式")
        num_artists = 5
        max_artworks = 2
        checkpoint_interval = 2
    else:
        num_artists = args.num_artists
        max_artworks = args.max_artworks
        checkpoint_interval = args.checkpoint_interval
    
    # 运行爬虫
    success = run_mass_scraper(
        num_artists=num_artists, 
        max_artworks=max_artworks, 
        checkpoint_interval=checkpoint_interval
    )
    
    if success:
        logger.info("✅ 大规模爬虫成功完成!")
        sys.exit(0)
    else:
        logger.error("❌ 大规模爬虫未完全完成!")
        sys.exit(1)

if __name__ == "__main__":
    # 确保数据目录存在
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "artsy")
    os.makedirs(os.path.join(data_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "checkpoints"), exist_ok=True)
    
    main() 