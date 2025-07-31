@echo off
echo Installing requirements for Python 3.13.5...

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install numpy first as it's a core dependency
echo Installing numpy...
python -m pip install numpy>=1.26.0

REM Install PyTorch CPU version (more stable for initial setup)
echo Installing PyTorch...
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

REM Install core requirements one by one
echo Installing core requirements...
python -m pip install fastapi>=0.104.1
python -m pip install uvicorn[standard]>=0.24.0
python -m pip install pydantic>=2.5.0
python -m pip install sqlalchemy>=2.0.23
python -m pip install psycopg2-binary>=2.9.9
python -m pip install python-jose[cryptography]>=3.3.0
python -m pip install passlib>=1.7.4
python -m pip install python-multipart>=0.0.6
python -m pip install python-dotenv>=1.0.0
python -m pip install httpx>=0.25.2
python -m pip install pillow>=10.1.0
python -m pip install opencv-python-headless>=4.8.1.78

echo Installation completed!
echo.
echo If you encounter any issues, try installing packages one by one from requirements-python313.txt
echo For PyTorch with GPU support, visit: https://pytorch.org/get-started/locally/
pause
