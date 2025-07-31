from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.core.database import Base

class BiometricData(Base):
    __tablename__ = "biometric_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    biometric_type = Column(String(20), nullable=False)  # 'fingerprint', 'face', 'palmprint'
    biometric_hash = Column(String(255), nullable=False)
    biometric_features = Column(Text)  # JSON string for additional features
    processing_analysis = Column(Text)  # JSON string for detailed processing analysis
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="biometric_data")

    def __repr__(self):
        return f"<BiometricData(id={self.id}, user_id={self.user_id}, type='{self.biometric_type}')>"

    @property
    def is_fingerprint(self):
        return self.biometric_type == "fingerprint"

    @property
    def is_face(self):
        return self.biometric_type == "face"

    @property
    def is_palmprint(self):
        return self.biometric_type == "palmprint" 
