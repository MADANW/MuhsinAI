from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """User registration request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="Password (8-100 characters)"
    )


class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenData(BaseModel):
    """Token payload data schema."""
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    """User response schema (without sensitive data)."""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response schema."""
    user: UserResponse = Field(..., description="User information")
    token: Token = Field(..., description="Authentication token")
    message: str = Field(..., description="Success message")


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")


class PasswordValidation(BaseModel):
    """Password validation schema."""
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$",
        description="Password must contain at least one lowercase letter, one uppercase letter, and one digit"
    ) 