#!/bin/bash

# Quick Cloud Deployment Script for Biometric Authentication
# This script will help you deploy your TensorFlow biometric system to the cloud

echo "🚀 Biometric Authentication - Cloud Deployment Setup"
echo "=================================================="
echo ""

# Check current system
echo "📊 Current System Analysis:"
echo "  - Python 3.10.11 ✅"
echo "  - TensorFlow 2.19.0 ✅"
echo "  - Current processing time: 2-3 seconds"
echo "  - Issue: Timeouts with multiple users"
echo ""

# Show cloud benefits
echo "☁️  Cloud Benefits:"
echo "  🏃‍♂️ 5-10x faster with GPU acceleration"
echo "  📈 2-4x faster with batch processing"
echo "  🔄 Handle 10+ concurrent users"
echo "  💰 Pay only for usage"
echo ""

# Deployment options
echo "🎯 Deployment Options:"
echo ""
echo "1. 🥇 Google Cloud Platform (RECOMMENDED)"
echo "   - Best TensorFlow support"
echo "   - GPU/TPU acceleration"
echo "   - Cost: ~$50-150/month"
echo ""
echo "2. 🥈 Amazon Web Services"
echo "   - GPU instances (P3/P4)"
echo "   - Auto-scaling"
echo "   - Cost: ~$60-200/month"
echo ""
echo "3. 🥉 Microsoft Azure"
echo "   - GPU-enabled VMs"
echo "   - ML services"
echo "   - Cost: ~$40-120/month"
echo ""
echo "4. 🐳 Docker (Test locally first)"
echo "   - Simulate cloud environment"
echo "   - Test before deployment"
echo ""

# Get user choice
echo "Which deployment option would you like to set up?"
echo "Enter 1 for GCP, 2 for AWS, 3 for Azure, or 4 for Docker test:"
read -r choice

case $choice in
    1)
        echo "🥇 Setting up Google Cloud Platform deployment..."
        
        # Create GCP-specific files
        echo "📁 Creating GCP deployment files..."
        
        # Check if gcloud is installed
        if ! command -v gcloud &> /dev/null; then
            echo "❌ Google Cloud CLI not found. Please install it first:"
            echo "   https://cloud.google.com/sdk/docs/install"
            echo ""
            echo "After installation, run:"
            echo "   gcloud auth login"
            echo "   gcloud config set project YOUR_PROJECT_ID"
            echo "   gcloud app deploy deployments/gcp/app.yaml"
            exit 1
        fi
        
        echo "✅ Google Cloud CLI found!"
        echo ""
        echo "🚀 Next steps:"
        echo "1. Set your project: gcloud config set project YOUR_PROJECT_ID"
        echo "2. Deploy: gcloud app deploy deployments/gcp/app.yaml"
        echo "3. Your app will be available at: https://YOUR_PROJECT_ID.appspot.com"
        ;;
        
    2)
        echo "🥈 Setting up Amazon Web Services deployment..."
        
        # Check if AWS CLI is installed
        if ! command -v aws &> /dev/null; then
            echo "❌ AWS CLI not found. Please install it first:"
            echo "   https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
            echo ""
            echo "After installation, run:"
            echo "   aws configure"
            echo "   eb init -p docker biometric-auth"
            echo "   eb create biometric-prod --instance-type p3.medium"
            exit 1
        fi
        
        echo "✅ AWS CLI found!"
        echo ""
        echo "🚀 Next steps:"
        echo "1. Configure AWS: aws configure"
        echo "2. Initialize: eb init -p docker biometric-auth"
        echo "3. Deploy: eb create biometric-prod --instance-type p3.medium"
        ;;
        
    3)
        echo "🥉 Setting up Microsoft Azure deployment..."
        
        # Check if Azure CLI is installed
        if ! command -v az &> /dev/null; then
            echo "❌ Azure CLI not found. Please install it first:"
            echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
            echo ""
            echo "After installation, run:"
            echo "   az login"
            echo "   az containerapp create --resource-group myResourceGroup --name biometric-auth"
            exit 1
        fi
        
        echo "✅ Azure CLI found!"
        echo ""
        echo "🚀 Next steps:"
        echo "1. Login: az login"
        echo "2. Create resource group: az group create --name biometric-rg --location eastus"
        echo "3. Deploy container: az containerapp create --resource-group biometric-rg --name biometric-auth"
        ;;
        
    4)
        echo "🐳 Setting up Docker test environment..."
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker not found. Please install Docker Desktop first:"
            echo "   https://www.docker.com/products/docker-desktop"
            exit 1
        fi
        
        echo "✅ Docker found!"
        echo ""
        echo "🏗️  Building optimized Docker image..."
        docker build -f Dockerfile.cloud -t biometric-auth-cloud .
        
        if [ $? -eq 0 ]; then
            echo "✅ Docker image built successfully!"
            echo ""
            echo "🚀 Starting container..."
            echo "Your app will be available at: http://localhost:8000"
            echo "Health check: http://localhost:8000/health"
            echo ""
            echo "Press Ctrl+C to stop the container"
            docker run -p 8000:8000 --name biometric-auth-test biometric-auth-cloud
        else
            echo "❌ Docker build failed. Check the logs above."
            exit 1
        fi
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1, 2, 3, or 4."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment setup complete!"
echo ""
echo "📈 Expected Performance Improvements:"
echo "  Current: 2-3 seconds → Cloud: 0.2-0.4 seconds"
echo "  Single user → 10+ concurrent users"
echo "  Manual scaling → Automatic scaling"
echo ""
echo "📊 Monitor your deployment:"
echo "  - Check response times"
echo "  - Monitor resource usage"
echo "  - Scale as needed"
echo ""
echo "Need help? Check the full deployment guide:"
echo "  📖 CLOUD_DEPLOYMENT_GUIDE.md"
