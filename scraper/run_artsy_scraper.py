#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Artsy爬虫统一运行脚本

这个脚本整合了所有爬虫相关操作，包括：
1. 启动GUI界面
2. 运行简单爬虫
3. 运行大规模爬虫 
4. 数据优化和清理

通过命令行参数选择不同的运行模式。
"""

import os
import sys
import time
import argparse
import logging
from datetime import datetime

# 配置日志
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"artsy_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("artsy_runner")

# 定义全局路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ARTSY_DIR = os.path.join(DATA_DIR, "artsy")
IMAGES_DIR = os.path.join(ARTSY_DIR, "images")
CHECKPOINTS_DIR = os.path.join(ARTSY_DIR, "checkpoints")

# 创建必要的目录
os.makedirs(ARTSY_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CHECKPOINTS_DIR, exist_ok=True)

def run_gui():
    """启动GUI界面"""
    logger.info("启动Artsy爬虫GUI界面...")
    try:
        from artsy_scraper_app import main as run_gui_main
        run_gui_main()
        return True
    except ImportError as e:
        logger.error(f"无法导入GUI模块: {str(e)}")
        logger.error("请确保artsy_scraper_app.py文件存在并且依赖已安装")
        return False
    except Exception as e:
        logger.error(f"启动GUI时出错: {str(e)}", exc_info=True)
        return False

def run_simple_scraper(args):
    """运行简单爬虫"""
    logger.info(f"启动简单爬虫 (艺术家: {args.num_artists}, 作品: {args.max_artworks}, 使用分类: {args.use_categories})")
    try:
        from simple_artsy_scraper import run_scraper
        
        success = run_scraper(
            num_artists=args.num_artists,
            max_artworks=args.max_artworks,
            use_categories=args.use_categories
        )
        
        if success:
            logger.info("简单爬虫运行成功完成")
        else:
            logger.error("简单爬虫运行失败")
        
        return success
    except ImportError as e:
        logger.error(f"无法导入简单爬虫模块: {str(e)}")
        logger.error("请确保simple_artsy_scraper.py文件存在并且依赖已安装")
        return False
    except Exception as e:
        logger.error(f"运行简单爬虫时出错: {str(e)}", exc_info=True)
        return False

def run_mass_scraper(args):
    """运行大规模爬虫"""
    logger.info(f"启动大规模爬虫 (艺术家: {args.num_artists}, 作品: {args.max_artworks}, 检查点间隔: {args.checkpoint_interval})")
    try:
        from mass_artsy_scraper import run_mass_scraper
        
        success = run_mass_scraper(
            num_artists=args.num_artists,
            max_artworks=args.max_artworks,
            checkpoint_interval=args.checkpoint_interval
        )
        
        if success:
            logger.info("大规模爬虫运行成功完成")
        else:
            logger.error("大规模爬虫运行失败或被中断")
        
        return success
    except ImportError as e:
        logger.error(f"无法导入大规模爬虫模块: {str(e)}")
        logger.error("请确保mass_artsy_scraper.py文件存在并且依赖已安装")
        return False
    except Exception as e:
        logger.error(f"运行大规模爬虫时出错: {str(e)}", exc_info=True)
        return False

def run_optimizer(args):
    """运行数据优化器"""
    logger.info("启动数据优化器...")
    try:
        from artsy_scraper_optimizer import ArtsyOptimizer
        
        optimizer = ArtsyOptimizer(
            min_image_size_kb=args.min_size,
            min_width=args.min_width,
            min_height=args.min_height,
            move_files=not args.delete
        )
        
        # 选择性运行优化任务
        if not args.no_quality:
            optimizer.clean_low_quality_images()
        
        if not args.no_duplicates:
            optimizer.remove_duplicates()
        
        if not args.no_rebuild:
            optimizer.rebuild_data_indices()
        
        logger.info("数据优化成功完成")
        return True
    except ImportError as e:
        logger.error(f"无法导入优化器模块: {str(e)}")
        logger.error("请确保artsy_scraper_optimizer.py文件存在并且依赖已安装")
        return False
    except Exception as e:
        logger.error(f"运行数据优化器时出错: {str(e)}", exc_info=True)
        return False

def main():
    """主函数，解析命令行参数并执行相应任务"""
    parser = argparse.ArgumentParser(description='Artsy艺术爬虫统一运行脚本')
    
    # 操作模式子解析器
    subparsers = parser.add_subparsers(dest='mode', help='运行模式')
    
    # GUI模式
    gui_parser = subparsers.add_parser('gui', help='启动图形界面')
    
    # 简单爬虫模式
    simple_parser = subparsers.add_parser('simple', help='运行简单爬虫')
    simple_parser.add_argument('--num-artists', type=int, default=100,
                             help='要爬取的艺术家数量，默认100')
    simple_parser.add_argument('--max-artworks', type=int, default=10,
                             help='每位艺术家最多爬取的作品数量，默认10')
    simple_parser.add_argument('--use-categories', action='store_true',
                             help='使用分类模式爬取（推荐）')
    
    # 大规模爬虫模式
    mass_parser = subparsers.add_parser('mass', help='运行大规模爬虫')
    mass_parser.add_argument('--num-artists', type=int, default=1000,
                           help='要爬取的艺术家总数量，默认1000')
    mass_parser.add_argument('--max-artworks', type=int, default=20,
                           help='每位艺术家最多爬取的作品数量，默认20')
    mass_parser.add_argument('--checkpoint-interval', type=int, default=10,
                           help='每爬取多少位艺术家保存一次检查点，默认10')
    
    # 优化工具模式
    optimizer_parser = subparsers.add_parser('optimize', help='运行数据优化工具')
    optimizer_parser.add_argument('--min-size', type=int, default=15,
                                help='最小图片文件大小（KB），默认15KB')
    optimizer_parser.add_argument('--min-width', type=int, default=400,
                                help='最小图片宽度（像素），默认400px')
    optimizer_parser.add_argument('--min-height', type=int, default=400,
                                help='最小图片高度（像素），默认400px')
    optimizer_parser.add_argument('--delete', action='store_true',
                                help='直接删除不合格的图片（默认是移动到特定目录）')
    optimizer_parser.add_argument('--no-duplicates', action='store_true',
                                help='跳过重复图片检测和处理')
    optimizer_parser.add_argument('--no-quality', action='store_true',
                                help='跳过低质量图片检测和处理')
    optimizer_parser.add_argument('--no-rebuild', action='store_true',
                                help='跳过数据索引重建')
    
    # 解析参数
    args = parser.parse_args()
    
    # 如果没有指定模式，显示帮助信息
    if not args.mode:
        parser.print_help()
        return False
    
    # 执行相应的操作
    if args.mode == 'gui':
        return run_gui()
    elif args.mode == 'simple':
        return run_simple_scraper(args)
    elif args.mode == 'mass':
        return run_mass_scraper(args)
    elif args.mode == 'optimize':
        return run_optimizer(args)

if __name__ == "__main__":
    # 确保数据目录存在
    os.makedirs(os.path.join(DATA_DIR, "logs"), exist_ok=True)
    
    start_time = time.time()
    success = main()
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    
    if success:
        logger.info(f"任务成功完成，总耗时: {int(minutes)}分钟 {int(seconds)}秒")
        sys.exit(0)
    else:
        logger.error(f"任务未成功完成，总耗时: {int(minutes)}分钟 {int(seconds)}秒")
        sys.exit(1) 