"""
Configuration management for MuhsinAI
Enhanced with Sprint 6 settings validation
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Union, Optional
import os


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    Enhanced with Sprint 6 user management configuration.
    """
    
    # Application settings
    app_name: str = Field(default="MuhsinAI", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment (development/production)")
    
    # Server settings
    api_host: str = Field(default="localhost", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # Database settings
    database_url: str = Field(default="./muhsinai.db", description="Database connection URL")
    
    # Security settings
    jwt_secret_key: str = Field(default="", description="JWT secret key")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="JWT token expiration (minutes)")
    
    # OpenAI settings
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    
    # CORS settings
    allowed_origins: Union[str, List[str]] = Field(
        default="http://localhost:3000,http://localhost:5173", 
        description="Allowed CORS origins (comma-separated string or list)"
    )
    
    # Frontend URL
    frontend_url: str = Field(default="http://localhost:5173", description="Frontend application URL")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Sprint 6: User Management Settings
    max_user_bio_length: int = Field(default=500, description="Maximum user bio length")
    default_timezone: str = Field(default="UTC", description="Default user timezone")
    enable_user_deletion: bool = Field(default=True, description="Allow users to delete their accounts")
    user_stats_cache_ttl: int = Field(default=300, description="User stats cache TTL in seconds")
    
    @validator('allowed_origins', pre=True, always=True)
    def parse_allowed_origins(cls, v):
        """Parse allowed origins from string or list."""
        if v is None:
            return ["http://localhost:3000", "http://localhost:5173"]
        if isinstance(v, str):
            # Handle comma-separated string from environment variable
            if v.strip():
                return [origin.strip() for origin in v.split(',') if origin.strip()]
            return ["http://localhost:3000", "http://localhost:5173"]
        elif isinstance(v, list):
            return v
        else:
            return ["http://localhost:3000", "http://localhost:5173"]
    
    @validator('jwt_secret_key')
    def validate_jwt_secret(cls, v):
        """Validate JWT secret key is provided."""
        if not v:
            print("⚠️  WARNING: JWT_SECRET_KEY not set. Using default (NOT for production!)")
            return "default-secret-key-not-for-production-use-please-change"
        return v
    
    @validator('openai_api_key')
    def validate_openai_key(cls, v):
        """Validate OpenAI API key format."""
        if not v:
            print("⚠️  WARNING: OPENAI_API_KEY not set. AI features will not work.")
            return ""
        if not v.startswith('sk-'):
            print("⚠️  WARNING: OpenAI API key format may be invalid.")
        return v
    
    @validator('database_url')
    def validate_database_url(cls, v):
        """Ensure database URL is properly formatted for async SQLite."""
        if not v:
            return "sqlite+aiosqlite:///./muhsinai.db"
        
        # If it's already a proper async SQLite URL, return as-is
        if v.startswith('sqlite+aiosqlite://'):
            return v
        
        # If it's a simple file path, format it for async SQLite
        if not v.startswith(('sqlite:///', './', '/')):
            v = f"./{v}"
        
        # Convert to async SQLite format
        if v.startswith('./'):
            return f"sqlite+aiosqlite:///{v}"
        elif v.startswith('/'):
            return f"sqlite+aiosqlite://{v}"
        else:
            return f"sqlite+aiosqlite:///{v}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Create settings instance
settings = Settings() 