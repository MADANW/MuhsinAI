"""
Chat API Endpoints for MuhsinAI
Handles AI-powered schedule generation and chat history
"""

import uuid
import json
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from ..db.database import get_db
from ..db.models import User, Chat
from ..db.crud import ChatCRUD
from ..models.chat import (
    ChatRequest, 
    ChatResponse, 
    ChatHistoryResponse, 
    ChatErrorResponse,
    OpenAITestResponse,
    Schedule
)
from ..services.openai_service import openai_service
from ..utils.auth import get_current_user

# Create router
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def create_schedule(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate an AI-powered schedule from a natural language prompt.
    
    This endpoint:
    1. Takes a user's natural language scheduling request
    2. Sends it to OpenAI for AI-powered schedule generation
    3. Validates and processes the AI response
    4. Stores the conversation in the database
    5. Returns the structured schedule to the user
    """
    try:
        # Generate a unique conversation ID
        conversation_id = str(uuid.uuid4())
        
        # Add user context (could include user preferences, timezone, etc.)
        user_context = request.user_context or {}
        user_context.update({
            "user_id": current_user.id,
            "user_email": current_user.email,
            "conversation_id": conversation_id
        })
        
        # Chat with user using the new conversational method
        ai_result = await openai_service.chat_with_user(
            user_prompt=request.prompt,
            user_context=user_context
        )
        
        if not ai_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Failed to get response from AI service"
            )
        
        # Extract the schedule data (if any)
        schedule = None
        if "schedule" in ai_result and ai_result["schedule"]:
            schedule_data = ai_result["schedule"]
            schedule = Schedule(**schedule_data)
        
        # Store the chat in database
        chat_data = {
            "user_id": current_user.id,
            "prompt": request.prompt,
            "response": ai_result,  # Store the full AI response
        }
        
        chat_record = await ChatCRUD.create_chat(
            db=db,
            user_id=current_user.id,
            prompt=request.prompt,
            response=json.dumps(ai_result)  # Store as JSON string
        )
        
        # Return the response
        return ChatResponse(
            success=True,
            message=ai_result.get("message", "Response generated successfully"),
            schedule=schedule,
            conversation_id=conversation_id,
            model_used=ai_result.get("model_used", "gpt-3.5-turbo")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Chat creation error: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate schedule: {str(e)}"
        )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the user's chat history with pagination.
    
    Returns the user's previous scheduling conversations, including:
    - Original prompts
    - AI-generated schedules
    - Timestamps
    - Pagination metadata
    """
    try:
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get user's chats with pagination
        chats = await ChatCRUD.get_user_chats(
            db=db, 
            user_id=current_user.id, 
            limit=per_page, 
            offset=offset
        )
        
        # Get total count for pagination
        count_query = select(Chat).where(Chat.user_id == current_user.id)
        result = await db.execute(count_query)
        total_count = len(result.scalars().all())
        
        # Format the response
        chat_items = []
        for chat in chats:
            chat_items.append({
                "id": chat.id,
                "prompt": chat.prompt,
                "response": json.loads(chat.response) if isinstance(chat.response, str) else chat.response,
                "created_at": chat.created_at
            })
        
        return ChatHistoryResponse(
            success=True,
            message="Chat history retrieved successfully",
            chats=chat_items,
            total_count=total_count,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        print(f"Chat history error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve chat history: {str(e)}"
        )


@router.get("/test-openai", response_model=OpenAITestResponse)
async def test_openai_connection(current_user: User = Depends(get_current_user)):
    """
    Test the OpenAI API connection.
    
    This endpoint is useful for:
    - Verifying the OpenAI API key is working
    - Checking if the service is available
    - Debugging connection issues
    """
    try:
        # Test the OpenAI connection
        test_result = await openai_service.test_connection()
        
        return OpenAITestResponse(
            success=test_result["success"],
            message=test_result["message"],
            model=test_result["model"],
            response=test_result.get("response")
        )
        
    except Exception as e:
        return OpenAITestResponse(
            success=False,
            message=f"OpenAI connection test failed: {str(e)}",
            model="gpt-3.5-turbo",
            response=None
        )


@router.delete("/history/{chat_id}")
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific chat from the user's history.
    
    Only the owner of the chat can delete it.
    """
    try:
        # Get the chat
        query = select(Chat).where(
            Chat.id == chat_id,
            Chat.user_id == current_user.id
        )
        result = await db.execute(query)
        chat = result.scalar_one_or_none()
        
        if not chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found or you don't have permission to delete it"
            )
        
        # Delete the chat
        await db.delete(chat)
        await db.commit()
        
        return {
            "success": True,
            "message": "Chat deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat deletion error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete chat: {str(e)}"
        ) 