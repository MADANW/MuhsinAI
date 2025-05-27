from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """
    User model with security constraints.
    
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
    created_at = Column(
        DateTime, 
        default=func.now(), 
        nullable=False,
        doc="Account creation timestamp"
    )

    # Relationships
    chats = relationship(
        "Chat", 
        back_populates="user", 
        cascade="all, delete-orphan",
        doc="User's chat history"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


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


# Additional indexes for performance
Index('idx_user_email', User.email)
Index('idx_chat_user_created', Chat.user_id, Chat.created_at)
Index('idx_chat_created_desc', Chat.created_at.desc()) 