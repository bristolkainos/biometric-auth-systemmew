#!/usr/bin/env python3
"""
Installation script for the Biometric Authentication System
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command):
    """Run a command and return True if successful"""
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("🚀 Installing Biometric Authentication System requirements...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Ensure pip is up to date
    print("\n📦 Updating pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install PyTorch first (it's a large package and might have specific requirements)
    print("\n📦 Installing PyTorch...")
    if not run_command(f"{sys.executable} -m pip install torch==2.1.0 torchvision==0.16.0"):
        print("❌ Failed to install PyTorch. Please install it manually:")
        print("pip install torch==2.1.0 torchvision==0.16.0")
        sys.exit(1)
    
    # Install other requirements
    print("\n📦 Installing other requirements...")
    if not run_command(f"{sys.executable} -m pip install -r {project_root / 'requirements.txt'}"):
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Verify key packages
    print("\n🔍 Verifying installations...")
    verify_imports = [
        "fastapi",
        "uvicorn",
        "torch",
        "numpy",
        "psycopg2",
        "dotenv",
    ]
    
    all_verified = True
    for package in verify_imports:
        try:
            __import__(package)
            print(f"✅ {package} successfully installed")
        except ImportError:
            print(f"❌ {package} not properly installed")
            all_verified = False
    
    if all_verified:
        print("\n✅ All requirements installed successfully!")
        print("\nYou can now run the system:")
        print("1. Start the local development environment:")
        print("   python start_local_dev.py")
        print("\n2. Run the system tests:")
        print("   python local_system_test.py")
    else:
        print("\n❌ Some packages failed to install. Please try installing them manually.")
        sys.exit(1)

if __name__ == "__main__":
    main()
