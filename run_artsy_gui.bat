@echo off
echo AIDA艺术爬虫启动器
echo ===================

cd scraper
python aida_art_scraper.py

if %ERRORLEVEL% neq 0 (
    echo 程序异常退出，错误码: %ERRORLEVEL%
    pause
) 