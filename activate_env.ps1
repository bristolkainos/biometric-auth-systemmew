Write-Host "Activating virtual environment..." -ForegroundColor Green
.\.venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Yellow
Write-Host "" 