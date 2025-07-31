#!/usr/bin/env python
"""Simple backend runner on port 8000"""
import os
import sys
import uvicorn

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Clear any problematic environment variables
for var in ['CORS_ORIGINS', 'ALLOWED_HOSTS', 'ALLOWED_FILE_TYPES']:
    if var in os.environ:
        del os.environ[var]

# Import the app
from app.main import app

print("\n" + "="*60)
print("Biometric Authentication Backend")
print("="*60)
print("Server URL: http://localhost:8000")
print("API Docs:   http://localhost:8000/docs")
print("Database:   SQLite (biometric_auth.db)")
print("="*60)
print("\nPress CTRL+C to stop the server\n")

# Run on port 8000
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 