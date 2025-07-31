#!/usr/bin/env python3
"""
Minimal test entry point for Google Cloud App Engine deployment
"""

import os
import sys
from pathlib import Path

# Set environment variables before importing modules
os.environ.setdefault("CLOUD_PROVIDER", "gcp")
os.environ.setdefault("ENVIRONMENT", "production")

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Create a minimal FastAPI app for testing
from fastapi import FastAPI

app = FastAPI(title="Minimal Test API")

@app.get("/")
async def root():
    return {"message": "Hello from minimal test", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy", "test": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
