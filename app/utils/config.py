from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "MuhsinAI Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./muhsinai.db"
    
    # Security Configuration
    secret_key: str = Field(
        default="############################################",  # Development fallback
        min_length=32,
        description="JWT signing secret key. MUST be set via SECRET_KEY environment variable for production."
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError(
                "SECRET_KEY must be at least 32 characters long. "
                "Generate one with: openssl rand -hex 32"
            )
        
        # Warn if using the development fallback in production
        if v == "#*ne73u98h1201(0uh82*@&*)" and not cls.debug:
            raise ValueError(
                "You're using the development SECRET_KEY in production! "
                "Set a secure SECRET_KEY environment variable. "
                "Generate one with: openssl rand -hex 32"
            )
        
        return v
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # CORS Configuration
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",  # Frontend dev server
        "http://localhost:8081",  # Frontend dev server (backup)
        "http://localhost:8082",  # Frontend dev server (current)
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",  # Frontend dev server
        "http://127.0.0.1:8081",  # Frontend dev server (backup)
        "http://127.0.0.1:8082",  # Frontend dev server (current)
        "http://localhost:4173",  # Vite preview
        "http://127.0.0.1:4173",  # Vite preview
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 