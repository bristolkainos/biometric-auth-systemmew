#!/usr/bin/env python3
"""
Optimized server startup script with increased timeouts for biometric processing
"""
import uvicorn
import os

if __name__ == "__main__":
    # Change to backend directory
    os.chdir("backend")
    
    # Start server with optimized settings
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        timeout_keep_alive=30,  # Keep connections alive longer
        timeout_graceful_shutdown=30,  # Give more time for graceful shutdown
        workers=1,  # Single worker for development (avoids model loading conflicts)
        log_level="info",
        reload_dirs=["backend/app"],  # Only watch app directory
        access_log=True
    )
