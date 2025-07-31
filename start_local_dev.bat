@echo off
echo 🚀 Starting local development environment...

REM Install required packages if needed
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install Python requirements
    pause
    exit /b 1
)

cd frontend
npm install
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ..

REM Start the local development environment
python start_local_dev.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to start development environment
    pause
    exit /b 1
)

pause
