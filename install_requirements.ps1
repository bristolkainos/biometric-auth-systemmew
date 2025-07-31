Write-Host "Installing Biometric Authentication System Dependencies..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not activated. Please run .\activate_env.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Yellow

# Upgrade pip first
Write-Host "Upgrading pip..." -ForegroundColor Cyan
pip install --upgrade pip

# Install core dependencies first
Write-Host "Installing core dependencies..." -ForegroundColor Cyan
$coreDeps = @(
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "pydantic-settings",
    "python-multipart",
    "python-dotenv",
    "email-validator"
)

foreach ($dep in $coreDeps) {
    Write-Host "Installing $dep..." -ForegroundColor Yellow
    pip install $dep
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $dep" -ForegroundColor Red
    }
}

# Install database dependencies
Write-Host "Installing database dependencies..." -ForegroundColor Cyan
$dbDeps = @(
    "sqlalchemy",
    "alembic"
)

foreach ($dep in $dbDeps) {
    Write-Host "Installing $dep..." -ForegroundColor Yellow
    pip install $dep
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $dep" -ForegroundColor Red
    }
}

# Install security dependencies
Write-Host "Installing security dependencies..." -ForegroundColor Cyan
$securityDeps = @(
    "python-jose[cryptography]",
    "passlib[bcrypt]"
)

foreach ($dep in $securityDeps) {
    Write-Host "Installing $dep..." -ForegroundColor Yellow
    pip install $dep
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $dep" -ForegroundColor Red
    }
}

# Install image processing dependencies (with fallbacks)
Write-Host "Installing image processing dependencies..." -ForegroundColor Cyan

# Try to install opencv-python
Write-Host "Installing opencv-python..." -ForegroundColor Yellow
pip install opencv-python
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install opencv-python, trying opencv-python-headless..." -ForegroundColor Yellow
    pip install opencv-python-headless
}

# Install numpy and scikit-learn
$mlDeps = @(
    "numpy",
    "scikit-learn",
    "pillow"
)

foreach ($dep in $mlDeps) {
    Write-Host "Installing $dep..." -ForegroundColor Yellow
    pip install $dep
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $dep" -ForegroundColor Red
    }
}

# Try to install face-recognition (may fail on Windows)
Write-Host "Installing face-recognition..." -ForegroundColor Yellow
pip install face-recognition
if ($LASTEXITCODE -ne 0) {
    Write-Host "face-recognition failed to install. This is common on Windows." -ForegroundColor Yellow
    Write-Host "The system will work without face recognition for now." -ForegroundColor Yellow
}

# Install dlib-binary (precompiled version)
Write-Host "Installing dlib-binary..." -ForegroundColor Yellow
pip install dlib-binary
if ($LASTEXITCODE -ne 0) {
    Write-Host "dlib-binary failed to install. This is common on Windows." -ForegroundColor Yellow
}

# Install additional dependencies
Write-Host "Installing additional dependencies..." -ForegroundColor Cyan
$additionalDeps = @(
    "httpx",
    "pytest",
    "pytest-asyncio",
    "redis",
    "celery"
)

foreach ($dep in $additionalDeps) {
    Write-Host "Installing $dep..." -ForegroundColor Yellow
    pip install $dep
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $dep" -ForegroundColor Red
    }
}

Write-Host "==================================================" -ForegroundColor Green
Write-Host "Installation completed!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Test if the main modules can be imported
Write-Host "Testing imports..." -ForegroundColor Cyan
try {
    python -c "import fastapi; print('✓ FastAPI imported successfully')"
    python -c "import uvicorn; print('✓ Uvicorn imported successfully')"
    python -c "import sqlalchemy; print('✓ SQLAlchemy imported successfully')"
    python -c "import pydantic; print('✓ Pydantic imported successfully')"
    Write-Host "✓ Core dependencies are working!" -ForegroundColor Green
} catch {
    Write-Host "✗ Some imports failed. Check the errors above." -ForegroundColor Red
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Navigate to backend: cd backend" -ForegroundColor White
Write-Host "2. Start the server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
Write-Host "" 