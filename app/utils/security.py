"""
Security utilities for MuhsinAI
Sprint 7: Production security enhancements for Render deployment
"""

from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import re
import html
import json
import time
from collections import defaultdict


class RateLimiter:
    """Simple in-memory rate limiter for API endpoints."""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limits = {
            "default": (100, 3600),  # 100 requests per hour
            "auth": (10, 300),       # 10 auth attempts per 5 minutes
            "chat": (50, 3600),      # 50 chat requests per hour
            "user": (200, 3600),     # 200 user management requests per hour
        }
    
    def is_allowed(self, key: str, endpoint_type: str = "default") -> bool:
        """
        Check if request is allowed based on rate limits.
        
        Args:
            key: Client identifier (IP address)
            endpoint_type: Type of endpoint (auth, chat, user, default)
            
        Returns:
            bool: True if allowed, False if rate limited
        """
        now = time.time()
        limit, window = self.limits.get(endpoint_type, self.limits["default"])
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key] 
            if now - req_time < window
        ]
        
        # Check if under limit
        if len(self.requests[key]) >= limit:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    def get_remaining(self, key: str, endpoint_type: str = "default") -> int:
        """Get remaining requests for the current window."""
        limit, _ = self.limits.get(endpoint_type, self.limits["default"])
        current_requests = len(self.requests.get(key, []))
        return max(0, limit - current_requests)


class InputSanitizer:
    """Input sanitization and validation utilities."""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input by removing dangerous content.
        
        Args:
            value: Input string
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized string
        """
        if not value:
            return ""
        
        # Truncate to max length
        value = value[:max_length]
        
        # HTML escape
        value = html.escape(value)
        
        # Remove potential SQL injection patterns
        dangerous_patterns = [
            r"(?i)(union\s+select)",
            r"(?i)(drop\s+table)",
            r"(?i)(delete\s+from)",
            r"(?i)(insert\s+into)",
            r"(?i)(update\s+.+set)",
            r"['\";].*--",
            r"['\"];.*#",
        ]
        
        for pattern in dangerous_patterns:
            value = re.sub(pattern, "", value)
        
        return value.strip()
    
    @staticmethod
    def sanitize_json(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively sanitize JSON data.
        
        Args:
            data: Input dictionary
            
        Returns:
            Dict: Sanitized dictionary
        """
        if not isinstance(data, dict):
            return {}
        
        sanitized = {}
        for key, value in data.items():
            # Sanitize key
            clean_key = InputSanitizer.sanitize_string(str(key), 100)
            
            if isinstance(value, str):
                sanitized[clean_key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[clean_key] = InputSanitizer.sanitize_json(value)
            elif isinstance(value, list):
                sanitized[clean_key] = [
                    InputSanitizer.sanitize_string(str(item)) if isinstance(item, str) else item
                    for item in value[:50]  # Limit list size
                ]
            else:
                sanitized[clean_key] = value
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format with strict rules."""
        if not email or len(email) > 254:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_timezone(timezone: str) -> bool:
        """Validate timezone string."""
        if not timezone or len(timezone) > 50:
            return False
        
        # Basic timezone validation
        valid_patterns = [
            r'^UTC$',
            r'^[A-Z][a-z]+/[A-Z][a-z_]+$',  # America/New_York
            r'^[A-Z][a-z]+/[A-Z][a-z]+/[A-Z][a-z_]+$',  # America/Argentina/Buenos_Aires
        ]
        
        return any(re.match(pattern, timezone) for pattern in valid_patterns)


class SecurityHeaders:
    """Security headers for production deployment."""
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Get security headers for production."""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://api.openai.com"
            ),
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }


# Global rate limiter instance
rate_limiter = RateLimiter()


def get_client_ip(request: Request) -> str:
    """Get client IP address, handling proxy headers."""
    # Check for forwarded headers (common in cloud deployments)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct client IP
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request, endpoint_type: str = "default") -> None:
    """
    Check rate limit for incoming request.
    
    Args:
        request: FastAPI request object
        endpoint_type: Type of endpoint for rate limiting
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    client_ip = get_client_ip(request)
    
    if not rate_limiter.is_allowed(client_ip, endpoint_type):
        remaining = rate_limiter.get_remaining(client_ip, endpoint_type)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests for {endpoint_type} endpoints",
                "remaining": remaining,
                "retry_after": 3600  # 1 hour
            }
        )


def sanitize_request_data(data: Any) -> Any:
    """
    Sanitize incoming request data.
    
    Args:
        data: Request data (dict, string, etc.)
        
    Returns:
        Sanitized data
    """
    if isinstance(data, dict):
        return InputSanitizer.sanitize_json(data)
    elif isinstance(data, str):
        return InputSanitizer.sanitize_string(data)
    else:
        return data 