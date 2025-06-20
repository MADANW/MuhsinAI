"""
CRUD operations for MuhsinAI Database
Enhanced with Sprint 6 user management features
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from app.db import models


class UserCRUD:
    """Enhanced CRUD operations for User model with profile management."""

    @staticmethod
    async def create_user(
        db: AsyncSession, 
        email: str, 
        hashed_password: str,
        **profile_data
    ) -> models.User:
        """
        Create a new user with optional profile data.
        
        Args:
            db: Database session
            email: User email (unique)
            hashed_password: Bcrypt hashed password
            **profile_data: Optional profile fields (first_name, last_name, etc.)
            
        Returns:
            User: Created user object
            
        Raises:
            IntegrityError: If email already exists
        """
        user = models.User(
            email=email,
            hashed_password=hashed_password,
            **profile_data
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create default preferences for new user
        await UserPreferencesCRUD.create_default_preferences(db, user.id)
        
        return user

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
    async def get_user_with_preferences(db: AsyncSession, user_id: int) -> Optional[models.User]:
        """Get user with preferences loaded."""
        stmt = select(models.User).options(
            selectinload(models.User.preferences)
        ).where(models.User.id == user_id)
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
    async def update_user_profile(
        db: AsyncSession, 
        user_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[models.User]:
        """
        Update user profile information.
        
        Args:
            db: Database session
            user_id: User ID to update
            update_data: Dictionary of fields to update
        """
        # Filter out None values and update timestamp
        filtered_data = {k: v for k, v in update_data.items() if v is not None}
        filtered_data['updated_at'] = datetime.utcnow()
        
        result = await db.execute(
            update(models.User)
            .where(models.User.id == user_id)
            .values(**filtered_data)
            .returning(models.User)
        )
        
        updated_user = result.scalar_one_or_none()
        if updated_user:
            await db.commit()
            await db.refresh(updated_user)
        
        return updated_user

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

    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user statistics."""
        # Get basic user info
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            return {}
        
        # Get chat statistics
        chat_stats = await db.execute(
            select(
                func.count(models.Chat.id).label('total_chats'),
                func.max(models.Chat.created_at).label('last_activity')
            ).where(models.Chat.user_id == user_id)
        )
        stats = chat_stats.first()
        
        # Get schedule statistics (count AI responses with schedules)
        schedule_count = await db.execute(
            select(func.count(models.Chat.id))
            .where(
                and_(
                    models.Chat.user_id == user_id,
                    models.Chat.response.like('%"schedule"%')
                )
            )
        )
        
        # Calculate account age
        account_age = (datetime.utcnow() - user.created_at).days
        
        # Get category usage from chat responses
        category_usage = await UserCRUD._get_category_usage(db, user_id)
        
        return {
            'total_chats': stats.total_chats or 0,
            'total_schedules': schedule_count.scalar() or 0,
            'account_age_days': account_age,
            'last_activity': stats.last_activity,
            'most_used_category': max(category_usage, key=category_usage.get) if category_usage else None,
            'category_usage': category_usage,
            'average_events_per_schedule': await UserCRUD._calculate_avg_events(db, user_id)
        }

    @staticmethod
    async def _get_category_usage(db: AsyncSession, user_id: int) -> Dict[str, int]:
        """Get category usage statistics from user's chat history."""
        chats = await db.execute(
            select(models.Chat.response).where(models.Chat.user_id == user_id)
        )
        
        category_counts = {}
        for chat in chats:
            try:
                response_data = json.loads(chat.response) if isinstance(chat.response, str) else chat.response
                if 'schedule' in response_data and 'events' in response_data['schedule']:
                    for event in response_data['schedule']['events']:
                        category = event.get('category', 'unknown')
                        category_counts[category] = category_counts.get(category, 0) + 1
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        
        return category_counts

    @staticmethod
    async def _calculate_avg_events(db: AsyncSession, user_id: int) -> float:
        """Calculate average events per schedule."""
        chats = await db.execute(
            select(models.Chat.response).where(models.Chat.user_id == user_id)
        )
        
        total_events = 0
        schedule_count = 0
        
        for chat in chats:
            try:
                response_data = json.loads(chat.response) if isinstance(chat.response, str) else chat.response
                if 'schedule' in response_data and 'events' in response_data['schedule']:
                    total_events += len(response_data['schedule']['events'])
                    schedule_count += 1
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        
        return total_events / schedule_count if schedule_count > 0 else 0.0


class UserPreferencesCRUD:
    """CRUD operations for UserPreferences model."""

    @staticmethod
    async def create_default_preferences(db: AsyncSession, user_id: int) -> models.UserPreferences:
        """Create default preferences for a new user."""
        preferences = models.UserPreferences(user_id=user_id)
        db.add(preferences)
        await db.commit()
        await db.refresh(preferences)
        return preferences

    @staticmethod
    async def get_user_preferences(db: AsyncSession, user_id: int) -> Optional[models.UserPreferences]:
        """Get user preferences by user ID."""
        stmt = select(models.UserPreferences).where(models.UserPreferences.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user_preferences(
        db: AsyncSession, 
        user_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[models.UserPreferences]:
        """Update user preferences."""
        # Filter out None values and update timestamp
        filtered_data = {k: v for k, v in update_data.items() if v is not None}
        filtered_data['updated_at'] = datetime.utcnow()
        
        result = await db.execute(
            update(models.UserPreferences)
            .where(models.UserPreferences.user_id == user_id)
            .values(**filtered_data)
            .returning(models.UserPreferences)
        )
        
        updated_prefs = result.scalar_one_or_none()
        if updated_prefs:
            await db.commit()
            await db.refresh(updated_prefs)
        
        return updated_prefs

    @staticmethod
    async def delete_user_preferences(db: AsyncSession, user_id: int) -> bool:
        """Delete user preferences."""
        result = await db.execute(
            delete(models.UserPreferences).where(models.UserPreferences.user_id == user_id)
        )
        await db.commit()
        return result.rowcount > 0


class ChatCRUD:
    """Enhanced CRUD operations for Chat model."""

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
        chat = models.Chat(
            user_id=user_id,
            prompt=prompt.strip(),
            response=response.strip()
        )
        db.add(chat)
        await db.commit()
        await db.refresh(chat)
        return chat

    @staticmethod
    async def get_chat_by_id(db: AsyncSession, chat_id: int, user_id: int) -> Optional[models.Chat]:
        """
        Get chat by ID with user relationship.
        
        Args:
            db: Database session
            chat_id: Chat ID
            user_id: User ID (ownership verification)
            
        Returns:
            Chat or None
        """
        stmt = select(models.Chat).options(
            selectinload(models.Chat.user)
        ).where(
            and_(
                models.Chat.id == chat_id,
                models.Chat.user_id == user_id
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_chats(
        db: AsyncSession, 
        user_id: int, 
        limit: int = 20, 
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

    @staticmethod
    async def get_recent_activity(db: AsyncSession, user_id: int, days: int = 7) -> Dict[str, Any]:
        """Get user's recent activity statistics."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        recent_chats = await db.execute(
            select(func.count(models.Chat.id))
            .where(
                and_(
                    models.Chat.user_id == user_id,
                    models.Chat.created_at >= cutoff_date
                )
            )
        )
        
        return {
            'recent_chats': recent_chats.scalar() or 0,
            'period_days': days,
            'activity_trend': 'stable'  # Could be enhanced with trend analysis
        } 