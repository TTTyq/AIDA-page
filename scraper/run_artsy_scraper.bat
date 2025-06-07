@echo off
echo ========================================
echo       AIDA Artsy Scraper Tool
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ and try again
    pause
    exit /b 1
)

echo Python found. Checking dependencies...

REM Check if we're in the scraper directory
if not exist "backend\requirements.txt" (
    echo Error: Please run this script from the scraper directory
    echo Current directory should contain backend\requirements.txt
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing/updating dependencies...
cd backend
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo Warning: Some dependencies might not have installed correctly
)
cd ..

echo.
echo ========================================
echo Choose an option:
echo ========================================
echo 1. Run example scraping (recommended for first time)
echo 2. Start scraper API server
echo 3. Test connection to Artsy.net
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto run_example
if "%choice%"=="2" goto start_server
if "%choice%"=="3" goto test_connection
if "%choice%"=="4" goto exit
goto invalid_choice

:run_example
echo.
echo Starting Artsy scraper example...
echo This will scrape a small amount of data for demonstration.
echo.
python examples\artsy_example.py
pause
goto menu

:start_server
echo.
echo Starting Artsy scraper API server...
echo The server will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd ..
pause
goto menu

:test_connection
echo.
echo Testing connection to Artsy.net...
python -c "
import asyncio
import sys
import os
sys.path.append(os.path.join('backend'))
from app.scrapers.artsy_scraper import ArtsyScraper

async def test():
    scraper = ArtsyScraper()
    if await scraper.test_connection():
        print('✅ Connection to Artsy.net successful!')
    else:
        print('❌ Failed to connect to Artsy.net')

asyncio.run(test())
"
pause
goto menu

:invalid_choice
echo.
echo Invalid choice. Please enter 1, 2, 3, or 4.
pause
goto menu

:menu
echo.
echo ========================================
echo Choose an option:
echo ========================================
echo 1. Run example scraping (recommended for first time)
echo 2. Start scraper API server
echo 3. Test connection to Artsy.net
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto run_example
if "%choice%"=="2" goto start_server
if "%choice%"=="3" goto test_connection
if "%choice%"=="4" goto exit
goto invalid_choice

:exit
echo.
echo Thank you for using AIDA Artsy Scraper Tool!
echo.
pause 