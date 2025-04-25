@echo off
echo AIDA Art Scraper Launcher
echo =======================

REM Set Python path
set PYTHONPATH=%~dp0..
set PYTHONIOENCODING=utf-8

REM Activate virtual environment (if exists)
if exist "%~dp0..\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%~dp0..\.venv\Scripts\activate.bat"
)

REM Check dependencies
echo Checking dependencies...
python -m pip install -r "%~dp0requirements.txt"

REM Launch GUI app
echo Launching scraper application...
cd "%~dp0"
python aida_art_scraper.py

REM If program exits with error, pause
if %ERRORLEVEL% neq 0 (
    echo Program exited abnormally with code: %ERRORLEVEL%
    pause
) 