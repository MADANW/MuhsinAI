from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.db.crud import UserCRUD
from app.utils.auth import verify_password, get_password_hash, create_access_token
from app.utils.config import settings
from app.models.auth import UserRegister, UserLogin, AuthResponse, Token, UserResponse


class AuthService:
    """Authentication service with business logic."""

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegister) -> AuthResponse:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            AuthResponse: User info and JWT token
            
        Raises:
            HTTPException: If email already exists or registration fails
        """
        try:
            # Check if user already exists
            existing_user = await UserCRUD.get_user_by_email(db, user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Create user
            user = await UserCRUD.create_user(
                db=db,
                email=user_data.email,
                hashed_password=hashed_password
            )
            
            # Create access token
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": str(user.id)},
                expires_delta=access_token_expires
            )
            
            # Prepare response
            user_response = UserResponse.model_validate(user)
            token = Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=settings.access_token_expire_minutes * 60
            )
            
            return AuthResponse(
                user=user_response,
                token=token,
                message="User registered successfully"
            )
            
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )

    @staticmethod
    async def login_user(db: AsyncSession, user_data: UserLogin) -> AuthResponse:
        """
        Authenticate and login a user.
        
        Args:
            db: Database session
            user_data: User login data
            
        Returns:
            AuthResponse: User info and JWT token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Get user by email
        user = await UserCRUD.get_user_by_email(db, user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        # Prepare response
        user_response = UserResponse.model_validate(user)
        token = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
        return AuthResponse(
            user=user_response,
            token=token,
            message="Login successful"
        )

    @staticmethod
    async def refresh_token(db: AsyncSession, user_id: int) -> Token:
        """
        Refresh user's access token.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Token: New JWT token
            
        Raises:
            HTTPException: If user not found
        """
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        ) 