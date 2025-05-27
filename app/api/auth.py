from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.auth import UserRegister, UserLogin, AuthResponse, UserResponse, Token
from app.services.auth_service import AuthService
from app.utils.auth import get_current_active_user
from app.db import models

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Valid email address (will be used for login)
    - **password**: Password (8-100 characters)
    
    Returns user information and JWT access token.
    """
    return await AuthService.register_user(db, user_data)


@router.post("/login", response_model=AuthResponse)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: Registered email address
    - **password**: User password
    
    Returns user information and JWT access token.
    """
    return await AuthService.login_user(db, user_data)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get current user's profile information.
    
    Requires valid JWT token in Authorization header:
    `Authorization: Bearer <token>`
    """
    return UserResponse.model_validate(current_user)


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh the current user's access token.
    
    Requires valid JWT token in Authorization header.
    Returns a new JWT token with extended expiration.
    """
    return await AuthService.refresh_token(db, current_user.id)


@router.post("/logout")
async def logout():
    """
    Logout endpoint (client-side token removal).
    
    Since JWT tokens are stateless, logout is handled client-side
    by removing the token from storage.
    """
    return {
        "message": "Logout successful",
        "detail": "Please remove the token from client storage"
    } 