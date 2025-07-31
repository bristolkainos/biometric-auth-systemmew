#!/usr/bin/env python
"""Simple server runner that bypasses environment variable issues"""
import os
import sys

# Set simple environment variables directly
os.environ['DATABASE_URL'] = 'sqlite:///biometric_auth.db'
os.environ['SECRET_KEY'] = 'dev-secret-key'
os.environ['JWT_SECRET'] = 'dev-jwt-secret' 
os.environ['ENVIRONMENT'] = 'development'
os.environ['DEBUG'] = 'true'
os.environ['MODEL_PATH'] = 'models'

# Don't set list-type environment variables - let defaults in config.py handle them

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import uvicorn
    from app.main import app
    
    print("Starting Biometric Authentication Backend...")
    print("Server will run on: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc() 