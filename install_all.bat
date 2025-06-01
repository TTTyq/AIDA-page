@echo off
REM 一键安装Node和Python依赖

REM 1. 安装Node依赖（包括frontend和docs）
echo 正在安装Node依赖...
npm install
if %errorlevel% neq 0 (
    echo npm install 失败，请检查Node环境。
    exit /b %errorlevel%
)

REM 2. 安装Python依赖
cd backend
if not exist venv (
    echo 正在创建Python虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo 正在安装Python依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo pip install 失败，请检查Python环境。
    exit /b %errorlevel%
)
cd ..

echo 所有依赖安装完成！
pause 