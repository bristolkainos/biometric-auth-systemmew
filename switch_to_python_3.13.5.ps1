# Require administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as Administrator!"
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "Checking current Python installation..." -ForegroundColor Yellow
python --version

Write-Host @"

========================================
IMPORTANT: Please close all Python processes and IDEs before continuing
This script will:
1. Help you uninstall existing Python
2. Install Python 3.13.5
3. Set up a new virtual environment
========================================

"@ -ForegroundColor Cyan

Read-Host "Press Enter to continue"

# List existing Python installations
Write-Host "Current Python installations:" -ForegroundColor Yellow
Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Python*"} | Select-Object Name, Version

# Uninstall existing Python installations
Write-Host "`nUninstalling existing Python installations..." -ForegroundColor Yellow
Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Python*"} | ForEach-Object {
    Write-Host "Uninstalling $($_.Name)..." -ForegroundColor Red
    $_.Uninstall()
}

# Remove Python directories
$pythonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:PROGRAMFILES\Python",
    "$env:PROGRAMFILES(X86)\Python"
)

foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        Write-Host "Removing $path..." -ForegroundColor Yellow
        Remove-Item -Path $path -Recurse -Force
    }
}

# Download Python 3.13.5
Write-Host "`nDownloading Python 3.13.5..." -ForegroundColor Green
$pythonUrl = "https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
$installerPath = "python-3.13.5-amd64.exe"
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

# Install Python 3.13.5
Write-Host "Installing Python 3.13.5..." -ForegroundColor Green
Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0", "Include_pip=1" -Wait

# Remove installer
Remove-Item $installerPath

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify Python installation
Write-Host "`nVerifying Python installation..." -ForegroundColor Green
python --version

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Green
python -m venv venv --clear

# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host @"

Installation completed!

If Python version is not 3.13.5, please:
1. Restart your computer
2. Run this script again

To activate the environment in the future, run:
    .\venv\Scripts\Activate.ps1

"@ -ForegroundColor Green

Read-Host "Press Enter to exit"
