@echo off
echo ===================================================
echo Artsy艺术数据工具 - 整合版
echo ===================================================

REM 检查虚拟环境并激活
if exist .venv\Scripts\activate.bat (
    echo 正在激活虚拟环境...
    call .venv\Scripts\activate.bat
) else (
    echo 未找到虚拟环境，使用系统Python...
)

REM 显示Python版本
python --version

REM 主菜单
:MENU
cls
echo.
echo Artsy艺术数据工具 - 请选择操作:
echo ---------------------------------------------------
echo  1. 简单爬虫 - 少量艺术家数据 (推荐测试用)
echo  2. 大规模爬虫 - 大量艺术家数据
echo  3. 清理数据 - 处理低质量和重复图片
echo  4. 重建艺术家文档
echo  5. 查看数据统计
echo  6. 打开数据文件夹
echo  7. 启动GUI工具 (如果可用)
echo  0. 退出
echo ---------------------------------------------------
echo.

set /p choice="请输入选项 (0-7): "

if "%choice%"=="1" goto RUN_SIMPLE
if "%choice%"=="2" goto RUN_MASS
if "%choice%"=="3" goto CLEANUP
if "%choice%"=="4" goto REBUILD_DOCS
if "%choice%"=="5" goto STATS
if "%choice%"=="6" goto OPEN_FOLDER
if "%choice%"=="7" goto RUN_GUI
if "%choice%"=="0" goto END
echo 无效选项，请重试!
timeout /t 2 >nul
goto MENU

:RUN_SIMPLE
cls
echo 运行简单爬虫 - 少量艺术家数据
echo ---------------------------------------------------
set /p num_artists="请输入要爬取的艺术家数量 (默认100): "
if "%num_artists%"=="" set num_artists=100

set /p max_artworks="请输入每位艺术家最多爬取的作品数量 (默认10): "
if "%max_artworks%"=="" set max_artworks=10

set /p use_cat="是否使用分类模式爬取？推荐！(Y/N，默认Y): "
if /i "%use_cat%"=="n" (
    set cat_param=
) else (
    set cat_param=--use-categories
)

echo.
echo 将爬取 %num_artists% 位艺术家，每位最多 %max_artworks% 件作品
echo.
set /p confirm="确认开始爬取? (Y/N): "
if /i not "%confirm%"=="y" goto MENU

echo 正在开始爬取...
python scraper\simple_artsy_scraper.py --num-artists %num_artists% --max-artworks %max_artworks% %cat_param%
echo.
pause
goto MENU

:RUN_MASS
cls
echo 运行大规模爬虫 - 大量艺术家数据
echo ---------------------------------------------------
echo 注意：这将爬取大量数据，可能需要很长时间！
echo.

set /p num_artists="请输入要爬取的艺术家数量 (默认2000): "
if "%num_artists%"=="" set num_artists=2000

set /p max_artworks="请输入每位艺术家最多爬取的作品数量 (默认30): "
if "%max_artworks%"=="" set max_artworks=30

set /p checkpoint="请输入保存检查点的间隔 (默认10): "
if "%checkpoint%"=="" set checkpoint=10

echo.
echo 将爬取 %num_artists% 位艺术家，每位最多 %max_artworks% 件作品
echo 每爬取 %checkpoint% 位艺术家保存一次进度
echo.
set /p confirm="确认开始爬取? (Y/N): "
if /i not "%confirm%"=="y" goto MENU

echo 正在开始大规模爬取...
python scraper\mass_artsy_scraper.py --num-artists %num_artists% --max-artworks %max_artworks% --checkpoint-interval %checkpoint%
echo.
pause
goto MENU

:CLEANUP
cls
echo 清理数据 - 处理低质量和重复图片
echo ---------------------------------------------------
set /p min_size="请输入最小文件大小 (KB，默认15): "
if "%min_size%"=="" set min_size=15

set /p min_width="请输入最小图像宽度 (像素，默认400): "
if "%min_width%"=="" set min_width=400

set /p min_height="请输入最小图像高度 (像素，默认400): "
if "%min_height%"=="" set min_height=400

echo.
echo 将清理小于 %min_size%KB 或尺寸小于 %min_width%x%min_height% 的图片
echo.
set /p confirm="确认开始清理? (Y/N): "
if /i not "%confirm%"=="y" goto MENU

echo 正在开始清理...
python cleanup_data.py --min-size %min_size% --min-width %min_width% --min-height %min_height%
echo.
pause
goto MENU

:REBUILD_DOCS
cls
echo 重建艺术家文档
echo ---------------------------------------------------
echo 将重建所有艺术家的文档，包括作品列表和图片链接
echo.
set /p confirm="确认重建文档? (Y/N): "
if /i not "%confirm%"=="y" goto MENU

echo 正在重建文档...
python cleanup_data.py --rebuild-docs
echo.
pause
goto MENU

:STATS
cls
echo 数据统计
echo ---------------------------------------------------
echo 正在收集数据统计...

set data_dir=%~dp0\data\artsy

echo.
echo Artsy艺术数据库统计
echo ===================================================

REM 检查艺术家数据文件
set artists_file=%data_dir%\artsy_artists.csv
if exist "%artists_file%" (
    REM 简单地统计行数作为艺术家数
    for /f %%a in ('type "%artists_file%" ^| find /c /v ""') do set num_artists=%%a
    set /a num_artists=%num_artists%-1
    echo 艺术家总数: %num_artists%
) else (
    echo 未找到艺术家数据文件
)

REM 检查艺术品数据文件
set artworks_file=%data_dir%\artsy_artworks.csv
if exist "%artworks_file%" (
    REM 简单地统计行数作为艺术品数
    for /f %%a in ('type "%artworks_file%" ^| find /c /v ""') do set num_artworks=%%a
    set /a num_artworks=%num_artworks%-1
    echo 艺术品总数: %num_artworks%
    
    if %num_artists% gtr 0 (
        set /a avg_artworks=%num_artworks%/%num_artists%
        echo 平均每位艺术家作品数: %avg_artworks%
    )
) else (
    echo 未找到艺术品数据文件
)

REM 检查图片数据
set images_dir=%data_dir%\images
if exist "%images_dir%" (
    echo.
    echo 图片数据统计:
    echo - 图片目录: %images_dir%
    
    REM 统计低质量图片
    set lq_dir=%images_dir%\low_quality
    if exist "%lq_dir%" (
        set lq_count=0
        for /r "%lq_dir%" %%f in (*.jpg, *.jpeg, *.png, *.webp) do set /a lq_count+=1
        echo - 低质量图片: %lq_count%
    )
    
    REM 统计重复图片
    set dup_dir=%images_dir%\duplicates
    if exist "%dup_dir%" (
        set dup_count=0
        for /r "%dup_dir%" %%f in (*.jpg, *.jpeg, *.png, *.webp) do set /a dup_count+=1
        echo - 重复图片: %dup_count%
    )
)

REM 检查文档数据
set docs_dir=%data_dir%\artist_docs
if exist "%docs_dir%" (
    echo.
    echo 文档数据统计:
    set doc_count=0
    for %%f in ("%docs_dir%\*.md") do set /a doc_count+=1
    echo - 艺术家文档: %doc_count%
)

echo.
echo 统计生成时间: %date% %time%
echo ===================================================
echo.
pause
goto MENU

:OPEN_FOLDER
echo 正在打开数据文件夹...
start "" "%~dp0\data\artsy"
goto MENU

:RUN_GUI
cls
echo 启动GUI工具
echo ---------------------------------------------------
if exist "scraper\artsy_scraper_app.py" (
    echo 正在启动GUI应用...
    start python scraper\artsy_scraper_app.py
) else (
    echo GUI工具不可用，请先创建scraper\artsy_scraper_app.py文件
    pause
)
goto MENU

:END
echo 感谢使用Artsy艺术数据工具！
exit /b 0 