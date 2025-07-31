from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    biometric_data = relationship("BiometricData", back_populates="user", cascade="all, delete-orphan")
    login_attempts = relationship("LoginAttempt", back_populates="user")
    # sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")  # Removed

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_locked_out(self):
        """Check if user account is locked due to too many failed attempts"""
        from core.config import settings
        return self.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS

    def increment_failed_attempts(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1

    def reset_failed_attempts(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0

    def update_last_login(self):
        """Update last login timestamp"""
        from datetime import datetime
        self.last_login = datetime.utcnow() 
