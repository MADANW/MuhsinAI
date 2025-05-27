from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from app.db import models


class UserCRUD:
    """Secure CRUD operations for User model."""

    @staticmethod
    async def create_user(
        db: AsyncSession, 
        email: str, 
        hashed_password: str
    ) -> models.User:
        """
        Create a new user with secure parameters.
        
        Args:
            db: Database session
            email: User email (already validated)
            hashed_password: Bcrypt hashed password
            
        Returns:
            User: Created user object
            
        Raises:
            IntegrityError: If email already exists
        """
        db_user = models.User(
            email=email.lower().strip(),  # Normalize email
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[models.User]:
        """
        Get user by ID with SQL injection protection.
        
        Args:
            db: Database session
            user_id: User ID (validated integer)
            
        Returns:
            User or None
        """
        stmt = select(models.User).where(models.User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
        """
        Get user by email with case-insensitive search.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User or None
        """
        stmt = select(models.User).where(
            models.User.email == email.lower().strip()
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_with_chats(
        db: AsyncSession, 
        user_id: int
    ) -> Optional[models.User]:
        """
        Get user with their chat history.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User with chats loaded
        """
        stmt = select(models.User).options(
            selectinload(models.User.chats)
        ).where(models.User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """
        Delete user and cascade delete their chats.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        user = await UserCRUD.get_user_by_id(db, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False


class ChatCRUD:
    """Secure CRUD operations for Chat model."""

    @staticmethod
    async def create_chat(
        db: AsyncSession,
        user_id: int,
        prompt: str,
        response: str
    ) -> models.Chat:
        """
        Create a new chat with secure parameters.
        
        Args:
            db: Database session
            user_id: User ID (validated)
            prompt: User's input prompt
            response: AI response
            
        Returns:
            Chat: Created chat object
        """
        db_chat = models.Chat(
            user_id=user_id,
            prompt=prompt.strip(),
            response=response.strip()
        )
        db.add(db_chat)
        await db.commit()
        await db.refresh(db_chat)
        return db_chat

    @staticmethod
    async def get_chat_by_id(db: AsyncSession, chat_id: int) -> Optional[models.Chat]:
        """
        Get chat by ID with user relationship.
        
        Args:
            db: Database session
            chat_id: Chat ID
            
        Returns:
            Chat or None
        """
        stmt = select(models.Chat).options(
            selectinload(models.Chat.user)
        ).where(models.Chat.id == chat_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_chats(
        db: AsyncSession, 
        user_id: int, 
        limit: int = 50,
        offset: int = 0
    ) -> List[models.Chat]:
        """
        Get user's chat history with pagination.
        
        Args:
            db: Database session
            user_id: User ID
            limit: Maximum number of chats to return
            offset: Number of chats to skip
            
        Returns:
            List of chats ordered by creation date (newest first)
        """
        stmt = select(models.Chat).where(
            models.Chat.user_id == user_id
        ).order_by(
            desc(models.Chat.created_at)
        ).limit(limit).offset(offset)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_user_chats_by_date(
        db: AsyncSession,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[models.Chat]:
        """
        Get user's chats within a date range.
        
        Args:
            db: Database session
            user_id: User ID
            start_date: Start date
            end_date: End date
            
        Returns:
            List of chats within date range
        """
        stmt = select(models.Chat).where(
            and_(
                models.Chat.user_id == user_id,
                models.Chat.created_at >= start_date,
                models.Chat.created_at <= end_date
            )
        ).order_by(desc(models.Chat.created_at))
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def delete_chat(db: AsyncSession, chat_id: int, user_id: int) -> bool:
        """
        Delete a chat (only if owned by user).
        
        Args:
            db: Database session
            chat_id: Chat ID
            user_id: User ID (ownership verification)
            
        Returns:
            bool: True if deleted, False if not found or not owned
        """
        stmt = select(models.Chat).where(
            and_(
                models.Chat.id == chat_id,
                models.Chat.user_id == user_id
            )
        )
        result = await db.execute(stmt)
        chat = result.scalar_one_or_none()
        
        if chat:
            await db.delete(chat)
            await db.commit()
            return True
        return False

    @staticmethod
    async def count_user_chats(db: AsyncSession, user_id: int) -> int:
        """
        Count total chats for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            int: Total number of chats
        """
        stmt = select(func.count(models.Chat.id)).where(
            models.Chat.user_id == user_id
        )
        result = await db.execute(stmt)
        return result.scalar() or 0 