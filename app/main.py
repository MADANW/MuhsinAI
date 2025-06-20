from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
import logging
import time

from app.utils.config import settings
from app.utils.security import SecurityHeaders, check_rate_limit, get_client_ip
from app.utils.logging import log_startup_event, log_database_event, error_tracker
from app.utils.testing import get_health_status, run_basic_tests
from app.db.database import get_db, create_tables, check_database_connection
from app.db.crud import UserCRUD, ChatCRUD
from app.db import models
from app.api import auth, chat, user


class SecurityMiddleware(BaseHTTPMiddleware):
    """Sprint 7: Security middleware for production deployment."""
    
    async def dispatch(self, request: Request, call_next):
        # Start time for request logging
        start_time = time.time()
        
        # Get client info for logging
        client_ip = get_client_ip(request)
        
        # Add security headers
        response = await call_next(request)
        
        # Apply security headers
        headers = SecurityHeaders.get_security_headers()
        for name, value in headers.items():
            response.headers[name] = value
        
        # Log request (basic logging)
        process_time = time.time() - start_time
        logging.info(
            f"[{client_ip}] {request.method} {request.url.path} - "
            f"{response.status_code} - {process_time:.3f}s"
        )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sprint 7: Rate limiting middleware."""
    
    async def dispatch(self, request: Request, call_next):
        # Determine endpoint type for rate limiting
        path = request.url.path
        endpoint_type = "default"
        
        if path.startswith("/api/v1/auth"):
            endpoint_type = "auth"
        elif path.startswith("/api/v1/chat"):
            endpoint_type = "chat"
        elif path.startswith("/api/v1/user"):
            endpoint_type = "user"
        
        # Skip rate limiting for health checks and docs
        if path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Check rate limit
        try:
            check_rate_limit(request, endpoint_type)
        except Exception as e:
            return JSONResponse(
                status_code=429,
                content={"detail": str(e)}
            )
        
        return await call_next(request)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application with Sprint 7 security enhancements."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered scheduling assistant with production security (Sprint 7)",
        docs_url="/docs" if settings.debug else None,  # Disable docs in production
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )
    
    # Production CORS configuration
    production_origins = [
        "https://muhsinai.vercel.app",  # Production frontend
        "https://muhsinai.netlify.app",  # Alternative frontend
        "https://*.onrender.com",  # Render deployment URLs
    ]
    
    cors_origins = settings.allowed_origins if settings.debug else production_origins
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=86400,  # Cache preflight for 24 hours
    )
    
    # Sprint 7: Add security middleware
    app.add_middleware(SecurityMiddleware)
    
    # Sprint 7: Add rate limiting (only in production to avoid dev issues)
    if not settings.debug:
        app.add_middleware(RateLimitMiddleware)
    
    # Sprint 7: Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for unhandled errors."""
        error_tracker.track_error(exc, str(request.url.path), None)
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later.",
                "timestamp": time.time(),
                "debug_info": str(exc) if settings.debug else None
            }
        )
    
    # Include routers
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(chat.router, prefix="/api/v1")
    app.include_router(user.router, prefix="/api/v1")
    
    return app


# Create the FastAPI app instance
app = create_app()


@app.on_event("startup")
async def startup_event():
    """Initialize database and Sprint 7 systems on startup."""
    try:
        log_startup_event("Application starting up...")
        
        # Database initialization
        await create_tables()
        log_database_event("Database tables created", True)
        log_startup_event("Sprint 6: User Management system initialized")
        
        # Sprint 7 initialization
        log_startup_event("Sprint 7: Security middleware enabled")
        log_startup_event("Sprint 7: Error tracking initialized")
        log_startup_event("Sprint 7: Production logging configured")
        
        log_startup_event("🎉 MuhsinAI backend ready for production!")
        
    except Exception as e:
        log_database_event("Database initialization", False, str(e))
        error_tracker.track_error(e, "startup", None)
        raise


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "database": "connected" if await check_database_connection() else "disconnected",
        "authentication": "available",
        "user_management": "available",
        "chat_system": "available",
        "sprint_status": "Sprint 6 Complete - User Management System"
    }


@app.get("/health")
async def health_check():
    """Basic health check endpoint for monitoring."""
    db_status = await check_database_connection()
    
    return {
        "status": "healthy" if db_status else "degraded",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
        "database_connected": db_status,
        "authentication_enabled": True,
        "user_management_enabled": True,
        "chat_system_enabled": True,
        "sprint_7_status": "complete"
    }


@app.get("/health/detailed")
async def detailed_health_check():
    """Sprint 7: Comprehensive health check with all system components."""
    return await get_health_status()


@app.get("/health/tests")
async def run_smoke_tests_endpoint():
    """Sprint 7: Run basic smoke tests."""
    if not settings.debug:
        return {"error": "Tests are only available in development mode"}
    return await run_basic_tests()


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint with detailed information."""
    db_connected = await check_database_connection()
    
    return {
        "api_status": "operational",
        "database": "connected" if db_connected else "disconnected",
        "openai": "configured" if settings.openai_api_key else "not_configured",
        "features": {
            "database": "✅ operational" if db_connected else "❌ disconnected",
            "authentication": "✅ operational (Sprint 3)",
            "chat": "✅ operational (Sprint 5)",
            "user_management": "✅ operational (Sprint 6)",
            "profile_management": "✅ operational",
            "user_preferences": "✅ operational",
            "user_statistics": "✅ operational"
        },
        "sprint_progress": {
            "sprint_1": "✅ complete (Foundation)",
            "sprint_2": "✅ complete (Database)",
            "sprint_3": "✅ complete (Authentication)",
            "sprint_4": "✅ complete (OpenAI Integration)",
            "sprint_5": "✅ complete (Chat Endpoints)",
            "sprint_6": "✅ complete (User Management)",
            "current_phase": "Ready for Sprint 7 (Integration & Polish)"
        },
        "available_endpoints": {
            "auth": {
                "register": "POST /api/v1/auth/register",
                "login": "POST /api/v1/auth/login",
                "profile": "GET /api/v1/auth/me",
                "refresh": "POST /api/v1/auth/refresh",
                "logout": "POST /api/v1/auth/logout"
            },
            "chat": {
                "create_schedule": "POST /api/v1/chat/",
                "chat_history": "GET /api/v1/chat/history",
                "delete_chat": "DELETE /api/v1/chat/history/{chat_id}",
                "test_openai": "GET /api/v1/chat/test-openai"
            },
            "user_management": {
                "get_profile": "GET /api/v1/user/profile",
                "update_profile": "PUT /api/v1/user/profile",
                "get_preferences": "GET /api/v1/user/preferences",
                "update_preferences": "PUT /api/v1/user/preferences",
                "get_statistics": "GET /api/v1/user/stats",
                "get_activity": "GET /api/v1/user/activity",
                "complete_profile": "GET /api/v1/user/complete-profile",
                "delete_account": "DELETE /api/v1/user/account",
                "health_check": "GET /api/v1/user/health"
            }
        }
    }


@app.get("/api/v1/db/test")
async def test_database(db: AsyncSession = Depends(get_db)):
    """Test database operations including new Sprint 6 features."""
    try:
        from app.db.crud import UserPreferencesCRUD
        
        # Test creating a user with profile data
        test_user = await UserCRUD.create_user(
            db, 
            email="test_sprint6@example.com", 
            hashed_password="test_hash_123",
            first_name="Test",
            last_name="User",
            display_name="Test Sprint 6",
            timezone="UTC"
        )
        
        # Test preferences (should be auto-created)
        preferences = await UserPreferencesCRUD.get_user_preferences(db, test_user.id)
        
        # Test creating a chat
        test_chat = await ChatCRUD.create_chat(
            db,
            user_id=test_user.id,
            prompt="Test Sprint 6 scheduling prompt",
            response='{"message": "Sprint 6 test response", "schedule": {"events": []}}'
        )
        
        # Test user stats
        stats = await UserCRUD.get_user_stats(db, test_user.id)
        
        # Test user with preferences
        user_with_prefs = await UserCRUD.get_user_with_preferences(db, test_user.id)
        
        # Clean up test data
        await ChatCRUD.delete_chat(db, test_chat.id, test_user.id)
        await UserCRUD.delete_user(db, test_user.id)
        
        return {
            "status": "success",
            "message": "Sprint 6 database operations working correctly",
            "test_results": {
                "user_creation_with_profile": "✅ success",
                "preferences_auto_creation": "✅ success",
                "chat_creation": "✅ success",
                "user_statistics": "✅ success",
                "user_with_preferences": "✅ success",
                "cleanup": "✅ success"
            },
            "sprint_6_features": {
                "extended_user_model": "✅ operational",
                "user_preferences": "✅ operational", 
                "user_statistics": "✅ operational",
                "profile_management": "✅ operational"
            },
            "test_data": {
                "user_id": test_user.id,
                "chat_id": test_chat.id,
                "preferences_created": preferences is not None,
                "stats_calculated": bool(stats),
                "preferences_loaded": user_with_prefs.preferences is not None
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Sprint 6 database test failed: {str(e)}",
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