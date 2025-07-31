# Database Configuration Switcher - GCP PostgreSQL Only
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("development", "production")]
    [string]$Environment
)

Write-Host "🔄 Switching to $Environment environment with GCP PostgreSQL..." -ForegroundColor Green

$envFile = "backend\.env"

if ($Environment -eq "development") {
    # Development environment with GCP PostgreSQL
    @"
# Database Configuration - GCP PostgreSQL (Development)
DB_USER=postgres
DB_PASSWORD=w14q4q4
DB_HOST=35.226.111.185
DB_PORT=5432
DB_NAME=bio_login
DATABASE_URL=postgresql://postgres:w14q4q4@35.226.111.185:5432/bio_login

# Security Configuration
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET=your-jwt-secret-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS Origins (comma-separated, no JSON)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*

# Biometric Settings
MIN_BIOMETRIC_METHODS=1
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30
SESSION_TIMEOUT_HOURS=24
ENABLE_STRICT_BIOMETRIC_VALIDATION=false
ALLOW_DEMO_BIOMETRIC_DATA=true
MIN_IMAGE_SIZE=32

# File Upload Settings
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=jpg,jpeg,png
UPLOAD_DIR=uploads

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379

# Model Settings
MODEL_PATH=models
FINGERPRINT_MATCH_THRESHOLD=0.8
PALMPRINT_MATCH_THRESHOLD=0.8
"@ | Set-Content $envFile
    Write-Host "✅ Switched to DEVELOPMENT environment with GCP PostgreSQL" -ForegroundColor Green
}
else {
    # Production environment with GCP PostgreSQL
    @"
# Database Configuration - GCP PostgreSQL (Production)
DB_USER=postgres
DB_PASSWORD=w14q4q4
DB_HOST=35.226.111.185
DB_PORT=5432
DB_NAME=bio_login
DATABASE_URL=postgresql://postgres:w14q4q4@35.226.111.185:5432/bio_login

# Security Configuration - CHANGE THESE IN PRODUCTION!
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET=your-jwt-secret-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS Origins (restricted for production)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Allowed Hosts (restricted for production)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Biometric Settings (stricter for production)
MIN_BIOMETRIC_METHODS=2
MAX_LOGIN_ATTEMPTS=3
LOCKOUT_DURATION_MINUTES=60
SESSION_TIMEOUT_HOURS=8
ENABLE_STRICT_BIOMETRIC_VALIDATION=true
ALLOW_DEMO_BIOMETRIC_DATA=false
MIN_IMAGE_SIZE=64

# File Upload Settings
MAX_FILE_SIZE_MB=5
ALLOWED_FILE_TYPES=jpg,jpeg,png
UPLOAD_DIR=uploads

# Model Settings
MODEL_PATH=models
FINGERPRINT_MATCH_THRESHOLD=0.9
PALMPRINT_MATCH_THRESHOLD=0.9
"@ | Set-Content $envFile
    Write-Host "✅ Switched to PRODUCTION environment with GCP PostgreSQL" -ForegroundColor Green
    Write-Host "⚠️  Remember to change SECRET_KEY and JWT_SECRET in production!" -ForegroundColor Yellow
}

Write-Host "🔗 Database: GCP PostgreSQL (35.226.111.185:5432/bio_login)" -ForegroundColor Cyan
Write-Host "📝 Configuration saved to: $envFile" -ForegroundColor Cyan
