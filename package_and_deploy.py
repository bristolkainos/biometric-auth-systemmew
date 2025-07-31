#!/usr/bin/env python3
"""
Biometric Authentication System - Package and Deploy Script
==========================================================

This script packages the entire biometric authentication system and provides
multiple deployment options with automated setup and configuration.

Usage:
    python package_and_deploy.py --help
    python package_and_deploy.py --package
    python package_and_deploy.py --deploy railway
    python package_and_deploy.py --deploy render
    python package_and_deploy.py --deploy fly
    python package_and_deploy.py --deploy gcp
    python package_and_deploy.py --deploy aws
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
import platform

class BiometricDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.package_dir = self.project_root / "deployment_package"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_banner(self):
        """Print deployment banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                BIOMETRIC AUTHENTICATION SYSTEM               ║
║                    PACKAGE & DEPLOY SCRIPT                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            return False
            
        # Check Docker
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            print("✅ Docker found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Docker not found - some deployment options may not work")
            
        # Check Git
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            print("✅ Git found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Git not found - some deployment options may not work")
            
        return True
        
    def create_deployment_package(self):
        """Create a complete deployment package"""
        print(f"📦 Creating deployment package...")
        
        # Clean previous package
        if self.package_dir.exists():
            shutil.rmtree(self.package_dir)
        self.package_dir.mkdir()
        
        # Copy essential files and directories
        essential_items = [
            "backend",
            "frontend", 
            "database",
            "models",
            "docker-compose.yml",
            "Dockerfile.cloud",
            "requirements.txt",
            "requirements-cloud.txt",
            "README.md",
            "DEPLOYMENT.md",
            "QUICK_DEPLOY.md"
        ]
        
        for item in essential_items:
            src = self.project_root / item
            dst = self.package_dir / item
            
            if src.exists():
                if src.is_dir():
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                        "__pycache__", "*.pyc", ".git", "node_modules", 
                        "venv", ".env", "*.log", "uploads/*"
                    ))
                else:
                    shutil.copy2(src, dst)
                    
        # Create deployment scripts
        self._create_deployment_scripts()
        
        # Create environment templates
        self._create_environment_templates()
        
        # Create deployment configuration
        self._create_deployment_config()
        
        print(f"✅ Deployment package created at: {self.package_dir}")
        return True
        
    def _create_deployment_scripts(self):
        """Create platform-specific deployment scripts"""
        scripts_dir = self.package_dir / "scripts"
        scripts_dir.mkdir()
        
        # Railway deployment script
        railway_script = scripts_dir / "deploy_railway.sh"
        railway_script.write_text("""#!/bin/bash
# Railway Deployment Script
echo "🚂 Deploying to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
railway login

# Deploy
railway up

echo "✅ Railway deployment complete!"
""")
        railway_script.chmod(0o755)
        
        # Render deployment script
        render_script = scripts_dir / "deploy_render.sh"
        render_script.write_text("""#!/bin/bash
# Render Deployment Script
echo "🎨 Deploying to Render..."

# Build and deploy backend
echo "Building backend..."
cd backend
docker build -t biometric-backend .

# Build and deploy frontend  
echo "Building frontend..."
cd ../frontend
npm install
npm run build

echo "✅ Render deployment ready!"
echo "Please configure in Render dashboard:"
echo "1. Connect GitHub repository"
echo "2. Set environment variables"
echo "3. Deploy backend and frontend services"
""")
        render_script.chmod(0o755)
        
        # Fly.io deployment script
        fly_script = scripts_dir / "deploy_fly.sh"
        fly_script.write_text("""#!/bin/bash
# Fly.io Deployment Script
echo "🪰 Deploying to Fly.io..."

# Check if fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo "Installing Fly CLI..."
    curl -L https://fly.io/install.sh | sh
fi

# Login to Fly
fly auth login

# Create app if it doesn't exist
fly apps create biometric-auth --org personal || true

# Deploy
fly deploy --dockerfile backend/Dockerfile.prod

echo "✅ Fly.io deployment complete!"
""")
        fly_script.chmod(0o755)
        
    def _create_environment_templates(self):
        """Create environment variable templates"""
        env_dir = self.package_dir / "env_templates"
        env_dir.mkdir()
        
        # Production environment template
        prod_env = env_dir / "production.env"
        prod_env.write_text("""# Production Environment Variables
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
SECRET_KEY=your-very-secure-secret-key-here
JWT_SECRET=your-jwt-secret-key-here

# CORS
CORS_ORIGINS=https://your-frontend-domain.com

# Optional: Redis for caching
REDIS_URL=redis://host:port

# Optional: Email service
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Performance
TENSORFLOW_OPTIMIZATION=true
GPU_ACCELERATION=auto
BATCH_PROCESSING=true
""")
        
        # Development environment template
        dev_env = env_dir / "development.env"
        dev_env.write_text("""# Development Environment Variables
# Database
DATABASE_URL=postgresql://biometric_user:secure_password_123@localhost:5432/biometric_auth

# Security
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=dev-jwt-secret-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000

# Performance
TENSORFLOW_OPTIMIZATION=false
GPU_ACCELERATION=false
BATCH_PROCESSING=false
""")
        
    def _create_deployment_config(self):
        """Create deployment configuration file"""
        config = {
            "project_info": {
                "name": "Biometric Authentication System",
                "version": "2.0.0",
                "description": "Multi-modal biometric authentication system",
                "packaged_at": self.timestamp
            },
            "deployment_options": {
                "railway": {
                    "description": "Fastest deployment option",
                    "time_estimate": "5 minutes",
                    "cost": "Free tier available",
                    "features": ["Auto-scaling", "SSL", "Database included"]
                },
                "render": {
                    "description": "Easy deployment with good performance",
                    "time_estimate": "10 minutes", 
                    "cost": "Free tier available",
                    "features": ["Auto-scaling", "SSL", "Database included"]
                },
                "fly": {
                    "description": "Global deployment with edge locations",
                    "time_estimate": "15 minutes",
                    "cost": "Free tier available", 
                    "features": ["Global CDN", "Auto-scaling", "SSL"]
                },
                "gcp": {
                    "description": "Google Cloud Platform deployment",
                    "time_estimate": "20 minutes",
                    "cost": "Pay per use",
                    "features": ["High performance", "GPU support", "Enterprise features"]
                },
                "aws": {
                    "description": "Amazon Web Services deployment",
                    "time_estimate": "25 minutes", 
                    "cost": "Pay per use",
                    "features": ["High availability", "Auto-scaling", "Enterprise features"]
                }
            },
            "system_requirements": {
                "backend": {
                    "python": "3.8+",
                    "memory": "2GB+",
                    "storage": "10GB+"
                },
                "frontend": {
                    "node": "16+",
                    "memory": "1GB+"
                },
                "database": {
                    "postgresql": "12+",
                    "storage": "5GB+"
                }
            }
        }
        
        config_file = self.package_dir / "deployment_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    def deploy_to_railway(self):
        """Deploy to Railway"""
        print("🚂 Deploying to Railway...")
        
        # Check if we're in a git repository
        if not (self.project_root / ".git").exists():
            print("❌ This directory is not a git repository")
            print("Please initialize git and push to GitHub first:")
            print("  git init")
            print("  git add .")
            print("  git commit -m 'Initial commit'")
            print("  git remote add origin <your-github-repo>")
            print("  git push -u origin main")
            return False
            
        try:
            # Check if railway CLI is installed
            result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Installing Railway CLI...")
                subprocess.run(["npm", "install", "-g", "@railway/cli"], check=True)
                
            print("✅ Railway CLI ready")
            print("📋 Next steps:")
            print("1. Go to https://railway.app")
            print("2. Sign up with GitHub")
            print("3. Click 'New Project' → 'Deploy from GitHub repo'")
            print("4. Select this repository")
            print("5. Railway will automatically deploy your app")
            print("6. Add environment variables in Railway dashboard")
            
            return True
            
        except Exception as e:
            print(f"❌ Railway deployment failed: {e}")
            return False
            
    def deploy_to_render(self):
        """Deploy to Render"""
        print("🎨 Deploying to Render...")
        
        try:
            print("📋 Render deployment steps:")
            print("1. Go to https://render.com")
            print("2. Sign up with GitHub")
            print("3. Click 'New Web Service'")
            print("4. Connect your GitHub repository")
            print("5. Configure backend service:")
            print("   - Name: biometric-auth-backend")
            print("   - Environment: Docker")
            print("   - Root Directory: backend")
            print("   - Dockerfile Path: Dockerfile")
            print("6. Configure frontend service:")
            print("   - Name: biometric-auth-frontend")
            print("   - Environment: Static Site")
            print("   - Build Command: cd frontend && npm install && npm run build")
            print("   - Publish Directory: frontend/build")
            print("7. Add environment variables in Render dashboard")
            
            return True
            
        except Exception as e:
            print(f"❌ Render deployment failed: {e}")
            return False
            
    def deploy_to_fly(self):
        """Deploy to Fly.io"""
        print("🪰 Deploying to Fly.io...")
        
        try:
            # Check if fly CLI is installed
            result = subprocess.run(["fly", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Installing Fly CLI...")
                if platform.system() == "Windows":
                    subprocess.run(["powershell", "-Command", "iwr https://fly.io/install.ps1 -useb | iex"], check=True)
                else:
                    subprocess.run(["curl", "-L", "https://fly.io/install.sh", "|", "sh"], check=True)
                    
            print("✅ Fly CLI ready")
            print("📋 Next steps:")
            print("1. Run: fly auth login")
            print("2. Run: fly apps create biometric-auth")
            print("3. Run: fly deploy --dockerfile backend/Dockerfile.prod")
            print("4. Add environment variables: fly secrets set KEY=VALUE")
            
            return True
            
        except Exception as e:
            print(f"❌ Fly.io deployment failed: {e}")
            return False
            
    def deploy_to_gcp(self):
        """Deploy to Google Cloud Platform"""
        print("☁️ Deploying to Google Cloud Platform...")
        
        try:
            # Check if gcloud CLI is installed
            result = subprocess.run(["gcloud", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Google Cloud CLI not found")
                print("Please install from: https://cloud.google.com/sdk/docs/install")
                return False
                
            print("✅ Google Cloud CLI ready")
            print("📋 GCP deployment steps:")
            print("1. Run: gcloud auth login")
            print("2. Run: gcloud config set project YOUR_PROJECT_ID")
            print("3. Run: gcloud app deploy app.yaml")
            print("4. Your app will be available at: https://YOUR_PROJECT_ID.uc.r.appspot.com")
            
            return True
            
        except Exception as e:
            print(f"❌ GCP deployment failed: {e}")
            return False
            
    def deploy_to_aws(self):
        """Deploy to AWS"""
        print("☁️ Deploying to AWS...")
        
        try:
            # Check if AWS CLI is installed
            result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ AWS CLI not found")
                print("Please install from: https://aws.amazon.com/cli/")
                return False
                
            print("✅ AWS CLI ready")
            print("📋 AWS deployment steps:")
            print("1. Configure AWS CLI: aws configure")
            print("2. Create ECR repository: aws ecr create-repository --repository-name biometric-auth")
            print("3. Build and push Docker image")
            print("4. Create ECS cluster and service")
            print("5. Configure load balancer and auto-scaling")
            
            return True
            
        except Exception as e:
            print(f"❌ AWS deployment failed: {e}")
            return False
            
    def create_zip_package(self):
        """Create a zip file of the deployment package"""
        print("📦 Creating zip package...")
        
        zip_path = self.project_root / f"biometric_auth_deployment_{self.timestamp}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.package_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(self.package_dir)
                    zipf.write(file_path, arc_name)
                    
        print(f"✅ Zip package created: {zip_path}")
        return zip_path
        
    def show_deployment_info(self):
        """Show deployment information and options"""
        print("🚀 Deployment Options Available:")
        print("=" * 50)
        
        options = [
            ("Railway", "🚂 Fastest deployment (5 min)", "railway"),
            ("Render", "🎨 Easy deployment (10 min)", "render"), 
            ("Fly.io", "🪰 Global deployment (15 min)", "fly"),
            ("Google Cloud", "☁️ Enterprise deployment (20 min)", "gcp"),
            ("AWS", "☁️ Enterprise deployment (25 min)", "aws")
        ]
        
        for i, (name, desc, key) in enumerate(options, 1):
            print(f"{i}. {name} - {desc}")
            
        print("\n💡 Quick Start:")
        print("   python package_and_deploy.py --deploy railway")
        print("   python package_and_deploy.py --package")
        print("   python package_and_deploy.py --help")

def main():
    parser = argparse.ArgumentParser(description="Package and deploy Biometric Authentication System")
    parser.add_argument("--package", action="store_true", help="Create deployment package")
    parser.add_argument("--deploy", choices=["railway", "render", "fly", "gcp", "aws"], 
                       help="Deploy to specified platform")
    parser.add_argument("--zip", action="store_true", help="Create zip package")
    parser.add_argument("--info", action="store_true", help="Show deployment information")
    
    args = parser.parse_args()
    
    deployer = BiometricDeployer()
    deployer.print_banner()
    
    if not deployer.check_prerequisites():
        sys.exit(1)
        
    if args.package:
        deployer.create_deployment_package()
        if args.zip:
            deployer.create_zip_package()
            
    elif args.deploy:
        deployer.create_deployment_package()
        
        if args.deploy == "railway":
            deployer.deploy_to_railway()
        elif args.deploy == "render":
            deployer.deploy_to_render()
        elif args.deploy == "fly":
            deployer.deploy_to_fly()
        elif args.deploy == "gcp":
            deployer.deploy_to_gcp()
        elif args.deploy == "aws":
            deployer.deploy_to_aws()
            
    elif args.info:
        deployer.show_deployment_info()
        
    else:
        parser.print_help()
        print("\n💡 Quick Start Examples:")
        print("   python package_and_deploy.py --package")
        print("   python package_and_deploy.py --deploy railway")
        print("   python package_and_deploy.py --info")

if __name__ == "__main__":
    main() 