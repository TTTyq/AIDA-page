# 卸载Python脚本

# 定义要卸载的Python路径
$pythonPath = "C:\Program Files\Python312"

# 检查Python安装文件夹是否存在
if (Test-Path $pythonPath) {
    Write-Host "找到Python安装目录: $pythonPath"
    
    # 查找卸载程序
    $uninstallExe = Join-Path $pythonPath "uninstall.exe"
    
    if (Test-Path $uninstallExe) {
        Write-Host "找到卸载程序，开始卸载Python..."
        # 执行卸载程序
        Start-Process -FilePath $uninstallExe -ArgumentList "/quiet" -Wait
        Write-Host "Python卸载程序已执行完毕。"
    } else {
        # 如果没有找到卸载程序，使用控制面板中的卸载功能
        Write-Host "未找到卸载程序，尝试从控制面板卸载..."
        # 查找控制面板卸载字符串
        $uninstallKey = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" | 
            Get-ItemProperty | 
            Where-Object {$_.DisplayName -like "*Python 3.12*" } | 
            Select-Object -ExpandProperty UninstallString

        if ($uninstallKey) {
            Write-Host "找到控制面板卸载字符串: $uninstallKey"
            # 执行卸载命令
            $uninstallArgs = ($uninstallKey -replace "msiexec.exe", "") + " /quiet"
            Start-Process "msiexec.exe" -ArgumentList $uninstallArgs -Wait
            Write-Host "Python卸载命令已执行完毕。"
        } else {
            Write-Host "未找到控制面板卸载项。尝试手动移除Python目录..."
            # 如果都失败了，尝试直接删除文件夹
            Remove-Item -Path $pythonPath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "已尝试删除Python目录。"
        }
    }
    
    # 检查是否还存在Python目录
    if (Test-Path $pythonPath) {
        Write-Host "警告: Python目录仍然存在，可能需要手动删除: $pythonPath"
    } else {
        Write-Host "Python目录已被成功删除。"
    }
    
    # 清理PATH环境变量
    Write-Host "正在清理PATH环境变量中的Python引用..."
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    $newPath = ($currentPath -split ';' | Where-Object { -not $_.Contains("Python") }) -join ';'
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
    Write-Host "PATH环境变量已更新，Python引用已移除。"
    
} else {
    Write-Host "未找到Python安装目录: $pythonPath"
}

# 检查其他可能的Python安装
$otherPythonPaths = @(
    "C:\Python*",
    "C:\Program Files (x86)\Python*",
    "$env:LOCALAPPDATA\Programs\Python\Python*"
)

foreach ($path in $otherPythonPaths) {
    $installations = Get-Item $path -ErrorAction SilentlyContinue
    if ($installations) {
        Write-Host "检测到其他Python安装:"
        $installations | ForEach-Object {
            Write-Host "  - $_"
            Write-Host "  尝试清理此安装，请手动检查和删除。"
        }
    }
}

Write-Host "Python卸载过程已完成。请重启计算机以确保所有更改生效。" 