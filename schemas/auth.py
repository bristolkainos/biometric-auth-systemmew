from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
import base64


class BiometricDataInput(BaseModel):
    biometric_type: str = Field(..., description="Type of biometric: fingerprint, face, or palmprint")
    image_data: str = Field(..., description="Base64 encoded image data")
    
    @field_validator('image_data', mode='before')
    @classmethod
    def validate_base64(cls, v):
        if isinstance(v, str):
            try:
                import base64
                # Validate that it's valid base64
                base64.b64decode(v)
                return v
            except Exception as e:
                raise ValueError(f"Invalid base64 encoding: {e}")
        return v

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password")
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Last name")
    biometric_data: List[BiometricDataInput] = Field(..., description="List of biometric data")

class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")
    biometric_type: str = Field(..., description="Type of biometric for verification (face, fingerprint, or palmprint)")
    biometric_data: str = Field(..., description="Base64 encoded biometric image data")
    
    @field_validator('biometric_data', mode='before')
    @classmethod
    def validate_base64(cls, v):
        if isinstance(v, str):
            try:
                import base64
                # Validate that it's valid base64
                base64.b64decode(v)
                return v
            except Exception as e:
                raise ValueError(f"Invalid base64 encoding: {e}")
        return v

class AdminLogin(BaseModel):
    username: str = Field(..., description="Admin username")
    password: str = Field(..., description="Admin password")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(..., description="Token type (bearer)")
    expires_in: int = Field(..., description="Token expiration time in seconds")

class RefreshToken(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")

class UserResponse(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    is_active: bool = Field(..., description="Account active status")
    is_verified: bool = Field(..., description="Email verification status")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True

class AdminResponse(BaseModel):
    id: int = Field(..., description="Admin ID")
    username: str = Field(..., description="Admin username")
    email: str = Field(..., description="Admin email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    is_super_admin: bool = Field(..., description="Super admin status")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True 
