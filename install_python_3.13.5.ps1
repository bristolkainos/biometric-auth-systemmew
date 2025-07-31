# Install Python 3.13.5 and set up environment
Write-Host "Installing Python 3.13.5..." -ForegroundColor Green

# Set download URL for Python 3.13.5
$pythonUrl = "https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
$installerPath = "python-3.13.5-installer.exe"

# Download Python installer
Write-Host "Downloading Python 3.13.5..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

# Install Python
Write-Host "Installing Python 3.13.5..." -ForegroundColor Yellow
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
python -m venv venv

# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install base requirements
Write-Host "`nInstalling base requirements..." -ForegroundColor Yellow
python -m pip install wheel setuptools

Write-Host "`nPython 3.13.5 installation completed!" -ForegroundColor Green
Write-Host "Virtual environment created and activated!" -ForegroundColor Green

Write-Host "`nTo activate the environment in the future, run:" -ForegroundColor Yellow
Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan

Write-Host "`nTo install project requirements, run:" -ForegroundColor Yellow
Write-Host "    python -m pip install -r requirements-python313.txt" -ForegroundColor Cyan

Read-Host "`nPress Enter to exit"
