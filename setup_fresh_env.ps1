# Create fresh Python 3.13.5 environment
Write-Host "Setting up fresh Python 3.13.5 environment..." -ForegroundColor Green

# Remove existing environment if it exists
if (Test-Path "venv") {
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Path "venv" -Recurse -Force
}
if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Path ".venv" -Recurse -Force
}

# Create new virtual environment
Write-Host "Creating new virtual environment..." -ForegroundColor Green
python -m venv venv --clear

# Activate the virtual environment
. .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Install base requirements
Write-Host "Installing base requirements..." -ForegroundColor Green
python -m pip install wheel setuptools

Write-Host "`nVirtual environment created successfully!" -ForegroundColor Green
Write-Host "`nTo activate the environment, run:" -ForegroundColor Yellow
Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "`nTo install requirements, run:" -ForegroundColor Yellow
Write-Host "    python -m pip install -r requirements-python313.txt" -ForegroundColor Cyan
Write-Host "`nCurrent Python version:" -ForegroundColor Yellow
python --version

Read-Host -Prompt "Press Enter to exit"
