#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIDA art scraper application - integrated GUI

This application integrates all scraper functionality, including:
- Scraping artist and artwork data
- Data cleaning and optimization
- Data statistics and visualization

Provides a modern graphical interface for easy user operation.
"""

import os
import sys
import time
import logging
import threading
import json
from datetime import datetime
import io
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, 
                            QTextEdit, QProgressBar, QComboBox, QFileDialog, QSpinBox, 
                            QGroupBox, QRadioButton, QMessageBox, QToolTip, QSplitter,
                            QScrollArea, QFrame, QGridLayout, QStatusBar, QStyle)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QDir, QTimer, QUrl
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor, QColor, QPalette, QDesktopServices
import pandas as pd
import shutil

# Import scraper class
from artsy_scraper import ArtsyScraper

# Solve Chinese output issue in Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configure logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(BASE_DIR, "data", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"aida_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))
    ]
)
logger = logging.getLogger("aida_scraper")

# Define global paths
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTSY_DIR = os.path.join(DATA_DIR, "artsy")
IMAGES_DIR = os.path.join(ARTSY_DIR, "images")
CHECKPOINTS_DIR = os.path.join(ARTSY_DIR, "checkpoints")
LOW_QUALITY_DIR = os.path.join(IMAGES_DIR, "low_quality")
DUPLICATES_DIR = os.path.join(IMAGES_DIR, "duplicates")

# Create necessary directories
os.makedirs(ARTSY_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CHECKPOINTS_DIR, exist_ok=True)
os.makedirs(LOW_QUALITY_DIR, exist_ok=True)
os.makedirs(DUPLICATES_DIR, exist_ok=True)

# Scraper thread class
class ScraperThread(QThread):
    """Background thread for scraping"""
    update_signal = pyqtSignal(str)  # Signal for updating UI
    progress_signal = pyqtSignal(int)  # Progress bar signal
    finished_signal = pyqtSignal(bool)  # Completion signal with success/failure status
    
    def __init__(self, mode, num_artists, max_artworks, checkpoint_interval, use_categories):
        super().__init__()
        self.mode = mode  # 'simple' or 'mass'
        self.num_artists = num_artists
        self.max_artworks = max_artworks
        self.checkpoint_interval = checkpoint_interval
        self.use_categories = use_categories
        self.running = True
        self.scraper = None
        
    def run(self):
        """Main thread function"""
        start_time = time.time()
        
        try:
            # Create scraper instance
            self.scraper = ArtsyScraper()
            self.scraper.checkpoint_interval = self.checkpoint_interval
            
            # Execute different scraping strategies based on mode
            if self.mode == 'simple':
                self.run_simple_mode()
            else:  # 'mass'
                self.run_mass_mode()
                
            # Statistics and reporting
            elapsed_time = time.time() - start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if self.scraper:
                total_artists = len(self.scraper.artists)
                total_artworks = len(self.scraper.artworks)
                
                msg = f"Scraping complete! Collected {total_artists} artists and {total_artworks} artworks\n"
                msg += f"Total time: {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"
                
                if total_artists > 0:
                    msg += f"\nAverage {total_artworks/total_artists:.1f} artworks per artist"
                
                self.update_signal.emit(msg)
                self.finished_signal.emit(True)
            else:
                self.update_signal.emit("Error during scraping, could not complete")
                self.finished_signal.emit(False)
                
        except Exception as e:
            error_msg = f"Error during scraping: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.update_signal.emit(error_msg)
            self.finished_signal.emit(False)
            
        finally:
            # Ensure resources are closed
            if self.scraper:
                try:
                    self.scraper.save_data()
                    self.scraper.close()
                except:
                    pass
    
    def run_simple_mode(self):
        """Run simple mode"""
        self.update_signal.emit(f"Starting simple scrape, target: {self.num_artists} artists, max {self.max_artworks} artworks each")
        
        # Decide whether to scrape by category or main list
        if self.use_categories:
            self.update_signal.emit("Using category mode for scraping...")
            self.scraper.scrape_multiple_categories(
                max_artists_per_category=min(300, self.num_artists // 10),
                max_artworks=self.max_artworks
            )
        else:
            self.update_signal.emit("Using main list mode for scraping...")
            self.scraper.scrape_artists_list(
                max_artists=self.num_artists,
                max_artworks=self.max_artworks
            )
    
    def run_mass_mode(self):
        """Run mass mode"""
        self.update_signal.emit(f"Starting mass scrape, target: {self.num_artists} artists, max {self.max_artworks} artworks each")
        
        # First scrape important categories
        self.update_signal.emit("Phase 1: Scraping artists from important categories...")
        categories_artists = min(self.num_artists // 3, 2000)  # Allocate 1/3 quota to categories, max 2000
        per_category = max(10, categories_artists // len(self.scraper.important_artists_categories))
        
        self.scraper.scrape_multiple_categories(
            max_artists_per_category=per_category,
            max_artworks=self.max_artworks
        )
        
        phase1_artists = len(self.scraper.artists)
        self.update_signal.emit(f"Phase 1 complete: Scraped {phase1_artists} artists")
        
        # Then scrape from main list to fulfill quota
        remaining_artists = max(0, self.num_artists - phase1_artists)
        if remaining_artists > 0:
            self.update_signal.emit(f"Phase 2: Scraping {remaining_artists} more artists from main list...")
            
            self.scraper.scrape_artists_list(
                max_artists=remaining_artists,
                max_artworks=self.max_artworks
            )
    
    def stop(self):
        """Stop scraper"""
        self.running = False
        self.update_signal.emit("User requested stop, saving collected data...")
        
        if self.scraper:
            try:
                self.scraper.save_data()
                total_artists = len(self.scraper.artists)
                total_artworks = len(self.scraper.artworks)
                self.update_signal.emit(f"Saved interrupted data: {total_artists} artists, {total_artworks} artworks")
            except Exception as e:
                self.update_signal.emit(f"Error saving data: {str(e)}")


# Cleanup thread class
class CleanupThread(QThread):
    """Background thread for data cleanup"""
    update_signal = pyqtSignal(str)  # Signal for updating UI
    progress_signal = pyqtSignal(int)  # Progress bar signal
    finished_signal = pyqtSignal(bool)  # Completion signal with success/failure status
    
    def __init__(self, min_size_kb, min_width, min_height, move_files, 
                 clean_quality, clean_duplicates, rebuild_data):
        super().__init__()
        self.min_size_kb = min_size_kb
        self.min_width = min_width
        self.min_height = min_height
        self.move_files = move_files
        self.clean_quality = clean_quality
        self.clean_duplicates = clean_duplicates
        self.rebuild_data = rebuild_data
        self.running = True
        
    def run(self):
        """Main thread function"""
        try:
            from artsy_scraper_optimizer import ArtsyOptimizer
            
            self.update_signal.emit("Starting data cleanup and optimization...")
            
            # Create optimizer instance
            optimizer = ArtsyOptimizer(
                min_image_size_kb=self.min_size_kb,
                min_width=self.min_width,
                min_height=self.min_height,
                move_files=self.move_files
            )
            
            # Clean low quality images
            if self.clean_quality and self.running:
                self.update_signal.emit("Cleaning low quality images...")
                low_quality_count = optimizer.clean_low_quality_images()
                self.update_signal.emit(f"Cleaning complete, processed {low_quality_count} low quality images")
                self.progress_signal.emit(33)
            
            # Clean duplicate images
            if self.clean_duplicates and self.running:
                self.update_signal.emit("Cleaning duplicate images...")
                duplicate_count = optimizer.remove_duplicates()
                self.update_signal.emit(f"Cleaning complete, processed {duplicate_count} duplicate images")
                self.progress_signal.emit(66)
            
            # Rebuild data indexes
            if self.rebuild_data and self.running:
                self.update_signal.emit("Rebuilding data indexes...")
                optimizer.rebuild_data_indices()
                self.update_signal.emit("Data index rebuild complete")
                self.progress_signal.emit(100)
            
            self.update_signal.emit("Data optimization complete!")
            self.finished_signal.emit(True)
            
        except Exception as e:
            error_msg = f"Error during data cleanup: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.update_signal.emit(error_msg)
            self.finished_signal.emit(False)
    
    def stop(self):
        """Stop cleanup"""
        self.running = False
        self.update_signal.emit("User requested stop, completing current operation...")


# Main application class
class AidaArtScraperApp(QMainWindow):
    """AIDA art scraper application main window"""
    
    def __init__(self):
        super().__init__()
        self.scraper_thread = None
        self.cleanup_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Set basic window properties
        self.setWindowTitle("AIDA Art Data Scraper")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Pre-initialize statistics labels to avoid errors when refreshing stats
        self.stats_artists_count = QLabel("0")
        self.stats_artworks_count = QLabel("0")
        self.stats_images_count = QLabel("0")
        self.stats_categories_count = QLabel("0")
        self.stats_total_size = QLabel("0 MB")
        self.stats_avg_artworks = QLabel("0")
        self.stats_avg_size = QLabel("0 KB")
        self.stats_low_quality = QLabel("0")
        self.stats_duplicates = QLabel("0")
        self.stats_missing_info = QLabel("0")
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_welcome_tab()
        self.create_scraper_tab()
        self.create_cleanup_tab()
        self.create_stats_tab()
        self.create_about_tab()
        
        # Timer for refreshing statistics
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.refresh_stats)
        self.stats_timer.start(60000)  # Refresh every minute
        
    def create_welcome_tab(self):
        """Create welcome tab"""
        welcome_tab = QWidget()
        welcome_layout = QVBoxLayout(welcome_tab)
        
        # Title and description
        title_label = QLabel("Welcome to AIDA Art Data Scraper")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        desc_label = QLabel(
            "AIDA (AI Artist Database) scraper tool helps you collect rich data about artists and artworks.\n"
            "You can use this tool to gather information about artists, their works, genres, and related art history for research or creating your own art database."
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        # Quick start buttons
        quick_start_group = QGroupBox("Quick Start")
        quick_start_layout = QVBoxLayout()
        
        start_simple_btn = QPushButton("Start Simple Scrape (100 artists)")
        start_simple_btn.clicked.connect(self.quick_start_simple)
        
        start_mass_btn = QPushButton("Start Mass Scrape (1000 artists)")
        start_mass_btn.clicked.connect(self.quick_start_mass)
        
        optimize_btn = QPushButton("Optimize Collected Data")
        optimize_btn.clicked.connect(self.quick_start_optimize)
        
        view_stats_btn = QPushButton("View Data Statistics")
        view_stats_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(3))
        
        quick_start_layout.addWidget(start_simple_btn)
        quick_start_layout.addWidget(start_mass_btn)
        quick_start_layout.addWidget(optimize_btn)
        quick_start_layout.addWidget(view_stats_btn)
        quick_start_group.setLayout(quick_start_layout)
        
        # Data overview
        data_overview_group = QGroupBox("Data Overview")
        data_overview_layout = QGridLayout()
        
        self.welcome_artists_count = QLabel("0")
        self.welcome_artworks_count = QLabel("0")
        self.welcome_images_count = QLabel("0")
        self.welcome_categories_count = QLabel("0")
        
        data_overview_layout.addWidget(QLabel("Artists:"), 0, 0)
        data_overview_layout.addWidget(self.welcome_artists_count, 0, 1)
        data_overview_layout.addWidget(QLabel("Artworks:"), 0, 2)
        data_overview_layout.addWidget(self.welcome_artworks_count, 0, 3)
        data_overview_layout.addWidget(QLabel("Images:"), 1, 0)
        data_overview_layout.addWidget(self.welcome_images_count, 1, 1)
        data_overview_layout.addWidget(QLabel("Categories:"), 1, 2)
        data_overview_layout.addWidget(self.welcome_categories_count, 1, 3)
        
        data_overview_group.setLayout(data_overview_layout)
        
        # Add to main layout
        welcome_layout.addWidget(title_label)
        welcome_layout.addWidget(desc_label)
        welcome_layout.addWidget(quick_start_group)
        welcome_layout.addWidget(data_overview_group)
        welcome_layout.addStretch()
        
        # Add to tabs
        self.tabs.addTab(welcome_tab, "Welcome")
        
        # Initial load of statistics
        self.refresh_stats()

    def create_scraper_tab(self):
        """Create scraper tab"""
        scraper_tab = QWidget()
        scraper_layout = QVBoxLayout(scraper_tab)
        
        # Create splitter for settings and log areas
        splitter = QSplitter(Qt.Vertical)
        scraper_layout.addWidget(splitter)
        
        # Scraper settings area
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # Scraper mode selection
        mode_group = QGroupBox("Scraper Mode")
        mode_layout = QVBoxLayout()
        
        self.simple_mode_radio = QRadioButton("Simple Mode - For first-time users, less data")
        self.simple_mode_radio.setChecked(True)
        self.mass_mode_radio = QRadioButton("Mass Mode - For longer runs, large amount of data")
        
        mode_layout.addWidget(self.simple_mode_radio)
        mode_layout.addWidget(self.mass_mode_radio)
        mode_group.setLayout(mode_layout)
        
        # Scraper parameter settings
        params_group = QGroupBox("Scraping Parameters")
        params_layout = QGridLayout()
        
        params_layout.addWidget(QLabel("Number of artists to scrape:"), 0, 0)
        self.artists_count_spin = QSpinBox()
        self.artists_count_spin.setRange(10, 10000)
        self.artists_count_spin.setValue(100)
        params_layout.addWidget(self.artists_count_spin, 0, 1)
        
        params_layout.addWidget(QLabel("Max artworks per artist:"), 1, 0)
        self.artworks_count_spin = QSpinBox()
        self.artworks_count_spin.setRange(1, 100)
        self.artworks_count_spin.setValue(10)
        params_layout.addWidget(self.artworks_count_spin, 1, 1)
        
        params_layout.addWidget(QLabel("Checkpoint interval (artists):"), 2, 0)
        self.checkpoint_interval_spin = QSpinBox()
        self.checkpoint_interval_spin.setRange(1, 100)
        self.checkpoint_interval_spin.setValue(10)
        params_layout.addWidget(self.checkpoint_interval_spin, 2, 1)
        
        self.use_categories_check = QCheckBox("Use artist categories for scraping (recommended)")
        self.use_categories_check.setChecked(True)
        params_layout.addWidget(self.use_categories_check, 3, 0, 1, 2)
        
        params_group.setLayout(params_layout)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        
        self.start_scraper_btn = QPushButton("Start Scraping")
        self.start_scraper_btn.clicked.connect(self.start_scraper)
        
        self.stop_scraper_btn = QPushButton("Stop Scraping")
        self.stop_scraper_btn.clicked.connect(self.stop_scraper)
        self.stop_scraper_btn.setEnabled(False)
        
        self.open_data_btn = QPushButton("Open Data Folder")
        self.open_data_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(ARTSY_DIR)))
        
        actions_layout.addWidget(self.start_scraper_btn)
        actions_layout.addWidget(self.stop_scraper_btn)
        actions_layout.addWidget(self.open_data_btn)
        
        # Add settings to layout
        settings_layout.addWidget(mode_group)
        settings_layout.addWidget(params_group)
        settings_layout.addLayout(actions_layout)
        
        # Scraper log and progress area
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        
        log_label = QLabel("Scraper Log")
        self.scraper_log = QTextEdit()
        self.scraper_log.setReadOnly(True)
        
        self.scraper_progress = QProgressBar()
        self.scraper_progress.setRange(0, 100)
        self.scraper_progress.setValue(0)
        
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.scraper_log)
        log_layout.addWidget(self.scraper_progress)
        
        # Add widgets to splitter
        splitter.addWidget(settings_widget)
        splitter.addWidget(log_widget)
        splitter.setSizes([300, 500])
        
        # Add to tabs
        self.tabs.addTab(scraper_tab, "Scraper")

    def create_cleanup_tab(self):
        """Create data cleanup tab"""
        cleanup_tab = QWidget()
        cleanup_layout = QVBoxLayout(cleanup_tab)
        
        # Create splitter for settings and log areas
        splitter = QSplitter(Qt.Vertical)
        cleanup_layout.addWidget(splitter)
        
        # Cleanup settings area
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # Image quality cleanup settings
        quality_group = QGroupBox("Image Quality Cleanup")
        quality_layout = QGridLayout()
        
        quality_layout.addWidget(QLabel("Minimum image size (KB):"), 0, 0)
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(5, 100)
        self.min_size_spin.setValue(15)
        quality_layout.addWidget(self.min_size_spin, 0, 1)
        
        quality_layout.addWidget(QLabel("Minimum image width (pixels):"), 1, 0)
        self.min_width_spin = QSpinBox()
        self.min_width_spin.setRange(100, 1000)
        self.min_width_spin.setValue(400)
        quality_layout.addWidget(self.min_width_spin, 1, 1)
        
        quality_layout.addWidget(QLabel("Minimum image height (pixels):"), 2, 0)
        self.min_height_spin = QSpinBox()
        self.min_height_spin.setRange(100, 1000)
        self.min_height_spin.setValue(400)
        quality_layout.addWidget(self.min_height_spin, 2, 1)
        
        quality_group.setLayout(quality_layout)
        
        # Cleanup options
        options_group = QGroupBox("Cleanup Options")
        options_layout = QVBoxLayout()
        
        self.clear_low_quality_check = QCheckBox("Clean low quality images")
        self.clear_low_quality_check.setChecked(True)
        
        self.clear_duplicates_check = QCheckBox("Clean duplicate images")
        self.clear_duplicates_check.setChecked(True)
        
        self.rebuild_data_check = QCheckBox("Rebuild data indexes")
        self.rebuild_data_check.setChecked(True)
        
        self.move_files_radio = QRadioButton("Move problematic files to dedicated directories")
        self.move_files_radio.setChecked(True)
        
        self.delete_files_radio = QRadioButton("Delete problematic files")
        
        options_layout.addWidget(self.clear_low_quality_check)
        options_layout.addWidget(self.clear_duplicates_check)
        options_layout.addWidget(self.rebuild_data_check)
        options_layout.addWidget(self.move_files_radio)
        options_layout.addWidget(self.delete_files_radio)
        options_group.setLayout(options_layout)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        
        self.start_cleanup_btn = QPushButton("Start Cleanup")
        self.start_cleanup_btn.clicked.connect(self.start_cleanup)
        
        self.stop_cleanup_btn = QPushButton("Stop Cleanup")
        self.stop_cleanup_btn.clicked.connect(self.stop_cleanup)
        self.stop_cleanup_btn.setEnabled(False)
        
        self.open_images_btn = QPushButton("Open Images Folder")
        self.open_images_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(IMAGES_DIR)))
        
        actions_layout.addWidget(self.start_cleanup_btn)
        actions_layout.addWidget(self.stop_cleanup_btn)
        actions_layout.addWidget(self.open_images_btn)
        
        # Add settings to layout
        settings_layout.addWidget(quality_group)
        settings_layout.addWidget(options_group)
        settings_layout.addLayout(actions_layout)
        
        # Cleanup log and progress area
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        
        log_label = QLabel("Cleanup Log")
        self.cleanup_log = QTextEdit()
        self.cleanup_log.setReadOnly(True)
        
        self.cleanup_progress = QProgressBar()
        self.cleanup_progress.setRange(0, 100)
        self.cleanup_progress.setValue(0)
        
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.cleanup_log)
        log_layout.addWidget(self.cleanup_progress)
        
        # Add widgets to splitter
        splitter.addWidget(settings_widget)
        splitter.addWidget(log_widget)
        splitter.setSizes([300, 500])
        
        # Add to tabs
        self.tabs.addTab(cleanup_tab, "Data Cleanup")

    def create_stats_tab(self):
        """Create statistics tab"""
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Statistics")
        refresh_btn.clicked.connect(self.refresh_stats)
        stats_layout.addWidget(refresh_btn)
        
        # Basic statistics
        basic_stats_group = QGroupBox("Basic Statistics")
        basic_stats_layout = QGridLayout()
        
        # Create data labels
        self.stats_artists_count = QLabel("0")
        self.stats_artworks_count = QLabel("0")
        self.stats_images_count = QLabel("0")
        self.stats_categories_count = QLabel("0")
        self.stats_total_size = QLabel("0 MB")
        self.stats_avg_artworks = QLabel("0")
        self.stats_avg_size = QLabel("0 KB")
        
        # Add to layout
        basic_stats_layout.addWidget(QLabel("Number of Artists:"), 0, 0)
        basic_stats_layout.addWidget(self.stats_artists_count, 0, 1)
        basic_stats_layout.addWidget(QLabel("Number of Artworks:"), 0, 2)
        basic_stats_layout.addWidget(self.stats_artworks_count, 0, 3)
        
        basic_stats_layout.addWidget(QLabel("Number of Images:"), 1, 0)
        basic_stats_layout.addWidget(self.stats_images_count, 1, 1)
        basic_stats_layout.addWidget(QLabel("Number of Categories:"), 1, 2)
        basic_stats_layout.addWidget(self.stats_categories_count, 1, 3)
        
        basic_stats_layout.addWidget(QLabel("Total Image Size:"), 2, 0)
        basic_stats_layout.addWidget(self.stats_total_size, 2, 1)
        basic_stats_layout.addWidget(QLabel("Avg Artworks per Artist:"), 2, 2)
        basic_stats_layout.addWidget(self.stats_avg_artworks, 2, 3)
        
        basic_stats_layout.addWidget(QLabel("Average Image Size:"), 3, 0)
        basic_stats_layout.addWidget(self.stats_avg_size, 3, 1)
        
        basic_stats_group.setLayout(basic_stats_layout)
        stats_layout.addWidget(basic_stats_group)
        
        # Problem data statistics
        issues_group = QGroupBox("Data Issues")
        issues_layout = QGridLayout()
        
        self.stats_low_quality = QLabel("0")
        self.stats_duplicates = QLabel("0")
        self.stats_missing_info = QLabel("0")
        
        issues_layout.addWidget(QLabel("Low Quality Images:"), 0, 0)
        issues_layout.addWidget(self.stats_low_quality, 0, 1)
        issues_layout.addWidget(QLabel("Duplicate Images:"), 0, 2)
        issues_layout.addWidget(self.stats_duplicates, 0, 3)
        issues_layout.addWidget(QLabel("Artists with Incomplete Info:"), 1, 0)
        issues_layout.addWidget(self.stats_missing_info, 1, 1)
        
        issues_group.setLayout(issues_layout)
        stats_layout.addWidget(issues_group)
        
        # Data export
        export_group = QGroupBox("Data Export")
        export_layout = QHBoxLayout()
        
        export_csv_btn = QPushButton("Export CSV Data")
        export_csv_btn.clicked.connect(self.export_csv_data)
        
        export_json_btn = QPushButton("Export JSON Data")
        export_json_btn.clicked.connect(self.export_json_data)
        
        export_layout.addWidget(export_csv_btn)
        export_layout.addWidget(export_json_btn)
        export_group.setLayout(export_layout)
        stats_layout.addWidget(export_group)
        
        # Fill empty space
        stats_layout.addStretch()
        
        # Add to tabs
        self.tabs.addTab(stats_tab, "Statistics")

    def create_about_tab(self):
        """Create about tab"""
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        # Title
        title_label = QLabel("About AIDA Art Scraper")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Version and description
        version_label = QLabel("Version: 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        
        desc_label = QLabel(
            "AIDA (AI Artist Database) Scraper is an efficient tool for collecting art data.\n"
            "It can scrape artist information, artwork data, and images from art websites like Artsy, providing high-quality data for art research and AI training."
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        # Features list
        features_group = QGroupBox("Main Features")
        features_layout = QVBoxLayout()
        
        features = [
            "✓ Artist Data Scraping - Support for categories and tags",
            "✓ Artwork Data Scraping - Collect details, images and category tags",
            "✓ Data Cleanup - Clean low quality and duplicate images",
            "✓ Statistics Analysis - View data distribution",
            "✓ Checkpoint Saving - Support for interruption recovery"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            features_layout.addWidget(feature_label)
        
        features_group.setLayout(features_layout)
        
        # Usage instructions
        usage_group = QGroupBox("Usage Instructions")
        usage_layout = QVBoxLayout()
        
        usage_text = QTextEdit()
        usage_text.setReadOnly(True)
        usage_text.setHtml("""
            <h3>How to use this tool</h3>
            <p>1. <b>Start Scraping</b>: Set parameters in the Scraper tab and click "Start Scraping"</p>
            <p>2. <b>Data Cleanup</b>: After scraping, use the Data Cleanup tab to optimize your data</p>
            <p>3. <b>Statistics</b>: View data distribution in the Statistics tab</p>
            <p>4. <b>Note</b>: Scraping may take a long time, use a stable network connection</p>
            
            <h3>Data Storage Location</h3>
            <p>All data is saved in the project's <code>data/artsy</code> directory:</p>
            <ul>
                <li>Artist data: artsy_artists.csv</li>
                <li>Artwork data: artsy_artworks.csv</li>
                <li>Image files: images/[artist_name]/[artwork_title].jpg</li>
            </ul>
        """)
        
        usage_layout.addWidget(usage_text)
        usage_group.setLayout(usage_layout)
        
        # Project links
        links_group = QGroupBox("Project Links")
        links_layout = QHBoxLayout()
        
        project_btn = QPushButton("Project Homepage")
        project_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/yourusername/aida")))
        
        docs_btn = QPushButton("Documentation")
        docs_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://aida-docs.example.com")))
        
        links_layout.addWidget(project_btn)
        links_layout.addWidget(docs_btn)
        links_group.setLayout(links_layout)
        
        # Add all elements to layout
        about_layout.addWidget(title_label)
        about_layout.addWidget(version_label)
        about_layout.addWidget(desc_label)
        about_layout.addWidget(features_group)
        about_layout.addWidget(usage_group)
        about_layout.addWidget(links_group)
        
        # Add to tabs
        self.tabs.addTab(about_tab, "About")
        
    def start_scraper(self):
        """Start scraper"""
        # Get parameters
        num_artists = self.artists_count_spin.value()
        max_artworks = self.artworks_count_spin.value()
        checkpoint_interval = self.checkpoint_interval_spin.value()
        use_categories = self.use_categories_check.isChecked()
        
        # Determine mode
        mode = 'simple' if self.simple_mode_radio.isChecked() else 'mass'
        
        # Create and start thread
        self.scraper_thread = ScraperThread(
            mode=mode,
            num_artists=num_artists,
            max_artworks=max_artworks,
            checkpoint_interval=checkpoint_interval,
            use_categories=use_categories
        )
        
        # Connect signals
        self.scraper_thread.update_signal.connect(self.update_scraper_log)
        self.scraper_thread.progress_signal.connect(self.update_scraper_progress)
        self.scraper_thread.finished_signal.connect(self.scraper_finished)
        
        # Update UI state
        self.start_scraper_btn.setEnabled(False)
        self.stop_scraper_btn.setEnabled(True)
        
        # Clear log and add starting information
        self.scraper_log.clear()
        
        # Start thread
        self.scraper_thread.start()
        
        # Update status bar
        self.status_bar.showMessage("Scraper is running...")
    
    def stop_scraper(self):
        """Stop scraper"""
        if self.scraper_thread and self.scraper_thread.isRunning():
            self.scraper_thread.stop()
            self.status_bar.showMessage("Stopping scraper, please wait...")
    
    def scraper_finished(self, success):
        """Scraper completion callback"""
        # Update UI state
        self.start_scraper_btn.setEnabled(True)
        self.stop_scraper_btn.setEnabled(False)
        
        # Update status bar
        if success:
            self.status_bar.showMessage("Scraper completed successfully")
            # Refresh statistics
            self.refresh_stats()
            # Notify user
            QMessageBox.information(self, "Scraping Complete", "Scraper has successfully completed data collection.\nYou can optimize data quality in the Data Cleanup tab.")
        else:
            self.status_bar.showMessage("Scraper encountered errors or was interrupted")
    
    def update_scraper_log(self, message):
        """Update scraper log"""
        self.scraper_log.append(message)
        # Auto-scroll to bottom
        self.scraper_log.moveCursor(QTextCursor.End)
    
    def update_scraper_progress(self, value):
        """Update scraper progress bar"""
        self.scraper_progress.setValue(value)
    
    def start_cleanup(self):
        """Start data cleanup"""
        # Get parameters
        min_size = self.min_size_spin.value()
        min_width = self.min_width_spin.value()
        min_height = self.min_height_spin.value()
        move_files = self.move_files_radio.isChecked()
        
        clean_quality = self.clear_low_quality_check.isChecked()
        clean_duplicates = self.clear_duplicates_check.isChecked()
        rebuild_data = self.rebuild_data_check.isChecked()
        
        # If no cleanup options selected, notify user
        if not any([clean_quality, clean_duplicates, rebuild_data]):
            QMessageBox.warning(self, "No Operations Selected", "Please select at least one cleanup operation")
            return
        
        # Create and start thread
        self.cleanup_thread = CleanupThread(
            min_size_kb=min_size,
            min_width=min_width,
            min_height=min_height,
            move_files=move_files,
            clean_quality=clean_quality,
            clean_duplicates=clean_duplicates,
            rebuild_data=rebuild_data
        )
        
        # Connect signals
        self.cleanup_thread.update_signal.connect(self.update_cleanup_log)
        self.cleanup_thread.progress_signal.connect(self.update_cleanup_progress)
        self.cleanup_thread.finished_signal.connect(self.cleanup_finished)
        
        # Update UI state
        self.start_cleanup_btn.setEnabled(False)
        self.stop_cleanup_btn.setEnabled(True)
        
        # Clear log and add starting information
        self.cleanup_log.clear()
        
        # Start thread
        self.cleanup_thread.start()
        
        # Update status bar
        self.status_bar.showMessage("Data cleanup is running...")
    
    def stop_cleanup(self):
        """Stop data cleanup"""
        if self.cleanup_thread and self.cleanup_thread.isRunning():
            self.cleanup_thread.stop()
            self.status_bar.showMessage("Stopping data cleanup, please wait...")
    
    def cleanup_finished(self, success):
        """Data cleanup completion callback"""
        # Update UI state
        self.start_cleanup_btn.setEnabled(True)
        self.stop_cleanup_btn.setEnabled(False)
        
        # Update status bar
        if success:
            self.status_bar.showMessage("Data cleanup completed successfully")
            # Refresh statistics
            self.refresh_stats()
            # Notify user
            QMessageBox.information(self, "Cleanup Complete", "Data cleanup has completed successfully.\nYou can view results in the Statistics tab.")
        else:
            self.status_bar.showMessage("Data cleanup encountered errors or was interrupted")
    
    def update_cleanup_log(self, message):
        """Update cleanup log"""
        self.cleanup_log.append(message)
        # Auto-scroll to bottom
        self.cleanup_log.moveCursor(QTextCursor.End)
    
    def update_cleanup_progress(self, value):
        """Update cleanup progress bar"""
        self.cleanup_progress.setValue(value)
    
    def refresh_stats(self):
        """Refresh statistics"""
        try:
            # Artist data
            artists_path = os.path.join(ARTSY_DIR, "artsy_artists.csv")
            artists_count = 0
            if os.path.exists(artists_path):
                try:
                    artists_df = pd.read_csv(artists_path)
                    artists_count = len(artists_df)
                except Exception as e:
                    logger.warning(f"Error reading artist data: {str(e)}")
            
            # Artwork data
            artworks_path = os.path.join(ARTSY_DIR, "artsy_artworks.csv")
            artworks_count = 0
            if os.path.exists(artworks_path):
                try:
                    artworks_df = pd.read_csv(artworks_path)
                    artworks_count = len(artworks_df)
                except Exception as e:
                    logger.warning(f"Error reading artwork data: {str(e)}")
            
            # Image data
            images_count = 0
            try:
                for root, dirs, files in os.walk(IMAGES_DIR):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            images_count += 1
            except Exception as e:
                logger.warning(f"Error counting images: {str(e)}")
            
            # Update statistics labels
            if hasattr(self, 'stats_artists_count'):
                self.stats_artists_count.setText(str(artists_count))
            if hasattr(self, 'stats_artworks_count'):
                self.stats_artworks_count.setText(str(artworks_count))
            if hasattr(self, 'stats_images_count'):
                self.stats_images_count.setText(str(images_count))
            
            # Update welcome page statistics
            if hasattr(self, 'welcome_artists_count'):
                self.welcome_artists_count.setText(str(artists_count))
            if hasattr(self, 'welcome_artworks_count'):
                self.welcome_artworks_count.setText(str(artworks_count))
            if hasattr(self, 'welcome_images_count'):
                self.welcome_images_count.setText(str(images_count))
            
            # Update status bar
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage(f"Statistics refreshed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            logger.error(f"Error refreshing statistics: {str(e)}", exc_info=True)
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("Error refreshing statistics")
    
    def export_csv_data(self):
        """Export CSV data"""
        # Implementation to be added later
        pass
    
    def export_json_data(self):
        """Export JSON data"""
        # Implementation to be added later
        pass
    
    def quick_start_simple(self):
        """Quick start simple scraping"""
        # Switch to scraper tab
        self.tabs.setCurrentIndex(1)
        
        # Set default parameters
        self.simple_mode_radio.setChecked(True)
        self.artists_count_spin.setValue(100)
        self.artworks_count_spin.setValue(10)
        self.use_categories_check.setChecked(True)
        
        # Start scraping
        QTimer.singleShot(500, self.start_scraper)
    
    def quick_start_mass(self):
        """Quick start mass scraping"""
        # Switch to scraper tab
        self.tabs.setCurrentIndex(1)
        
        # Set default parameters
        self.mass_mode_radio.setChecked(True)
        self.artists_count_spin.setValue(1000)
        self.artworks_count_spin.setValue(20)
        self.use_categories_check.setChecked(True)
        
        # Start scraping
        QTimer.singleShot(500, self.start_scraper)
    
    def quick_start_optimize(self):
        """Quick start data optimization"""
        # Switch to cleanup tab
        self.tabs.setCurrentIndex(2)
        
        # Set default parameters
        self.clear_low_quality_check.setChecked(True)
        self.clear_duplicates_check.setChecked(True)
        self.rebuild_data_check.setChecked(True)
        self.move_files_radio.setChecked(True)
        
        # Start cleanup
        QTimer.singleShot(500, self.start_cleanup)

# Main function
def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and display main window
    main_window = AidaArtScraperApp()
    main_window.show()
    
    # Run application loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 