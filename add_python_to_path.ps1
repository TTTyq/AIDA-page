# 添加Python到系统PATH
$pythonPath = "C:\Program Files\Python312"
$pythonScriptsPath = "C:\Program Files\Python312\Scripts"

# 获取当前PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")

# 检查是否已经在PATH中
if (-not $currentPath.Contains($pythonPath)) {
    # 添加Python目录到PATH
    $newPath = "$pythonPath;$pythonScriptsPath;$currentPath"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
    Write-Host "Python已成功添加到系统PATH变量。"
} else {
    Write-Host "Python已在PATH变量中，无需添加。"
}

# 显示当前PATH
Write-Host "当前系统PATH环境变量:"
[Environment]::GetEnvironmentVariable("PATH", "Machine")

# 提示需要重启终端
Write-Host "请重启PowerShell或命令提示符以使更改生效。" 