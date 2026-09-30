"""
Vastu One - Pydantic Schemas
Request/Response models
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserSignup(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    password: str = Field(..., min_length=8, max_length=100)

    @validator("password")
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @validator("phone")
    def phone_format(cls, v):
        if v and not v.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise ValueError("Invalid phone number")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    email_verified: bool
    phone_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

    @validator("new_password")
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    profile_image: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
    success: bool = True