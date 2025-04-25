@echo off
:: AIDA艺术爬虫工具 - 启动脚本
title AIDA艺术爬虫工具

:: 设置Python环境和工作目录
set PYTHONPATH=%~dp0
cd %~dp0

echo ================================================
echo           AIDA艺术爬虫工具正在启动...
echo ================================================
echo.
echo 正在启动图形界面，请稍候...
echo.

:: 启动GUI界面
python scraper/artsy_scraper_app.py

if ERRORLEVEL 1 (
    echo.
    echo 启动失败！请确认已安装所需依赖：
    echo pip install -r scraper/requirements.txt
    echo.
    pause
    exit /b 1
)

exit /b 0 