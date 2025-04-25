#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Artsy爬虫优化工具

此脚本用于整理和优化Artsy爬虫功能，包括：
1. 优化数据存储结构
2. 移除重复图片
3. 清理低质量图片
4. 重建索引和文档
5. 检查和修复不完整数据
"""

import os
import sys
import time
import hashlib
import shutil
import logging
import argparse
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from PIL import Image, ImageFile
import json

# 允许打开截断的图片
ImageFile.LOAD_TRUNCATED_IMAGES = True

# 配置日志
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"artsy_optimizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("artsy_optimizer")

# 定义全局路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ARTSY_DIR = os.path.join(DATA_DIR, "artsy")
IMAGES_DIR = os.path.join(ARTSY_DIR, "images")
LOW_QUALITY_DIR = os.path.join(IMAGES_DIR, "low_quality")
DUPLICATES_DIR = os.path.join(IMAGES_DIR, "duplicates")

# 创建必要的目录
os.makedirs(ARTSY_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(LOW_QUALITY_DIR, exist_ok=True)
os.makedirs(DUPLICATES_DIR, exist_ok=True)

class ArtsyOptimizer:
    """Artsy爬虫数据优化器"""
    
    def __init__(self, min_image_size_kb=15, min_width=400, min_height=400, move_files=True):
        """
        初始化优化器
        
        参数:
            min_image_size_kb (int): 最小图片文件大小（KB）
            min_width (int): 最小图片宽度（像素）
            min_height (int): 最小图片高度（像素）
            move_files (bool): 是否移动不合格文件（True）或直接删除（False）
        """
        self.min_image_size_kb = min_image_size_kb
        self.min_width = min_width
        self.min_height = min_height
        self.move_files = move_files
        
        # 统计
        self.stats = {
            'total_images': 0,
            'low_quality': 0,
            'duplicates': 0,
            'errors': 0,
            'artists': 0
        }
        
        # 读取现有数据
        self.artists_df = None
        self.artworks_df = None
        self.load_data()
    
    def load_data(self):
        """加载现有CSV数据"""
        artists_file = os.path.join(ARTSY_DIR, "artsy_artists.csv")
        artworks_file = os.path.join(ARTSY_DIR, "artsy_artworks.csv")
        
        if os.path.exists(artists_file):
            try:
                self.artists_df = pd.read_csv(artists_file)
                logger.info(f"加载了 {len(self.artists_df)} 位艺术家数据")
            except Exception as e:
                logger.error(f"加载艺术家数据时出错: {str(e)}")
                self.artists_df = pd.DataFrame()
        else:
            logger.warning("艺术家数据文件不存在")
            self.artists_df = pd.DataFrame()
            
        if os.path.exists(artworks_file):
            try:
                self.artworks_df = pd.read_csv(artworks_file)
                logger.info(f"加载了 {len(self.artworks_df)} 件艺术品数据")
            except Exception as e:
                logger.error(f"加载艺术品数据时出错: {str(e)}")
                self.artworks_df = pd.DataFrame()
        else:
            logger.warning("艺术品数据文件不存在")
            self.artworks_df = pd.DataFrame()
    
    def clean_low_quality_images(self):
        """清理低质量图片"""
        logger.info(f"开始清理低质量图片 (最小尺寸: {self.min_width}x{self.min_height}, 最小大小: {self.min_image_size_kb}KB)")
        
        # 创建低质量图片目录
        os.makedirs(LOW_QUALITY_DIR, exist_ok=True)
        
        # 遍历所有艺术家文件夹
        artist_dirs = [d for d in os.listdir(IMAGES_DIR) if os.path.isdir(os.path.join(IMAGES_DIR, d)) and d not in ["low_quality", "duplicates"]]
        self.stats['artists'] = len(artist_dirs)
        
        for artist_dir in tqdm(artist_dirs, desc="处理艺术家目录"):
            artist_path = os.path.join(IMAGES_DIR, artist_dir)
            
            # 跳过特殊目录
            if artist_dir in ["low_quality", "duplicates"]:
                continue
                
            # 扫描所有图片文件
            image_files = [f for f in os.listdir(artist_path) if os.path.isfile(os.path.join(artist_path, f)) and 
                          f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            
            self.stats['total_images'] += len(image_files)
            
            for img_file in image_files:
                img_path = os.path.join(artist_path, img_file)
                
                try:
                    # 检查文件大小
                    file_size_kb = os.path.getsize(img_path) / 1024
                    
                    if file_size_kb < self.min_image_size_kb:
                        self._handle_low_quality(img_path, artist_dir, img_file, f"小于{self.min_image_size_kb}KB")
                        continue
                    
                    # 检查图片尺寸
                    with Image.open(img_path) as img:
                        width, height = img.size
                        
                        if width < self.min_width or height < self.min_height:
                            self._handle_low_quality(img_path, artist_dir, img_file, f"尺寸({width}x{height})小于最小要求")
                
                except Exception as e:
                    logger.error(f"处理图片 {img_path} 时出错: {str(e)}")
                    self.stats['errors'] += 1
        
        logger.info(f"低质量图片清理完成: 找到 {self.stats['low_quality']} 张低质量图片")
    
    def _handle_low_quality(self, img_path, artist_dir, img_file, reason):
        """处理低质量图片"""
        self.stats['low_quality'] += 1
        
        if self.move_files:
            # 创建艺术家专属的低质量图片目录
            artist_low_quality_dir = os.path.join(LOW_QUALITY_DIR, artist_dir)
            os.makedirs(artist_low_quality_dir, exist_ok=True)
            
            # 移动文件
            target_path = os.path.join(artist_low_quality_dir, img_file)
            try:
                shutil.move(img_path, target_path)
                logger.debug(f"已移动低质量图片: {img_path} -> {target_path} ({reason})")
            except Exception as e:
                logger.error(f"移动图片 {img_path} 时出错: {str(e)}")
                self.stats['errors'] += 1
        else:
            # 直接删除文件
            try:
                os.remove(img_path)
                logger.debug(f"已删除低质量图片: {img_path} ({reason})")
            except Exception as e:
                logger.error(f"删除图片 {img_path} 时出错: {str(e)}")
                self.stats['errors'] += 1
    
    def remove_duplicates(self):
        """删除重复图片"""
        logger.info("开始查找重复图片...")
        
        # 创建重复图片目录
        os.makedirs(DUPLICATES_DIR, exist_ok=True)
        
        # 用于存储所有图片哈希值
        image_hashes = {}
        
        # 遍历所有艺术家文件夹
        artist_dirs = [d for d in os.listdir(IMAGES_DIR) if os.path.isdir(os.path.join(IMAGES_DIR, d)) and d not in ["low_quality", "duplicates"]]
        
        for artist_dir in tqdm(artist_dirs, desc="查找重复图片"):
            artist_path = os.path.join(IMAGES_DIR, artist_dir)
            
            # 跳过特殊目录
            if artist_dir in ["low_quality", "duplicates"]:
                continue
                
            # 扫描所有图片文件
            image_files = [f for f in os.listdir(artist_path) if os.path.isfile(os.path.join(artist_path, f)) and 
                          f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            
            for img_file in image_files:
                img_path = os.path.join(artist_path, img_file)
                
                try:
                    # 计算图片哈希值
                    img_hash = self._calculate_image_hash(img_path)
                    
                    if img_hash in image_hashes:
                        # 发现重复
                        self.stats['duplicates'] += 1
                        orig_path = image_hashes[img_hash]
                        
                        # 文件大小
                        orig_size = os.path.getsize(orig_path)
                        current_size = os.path.getsize(img_path)
                        
                        # 默认保留大小较大的文件
                        if current_size > orig_size:
                            # 新文件更大，移动旧文件到重复目录
                            to_move_path = orig_path
                            to_keep_path = img_path
                            # 更新哈希字典
                            image_hashes[img_hash] = img_path
                        else:
                            # 旧文件更大或相等，移动新文件到重复目录
                            to_move_path = img_path
                            to_keep_path = orig_path
                        
                        # 处理重复文件
                        if self.move_files:
                            # 获取相对路径作为目标路径
                            rel_path = os.path.relpath(to_move_path, IMAGES_DIR)
                            target_dir = os.path.dirname(os.path.join(DUPLICATES_DIR, rel_path))
                            os.makedirs(target_dir, exist_ok=True)
                            
                            # 移动文件
                            target_path = os.path.join(DUPLICATES_DIR, rel_path)
                            try:
                                shutil.move(to_move_path, target_path)
                                logger.debug(f"已移动重复图片: {to_move_path} -> {target_path}")
                            except Exception as e:
                                logger.error(f"移动重复图片 {to_move_path} 时出错: {str(e)}")
                                self.stats['errors'] += 1
                        else:
                            # 删除文件
                            try:
                                os.remove(to_move_path)
                                logger.debug(f"已删除重复图片: {to_move_path}")
                            except Exception as e:
                                logger.error(f"删除重复图片 {to_move_path} 时出错: {str(e)}")
                                self.stats['errors'] += 1
                    else:
                        # 添加到哈希字典
                        image_hashes[img_hash] = img_path
                
                except Exception as e:
                    logger.error(f"处理图片 {img_path} 时出错: {str(e)}")
                    self.stats['errors'] += 1
        
        logger.info(f"重复图片处理完成: 找到 {self.stats['duplicates']} 张重复图片")
    
    def _calculate_image_hash(self, img_path, block_size=8):
        """计算图片的感知哈希"""
        try:
            with Image.open(img_path) as img:
                # 转换为灰度图
                img = img.convert('L').resize((block_size, block_size), Image.LANCZOS)
                
                # 计算平均值
                pixels = list(img.getdata())
                avg = sum(pixels) / len(pixels)
                
                # 生成hash值
                bits = ''.join('1' if pixel >= avg else '0' for pixel in pixels)
                return bits
        except Exception as e:
            # 如果无法计算感知哈希，回退到文件MD5
            try:
                with open(img_path, 'rb') as f:
                    return hashlib.md5(f.read()).hexdigest()
            except Exception as e2:
                logger.error(f"计算图片 {img_path} 哈希值时出错: {str(e)} -> {str(e2)}")
                return None
    
    def rebuild_data_indices(self):
        """重建数据索引"""
        logger.info("开始重建数据索引...")
        
        # 统计所有艺术家的图片数量
        artist_stats = {}
        updated_artworks = []
        
        # 遍历所有艺术家文件夹
        artist_dirs = [d for d in os.listdir(IMAGES_DIR) if os.path.isdir(os.path.join(IMAGES_DIR, d)) and d not in ["low_quality", "duplicates"]]
        
        for artist_dir in tqdm(artist_dirs, desc="重建索引"):
            artist_path = os.path.join(IMAGES_DIR, artist_dir)
            
            # 跳过特殊目录
            if artist_dir in ["low_quality", "duplicates"]:
                continue
            
            # 扫描所有图片文件
            image_files = [f for f in os.listdir(artist_path) if os.path.isfile(os.path.join(artist_path, f)) and 
                          f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            
            # 更新艺术家统计
            artist_stats[artist_dir] = len(image_files)
            
            # 更新艺术品索引
            if self.artworks_df is not None and not self.artworks_df.empty:
                for img_file in image_files:
                    # 查找对应的艺术品记录
                    artwork_records = self.artworks_df[
                        (self.artworks_df['artist_name'] == artist_dir) & 
                        (self.artworks_df['image_filename'].str.contains(img_file.split('_')[0], na=False))
                    ]
                    
                    if not artwork_records.empty:
                        for _, artwork in artwork_records.iterrows():
                            # 验证图片存在
                            artwork_dict = artwork.to_dict()
                            artwork_dict['image_exists'] = True
                            artwork_dict['image_filename'] = img_file
                            updated_artworks.append(artwork_dict)
        
        # 更新艺术家数据
        if self.artists_df is not None and not self.artists_df.empty:
            for idx, artist in self.artists_df.iterrows():
                artist_name = artist['name']
                if artist_name in artist_stats:
                    self.artists_df.at[idx, 'artwork_count'] = artist_stats.get(artist_name, 0)
        
        # 保存更新的数据
        if updated_artworks:
            updated_df = pd.DataFrame(updated_artworks)
            output_file = os.path.join(ARTSY_DIR, f"artsy_artworks_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            updated_df.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"已保存更新的艺术品数据: {output_file}")
        
        if self.artists_df is not None and not self.artists_df.empty:
            output_file = os.path.join(ARTSY_DIR, f"artsy_artists_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            self.artists_df.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"已保存更新的艺术家数据: {output_file}")
        
        logger.info("数据索引重建完成")
    
    def run_all_optimizations(self):
        """运行所有优化任务"""
        start_time = time.time()
        
        # 清理低质量图片
        self.clean_low_quality_images()
        
        # 删除重复图片
        self.remove_duplicates()
        
        # 重建数据索引
        self.rebuild_data_indices()
        
        # 汇总统计信息
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        
        logger.info("="*80)
        logger.info("优化完成! 统计信息:")
        logger.info(f"- 处理艺术家目录: {self.stats['artists']}个")
        logger.info(f"- 扫描图片总数: {self.stats['total_images']}张")
        logger.info(f"- 低质量图片: {self.stats['low_quality']}张")
        logger.info(f"- 重复图片: {self.stats['duplicates']}张")
        logger.info(f"- 处理错误: {self.stats['errors']}个")
        logger.info(f"- 总耗时: {int(minutes)}分钟 {int(seconds)}秒")
        logger.info("="*80)
        
        return self.stats

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Artsy爬虫数据优化工具')
    parser.add_argument('--min-size', type=int, default=15,
                      help='最小图片文件大小（KB），默认15KB')
    parser.add_argument('--min-width', type=int, default=400,
                      help='最小图片宽度（像素），默认400px')
    parser.add_argument('--min-height', type=int, default=400,
                      help='最小图片高度（像素），默认400px')
    parser.add_argument('--delete', action='store_true',
                      help='直接删除不合格的图片（默认是移动到特定目录）')
    parser.add_argument('--no-duplicates', action='store_true',
                      help='跳过重复图片检测和处理')
    parser.add_argument('--no-quality', action='store_true',
                      help='跳过低质量图片检测和处理')
    parser.add_argument('--no-rebuild', action='store_true',
                      help='跳过数据索引重建')
    
    args = parser.parse_args()
    
    # 创建优化器
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
    
    logger.info("优化任务已完成")

if __name__ == "__main__":
    main() 