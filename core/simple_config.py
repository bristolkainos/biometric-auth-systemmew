"""Simple configuration without .env file complications"""
import os
from typing import List


class SimpleSettings:
    """Simple settings class that only uses environment variables"""
    
    # Application settings
    APP_NAME: str = "Biometric Authentication System"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Database settings
    DATABASE_URL: str = (
        "postgresql://postgres:HPQkWaZMFgDluBdkRhJhScBhFuSkvKtm@"
        "trolley.proxy.rlwy.net:43702/railway"
    )
    
    # Security settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-here-change-in-production"
    )
    JWT_SECRET: str = os.getenv(
        "JWT_SECRET", "your-jwt-secret-here-change-in-production"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings - hardcoded for development
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Allowed hosts for security
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "*"
    ]
    
    # Biometric settings
    MIN_BIOMETRIC_METHODS: int = 1
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 30
    SESSION_TIMEOUT_HOURS: int = 24
    
    # Biometric validation settings
    ENABLE_STRICT_BIOMETRIC_VALIDATION: bool = False  # Disabled for testing
    ALLOW_DEMO_BIOMETRIC_DATA: bool = True  # Enabled for testing
    MIN_IMAGE_SIZE: int = 32
    
    # File upload settings
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = ["jpg", "jpeg", "png", "tiff", "tif", "bmp"]
    UPLOAD_DIR: str = "uploads"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email settings
    SMTP_HOST = None
    SMTP_PORT: int = 587
    SMTP_USERNAME = None
    SMTP_PASSWORD = None
    SMTP_TLS: bool = True
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "% (asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Model settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models")
    FACE_RECOGNITION_TOLERANCE: float = 0.6
    FINGERPRINT_MATCH_THRESHOLD: float = 0.8
    PALMPRINT_MATCH_THRESHOLD: float = 0.8
    
    # Rate limiting settings
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    
    # Session settings
    SESSION_SECRET_KEY: str = SECRET_KEY
    SESSION_COOKIE_NAME: str = "biometric_session"
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SECURE: bool = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE: str = "lax"
    
    # Admin settings
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_EMAIL: str = "admin@company.com"
    
    # Password policy
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True


# Create a simple settings instance
settings = SimpleSettings() 
