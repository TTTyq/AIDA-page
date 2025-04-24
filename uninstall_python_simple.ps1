# Simple Python Uninstall Script

# Define Python path
$pythonPath = "C:\Program Files\Python312"

# Check if Python folder exists
if (Test-Path $pythonPath) {
    Write-Host "Found Python installation at: $pythonPath"
    
    # Try to delete Python folder directly
    try {
        Remove-Item -Path $pythonPath -Recurse -Force -ErrorAction Stop
        Write-Host "Successfully deleted Python directory."
    }
    catch {
        Write-Host "Could not delete Python directory. Error: $_"
        Write-Host "Please manually delete: $pythonPath"
    }
    
    # Clean PATH environment variable
    try {
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        $pathItems = $currentPath -split ';' | Where-Object { -not $_.Contains("Python") }
        $newPath = $pathItems -join ';'
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
        Write-Host "Cleaned PATH environment variable."
    }
    catch {
        Write-Host "Could not update PATH environment variable. Error: $_"
    }
}
else {
    Write-Host "Could not find Python installation at: $pythonPath"
}

# Check other possible Python installations
$otherPaths = @(
    "C:\Python*",
    "C:\Program Files (x86)\Python*",
    "$env:LOCALAPPDATA\Programs\Python\Python*"
)

foreach ($path in $otherPaths) {
    $found = Get-Item $path -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "Found other Python installation(s):"
        foreach ($item in $found) {
            Write-Host "  - $($item.FullName)"
            Write-Host "    Please manually delete this directory."
        }
    }
}

Write-Host "Python uninstallation process completed."
Write-Host "Please restart your computer to ensure all changes take effect." 