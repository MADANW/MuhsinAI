"""
User Management Service for MuhsinAI
Business logic for user profiles, preferences, and statistics
"""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..db.crud import UserCRUD, UserPreferencesCRUD, ChatCRUD
from ..models.user import (
    UserProfileUpdate, 
    UserProfileResponse, 
    UserPreferencesUpdate,
    UserPreferencesResponse,
    UserPreferences,
    UserStatsResponse,
    UserActivityResponse,
    CompleteUserProfile,
    NotificationPreferences,
    SchedulePreferences,
    AIPreferences
)
from ..db.models import User, UserPreferences as DBUserPreferences


class UserService:
    """Service layer for user management operations."""
    
    @staticmethod
    async def get_user_profile(db: AsyncSession, user_id: int) -> UserProfileResponse:
        """
        Get user profile information.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            UserProfileResponse: User profile data
            
        Raises:
            HTTPException: If user not found
        """
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfileResponse.model_validate(user)
    
    @staticmethod
    async def update_user_profile(
        db: AsyncSession, 
        user_id: int, 
        profile_update: UserProfileUpdate
    ) -> UserProfileResponse:
        """
        Update user profile information.
        
        Args:
            db: Database session
            user_id: User ID
            profile_update: Profile update data
            
        Returns:
            UserProfileResponse: Updated profile data
            
        Raises:
            HTTPException: If user not found or validation fails
        """
        # Check if user exists
        existing_user = await UserCRUD.get_user_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if email is being updated and already exists
        if profile_update.email and profile_update.email != existing_user.email:
            email_exists = await UserCRUD.get_user_by_email(db, profile_update.email)
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email address already in use"
                )
        
        # Prepare update data
        update_data = profile_update.model_dump(exclude_unset=True)
        
        # Update user profile
        updated_user = await UserCRUD.update_user_profile(db, user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )
        
        return UserProfileResponse.model_validate(updated_user)
    
    @staticmethod
    async def get_user_preferences(db: AsyncSession, user_id: int) -> UserPreferencesResponse:
        """
        Get user preferences.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            UserPreferencesResponse: User preferences data
            
        Raises:
            HTTPException: If user or preferences not found
        """
        # Verify user exists
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get preferences
        db_preferences = await UserPreferencesCRUD.get_user_preferences(db, user_id)
        if not db_preferences:
            # Create default preferences if they don't exist
            db_preferences = await UserPreferencesCRUD.create_default_preferences(db, user_id)
        
        # Convert to response model
        preferences_data = UserService._db_preferences_to_model(db_preferences)
        
        return UserPreferencesResponse(
            user_id=user_id,
            preferences=preferences_data,
            updated_at=db_preferences.updated_at
        )
    
    @staticmethod
    async def update_user_preferences(
        db: AsyncSession, 
        user_id: int, 
        preferences_update: UserPreferencesUpdate
    ) -> UserPreferencesResponse:
        """
        Update user preferences.
        
        Args:
            db: Database session
            user_id: User ID
            preferences_update: Preferences update data
            
        Returns:
            UserPreferencesResponse: Updated preferences data
            
        Raises:
            HTTPException: If user not found or validation fails
        """
        # Verify user exists
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get existing preferences
        existing_prefs = await UserPreferencesCRUD.get_user_preferences(db, user_id)
        if not existing_prefs:
            existing_prefs = await UserPreferencesCRUD.create_default_preferences(db, user_id)
        
        # Prepare update data
        update_data = {}
        
        if preferences_update.notifications:
            notification_data = preferences_update.notifications.model_dump()
            update_data.update(notification_data)
        
        if preferences_update.schedule:
            schedule_data = preferences_update.schedule.model_dump()
            update_data.update(schedule_data)
        
        if preferences_update.ai:
            ai_data = preferences_update.ai.model_dump()
            update_data.update(ai_data)
        
        if preferences_update.custom_settings is not None:
            update_data['custom_settings'] = preferences_update.custom_settings
        
        # Update preferences
        updated_prefs = await UserPreferencesCRUD.update_user_preferences(
            db, user_id, update_data
        )
        
        if not updated_prefs:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update preferences"
            )
        
        # Convert to response model
        preferences_data = UserService._db_preferences_to_model(updated_prefs)
        
        return UserPreferencesResponse(
            user_id=user_id,
            preferences=preferences_data,
            updated_at=updated_prefs.updated_at
        )
    
    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: int) -> UserStatsResponse:
        """
        Get comprehensive user statistics.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            UserStatsResponse: User statistics
            
        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get statistics
        stats = await UserCRUD.get_user_stats(db, user_id)
        
        return UserStatsResponse(**stats)
    
    @staticmethod
    async def get_user_activity(db: AsyncSession, user_id: int, days: int = 7) -> UserActivityResponse:
        """
        Get user activity summary.
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            UserActivityResponse: Activity summary
            
        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get activity data
        activity = await ChatCRUD.get_recent_activity(db, user_id, days)
        stats = await UserCRUD.get_user_stats(db, user_id)
        
        return UserActivityResponse(
            user_id=user_id,
            recent_chats=activity['recent_chats'],
            recent_schedules=0,  # Could be enhanced to count recent schedules
            preferred_schedule_times={},  # Could be enhanced with time analysis
            category_usage=stats.get('category_usage', {}),
            activity_trend=activity['activity_trend']
        )
    
    @staticmethod
    async def get_complete_profile(db: AsyncSession, user_id: int) -> CompleteUserProfile:
        """
        Get complete user profile including preferences and stats.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            CompleteUserProfile: Complete profile data
            
        Raises:
            HTTPException: If user not found
        """
        # Get profile
        profile = await UserService.get_user_profile(db, user_id)
        
        # Get preferences
        preferences_response = await UserService.get_user_preferences(db, user_id)
        
        # Get stats
        stats_response = await UserService.get_user_stats(db, user_id)
        stats_dict = stats_response.model_dump()
        
        return CompleteUserProfile(
            profile=profile,
            preferences=preferences_response.preferences,
            stats=stats_dict
        )
    
    @staticmethod
    def _db_preferences_to_model(db_prefs: DBUserPreferences) -> UserPreferences:
        """Convert database preferences to Pydantic model."""
        return UserPreferences(
            notifications=NotificationPreferences(
                email_notifications=db_prefs.email_notifications,
                push_notifications=db_prefs.push_notifications,
                schedule_reminders=db_prefs.schedule_reminders,
                daily_summary=db_prefs.daily_summary,
                new_features=db_prefs.new_features
            ),
            schedule=SchedulePreferences(
                default_work_hours_start=db_prefs.default_work_hours_start,
                default_work_hours_end=db_prefs.default_work_hours_end,
                default_break_duration=db_prefs.default_break_duration,
                default_lunch_duration=db_prefs.default_lunch_duration,
                prefer_morning_workouts=db_prefs.prefer_morning_workouts,
                include_travel_time=db_prefs.include_travel_time,
                default_schedule_type=db_prefs.default_schedule_type
            ),
            ai=AIPreferences(
                conversation_style=db_prefs.conversation_style,
                detail_level=db_prefs.detail_level,
                include_explanations=db_prefs.include_explanations,
                suggest_optimizations=db_prefs.suggest_optimizations,
                learning_mode=db_prefs.learning_mode
            ),
            custom_settings=db_prefs.custom_settings or {}
        )


class UserValidationService:
    """Service for user data validation and business rules."""
    
    @staticmethod
    def validate_timezone(timezone: str) -> bool:
        """Validate timezone string (basic validation)."""
        # This could be enhanced with pytz validation
        return len(timezone) <= 50
    
    @staticmethod
    def validate_work_hours(start_time: str, end_time: str) -> Tuple[bool, str]:
        """Validate work hours make sense."""
        try:
            start_hour, start_min = map(int, start_time.split(':'))
            end_hour, end_min = map(int, end_time.split(':'))
            
            start_minutes = start_hour * 60 + start_min
            end_minutes = end_hour * 60 + end_min
            
            if end_minutes <= start_minutes:
                return False, "End time must be after start time"
            
            if end_minutes - start_minutes > 16 * 60:  # More than 16 hours
                return False, "Work day cannot exceed 16 hours"
            
            return True, "Valid"
        except (ValueError, IndexError):
            return False, "Invalid time format" 