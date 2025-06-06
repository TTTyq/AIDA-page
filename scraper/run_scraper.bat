@echo off
setlocal enabledelayedexpansion

:: AIDA Scraper Tool Management
echo AIDA Scraper Tool Manager
echo ========================

:: Check command line arguments
if "%1"=="stop" goto :stop_services
if "%1"=="install" goto :install_dependencies
if "%1"=="help" goto :show_help
if not "%1"=="" (
    echo Unknown command: %1
    echo Use "run_scraper.bat help" to see available commands
    exit /b 1
)

:: Default operation: start services
goto :start_services

:show_help
echo.
echo AIDA Scraper Tool Manager - Help
echo -------------------------------
echo.
echo Usage:
echo   run_scraper.bat            - Start the scraper tool (default)
echo   run_scraper.bat install    - Install dependencies only
echo   run_scraper.bat stop       - Stop running services
echo   run_scraper.bat help       - Show this help information
echo.
exit /b 0

:check_requirements
:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python not found. Please ensure Python is installed and added to PATH
    pause
    exit /b 1
)

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Node.js not found. Please ensure Node.js is installed and added to PATH
    pause
    exit /b 1
)
exit /b 0

:install_dependencies
echo.
echo Installing dependencies...
echo =========================

call :check_requirements
if %errorlevel% neq 0 exit /b %errorlevel%

:: Create virtual environment (if it doesn't exist)
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    python -m venv backend\venv
)

:: Activate virtual environment and install backend dependencies
echo Installing backend dependencies...
call backend\venv\Scripts\activate.bat
pip install -r backend\requirements.txt

:: Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
if not exist "node_modules" (
    call npm install
)
cd ..

echo.
echo Dependencies installation completed!
echo.
if "%1"=="install" (
    pause
    exit /b 0
)
exit /b 0

:stop_services
echo.
echo Stopping scraper services...
echo ===========================

:: Use taskkill to terminate related processes
:: Find and kill Node.js processes related to our app
echo Stopping frontend service...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq node.exe" /fo csv ^| findstr /i "node.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
)

:: Find and kill Python processes related to our app
echo Stopping backend service...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| findstr /i "python.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
)

echo.
echo AIDA Scraper services stopped
echo.
pause
exit /b 0

:start_services
echo.
echo Starting scraper services...
echo ===========================

:: Install dependencies
call :install_dependencies
if %errorlevel% neq 0 exit /b %errorlevel%

:: Create data directory for storing website configurations
if not exist "backend\data" mkdir backend\data

:: Start the services
echo Starting services in single window mode...
echo.
echo AIDA Scraper Tool started successfully!
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all services
echo.

:: Start both services
start /b "" cmd /c "cd backend && call venv\Scripts\activate.bat && python main.py > ..\backend_log.txt 2>&1"
timeout /t 5 /nobreak > nul
start /b "" cmd /c "cd frontend && npm run dev > ..\frontend_log.txt 2>&1"

:: Keep the window open and show a simple status monitor
:monitor_loop
cls
echo AIDA Scraper Tool is running
echo ===========================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo.
echo Backend Log (last 5 lines):
echo ---------------------------
type backend_log.txt | findstr /n ".*" | findstr /r "^[1-5]:" 2>nul
echo.
echo Frontend Log (last 5 lines):
echo ---------------------------
type frontend_log.txt | findstr /n ".*" | findstr /r "^[1-5]:" 2>nul
echo.
echo Press Ctrl+C to stop all services
echo Press any key to refresh status...
timeout /t 10 > nul
goto monitor_loop 