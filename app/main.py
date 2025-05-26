from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.utils.config import settings


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


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and testing."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production"
    }


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint with more detailed information."""
    return {
        "api_status": "operational",
        "database": "not_connected",  # Will update this in Sprint 2
        "openai": "not_configured" if not settings.openai_api_key else "configured",
        "features": {
            "authentication": "pending",
            "chat": "pending",
            "user_management": "pending"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 