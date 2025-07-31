#!/usr/bin/env python3
"""
Setup script for secure environment configuration
"""
import os
import secrets
import argparse
from pathlib import Path
import base64

def generate_secure_key(length=32):
    """Generate a secure random key"""
    return base64.b64encode(secrets.token_bytes(length)).decode('utf-8')

def create_env_file(env_path: Path, use_example=True):
    """Create a new .env file with secure keys"""
    if use_example and (env_path.parent / 'env.example').exists():
        with open(env_path.parent / 'env.example', 'r') as f:
            template = f.read()
    else:
        template = """# Database Configuration
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=

# Security Keys
SECRET_KEY=
JWT_SECRET=

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS and Security
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
ALLOWED_HOSTS=*

# Application Settings
PYTORCH_ENABLED=true
MIN_BIOMETRIC_METHODS=2
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
"""

    # Generate secure keys
    env_content = template.replace('SECRET_KEY=', f'SECRET_KEY={generate_secure_key()}')
    env_content = env_content.replace('JWT_SECRET=', f'JWT_SECRET={generate_secure_key()}')

    # Write the .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"Created secure .env file at {env_path}")
    print("IMPORTANT: Make sure to fill in the database credentials!")

def main():
    parser = argparse.ArgumentParser(description='Setup secure environment configuration')
    parser.add_argument('--env-file', default='.env',
                      help='Path to the .env file (default: .env)')
    parser.add_argument('--no-example', action='store_true',
                      help='Don\'t use env.example as template')
    
    args = parser.parse_args()
    env_path = Path(args.env_file).resolve()
    
    if env_path.exists():
        response = input(f"{env_path} already exists. Overwrite? [y/N] ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    create_env_file(env_path, not args.no_example)

if __name__ == '__main__':
    main()
