#!/usr/bin/env python
"""
Simple backend startup script with error handling
"""
import sys
import os
import logging

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import uvicorn
    from app.main import app
    from app.core.config import settings
    
    logger.info("Starting Biometric Authentication Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Please make sure all dependencies are installed:")
    logger.error("pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    logger.error(f"Failed to start server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 