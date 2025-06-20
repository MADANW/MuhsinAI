"""
User Management Models for MuhsinAI
Pydantic schemas for user profile management and preferences
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any, Literal
from datetime import datetime


# User Profile Models
class UserProfileUpdate(BaseModel):
    """Model for updating user profile information."""
    
    email: Optional[EmailStr] = Field(None, description="User email address")
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's last name")
    display_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Display name for UI")
    bio: Optional[str] = Field(None, max_length=500, description="User biography/description")
    timezone: Optional[str] = Field("UTC", description="User's timezone (e.g., 'America/New_York')")
    
    @validator('display_name')
    def validate_display_name(cls, v):
        if v and len(v.strip()) < 1:
            raise ValueError('Display name cannot be empty')
        return v.strip() if v else v


class UserProfileResponse(BaseModel):
    """Model for user profile response."""
    
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    bio: Optional[str] = None
    timezone: str = "UTC"
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# User Preferences Models
class NotificationPreferences(BaseModel):
    """User notification preferences."""
    
    email_notifications: bool = Field(True, description="Enable email notifications")
    push_notifications: bool = Field(True, description="Enable push notifications")
    schedule_reminders: bool = Field(True, description="Enable schedule reminders")
    daily_summary: bool = Field(True, description="Enable daily schedule summary")
    new_features: bool = Field(False, description="Notifications about new features")


class SchedulePreferences(BaseModel):
    """User schedule generation preferences."""
    
    default_work_hours_start: str = Field("09:00", description="Default work day start time (HH:MM)")
    default_work_hours_end: str = Field("17:00", description="Default work day end time (HH:MM)")
    default_break_duration: int = Field(15, ge=5, le=120, description="Default break duration in minutes")
    default_lunch_duration: int = Field(60, ge=15, le=180, description="Default lunch duration in minutes")
    prefer_morning_workouts: bool = Field(False, description="Prefer scheduling workouts in the morning")
    include_travel_time: bool = Field(True, description="Include travel time in schedules")
    default_schedule_type: Literal["daily", "weekly"] = Field("daily", description="Default schedule generation type")
    
    @validator('default_work_hours_start', 'default_work_hours_end')
    def validate_time_format(cls, v):
        try:
            hour, minute = v.split(':')
            hour, minute = int(hour), int(minute)
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
            return f"{hour:02d}:{minute:02d}"
        except (ValueError, AttributeError):
            raise ValueError('Time must be in HH:MM format (24-hour)')


class AIPreferences(BaseModel):
    """User AI interaction preferences."""
    
    conversation_style: Literal["professional", "casual", "friendly"] = Field("friendly", description="AI conversation style")
    detail_level: Literal["brief", "detailed", "comprehensive"] = Field("detailed", description="Level of detail in AI responses")
    include_explanations: bool = Field(True, description="Include explanations for scheduling decisions")
    suggest_optimizations: bool = Field(True, description="Allow AI to suggest schedule optimizations")
    learning_mode: bool = Field(True, description="Allow AI to learn from user preferences")


class UserPreferences(BaseModel):
    """Complete user preferences model."""
    
    notifications: NotificationPreferences = Field(default_factory=NotificationPreferences)
    schedule: SchedulePreferences = Field(default_factory=SchedulePreferences)
    ai: AIPreferences = Field(default_factory=AIPreferences)
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="Custom user-defined settings")


class UserPreferencesUpdate(BaseModel):
    """Model for updating user preferences."""
    
    notifications: Optional[NotificationPreferences] = None
    schedule: Optional[SchedulePreferences] = None
    ai: Optional[AIPreferences] = None
    custom_settings: Optional[Dict[str, Any]] = None


class UserPreferencesResponse(BaseModel):
    """Model for user preferences response."""
    
    user_id: int
    preferences: UserPreferences
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Complete User Profile with Preferences
class CompleteUserProfile(BaseModel):
    """Complete user profile including preferences."""
    
    profile: UserProfileResponse
    preferences: UserPreferences
    stats: Dict[str, Any] = Field(default_factory=dict, description="User statistics (chats, schedules, etc.)")


# Request/Response Models for API endpoints
class UserStatsResponse(BaseModel):
    """User statistics response."""
    
    total_chats: int = 0
    total_schedules: int = 0
    average_events_per_schedule: float = 0.0
    most_used_category: Optional[str] = None
    account_age_days: int = 0
    last_activity: Optional[datetime] = None


class UserActivityResponse(BaseModel):
    """User activity summary."""
    
    user_id: int
    recent_chats: int = 0
    recent_schedules: int = 0
    preferred_schedule_times: Dict[str, int] = Field(default_factory=dict)
    category_usage: Dict[str, int] = Field(default_factory=dict)
    activity_trend: Literal["increasing", "stable", "decreasing"] = "stable" 