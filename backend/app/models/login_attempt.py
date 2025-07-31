from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if user doesn't exist
    username = Column(String(50), nullable=True)  # Store username even if user is deleted
    attempt_type = Column(String(20), nullable=False)  # 'password', 'fingerprint', 'face', 'palmprint'
    success = Column(Boolean, nullable=False)
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    location_info = Column(JSON)  # Store geolocation if available
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="login_attempts")

    def __repr__(self):
        return f"<LoginAttempt(id={self.id}, username='{self.username}', type='{self.attempt_type}', success={self.success})>"

    @property
    def is_password_attempt(self):
        return self.attempt_type == "password"

    @property
    def is_biometric_attempt(self):
        return self.attempt_type in ["fingerprint", "face", "palmprint"]

    @property
    def is_successful(self):
        return self.success

    @property
    def is_failed(self):
        return not self.success 