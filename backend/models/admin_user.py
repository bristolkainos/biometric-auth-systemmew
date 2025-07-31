from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
from backend.core.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_super_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    # admin_actions = relationship("AdminAction", back_populates="admin_user")

    def __repr__(self):
        return f"<AdminUser(id={self.id}, username='{self.username}', email='{self.email}')>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_last_login(self):
        """Update last login timestamp"""
        from datetime import datetime
        self.last_login = datetime.utcnow()

    def can_manage_admins(self):
        """Check if admin can manage other admins"""
        return self.is_super_admin 
