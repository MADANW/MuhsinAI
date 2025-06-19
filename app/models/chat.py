"""
Chat API Models for MuhsinAI
Pydantic schemas for chat request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


# Request Models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    prompt: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="User's natural language scheduling request"
    )
    user_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional context about user preferences, constraints, etc."
    )
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


# Schedule Event Model
class ScheduleEvent(BaseModel):
    """Model for individual schedule events."""
    title: str = Field(..., description="Event title")
    description: str = Field(default="", description="Event description")
    start_time: str = Field(..., pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", description="Start time in HH:MM format")
    end_time: str = Field(..., pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", description="End time in HH:MM format")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date in YYYY-MM-DD format")
    category: Literal["work", "personal", "health", "education", "social"] = Field(
        default="personal",
        description="Event category"
    )
    priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Event priority"
    )


# Date Range Model
class DateRange(BaseModel):
    """Model for schedule date range."""
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="End date in YYYY-MM-DD format")


# Schedule Model
class Schedule(BaseModel):
    """Model for the generated schedule."""
    schedule_type: Literal["daily", "weekly", "custom"] = Field(..., description="Type of schedule")
    date_range: DateRange = Field(..., description="Date range for the schedule")
    events: List[ScheduleEvent] = Field(default=[], description="List of scheduled events")
    suggestions: List[str] = Field(default=[], description="AI suggestions for the user")


# Response Models
class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    schedule: Optional[Schedule] = Field(None, description="Generated schedule if successful")
    conversation_id: str = Field(..., description="Unique conversation identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    model_used: str = Field(default="gpt-3.5-turbo", description="AI model used for generation")


# Chat History Models
class ChatHistoryItem(BaseModel):
    """Model for individual chat history item."""
    id: int = Field(..., description="Chat ID from database")
    prompt: str = Field(..., description="User's original prompt")
    response: Dict[str, Any] = Field(..., description="AI response data")
    created_at: datetime = Field(..., description="When the chat was created")


class ChatHistoryResponse(BaseModel):
    """Response model for chat history endpoint."""
    success: bool = Field(default=True, description="Whether the request was successful")
    message: str = Field(default="Chat history retrieved successfully", description="Response message")
    chats: List[ChatHistoryItem] = Field(default=[], description="List of user's chat history")
    total_count: int = Field(default=0, description="Total number of chats")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=20, description="Items per page")


# Error Response Models
class ChatErrorResponse(BaseModel):
    """Error response model for chat endpoints."""
    success: bool = Field(default=False, description="Always false for errors")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Specific error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


# Test Response Model
class OpenAITestResponse(BaseModel):
    """Response model for OpenAI connection test."""
    success: bool = Field(..., description="Whether the connection test was successful")
    message: str = Field(..., description="Test result message")
    model: str = Field(..., description="OpenAI model used for testing")
    response: Optional[str] = Field(None, description="AI response from test (if successful)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Test timestamp") 