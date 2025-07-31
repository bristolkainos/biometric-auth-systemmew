#!/usr/bin/env python3
"""
Main entry point for Google Cloud App Engine deployment
"""

import os
import sys
import uvicorn
from pathlib import Path

# Set environment variables before importing modules
os.environ.setdefault("CLOUD_PROVIDER", "gcp")
os.environ.setdefault("ENVIRONMENT", "production")

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    # Import the FastAPI app
    from app.main import app
    
    print("✅ FastAPI app imported successfully for GCP deployment")
    
except ImportError as ie:
    print(f"❌ Import error: {ie}")
    print("Python path:", sys.path)
    print("Backend path exists:", backend_path.exists())
    print("Files in backend:", list(backend_path.iterdir()) if backend_path.exists() else "backend path not found")
    raise
except Exception as e:
    print(f"❌ Error importing FastAPI app: {e}")
    print("Python path:", sys.path)
    raise

# Cloud optimization setup
os.environ.setdefault("TENSORFLOW_OPTIMIZATION", "true")
os.environ.setdefault("GPU_ACCELERATION", "auto")
os.environ.setdefault("BATCH_PROCESSING", "true")

# For App Engine, we need to run the app directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        workers=1,  # App Engine handles scaling
        log_level="info"
    )
else:
    # For App Engine's gunicorn server
    application = app
