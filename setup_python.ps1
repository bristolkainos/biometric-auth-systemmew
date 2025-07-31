# Python installation paths
$pythonPath = "C:\Users\BRISTOL\AppData\Local\Programs\Python\Python313"
$pythonExe = Join-Path $pythonPath "python.exe"
$projectPath = "D:\Chantal\Biometric_Login_auth-main\Biometric_Login_auth-main"

# Check if Python exists
if (-not (Test-Path $pythonExe)) {
    Write-Host "Python not found at $pythonExe" -ForegroundColor Red
    Write-Host "Please install Python 3.13.5 first" -ForegroundColor Yellow
    exit 1
}

# Add Python to current session Path
$env:Path = "$pythonPath;$pythonPath\Scripts;$env:Path"

# Add Python to system Path permanently
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath.Contains($pythonPath)) {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$pythonPath;$pythonPath\Scripts;$userPath",
        "User"
    )
}

# Remove old venv if exists
if (Test-Path "venv") {
    Remove-Item -Recurse -Force "venv"
}

# Create new virtual environment using full path
Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
& $pythonExe -m venv venv

# Verify venv creation
if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "Virtual environment creation failed!" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip using full path
Write-Host "Upgrading pip..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
.\venv\Scripts\pip.exe install -r requirements.txt

Write-Host "Setup complete!" -ForegroundColor Green
& .\venv\Scripts\python.exe --version