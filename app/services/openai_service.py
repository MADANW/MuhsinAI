"""
OpenAI Service for MuhsinAI - AI-Powered Schedule Generation
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai
from openai import OpenAI
from ..utils.config import settings


class OpenAIService:
    """Service for handling OpenAI API interactions and AI-powered scheduling."""
    
    def __init__(self):
        """Initialize OpenAI client with API key from settings."""
        if not settings.openai_api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Please set OPENAI_API_KEY in your environment variables."
            )
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-3.5-turbo"
    
    def _create_assistant_prompt(self) -> str:
        """
        Create the system prompt for MuhsinAI as a conversational assistant.
        """
        return """You are MuhsinAI, a helpful and friendly AI scheduling assistant. Your primary role is to help users with scheduling, time management, and productivity, but you can also engage in normal conversation.

CORE PERSONALITY:
- Friendly, professional, and helpful
- Knowledgeable about productivity and time management
- Conversational and engaging
- Always try to be helpful and constructive

CAPABILITIES:
1. **Schedule Creation**: When users ask for schedules, plans, or time management help
2. **General Conversation**: Answer questions, provide advice, have discussions
3. **Productivity Tips**: Share time management and productivity insights
4. **Problem Solving**: Help users think through challenges

RESPONSE GUIDELINES:
- For scheduling requests: Create detailed, realistic schedules
- For general questions: Provide helpful, accurate information
- For productivity questions: Share practical advice and tips
- Always be conversational and engaging
- If unsure about something, say so honestly
- Keep responses concise but thorough

SCHEDULING BEHAVIOR:
When users specifically ask for schedules, plans, or time management, respond with structured JSON in this format:
{
  "message": "Your conversational response about the schedule",
  "schedule_type": "daily" | "weekly" | "custom",
  "date_range": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  },
  "events": [
    {
      "title": "Event Title",
      "description": "Brief description",
      "start_time": "HH:MM",
      "end_time": "HH:MM", 
      "date": "YYYY-MM-DD",
      "category": "work" | "personal" | "health" | "education" | "social",
      "priority": "high" | "medium" | "low"
    }
  ],
  "suggestions": [
    "Helpful tip 1",
    "Helpful tip 2"
  ]
}

For non-scheduling conversations, respond naturally with just text - no JSON required."""

    def _is_scheduling_request(self, user_prompt: str) -> bool:
        """
        Determine if the user prompt is asking for schedule creation.
        """
        scheduling_keywords = [
            'schedule', 'plan', 'organize', 'time', 'calendar', 'agenda',
            'routine', 'timetable', 'arrange', 'allocate', 'block',
            'morning', 'afternoon', 'evening', 'today', 'tomorrow',
            'week', 'day', 'hour', 'minute', 'appointment', 'meeting'
        ]
        
        prompt_lower = user_prompt.lower()
        return any(keyword in prompt_lower for keyword in scheduling_keywords)
    
    async def chat_with_user(
        self, 
        user_prompt: str, 
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Have a conversation with the user, handling both scheduling and general queries.
        
        Args:
            user_prompt: The user's message
            user_context: Optional context about the user
        
        Returns:
            Dict containing the response and any schedule data
        """
        try:
            # Determine if this is a scheduling request
            is_scheduling = self._is_scheduling_request(user_prompt)
            
            # Create system prompt
            system_prompt = self._create_assistant_prompt()
            
            # Add user context if provided
            if user_context:
                system_prompt += f"\n\nUser context: {json.dumps(user_context, indent=2)}"
            
            # Create user message with scheduling hint if needed
            user_message = user_prompt
            if is_scheduling:
                user_message += "\n\n[Note: This appears to be a scheduling request. Please provide a structured schedule response.]"
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract the response content
            ai_response = response.choices[0].message.content
            
            # Try to parse as JSON (for scheduling responses)
            try:
                if is_scheduling and ai_response.strip().startswith('{'):
                    schedule_data = json.loads(ai_response)
                    
                    # Validate schedule structure
                    if "schedule_type" in schedule_data and "events" in schedule_data:
                        validated_schedule = self._validate_schedule_response(schedule_data)
                        return {
                            "success": True,
                            "message": schedule_data.get("message", "I've created a schedule for you!"),
                            "schedule": validated_schedule,
                            "conversation_id": f"chat_{datetime.now().timestamp()}",
                            "model_used": self.model,
                            "timestamp": datetime.now().isoformat()
                        }
            except json.JSONDecodeError:
                pass  # Not JSON, treat as regular conversation
            
            # Regular conversation response
            return {
                "success": True,
                "message": ai_response,
                "conversation_id": f"chat_{datetime.now().timestamp()}",
                "model_used": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except openai.APIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Chat failed: {str(e)}")

    # Keep the old method for backward compatibility
    async def generate_schedule(
        self, 
        user_prompt: str, 
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Legacy method - now redirects to chat_with_user for scheduling requests.
        """
        return await self.chat_with_user(user_prompt, user_context)
    
    def _validate_schedule_response(self, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize the AI-generated schedule response.
        """
        required_fields = ["schedule_type", "date_range", "events"]
        
        # Check required fields
        for field in required_fields:
            if field not in schedule_data:
                if field == "schedule_type":
                    schedule_data[field] = "custom"
                elif field == "date_range":
                    today = datetime.now().date()
                    schedule_data[field] = {
                        "start_date": today.isoformat(),
                        "end_date": (today + timedelta(days=1)).isoformat()
                    }
                elif field == "events":
                    schedule_data[field] = []
        
        # Validate schedule type
        valid_types = ["daily", "weekly", "custom"]
        if schedule_data["schedule_type"] not in valid_types:
            schedule_data["schedule_type"] = "custom"
        
        # Validate date range
        date_range = schedule_data["date_range"]
        if not isinstance(date_range, dict) or "start_date" not in date_range or "end_date" not in date_range:
            today = datetime.now().date()
            schedule_data["date_range"] = {
                "start_date": today.isoformat(),
                "end_date": (today + timedelta(days=1)).isoformat()
            }
        
        # Validate events
        if not isinstance(schedule_data["events"], list):
            schedule_data["events"] = []
        
        # Validate each event
        validated_events = []
        for event in schedule_data["events"]:
            if isinstance(event, dict) and "title" in event:
                validated_event = {
                    "title": str(event.get("title", "Untitled Event")),
                    "description": str(event.get("description", "")),
                    "start_time": str(event.get("start_time", "09:00")),
                    "end_time": str(event.get("end_time", "10:00")),
                    "date": str(event.get("date", datetime.now().date().isoformat())),
                    "category": str(event.get("category", "personal")),
                    "priority": str(event.get("priority", "medium"))
                }
                
                # Validate category
                valid_categories = ["work", "personal", "health", "education", "social"]
                if validated_event["category"] not in valid_categories:
                    validated_event["category"] = "personal"
                
                # Validate priority
                valid_priorities = ["high", "medium", "low"]
                if validated_event["priority"] not in valid_priorities:
                    validated_event["priority"] = "medium"
                
                validated_events.append(validated_event)
        
        schedule_data["events"] = validated_events
        
        # Ensure suggestions field exists
        if "suggestions" not in schedule_data:
            schedule_data["suggestions"] = []
        elif not isinstance(schedule_data["suggestions"], list):
            schedule_data["suggestions"] = []
        
        return schedule_data
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the OpenAI API connection.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, please respond with just 'OK' to test the connection."
                    }
                ],
                max_tokens=10
            )
            
            return {
                "success": True,
                "message": "OpenAI API connection successful",
                "model": self.model,
                "response": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"OpenAI API connection failed: {str(e)}",
                "model": self.model,
                "timestamp": datetime.now().isoformat()
            }


# Global service instance
openai_service = OpenAIService() 