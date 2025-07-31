@echo off
setlocal enabledelayedexpansion

echo Installing Python 3.13.5...

REM Set download URL for Python 3.13.5
set PYTHON_URL=https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe
set INSTALLER_NAME=python-3.13.5-installer.exe

REM Download Python installer
echo Downloading Python 3.13.5...
curl -L -o %INSTALLER_NAME% %PYTHON_URL%

REM Install Python with required features and add to PATH
echo Installing Python 3.13.5...
%INSTALLER_NAME% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1

REM Wait a moment for installation to complete
timeout /t 5 /nobreak

REM Delete the installer
del %INSTALLER_NAME%

REM Verify Python installation
echo Verifying Python installation...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

echo Python 3.13.5 installation completed!
echo Virtual environment created and activated!

REM Install base requirements
python -m pip install wheel setuptools

echo.
echo To activate the environment in the future, run:
echo     venv\Scripts\activate.bat
echo.
echo To install project requirements, run:
echo     python -m pip install -r requirements-python313.txt
echo.

pause
