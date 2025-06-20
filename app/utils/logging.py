"""
Logging utilities for MuhsinAI
Sprint 7: Production logging and error tracking
"""

import logging
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import Request, Response
import os


class MuhsinAILogger:
    """Custom logger for MuhsinAI with structured logging."""
    
    def __init__(self, name: str = "muhsinai"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with appropriate handlers and formatters."""
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler for production
        if not os.getenv("DEBUG", "true").lower() == "true":
            file_handler = logging.FileHandler("muhsinai.log")
            file_handler.setLevel(logging.INFO)
            
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Console formatter
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def log_request(self, request: Request, response: Response, process_time: float):
        """Log HTTP request with structured data."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "client_host": getattr(request.client, 'host', 'unknown') if request.client else 'unknown',
            "user_agent": request.headers.get("user-agent", "unknown"),
        }
        
        # Add query parameters if present
        if request.url.query:
            log_data["query_params"] = str(request.url.query)
        
        # Log level based on status code
        if response.status_code >= 500:
            self.logger.error(f"Server Error: {json.dumps(log_data)}")
        elif response.status_code >= 400:
            self.logger.warning(f"Client Error: {json.dumps(log_data)}")
        else:
            self.logger.info(f"Request: {json.dumps(log_data)}")
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Log error with full context and traceback."""
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.logger.error(f"Application Error: {json.dumps(error_data, indent=2)}")
    
    def log_auth_event(self, event_type: str, user_email: str, success: bool, details: Optional[Dict] = None):
        """Log authentication events for security monitoring."""
        auth_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_email": user_email,
            "success": success,
            "details": details or {}
        }
        
        level = logging.INFO if success else logging.WARNING
        self.logger.log(level, f"Auth Event: {json.dumps(auth_data)}")
    
    def log_ai_interaction(self, user_id: int, prompt_length: int, response_length: int, processing_time: float):
        """Log AI interactions for monitoring and analytics."""
        ai_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "prompt_length": prompt_length,
            "response_length": response_length,
            "processing_time_ms": round(processing_time * 1000, 2),
            "event_type": "ai_interaction"
        }
        
        self.logger.info(f"AI Interaction: {json.dumps(ai_data)}")


class ErrorTracker:
    """Track and categorize application errors."""
    
    def __init__(self):
        self.error_counts = {}
        self.logger = MuhsinAILogger("error_tracker")
    
    def track_error(self, error: Exception, endpoint: str, user_id: Optional[int] = None):
        """Track error occurrence for monitoring."""
        error_key = f"{type(error).__name__}:{endpoint}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        context = {
            "endpoint": endpoint,
            "user_id": user_id,
            "occurrence_count": self.error_counts[error_key]
        }
        
        self.logger.log_error(error, context)
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of error occurrences."""
        return self.error_counts.copy()


# Global instances
logger = MuhsinAILogger()
error_tracker = ErrorTracker()


def log_startup_event(message: str):
    """Log application startup events."""
    logger.logger.info(f"🚀 STARTUP: {message}")


def log_database_event(event: str, success: bool, details: Optional[str] = None):
    """Log database events."""
    level = logging.INFO if success else logging.ERROR
    status = "✅" if success else "❌"
    message = f"{status} DATABASE: {event}"
    if details:
        message += f" - {details}"
    logger.logger.log(level, message)


def log_security_event(event: str, client_ip: str, details: Optional[Dict] = None):
    """Log security-related events."""
    security_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "client_ip": client_ip,
        "details": details or {}
    }
    logger.logger.warning(f"🔒 SECURITY: {json.dumps(security_data)}") 