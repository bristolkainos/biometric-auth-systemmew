#!/usr/bin/env python
"""Fixed server starter that handles environment variable issues"""
import os
import sys
import multiprocessing


def main():
    # Clear problematic environment variables that cause JSON parsing errors
    problematic_vars = ['CORS_ORIGINS', 'ALLOWED_HOSTS', 'ALLOWED_FILE_TYPES']
    for var in problematic_vars:
        if var in os.environ:
            print(f"Clearing environment variable: {var}")
            del os.environ[var]

    # Set simple environment variables that won't cause issues
    os.environ['DATABASE_URL'] = 'sqlite:///biometric_auth.db'
    os.environ['SECRET_KEY'] = 'dev-secret-key'
    os.environ['JWT_SECRET'] = 'dev-jwt-secret'
    os.environ['ENVIRONMENT'] = 'development'
    os.environ['DEBUG'] = 'true'
    os.environ['MODEL_PATH'] = 'models'

    # Add backend to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    try:
        import uvicorn
        
        print("\n" + "="*60)
        print("Biometric Authentication Backend")
        print("="*60)
        print("Server URL: http://localhost:8000")
        print("API Docs:   http://localhost:8000/docs")
        print("Database:   SQLite (biometric_auth.db)")
        print("="*60)
        print("\nPress CTRL+C to stop the server\n")
        
        # Use import string format when reload is enabled
        uvicorn.run(
            "app.main:app",  # Import string format
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except ImportError as e:
        print(f"\nImport error: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main() 