#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Artsy艺术爬虫应用 - GUI界面

这个应用程序整合了所有爬虫功能，包括：
- 基本爬虫（简单模式）
- 大规模爬虫（大量数据）
- 数据清理功能

提供了图形界面，方便用户操作。
"""

import os
import sys
import time
import logging
import argparse
import threading
import hashlib
import shutil
import pandas as pd
from datetime import datetime
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, 
                            QTextEdit, QProgressBar, QComboBox, QFileDialog, QSpinBox, 
                            QGroupBox, QRadioButton, QMessageBox, QToolTip, QSplitter,
                            QScrollArea, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QDir, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor, QColor, QPalette

# 导入主爬虫类
from artsy_scraper import ArtsyScraper

# 配置日志
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"artsy_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("artsy_app")

# 定义全局路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ARTSY_DIR = os.path.join(DATA_DIR, "artsy")
IMAGES_DIR = os.path.join(ARTSY_DIR, "images")
CHECKPOINTS_DIR = os.path.join(ARTSY_DIR, "checkpoints")
LOW_QUALITY_DIR = os.path.join(IMAGES_DIR, "low_quality")
DUPLICATES_DIR = os.path.join(IMAGES_DIR, "duplicates")

# 创建必要的目录
os.makedirs(ARTSY_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CHECKPOINTS_DIR, exist_ok=True)
os.makedirs(LOW_QUALITY_DIR, exist_ok=True)
os.makedirs(DUPLICATES_DIR, exist_ok=True)

# 爬虫工作线程
class ScraperThread(QThread):
    """爬虫后台线程"""
    update_signal = pyqtSignal(str)  # 用于更新UI的信号
    progress_signal = pyqtSignal(int)  # 进度条信号
    finished_signal = pyqtSignal(bool)  # 完成信号，带有成功/失败状态

    def __init__(self, mode, num_artists, max_artworks, checkpoint_interval, use_categories):
        super().__init__()
        self.mode = mode  # 'simple' 或 'mass'
        self.num_artists = num_artists
        self.max_artworks = max_artworks
        self.checkpoint_interval = checkpoint_interval
        self.use_categories = use_categories
        self.running = True
        self.scraper = None
        
    def run(self):
        """线程主要运行函数"""
        start_time = time.time()
        
        try:
            # 创建爬虫实例
            self.scraper = ArtsyScraper()
            self.scraper.checkpoint_interval = self.checkpoint_interval
            
            # 根据模式执行不同的爬取策略
            if self.mode == 'simple':
                self.run_simple_mode()
            else:  # 'mass'
                self.run_mass_mode()
                
            # 统计和报告
            elapsed_time = time.time() - start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if self.scraper:
                total_artists = len(self.scraper.artists)
                total_artworks = len(self.scraper.artworks)
                
                msg = f"爬取完成！共爬取了 {total_artists} 位艺术家，{total_artworks} 件艺术品\n"
                msg += f"总耗时: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒"
                
                if total_artists > 0:
                    msg += f"\n平均每位艺术家 {total_artworks/total_artists:.1f} 件艺术品"
                
                self.update_signal.emit(msg)
                self.finished_signal.emit(True)
            else:
                self.update_signal.emit("爬取过程中出现错误，未能完成")
                self.finished_signal.emit(False)
                
        except Exception as e:
            error_msg = f"爬取过程中出错: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.update_signal.emit(error_msg)
            self.finished_signal.emit(False)
            
        finally:
            # 确保关闭资源
            if self.scraper:
                try:
                    self.scraper.save_data()
                    self.scraper.close()
                except:
                    pass
    
    def run_simple_mode(self):
        """运行简单模式"""
        self.update_signal.emit(f"开始简单爬取，目标: {self.num_artists}位艺术家，每位最多{self.max_artworks}件作品")
        
        # 根据参数决定是爬取分类还是主列表
        if self.use_categories:
            self.update_signal.emit("使用分类模式爬取...")
            self.scraper.scrape_multiple_categories(
                max_artists_per_category=min(300, self.num_artists // 10),
                max_artworks=self.max_artworks
            )
        else:
            self.update_signal.emit("使用主列表模式爬取...")
            self.scraper.scrape_artists_list(
                max_artists=self.num_artists,
                max_artworks=self.max_artworks
            )
    
    def run_mass_mode(self):
        """运行大规模模式"""
        self.update_signal.emit(f"开始大规模爬取，目标: {self.num_artists}位艺术家，每位最多{self.max_artworks}件作品")
        
        # 先爬取重要分类的艺术家
        self.update_signal.emit("第1阶段: 爬取重要分类的艺术家...")
        categories_artists = min(self.num_artists // 3, 2000)  # 分配1/3的配额给分类，但最多2000
        per_category = max(10, categories_artists // len(self.scraper.important_artists_categories))
        
        self.scraper.scrape_multiple_categories(
            max_artists_per_category=per_category,
            max_artworks=self.max_artworks
        )
        
        phase1_artists = len(self.scraper.artists)
        self.update_signal.emit(f"第1阶段完成: 已爬取{phase1_artists}位艺术家")
        
        # 然后爬取主艺术家列表，补足剩余的配额
        remaining_artists = max(0, self.num_artists - phase1_artists)
        if remaining_artists > 0:
            self.update_signal.emit(f"第2阶段: 从主列表爬取剩余{remaining_artists}位艺术家...")
            
            self.scraper.scrape_artists_list(
                max_artists=remaining_artists,
                max_artworks=self.max_artworks
            )
    
    def stop(self):
        """停止爬虫"""
        self.running = False
        self.update_signal.emit("用户请求停止爬虫，正在保存已爬取的数据...")
        
        if self.scraper:
            try:
                self.scraper.save_data()
                total_artists = len(self.scraper.artists)
                total_artworks = len(self.scraper.artworks)
                self.update_signal.emit(f"已保存中断时的数据：{total_artists}位艺术家，{total_artworks}件艺术品")
            except Exception as e:
                self.update_signal.emit(f"保存数据时出错: {str(e)}")

# 清理工作线程
class CleanupThread(QThread):
    """清理数据的后台线程"""
    update_signal = pyqtSignal(str)  # 用于更新UI的信号
    progress_signal = pyqtSignal(int)  # 进度条信号
    finished_signal = pyqtSignal(bool)  # 完成信号，带有成功/失败状态

    def __init__(self, min_size_kb, min_dimensions, move_files, rebuild_docs):
        super().__init__()
        self.min_size_kb = min_size_kb
        self.min_dimensions = min_dimensions
        self.move_files = move_files
        self.rebuild_docs = rebuild_docs
        self.total_processed = 0
        self.low_quality_count = 0
        self.duplicate_count = 0
        
    def run(self):
        """线程主要运行函数"""
        try:
            self.update_signal.emit("开始清理图片...")
            
            # 清理图片
            result = self.cleanup_images(
                min_size_kb=self.min_size_kb,
                min_dimensions=self.min_dimensions,
                move_files=self.move_files
            )
            
            if result:
                self.update_signal.emit(f"清理完成！处理了 {self.total_processed} 张图片")
                self.update_signal.emit(f"发现 {self.low_quality_count} 张低质量图片")
                self.update_signal.emit(f"发现 {self.duplicate_count} 张重复图片")
                
                # 重建文档
                if self.rebuild_docs:
                    self.update_signal.emit("开始重建艺术家文档...")
                    self.update_artist_docs()
                    self.update_signal.emit("文档重建完成！")
                
                self.finished_signal.emit(True)
            else:
                self.update_signal.emit("清理过程中遇到错误")
                self.finished_signal.emit(False)
                
        except Exception as e:
            error_msg = f"清理过程中出错: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.update_signal.emit(error_msg)
            self.finished_signal.emit(False) 

# 主应用界面
class ArtsyScraperApp(QMainWindow):
    """Artsy艺术爬虫应用主界面"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Artsy艺术爬虫应用")
        self.setGeometry(100, 100, 900, 600)
        
        # 设置应用图标
        # self.setWindowIcon(QIcon("icon.png"))
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 创建各个标签页
        self.create_scraper_tab()
        self.create_cleanup_tab()
        self.create_stats_tab()
        
        # 初始化线程变量
        self.scraper_thread = None
        self.cleanup_thread = None
        
        # 显示状态栏
        self.statusBar().showMessage("就绪")
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #1e88e5;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:disabled {
                background-color: #b0bec5;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: #fafafa;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                background-color: #f5f5f5;
            }
            QProgressBar::chunk {
                background-color: #1e88e5;
                width: 10px;
            }
        """)
    
    def create_scraper_tab(self):
        """创建爬虫标签页"""
        scraper_tab = QWidget()
        self.tabs.addTab(scraper_tab, "爬虫")
        
        layout = QVBoxLayout()
        
        # 创建模式选择区域
        mode_group = QGroupBox("爬虫模式")
        mode_layout = QVBoxLayout()
        
        self.simple_mode_radio = QRadioButton("简单模式 - 适合少量艺术家")
        self.mass_mode_radio = QRadioButton("大规模模式 - 适合大量数据")
        self.simple_mode_radio.setChecked(True)
        
        mode_layout.addWidget(self.simple_mode_radio)
        mode_layout.addWidget(self.mass_mode_radio)
        mode_group.setLayout(mode_layout)
        
        # 创建参数设置区域
        params_group = QGroupBox("爬虫参数")
        params_layout = QGridLayout()
        
        # 艺术家数量
        params_layout.addWidget(QLabel("艺术家数量:"), 0, 0)
        self.num_artists_spin = QSpinBox()
        self.num_artists_spin.setRange(1, 10000)
        self.num_artists_spin.setValue(500)
        params_layout.addWidget(self.num_artists_spin, 0, 1)
        
        # 每位艺术家作品数量
        params_layout.addWidget(QLabel("每位艺术家最多作品数:"), 1, 0)
        self.max_artworks_spin = QSpinBox()
        self.max_artworks_spin.setRange(1, 100)
        self.max_artworks_spin.setValue(20)
        params_layout.addWidget(self.max_artworks_spin, 1, 1)
        
        # 检查点间隔
        params_layout.addWidget(QLabel("检查点保存间隔:"), 2, 0)
        self.checkpoint_spin = QSpinBox()
        self.checkpoint_spin.setRange(1, 100)
        self.checkpoint_spin.setValue(10)
        params_layout.addWidget(self.checkpoint_spin, 2, 1)
        
        # 使用分类
        self.use_categories_check = QCheckBox("使用分类模式爬取（推荐）")
        self.use_categories_check.setChecked(True)
        params_layout.addWidget(self.use_categories_check, 3, 0, 1, 2)
        
        params_group.setLayout(params_layout)
        
        # 创建按钮区域
        buttons_layout = QHBoxLayout()
        
        self.start_button = QPushButton("开始爬取")
        self.start_button.clicked.connect(self.start_scraper)
        
        self.stop_button = QPushButton("停止爬取")
        self.stop_button.clicked.connect(self.stop_scraper)
        self.stop_button.setEnabled(False)
        
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        
        # 创建日志区域
        self.scraper_log = QTextEdit()
        self.scraper_log.setReadOnly(True)
        
        # 创建进度条
        self.scraper_progress = QProgressBar()
        self.scraper_progress.setRange(0, 100)
        self.scraper_progress.setValue(0)
        
        # 添加所有组件到布局
        layout.addWidget(mode_group)
        layout.addWidget(params_group)
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("爬取日志:"))
        layout.addWidget(self.scraper_log)
        layout.addWidget(self.scraper_progress)
        
        scraper_tab.setLayout(layout)
    
    def create_cleanup_tab(self):
        """创建清理标签页"""
        cleanup_tab = QWidget()
        self.tabs.addTab(cleanup_tab, "数据清理")
        
        layout = QVBoxLayout()
        
        # 创建参数设置区域
        params_group = QGroupBox("清理参数")
        params_layout = QGridLayout()
        
        # 最小文件大小
        params_layout.addWidget(QLabel("最小文件大小 (KB):"), 0, 0)
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(1, 1000)
        self.min_size_spin.setValue(15)
        params_layout.addWidget(self.min_size_spin, 0, 1)
        
        # 最小图像宽度
        params_layout.addWidget(QLabel("最小图像宽度 (像素):"), 1, 0)
        self.min_width_spin = QSpinBox()
        self.min_width_spin.setRange(100, 2000)
        self.min_width_spin.setValue(400)
        params_layout.addWidget(self.min_width_spin, 1, 1)
        
        # 最小图像高度
        params_layout.addWidget(QLabel("最小图像高度 (像素):"), 2, 0)
        self.min_height_spin = QSpinBox()
        self.min_height_spin.setRange(100, 2000)
        self.min_height_spin.setValue(400)
        params_layout.addWidget(self.min_height_spin, 2, 1)
        
        # 模式选项
        self.move_files_check = QCheckBox("移动文件而不是标记")
        self.move_files_check.setChecked(True)
        params_layout.addWidget(self.move_files_check, 3, 0, 1, 2)
        
        self.rebuild_docs_check = QCheckBox("重建艺术家文档")
        self.rebuild_docs_check.setChecked(True)
        params_layout.addWidget(self.rebuild_docs_check, 4, 0, 1, 2)
        
        params_group.setLayout(params_layout)
        
        # 创建按钮区域
        buttons_layout = QHBoxLayout()
        
        self.start_cleanup_button = QPushButton("开始清理")
        self.start_cleanup_button.clicked.connect(self.start_cleanup)
        
        self.stop_cleanup_button = QPushButton("停止清理")
        self.stop_cleanup_button.clicked.connect(self.stop_cleanup)
        self.stop_cleanup_button.setEnabled(False)
        
        buttons_layout.addWidget(self.start_cleanup_button)
        buttons_layout.addWidget(self.stop_cleanup_button)
        
        # 创建日志区域
        self.cleanup_log = QTextEdit()
        self.cleanup_log.setReadOnly(True)
        
        # 创建进度条
        self.cleanup_progress = QProgressBar()
        self.cleanup_progress.setRange(0, 100)
        self.cleanup_progress.setValue(0)
        
        # 添加所有组件到布局
        layout.addWidget(params_group)
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("清理日志:"))
        layout.addWidget(self.cleanup_log)
        layout.addWidget(self.cleanup_progress)
        
        cleanup_tab.setLayout(layout)
    
    def create_stats_tab(self):
        """创建统计信息标签页"""
        stats_tab = QWidget()
        self.tabs.addTab(stats_tab, "数据统计")
        
        layout = QVBoxLayout()
        
        # 创建按钮区域
        buttons_layout = QHBoxLayout()
        
        self.refresh_stats_button = QPushButton("刷新统计信息")
        self.refresh_stats_button.clicked.connect(self.refresh_stats)
        
        self.open_data_folder_button = QPushButton("打开数据文件夹")
        self.open_data_folder_button.clicked.connect(self.open_data_folder)
        
        buttons_layout.addWidget(self.refresh_stats_button)
        buttons_layout.addWidget(self.open_data_folder_button)
        
        # 创建统计信息显示区域
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        
        # 添加所有组件到布局
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("数据统计:"))
        layout.addWidget(self.stats_text)
        
        stats_tab.setLayout(layout)
        
        # 初始刷新统计信息
        self.refresh_stats()
    
    def start_scraper(self):
        """开始爬虫"""
        # 获取参数
        num_artists = self.num_artists_spin.value()
        max_artworks = self.max_artworks_spin.value()
        checkpoint_interval = self.checkpoint_spin.value()
        use_categories = self.use_categories_check.isChecked()
        
        # 确定模式
        mode = 'simple' if self.simple_mode_radio.isChecked() else 'mass'
        
        # 更新界面状态
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.scraper_progress.setValue(0)
        self.scraper_log.clear()
        self.add_to_scraper_log(f"开始{mode}模式爬虫...")
        
        # 创建并启动线程
        self.scraper_thread = ScraperThread(
            mode, 
            num_artists, 
            max_artworks, 
            checkpoint_interval, 
            use_categories
        )
        
        # 连接信号
        self.scraper_thread.update_signal.connect(self.update_scraper_log)
        self.scraper_thread.progress_signal.connect(self.update_scraper_progress)
        self.scraper_thread.finished_signal.connect(self.scraper_finished)
        
        # 启动线程
        self.scraper_thread.start()
    
    def stop_scraper(self):
        """停止爬虫"""
        if self.scraper_thread is not None and self.scraper_thread.isRunning():
            self.add_to_scraper_log("正在停止爬虫...")
            self.scraper_thread.stop()
            self.scraper_thread.wait()  # 等待线程结束
    
    def scraper_finished(self, success):
        """爬虫完成回调"""
        # 恢复界面状态
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # 更新状态栏
        if success:
            self.statusBar().showMessage("爬虫完成")
            self.add_to_scraper_log("爬虫任务成功完成!")
        else:
            self.statusBar().showMessage("爬虫出错")
            self.add_to_scraper_log("爬虫任务未成功完成。")
        
        # 刷新统计信息
        self.refresh_stats()
    
    def add_to_scraper_log(self, message):
        """添加消息到爬虫日志"""
        self.scraper_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        # 滚动到底部
        self.scraper_log.moveCursor(QTextCursor.End)
    
    def update_scraper_log(self, message):
        """更新爬虫日志（由线程触发）"""
        self.add_to_scraper_log(message)
    
    def update_scraper_progress(self, value):
        """更新爬虫进度条（由线程触发）"""
        self.scraper_progress.setValue(value)
    
    def start_cleanup(self):
        """开始清理数据"""
        # 获取参数
        min_size = self.min_size_spin.value()
        min_width = self.min_width_spin.value()
        min_height = self.min_height_spin.value()
        move_files = self.move_files_check.isChecked()
        rebuild_docs = self.rebuild_docs_check.isChecked()
        
        # 确认是否继续
        if move_files:
            confirm = QMessageBox.question(
                self,
                "确认操作",
                "这将移动低质量和重复图片到单独的文件夹。是否继续？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if confirm != QMessageBox.Yes:
                return
        
        # 更新界面状态
        self.start_cleanup_button.setEnabled(False)
        self.stop_cleanup_button.setEnabled(True)
        self.cleanup_progress.setValue(0)
        self.cleanup_log.clear()
        self.add_to_cleanup_log("开始清理数据...")
        
        # 创建并启动线程
        self.cleanup_thread = CleanupThread(
            min_size,
            (min_width, min_height),
            move_files,
            rebuild_docs
        )
        
        # 连接信号
        self.cleanup_thread.update_signal.connect(self.update_cleanup_log)
        self.cleanup_thread.progress_signal.connect(self.update_cleanup_progress)
        self.cleanup_thread.finished_signal.connect(self.cleanup_finished)
        
        # 启动线程
        self.cleanup_thread.start()
    
    def stop_cleanup(self):
        """停止清理数据"""
        if self.cleanup_thread is not None and self.cleanup_thread.isRunning():
            self.add_to_cleanup_log("正在停止清理...")
            self.cleanup_thread.terminate()  # 强制终止
            self.cleanup_thread.wait()  # 等待线程结束
    
    def cleanup_finished(self, success):
        """清理完成回调"""
        # 恢复界面状态
        self.start_cleanup_button.setEnabled(True)
        self.stop_cleanup_button.setEnabled(False)
        
        # 更新状态栏
        if success:
            self.statusBar().showMessage("数据清理完成")
            self.add_to_cleanup_log("数据清理任务成功完成!")
        else:
            self.statusBar().showMessage("数据清理出错")
            self.add_to_cleanup_log("数据清理任务未成功完成。")
        
        # 刷新统计信息
        self.refresh_stats()
    
    def add_to_cleanup_log(self, message):
        """添加消息到清理日志"""
        self.cleanup_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        # 滚动到底部
        self.cleanup_log.moveCursor(QTextCursor.End)
    
    def update_cleanup_log(self, message):
        """更新清理日志（由线程触发）"""
        self.add_to_cleanup_log(message)
    
    def update_cleanup_progress(self, value):
        """更新清理进度条（由线程触发）"""
        self.cleanup_progress.setValue(value)
    
    def refresh_stats(self):
        """刷新统计信息"""
        try:
            # 清空现有内容
            self.stats_text.clear()
            
            # 添加标题
            self.stats_text.append("# Artsy艺术数据库统计\n")
            
            # 检查数据目录
            if not os.path.exists(ARTSY_DIR):
                self.stats_text.append("数据目录不存在。请先运行爬虫采集数据。")
                return
            
            # 艺术家统计
            artists_csv = os.path.join(ARTSY_DIR, "artsy_artists.csv")
            if os.path.exists(artists_csv):
                try:
                    artists_df = pd.read_csv(artists_csv)
                    num_artists = len(artists_df)
                    self.stats_text.append(f"## 艺术家数据\n")
                    self.stats_text.append(f"- 总艺术家数量: {num_artists}")
                    
                    # 统计国籍
                    if 'nationality' in artists_df.columns:
                        nationality_counts = artists_df['nationality'].value_counts().head(10)
                        if not nationality_counts.empty:
                            self.stats_text.append("\n- 国籍分布 (前10):")
                            for nat, count in nationality_counts.items():
                                if isinstance(nat, str) and nat.strip():
                                    self.stats_text.append(f"  - {nat}: {count}")
                    
                    # 统计艺术流派
                    if 'art_movement' in artists_df.columns:
                        movement_counts = artists_df['art_movement'].value_counts().head(10)
                        if not movement_counts.empty:
                            self.stats_text.append("\n- 艺术流派分布 (前10):")
                            for mov, count in movement_counts.items():
                                if isinstance(mov, str) and mov.strip():
                                    self.stats_text.append(f"  - {mov}: {count}")
                except Exception as e:
                    self.stats_text.append(f"读取艺术家数据出错: {str(e)}")
            else:
                self.stats_text.append("未找到艺术家数据文件。")
            
            # 艺术品统计
            artworks_csv = os.path.join(ARTSY_DIR, "artsy_artworks.csv")
            if os.path.exists(artworks_csv):
                try:
                    artworks_df = pd.read_csv(artworks_csv)
                    num_artworks = len(artworks_df)
                    self.stats_text.append(f"\n## 艺术品数据\n")
                    self.stats_text.append(f"- 总艺术品数量: {num_artworks}")
                    
                    # 统计每位艺术家的作品数量
                    if 'artist_name' in artworks_df.columns:
                        artworks_per_artist = artworks_df.groupby('artist_name').size()
                        avg_artworks = artworks_per_artist.mean()
                        max_artworks = artworks_per_artist.max()
                        min_artworks = artworks_per_artist.min()
                        
                        self.stats_text.append(f"- 平均每位艺术家作品数量: {avg_artworks:.2f}")
                        self.stats_text.append(f"- 最多作品数量: {max_artworks}")
                        self.stats_text.append(f"- 最少作品数量: {min_artworks}")
                        
                        # 作品数量最多的艺术家
                        top_artists = artworks_per_artist.sort_values(ascending=False).head(10)
                        if not top_artists.empty:
                            self.stats_text.append("\n- 作品最多的艺术家 (前10):")
                            for artist, count in top_artists.items():
                                self.stats_text.append(f"  - {artist}: {count}")
                except Exception as e:
                    self.stats_text.append(f"读取艺术品数据出错: {str(e)}")
            else:
                self.stats_text.append("未找到艺术品数据文件。")
            
            # 图片统计
            if os.path.exists(IMAGES_DIR):
                self.stats_text.append(f"\n## 图片数据\n")
                
                # 统计图片总数
                total_images = 0
                artist_dirs = [d for d in os.listdir(IMAGES_DIR) 
                              if os.path.isdir(os.path.join(IMAGES_DIR, d))
                              and d not in ['low_quality', 'duplicates']]
                
                # 有图片的艺术家数量
                artists_with_images = 0
                
                for artist_dir in artist_dirs:
                    artist_path = os.path.join(IMAGES_DIR, artist_dir)
                    images = [f for f in os.listdir(artist_path) 
                             if os.path.isfile(os.path.join(artist_path, f))
                             and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                    
                    if images:
                        artists_with_images += 1
                        total_images += len(images)
                
                self.stats_text.append(f"- 总图片数量: {total_images}")
                self.stats_text.append(f"- 有图片的艺术家: {artists_with_images}/{len(artist_dirs)}")
                
                # 统计低质量图片
                if os.path.exists(LOW_QUALITY_DIR):
                    low_quality_images = 0
                    low_quality_dirs = [d for d in os.listdir(LOW_QUALITY_DIR) 
                                      if os.path.isdir(os.path.join(LOW_QUALITY_DIR, d))]
                    
                    for lq_dir in low_quality_dirs:
                        lq_path = os.path.join(LOW_QUALITY_DIR, lq_dir)
                        lq_images = [f for f in os.listdir(lq_path) 
                                   if os.path.isfile(os.path.join(lq_path, f))
                                   and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                        
                        low_quality_images += len(lq_images)
                    
                    self.stats_text.append(f"- 低质量图片: {low_quality_images}")
                
                # 统计重复图片
                if os.path.exists(DUPLICATES_DIR):
                    duplicate_images = 0
                    duplicate_dirs = [d for d in os.listdir(DUPLICATES_DIR) 
                                     if os.path.isdir(os.path.join(DUPLICATES_DIR, d))]
                    
                    for dup_dir in duplicate_dirs:
                        dup_path = os.path.join(DUPLICATES_DIR, dup_dir)
                        dup_images = [f for f in os.listdir(dup_path) 
                                    if os.path.isfile(os.path.join(dup_path, f))
                                    and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                        
                        duplicate_images += len(dup_images)
                    
                    self.stats_text.append(f"- 重复图片: {duplicate_images}")
            else:
                self.stats_text.append("未找到图片目录。")
            
            # 文档统计
            docs_dir = os.path.join(ARTSY_DIR, "artist_docs")
            if os.path.exists(docs_dir):
                self.stats_text.append(f"\n## 文档数据\n")
                
                # 统计文档数量
                docs = [f for f in os.listdir(docs_dir) 
                       if os.path.isfile(os.path.join(docs_dir, f))
                       and f.lower().endswith('.md')]
                
                self.stats_text.append(f"- 艺术家文档数量: {len(docs)}")
            
            # 更新时间
            self.stats_text.append(f"\n\n最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            self.stats_text.append(f"生成统计信息时出错: {str(e)}")
    
    def open_data_folder(self):
        """打开数据文件夹"""
        import os
        import platform
        import subprocess
        
        try:
            if platform.system() == "Windows":
                os.startfile(ARTSY_DIR)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", ARTSY_DIR])
            else:  # Linux
                subprocess.Popen(["xdg-open", ARTSY_DIR])
                
            self.statusBar().showMessage("已打开数据文件夹")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法打开数据文件夹: {str(e)}")
    
    def closeEvent(self, event):
        """应用关闭事件处理"""
        # 停止正在运行的线程
        if self.scraper_thread is not None and self.scraper_thread.isRunning():
            self.scraper_thread.stop()
            self.scraper_thread.wait()
        
        if self.cleanup_thread is not None and self.cleanup_thread.isRunning():
            self.cleanup_thread.terminate()
            self.cleanup_thread.wait()
        
        event.accept()

# 程序入口
def main():
    """主函数"""
    # 创建应用
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格，在所有平台上看起来一致
    
    # 创建并显示主窗口
    window = ArtsyScraperApp()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 