#!/usr/bin/env python3
"""
Local development environment startup script
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the process"""
    if sys.platform == "win32":
        return subprocess.Popen(command, cwd=cwd, shell=True)
    return subprocess.Popen(command, cwd=cwd, shell=True)

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    print("🚀 Starting local development environment...")
    
    # Start backend server
    print("\n📡 Starting backend server...")
    backend_process = run_command(
        "uvicorn main:app --reload --host 0.0.0.0 --port 8000",
        cwd=str(project_root / "backend")
    )
    
    # Start frontend development server
    print("\n🌐 Starting frontend development server...")
    frontend_process = run_command(
        "npm start",
        cwd=str(project_root / "frontend")
    )
    
    print("\n🚀 Local development environment is starting up...")
    print("📡 Backend server: http://localhost:8000")
    print("🌐 Frontend server: http://localhost:3000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all servers...")
    
    try:
        # Wait for processes
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        
        print("✅ Servers stopped successfully!")

if __name__ == "__main__":
    main()
