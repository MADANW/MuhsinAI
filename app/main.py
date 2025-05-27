from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from app.utils.config import settings
from app.db.database import get_db, create_tables, check_database_connection
from app.db.crud import UserCRUD, ChatCRUD
from app.db import models


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered scheduling assistant backend API",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    return app


# Create the FastAPI app instance
app = create_app()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        await create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "database": "connected" if await check_database_connection() else "disconnected"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and testing."""
    db_status = await check_database_connection()
    
    return {
        "status": "healthy" if db_status else "degraded",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
        "database_connected": db_status
    }


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint with detailed information."""
    db_connected = await check_database_connection()
    
    return {
        "api_status": "operational",
        "database": "connected" if db_connected else "disconnected",
        "openai": "not_configured" if not settings.openai_api_key else "configured",
        "features": {
            "database": "✅ operational" if db_connected else "❌ disconnected",
            "authentication": "⏳ pending (Sprint 3)",
            "chat": "⏳ pending (Sprint 5)",
            "user_management": "⏳ pending (Sprint 6)"
        },
        "sprint_progress": {
            "sprint_1": "✅ complete (Foundation)",
            "sprint_2": "🚧 in_progress (Database)",
            "current_phase": "Database integration"
        }
    }


@app.get("/api/v1/db/test")
async def test_database(db: AsyncSession = Depends(get_db)):
    """Test database operations (for development only)."""
    try:
        # Test creating a user
        test_user = await UserCRUD.create_user(
            db, 
            email="test@example.com", 
            hashed_password="test_hash_123"
        )
        
        # Test creating a chat
        test_chat = await ChatCRUD.create_chat(
            db,
            user_id=test_user.id,
            prompt="Test prompt for scheduling",
            response="Test AI response with sample schedule"
        )
        
        # Test retrieving user with chats
        user_with_chats = await UserCRUD.get_user_with_chats(db, test_user.id)
        
        # Clean up test data
        await ChatCRUD.delete_chat(db, test_chat.id, test_user.id)
        await UserCRUD.delete_user(db, test_user.id)
        
        return {
            "status": "success",
            "message": "Database operations working correctly",
            "test_results": {
                "user_creation": "✅ success",
                "chat_creation": "✅ success", 
                "data_retrieval": "✅ success",
                "relationships": "✅ success",
                "cleanup": "✅ success"
            },
            "test_data": {
                "user_id": test_user.id,
                "chat_id": test_chat.id,
                "user_chats_count": len(user_with_chats.chats) if user_with_chats else 0
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database test failed: {str(e)}",
            "error_type": type(e).__name__
        }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 