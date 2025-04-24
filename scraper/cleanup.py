#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
清理爬虫目录中的不相关文件

这个脚本会删除爬虫目录中的不相关文件，只保留必要的文件：
- artsy_scraper.py (主爬虫类)
- simple_artsy_scraper.py (简化版爬虫执行程序)
- mass_artsy_scraper.py (大规模爬虫执行程序)
- requirements.txt (依赖)
- cleanup.py (当前清理脚本)
"""

import os
import sys
import shutil
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("cleanup")

# 要保留的文件
KEEP_FILES = [
    'artsy_scraper.py',        # 主爬虫类
    'simple_artsy_scraper.py', # 简化版爬虫执行程序
    'mass_artsy_scraper.py',   # 大规模爬虫执行程序
    'requirements.txt',        # 依赖
    'cleanup.py'               # 当前脚本
]

def cleanup_directory():
    """清理当前目录中的不相关文件"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    logger.info(f"开始清理目录: {current_dir}")
    logger.info(f"将保留以下文件: {', '.join(KEEP_FILES)}")
    
    # 获取当前目录中的所有文件
    all_files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    
    # 计算要删除的文件
    files_to_delete = [f for f in all_files if f not in KEEP_FILES]
    
    if not files_to_delete:
        logger.info("没有需要删除的文件")
        return
    
    logger.info(f"将删除以下文件: {', '.join(files_to_delete)}")
    
    # 确认是否继续
    confirm = input("确认删除这些文件吗? [y/N]: ")
    if confirm.lower() != 'y':
        logger.info("操作已取消")
        return
    
    # 删除文件
    for file in files_to_delete:
        file_path = os.path.join(current_dir, file)
        try:
            os.remove(file_path)
            logger.info(f"已删除: {file}")
        except Exception as e:
            logger.error(f"删除 {file} 时出错: {str(e)}")
    
    # 删除__pycache__目录
    pycache_dir = os.path.join(current_dir, '__pycache__')
    if os.path.exists(pycache_dir) and os.path.isdir(pycache_dir):
        try:
            shutil.rmtree(pycache_dir)
            logger.info("已删除: __pycache__/")
        except Exception as e:
            logger.error(f"删除 __pycache__/ 时出错: {str(e)}")
    
    logger.info("清理完成")

if __name__ == "__main__":
    cleanup_directory() 