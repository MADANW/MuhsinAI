"""
User Management API Endpoints for MuhsinAI
Comprehensive user profile, preferences, and statistics management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..db.database import get_db
from ..db.models import User
from ..utils.auth import get_current_user
from ..services.user_service import UserService, UserValidationService
from ..models.user import (
    UserProfileUpdate,
    UserProfileResponse,
    UserPreferencesUpdate, 
    UserPreferencesResponse,
    UserStatsResponse,
    UserActivityResponse,
    CompleteUserProfile
)

# Create router with user tag
router = APIRouter(prefix="/user", tags=["User Management"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's profile information.
    
    **Returns:**
    - User ID, email, and profile information
    - Profile fields: first_name, last_name, display_name, bio, timezone
    - Account creation and last update timestamps
    
    **Authentication:** Required (JWT token)
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "display_name": "John D.",
        "bio": "AI enthusiast and productivity optimizer",
        "timezone": "America/New_York",
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-06-19T14:30:00Z"
    }
    ```
    """
    return await UserService.get_user_profile(db, current_user.id)


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the current user's profile information.
    
    **Request Body:**
    - All fields are optional - only provided fields will be updated
    - Email must be unique across all users
    - Display name will be used in the UI (falls back to first_name)
    - Timezone should be a valid timezone string (e.g., 'America/New_York')
    
    **Example Request:**
    ```json
    {
        "first_name": "John",
        "last_name": "Doe",
        "display_name": "Johnny",
        "bio": "Updated bio text",
        "timezone": "Europe/London"
    }
    ```
    
    **Authentication:** Required (JWT token)
    
    **Error Codes:**
    - 400: Email already in use
    - 404: User not found
    - 422: Validation error
    """
    return await UserService.update_user_profile(db, current_user.id, profile_update)


@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's preferences and settings.
    
    **Returns comprehensive preferences including:**
    
    **Notification Preferences:**
    - Email notifications, push notifications
    - Schedule reminders and daily summaries
    - New feature announcements
    
    **Schedule Preferences:**
    - Default work hours and break durations
    - Workout preferences and travel time inclusion
    - Default schedule generation type (daily/weekly)
    
    **AI Interaction Preferences:**
    - Conversation style (professional/casual/friendly)
    - Detail level (brief/detailed/comprehensive)
    - AI explanations and optimization suggestions
    
    **Custom Settings:**
    - User-defined key-value pairs for additional customization
    
    **Authentication:** Required (JWT token)
    
    **Example Response:**
    ```json
    {
        "user_id": 1,
        "preferences": {
            "notifications": {
                "email_notifications": true,
                "schedule_reminders": true,
                "daily_summary": false
            },
            "schedule": {
                "default_work_hours_start": "09:00",
                "default_work_hours_end": "17:00",
                "default_break_duration": 15,
                "prefer_morning_workouts": true
            },
            "ai": {
                "conversation_style": "friendly",
                "detail_level": "detailed",
                "include_explanations": true
            },
            "custom_settings": {}
        },
        "updated_at": "2024-06-19T14:30:00Z"
    }
    ```
    """
    return await UserService.get_user_preferences(db, current_user.id)


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    preferences_update: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the current user's preferences and settings.
    
    **Request Body:**
    - All sections are optional - only provided sections will be updated
    - Individual fields within sections can be partially updated
    - Custom settings support any JSON-serializable values
    
    **Validation Rules:**
    - Work hours: End time must be after start time, max 16-hour workday
    - Break durations: Must be between 5-120 minutes
    - Time format: HH:MM (24-hour format)
    
    **Example Request:**
    ```json
    {
        "notifications": {
            "email_notifications": false,
            "schedule_reminders": true
        },
        "schedule": {
            "default_work_hours_start": "08:30",
            "default_work_hours_end": "16:30",
            "prefer_morning_workouts": true
        },
        "ai": {
            "conversation_style": "professional",
            "detail_level": "brief"
        },
        "custom_settings": {
            "theme": "dark",
            "language": "en"
        }
    }
    ```
    
    **Authentication:** Required (JWT token)
    
    **Error Codes:**
    - 400: Invalid work hours or validation error
    - 404: User not found
    - 422: Validation error
    """
    return await UserService.update_user_preferences(db, current_user.id, preferences_update)


@router.get("/stats", response_model=UserStatsResponse)
async def get_user_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive statistics about the user's account and activity.
    
    **Returns detailed statistics including:**
    - Total number of chat conversations
    - Total number of generated schedules
    - Average events per schedule
    - Most frequently used schedule category
    - Account age in days
    - Last activity timestamp
    
    **Use Cases:**
    - Profile dashboards and analytics
    - User engagement tracking
    - Personalization insights
    
    **Authentication:** Required (JWT token)
    
    **Example Response:**
    ```json
    {
        "total_chats": 45,
        "total_schedules": 32,
        "average_events_per_schedule": 6.5,
        "most_used_category": "work",
        "account_age_days": 120,
        "last_activity": "2024-06-19T14:30:00Z"
    }
    ```
    """
    return await UserService.get_user_stats(db, current_user.id)


@router.get("/activity", response_model=UserActivityResponse)
async def get_user_activity(
    days: int = Query(7, ge=1, le=365, description="Number of days to analyze (1-365)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user activity summary for a specified time period.
    
    **Query Parameters:**
    - `days`: Number of days to analyze (default: 7, max: 365)
    
    **Returns activity data including:**
    - Recent chat count for the specified period
    - Schedule generation activity
    - Category usage patterns
    - Activity trend analysis
    - Preferred scheduling times (future enhancement)
    
    **Use Cases:**
    - Activity dashboards
    - Usage pattern analysis
    - Recommendation systems
    
    **Authentication:** Required (JWT token)
    
    **Example Response:**
    ```json
    {
        "user_id": 1,
        "recent_chats": 8,
        "recent_schedules": 5,
        "preferred_schedule_times": {},
        "category_usage": {
            "work": 15,
            "personal": 8,
            "health": 4
        },
        "activity_trend": "increasing"
    }
    ```
    """
    return await UserService.get_user_activity(db, current_user.id, days)


@router.get("/complete-profile", response_model=CompleteUserProfile)
async def get_complete_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a comprehensive view of the user's complete profile.
    
    **This endpoint combines:**
    - User profile information
    - All user preferences and settings
    - Account statistics and activity data
    
    **Use Cases:**
    - Complete user dashboards
    - Profile management interfaces
    - Data export functionality
    - Comprehensive user insights
    
    **Response includes:**
    - Profile: Basic user information and settings
    - Preferences: All notification, schedule, and AI preferences
    - Stats: Comprehensive account statistics and usage data
    
    **Authentication:** Required (JWT token)
    
    **Example Response:**
    ```json
    {
        "profile": {
            "id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "display_name": "Johnny"
        },
        "preferences": {
            "notifications": {...},
            "schedule": {...},
            "ai": {...}
        },
        "stats": {
            "total_chats": 45,
            "total_schedules": 32,
            "account_age_days": 120
        }
    }
    ```
    """
    return await UserService.get_complete_profile(db, current_user.id)


@router.delete("/account")
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete the current user's account and all associated data.
    
    **⚠️ WARNING: This action is irreversible!**
    
    **This will permanently delete:**
    - User profile and account information
    - All chat history and conversations
    - All user preferences and settings
    - All generated schedules and data
    
    **Security Notes:**
    - Requires valid authentication
    - User must be the account owner
    - No recovery options available
    
    **Use Cases:**
    - GDPR compliance (right to be forgotten)
    - Account closure requests
    - Data privacy requirements
    
    **Authentication:** Required (JWT token)
    
    **Response:**
    ```json
    {
        "message": "Account deleted successfully",
        "user_id": 1,
        "deleted_at": "2024-06-19T14:30:00Z"
    }
    ```
    """
    from ..db.crud import UserCRUD
    from datetime import datetime
    
    success = await UserCRUD.delete_user(db, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )
    
    return {
        "message": "Account deleted successfully",
        "user_id": current_user.id,
        "deleted_at": datetime.utcnow().isoformat()
    }


# Health check endpoint for user management system
@router.get("/health")
async def user_management_health_check(
    db: AsyncSession = Depends(get_db)
):
    """
    Health check endpoint for the user management system.
    
    **Returns:**
    - System status and availability
    - Database connectivity
    - Feature availability status
    
    **No authentication required**
    
    **Example Response:**
    ```json
    {
        "status": "healthy",
        "features": {
            "profile_management": "operational",
            "preferences": "operational", 
            "statistics": "operational"
        },
        "database": "connected",
        "timestamp": "2024-06-19T14:30:00Z"
    }
    ```
    """
    from datetime import datetime
    from ..db.database import check_database_connection
    
    db_connected = await check_database_connection()
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "features": {
            "profile_management": "operational",
            "preferences": "operational",
            "statistics": "operational",
            "user_analytics": "operational"
        },
        "database": "connected" if db_connected else "disconnected",
        "sprint": "Sprint 6 - User Management",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    } 