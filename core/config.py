from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Biometric Authentication System"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # GCP PostgreSQL Database settings - Using existing bio_login database
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "w14q4q4")
    DB_HOST: str = os.getenv("DB_HOST", "35.226.111.185")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "bio_login")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:w14q4q4@35.226.111.185:5432/bio_login")
    
    # Security settings - Must be set via environment variables
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # CORS settings - Updated for Railway deployment
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "https://frontend-production-2a3e.up.railway.app,https://biometric-auth-v2-7019.uc.r.appspot.com,https://frontend-dot-biometric-auth-v2-7019.uc.r.appspot.com,http://localhost:3000,http://localhost:3001,http://localhost:8080")
    
    # Allowed hosts for security - Updated for Railway
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS", "frontend-production-2a3e.up.railway.app,backend-production-9ec1.up.railway.app,biometric-auth-v2-7019.uc.r.appspot.com,frontend-dot-biometric-auth-v2-7019.uc.r.appspot.com,localhost,127.0.0.1,0.0.0.0")
    
    # Biometric settings
    MIN_BIOMETRIC_METHODS: int = int(os.getenv("MIN_BIOMETRIC_METHODS", "1"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES: int = int(os.getenv("LOCKOUT_DURATION_MINUTES", "30"))
    SESSION_TIMEOUT_HOURS: int = int(os.getenv("SESSION_TIMEOUT_HOURS", "24"))
    
    # Biometric validation settings
    ENABLE_STRICT_BIOMETRIC_VALIDATION: bool = os.getenv("ENABLE_STRICT_BIOMETRIC_VALIDATION", "false").lower() == "true"
    ALLOW_DEMO_BIOMETRIC_DATA: bool = os.getenv("ALLOW_DEMO_BIOMETRIC_DATA", "true").lower() == "true"
    MIN_IMAGE_SIZE: int = int(os.getenv("MIN_IMAGE_SIZE", "32"))
    
    # File upload settings
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    ALLOWED_FILE_TYPES: str = os.getenv("ALLOWED_FILE_TYPES", "jpg,jpeg,png,tiff,tif,bmp")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Email settings
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "true").lower() == "true"
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    # Model settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "../models")
    FINGERPRINT_MATCH_THRESHOLD: float = float(os.getenv("FINGERPRINT_MATCH_THRESHOLD", "0.8"))
    PALMPRINT_MATCH_THRESHOLD: float = float(os.getenv("PALMPRINT_MATCH_THRESHOLD", "0.8"))
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Convert ALLOWED_HOSTS string to list"""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",") if host.strip()]
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Convert ALLOWED_FILE_TYPES string to list"""
        return [file_type.strip().lower() for file_type in self.ALLOWED_FILE_TYPES.split(",") if file_type.strip()]
    
    def validate_security_settings(self):
        """Validate critical security settings"""
        if not self.SECRET_KEY or self.SECRET_KEY == "your-secret-key-here-change-in-production":
            if self.ENVIRONMENT == "production":
                raise ValueError("SECRET_KEY must be set in production environment")
            else:
                # Generate a secure key for development
                import secrets
                self.SECRET_KEY = secrets.token_urlsafe(32)
                print("⚠️  WARNING: Using auto-generated SECRET_KEY for development. Set SECRET_KEY environment variable.")
        
        if not self.JWT_SECRET or self.JWT_SECRET == "your-jwt-secret-here-change-in-production":
            if self.ENVIRONMENT == "production":
                raise ValueError("JWT_SECRET must be set in production environment")
            else:
                # Generate a secure key for development
                import secrets
                self.JWT_SECRET = secrets.token_urlsafe(32)
                print("⚠️  WARNING: Using auto-generated JWT_SECRET for development. Set JWT_SECRET environment variable.")
        
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set")
    
    def ensure_upload_directory(self):
        """Ensure upload directory exists"""
        try:
            os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        except (OSError, PermissionError):
            # For cloud environments, use /tmp
            if os.getenv("CLOUD_PROVIDER") in ["gcp", "aws", "azure"]:
                self.UPLOAD_DIR = "/tmp/uploads"
                os.makedirs(self.UPLOAD_DIR, exist_ok=True)
            else:
                raise
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

# Create and validate settings instance
settings = Settings()

# Validate security settings on import
try:
    settings.validate_security_settings()
    settings.ensure_upload_directory()
except Exception as e:
    if settings.ENVIRONMENT == "production":
        raise
    else:
        print(f"⚠️  Configuration warning: {e}")
