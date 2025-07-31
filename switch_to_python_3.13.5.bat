@echo off
setlocal enabledelayedexpansion

echo Checking current Python installation...
python --version

echo.
echo ========================================
echo IMPORTANT: Please close all Python processes and IDEs before continuing
echo This script will:
echo 1. Help you uninstall existing Python
echo 2. Install Python 3.13.5
echo 3. Set up a new virtual environment
echo ========================================
echo.

pause

REM Open Programs and Features to uninstall existing Python
echo Opening Programs and Features...
echo Please uninstall any existing Python versions
start appwiz.cpl
pause

REM Clear Python from PATH
echo Removing Python from PATH...
setx PATH "%PATH:Python;=%" /M
setx PATH "%PATH:Python310;=%" /M

REM Download Python 3.13.5
echo Downloading Python 3.13.5...
curl -L -o python-3.13.5-amd64.exe https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe

REM Install Python 3.13.5
echo Installing Python 3.13.5...
python-3.13.5-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1

echo Waiting for installation to complete...
timeout /t 10 /nobreak

REM Remove the installer
del python-3.13.5-amd64.exe

REM Refresh environment variables
echo Refreshing environment variables...
refreshenv

echo Verifying Python installation...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv --clear

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

echo.
echo If Python version is not 3.13.5, please:
echo 1. Restart your computer
echo 2. Run this script again
echo.
echo To activate the environment in the future, run:
echo     venv\Scripts\activate.bat
echo.

pause
