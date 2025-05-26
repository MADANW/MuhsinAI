from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "MuhsinAI Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./muhsinai.db"
    
    # Security Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # CORS Configuration
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 