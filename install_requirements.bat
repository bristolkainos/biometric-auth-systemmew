@echo off
echo ==================================================
echo Installing Biometric Authentication System Dependencies...
echo ==================================================

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo Virtual environment not activated. Please run activate_env.bat first.
    pause
    exit /b 1
)

echo Virtual environment: %VIRTUAL_ENV%

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install core dependencies
echo Installing core dependencies...
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-multipart python-dotenv email-validator

REM Install database dependencies
echo Installing database dependencies...
pip install sqlalchemy alembic

REM Install security dependencies
echo Installing security dependencies...
pip install "python-jose[cryptography]" "passlib[bcrypt]"

REM Install image processing dependencies
echo Installing image processing dependencies...
pip install opencv-python numpy scikit-learn pillow

REM Try to install face-recognition (may fail on Windows)
echo Installing face-recognition...
pip install face-recognition
if errorlevel 1 (
    echo face-recognition failed to install. This is common on Windows.
    echo The system will work without face recognition for now.
)

REM Install dlib-binary
echo Installing dlib-binary...
pip install dlib-binary
if errorlevel 1 (
    echo dlib-binary failed to install. This is common on Windows.
)

REM Install additional dependencies
echo Installing additional dependencies...
pip install httpx pytest pytest-asyncio redis celery

echo ==================================================
echo Installation completed!
echo ==================================================

REM Test imports
echo Testing imports...
python -c "import fastapi; print('✓ FastAPI imported successfully')"
python -c "import uvicorn; print('✓ Uvicorn imported successfully')"
python -c "import sqlalchemy; print('✓ SQLAlchemy imported successfully')"
python -c "import pydantic; print('✓ Pydantic imported successfully')"

echo.
echo Next steps:
echo 1. Navigate to backend: cd backend
echo 2. Start the server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
pause 