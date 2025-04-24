#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
清理数据目录中的测试数据

这个脚本会删除数据目录中的测试文件和日志文件，
同时保留artsy目录下的实际爬取数据。
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
logger = logging.getLogger("cleanup_data")

def cleanup_data_directory():
    """清理数据目录中的测试数据"""
    # 获取数据目录路径
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    
    if not os.path.exists(data_dir):
        logger.error(f"数据目录不存在: {data_dir}")
        return
    
    logger.info(f"开始清理数据目录: {data_dir}")
    
    # 清理根目录下的测试文件和日志文件
    files_to_delete = []
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        if os.path.isfile(file_path):
            # 删除测试文件和日志文件
            if file.startswith("test_") or file.endswith(".log"):
                files_to_delete.append(file_path)
    
    if files_to_delete:
        logger.info(f"将删除以下文件: {', '.join(os.path.basename(f) for f in files_to_delete)}")
        
        # 确认是否继续
        confirm = input("确认删除这些文件吗? [y/N]: ")
        if confirm.lower() != 'y':
            logger.info("操作已取消")
            return
        
        # 删除文件
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                logger.info(f"已删除: {os.path.basename(file_path)}")
            except Exception as e:
                logger.error(f"删除 {os.path.basename(file_path)} 时出错: {str(e)}")
    else:
        logger.info("没有找到需要删除的测试文件")
    
    # 清理logs目录
    logs_dir = os.path.join(data_dir, "logs")
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        log_files = [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f)) and f.endswith(".log")]
        
        if log_files:
            logger.info(f"将清理 logs 目录中的 {len(log_files)} 个日志文件")
            
            # 确认是否继续
            confirm = input("确认删除这些日志文件吗? [y/N]: ")
            if confirm.lower() != 'y':
                logger.info("操作已取消")
            else:
                for file in log_files:
                    file_path = os.path.join(logs_dir, file)
                    try:
                        os.remove(file_path)
                        logger.info(f"已删除: logs/{file}")
                    except Exception as e:
                        logger.error(f"删除 logs/{file} 时出错: {str(e)}")
        else:
            logger.info("logs 目录中没有日志文件")
    
    # 清理artsy目录下的测试文件，但保留目录结构和主要数据文件
    artsy_dir = os.path.join(data_dir, "artsy")
    if os.path.exists(artsy_dir) and os.path.isdir(artsy_dir):
        # 清理checkpoints目录
        checkpoints_dir = os.path.join(artsy_dir, "checkpoints")
        if os.path.exists(checkpoints_dir) and os.path.isdir(checkpoints_dir):
            checkpoint_files = [f for f in os.listdir(checkpoints_dir) if f.startswith("test_") or "temp" in f.lower()]
            
            if checkpoint_files:
                logger.info(f"将清理 artsy/checkpoints 目录中的 {len(checkpoint_files)} 个测试检查点文件")
                
                # 确认是否继续
                confirm = input("确认删除这些检查点文件吗? [y/N]: ")
                if confirm.lower() != 'y':
                    logger.info("操作已取消")
                else:
                    for file in checkpoint_files:
                        file_path = os.path.join(checkpoints_dir, file)
                        try:
                            os.remove(file_path)
                            logger.info(f"已删除: artsy/checkpoints/{file}")
                        except Exception as e:
                            logger.error(f"删除 artsy/checkpoints/{file} 时出错: {str(e)}")
            else:
                logger.info("artsy/checkpoints 目录中没有测试检查点文件")
    
    logger.info("数据目录清理完成")

if __name__ == "__main__":
    cleanup_data_directory() 