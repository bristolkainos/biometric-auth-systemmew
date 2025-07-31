@echo off
echo Creating new Python 3.13.5 environment...

REM Remove existing environment if it exists
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)
if exist ".venv" (
    echo Removing existing virtual environment...
    rmdir /s /q .venv
)

REM Create new virtual environment
echo Creating new virtual environment with Python 3.13.5...
python -m venv venv --clear

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install base requirements
echo Installing base requirements...
python -m pip install wheel setuptools

echo Virtual environment created successfully!
echo.
echo To activate the environment, run:
echo     venv\Scripts\activate.bat
echo.
echo To install requirements, run:
echo     python -m pip install -r requirements-python313.txt
echo.
echo Current Python version:
python --version
echo.
pause
