# PowerShell installation script for Python 3.13.5
# This version is optimized for Windows Store PowerShell and handles permission issues

# Check if running in Windows Store PowerShell
$isStorePowershell = $PSVersionTable.PSEdition -eq 'Core' -and $PSVersionTable.PSVersion.Major -eq 7

# Function to request elevation if needed
function Request-AdminPrivileges {
    if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Warning "This script requires administrator privileges."
        Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit
    }
}

# Function to safely remove directory
function Remove-DirectorySafely {
    param([string]$path)
    if (Test-Path $path) {
        try {
            Remove-Item -Path $path -Recurse -Force -ErrorAction Stop
            Write-Host "Successfully removed $path" -ForegroundColor Green
        } catch {
            Write-Warning "Could not remove $path. Error: $_"
        }
    }
}

# Main installation function
function Install-Python313 {
    Write-Host @"
========================================
Python 3.13.5 Installation Script
----------------------------------------
This script will:
1. Remove existing Python installations
2. Install Python 3.13.5
3. Set up a virtual environment
4. Configure pip and basic packages
========================================
"@ -ForegroundColor Cyan

    Read-Host "Press Enter to continue or Ctrl+C to cancel"

    # Create a temporary directory for downloads
    $tempDir = Join-Path $env:TEMP "Python313Install"
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

    # Download Python 3.13.5
    $pythonUrl = "https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
    $installerPath = Join-Path $tempDir "python-3.13.5-amd64.exe"
    
    Write-Host "`nDownloading Python 3.13.5..." -ForegroundColor Yellow
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
    } catch {
        Write-Error "Failed to download Python installer: $_"
        exit 1
    }

    # Install Python with specific configurations
    Write-Host "`nInstalling Python 3.13.5..." -ForegroundColor Yellow
    $installArgs = @(
        "/quiet"
        "InstallAllUsers=1"
        "PrependPath=1"
        "Include_test=0"
        "Include_pip=1"
        "Include_doc=0"
        "CompileAll=1"
        "SimpleInstall=1"
    )
    try {
        Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -NoNewWindow
    } catch {
        Write-Error "Failed to install Python: $_"
        exit 1
    }

    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    # Verify Python installation
    Write-Host "`nVerifying Python installation..." -ForegroundColor Yellow
    try {
        $pythonVersion = python --version
        Write-Host "Installed: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Error "Python verification failed. Please restart your computer and try again."
        exit 1
    }

    # Set up virtual environment
    Write-Host "`nSetting up virtual environment..." -ForegroundColor Yellow
    try {
        python -m venv venv --clear
        Write-Host "Virtual environment created successfully!" -ForegroundColor Green
    } catch {
        Write-Error "Failed to create virtual environment: $_"
        exit 1
    }

    # Activate virtual environment
    Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
    try {
        . .\venv\Scripts\Activate.ps1
        Write-Host "Virtual environment activated!" -ForegroundColor Green
    } catch {
        Write-Error "Failed to activate virtual environment: $_"
        exit 1
    }

    # Upgrade pip and install basic packages
    Write-Host "`nUpgrading pip and installing basic packages..." -ForegroundColor Yellow
    try {
        python -m pip install --upgrade pip
        python -m pip install wheel setuptools
        Write-Host "Basic packages installed successfully!" -ForegroundColor Green
    } catch {
        Write-Error "Failed to upgrade pip or install basic packages: $_"
        exit 1
    }

    # Clean up
    Remove-DirectorySafely $tempDir

    Write-Host @"
`nPython 3.13.5 Installation Complete!
----------------------------------------
To activate the virtual environment:
    .\venv\Scripts\Activate.ps1

To install project requirements:
    python -m pip install -r requirements-python313.txt

To verify installation:
    python --version
    pip --version
----------------------------------------
"@ -ForegroundColor Green
}

# Main script execution
try {
    Request-AdminPrivileges
    Install-Python313
} catch {
    Write-Error "An unexpected error occurred: $_"
    exit 1
} finally {
    Read-Host "`nPress Enter to exit"
}
