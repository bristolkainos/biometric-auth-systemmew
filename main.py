from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging
import time
import traceback
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from core.config import settings
from api.v1.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Biometric Authentication System (minimal debug mode)...")
    
    try:
        logger.info("Minimal startup completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Biometric Authentication System...")

# Create FastAPI app
app = FastAPI(
    title="Biometric Authentication System",
    description="A comprehensive multi-modal biometric authentication system for enterprise use",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception caught: {exc}", exc_info=True)
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    # Return JSONResponse
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    # Temporarily allow all origins to fix CORS for admin login
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add trusted host middleware for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts_list
    )

# Include API router
app.include_router(api_router, prefix="/api/v1")
logger.info("API router enabled")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        logger.info("Health check endpoint called")
        return {"status": "healthy", "service": "biometric-auth", "version": "1.0.0"}
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

# Global OPTIONS handler for CORS preflight requests
@app.options("/{path:path}")
async def options_handler(path: str, request: Request):
    """Handle OPTIONS requests for CORS preflight"""
    origin = request.headers.get("origin", "*")
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "86400"
        }
    )

# Root endpoint
@app.get("/")
async def root():
    try:
        logger.info("Root endpoint called")
        return {
            "message": "Biometric Authentication System API",
            "version": "1.0.0",
            "docs": "/docs" if settings.ENVIRONMENT == "development" else "Documentation disabled in production"
        }
    except Exception as e:
        logger.error(f"Root endpoint failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
