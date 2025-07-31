#!/usr/bin/env python3
"""
Helper script to deploy secure configuration to cloud platforms
"""
import os
import argparse
from pathlib import Path
import subprocess
import json
from dotenv import load_dotenv

def setup_gcp_secrets(project_id: str, env_file: Path):
    """Setup secrets in Google Cloud Secret Manager"""
    print("Setting up GCP secrets...")
    
    # Load environment variables
    load_dotenv(env_file)
    
    # Create secrets for database credentials
    db_secrets = {
        'DATABASE_URL': f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    }
    
    # Create secrets for application secrets
    app_secrets = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'JWT_SECRET': os.getenv('JWT_SECRET')
    }
    
    # Create and upload secrets
    for name, values in [('db-credentials', db_secrets), ('app-secrets', app_secrets)]:
        # Create secret if it doesn't exist
        try:
            subprocess.run([
                'gcloud', 'secrets', 'create', name,
                f'--project={project_id}',
                '--replication-policy=automatic'
            ], check=True)
        except subprocess.CalledProcessError:
            print(f"Secret {name} already exists")
        
        # Update secret version
        with open('temp_secret.json', 'w') as f:
            json.dump(values, f)
        
        subprocess.run([
            'gcloud', 'secrets', 'versions', 'add', name,
            f'--project={project_id}',
            '--data-file=temp_secret.json'
        ], check=True)
        
        os.remove('temp_secret.json')
    
    print("GCP secrets setup complete!")

def main():
    parser = argparse.ArgumentParser(description='Deploy secure configuration to cloud platforms')
    parser.add_argument('--platform', choices=['gcp', 'railway', 'render'],
                      required=True, help='Target cloud platform')
    parser.add_argument('--project-id', help='GCP project ID (required for GCP)')
    parser.add_argument('--env-file', default='.env',
                      help='Path to the .env file (default: .env)')
    
    args = parser.parse_args()
    env_path = Path(args.env_file).resolve()
    
    if not env_path.exists():
        print(f"Error: {env_path} does not exist")
        return
    
    if args.platform == 'gcp':
        if not args.project_id:
            print("Error: --project-id is required for GCP deployment")
            return
        setup_gcp_secrets(args.project_id, env_path)
    else:
        print(f"Support for {args.platform} coming soon!")

if __name__ == '__main__':
    main()
