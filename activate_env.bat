@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Virtual environment activated!
echo.
echo You can now run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
cmd /k 