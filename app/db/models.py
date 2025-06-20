from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """
    User model with security constraints and extended profile fields.
    
    Constraints:
    - email: UNIQUE, NOT NULL, max 255 chars
    - hashed_password: NOT NULL, 60 chars (bcrypt)
    - created_at: NOT NULL, auto-generated
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False,
        doc="User email address - unique identifier"
    )
    hashed_password = Column(
        String(60), 
        nullable=False,
        doc="Bcrypt hashed password (60 chars)"
    )
    
    # Extended profile fields for Sprint 6
    first_name = Column(
        String(50),
        nullable=True,
        doc="User's first name"
    )
    last_name = Column(
        String(50),
        nullable=True,
        doc="User's last name"
    )
    display_name = Column(
        String(100),
        nullable=True,
        doc="Display name for UI (defaults to first_name)"
    )
    bio = Column(
        Text,
        nullable=True,
        doc="User biography/description"
    )
    timezone = Column(
        String(50),
        nullable=False,
        default="UTC",
        doc="User's timezone (e.g., 'America/New_York')"
    )
    
    # Timestamps
    created_at = Column(
        DateTime, 
        default=func.now(), 
        nullable=False,
        doc="Account creation timestamp"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=True,
        doc="Profile last updated timestamp"
    )

    # Relationships
    chats = relationship(
        "Chat", 
        back_populates="user", 
        cascade="all, delete-orphan",
        doc="User's chat history"
    )
    preferences = relationship(
        "UserPreferences",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        doc="User's preferences (one-to-one)"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, display_name={self.display_name})>"


class UserPreferences(Base):
    """
    User preferences model for storing user settings and AI preferences.
    
    Uses JSON column for flexible preference storage.
    """
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        doc="Reference to user (one-to-one relationship)"
    )
    
    # Notification preferences
    email_notifications = Column(Boolean, default=True, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)
    schedule_reminders = Column(Boolean, default=True, nullable=False)
    daily_summary = Column(Boolean, default=True, nullable=False)
    new_features = Column(Boolean, default=False, nullable=False)
    
    # Schedule preferences
    default_work_hours_start = Column(String(5), default="09:00", nullable=False)
    default_work_hours_end = Column(String(5), default="17:00", nullable=False)
    default_break_duration = Column(Integer, default=15, nullable=False)
    default_lunch_duration = Column(Integer, default=60, nullable=False)
    prefer_morning_workouts = Column(Boolean, default=False, nullable=False)
    include_travel_time = Column(Boolean, default=True, nullable=False)
    default_schedule_type = Column(String(10), default="daily", nullable=False)
    
    # AI preferences
    conversation_style = Column(String(20), default="friendly", nullable=False)
    detail_level = Column(String(20), default="detailed", nullable=False)
    include_explanations = Column(Boolean, default=True, nullable=False)
    suggest_optimizations = Column(Boolean, default=True, nullable=False)
    learning_mode = Column(Boolean, default=True, nullable=False)
    
    # Custom settings (flexible JSON storage)
    custom_settings = Column(
        JSON,
        default=dict,
        nullable=False,
        doc="Custom user-defined settings as JSON"
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        doc="Preferences creation timestamp"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Preferences last updated timestamp"
    )
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreferences(id={self.id}, user_id={self.user_id})>"


class Chat(Base):
    """
    Chat model for storing conversation history.
    
    Constraints:
    - user_id: FOREIGN KEY, NOT NULL, indexed
    - prompt: NOT NULL, TEXT type
    - response: NOT NULL, TEXT type  
    - created_at: NOT NULL, auto-generated, indexed
    """
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True,
        doc="Reference to user who owns this chat"
    )
    prompt = Column(
        Text, 
        nullable=False,
        doc="User's input prompt/question"
    )
    response = Column(
        Text, 
        nullable=False,
        doc="AI-generated response/schedule"
    )
    created_at = Column(
        DateTime, 
        default=func.now(), 
        nullable=False,
        index=True,
        doc="Chat creation timestamp"
    )

    # Relationships
    user = relationship("User", back_populates="chats")

    def __repr__(self):
        return f"<Chat(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"


# Enhanced indexes for performance (including new fields)
Index('idx_user_email', User.email)
Index('idx_user_display_name', User.display_name)
Index('idx_user_created_updated', User.created_at, User.updated_at)
Index('idx_preferences_user_id', UserPreferences.user_id)
Index('idx_preferences_updated', UserPreferences.updated_at.desc())
Index('idx_chat_user_created', Chat.user_id, Chat.created_at)
Index('idx_chat_created_desc', Chat.created_at.desc()) 