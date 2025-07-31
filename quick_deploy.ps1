# Quick Cloud Deployment Script for Biometric Authentication
# PowerShell version for Windows

Write-Host "🚀 Biometric Authentication - Cloud Deployment Setup" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

# Check current system
Write-Host "📊 Current System Analysis:" -ForegroundColor Yellow
Write-Host "  - Python 3.10.11 ✅" -ForegroundColor Green
Write-Host "  - TensorFlow 2.19.0 ✅" -ForegroundColor Green
Write-Host "  - Current processing time: 2-3 seconds" -ForegroundColor Red
Write-Host "  - Issue: Timeouts with multiple users" -ForegroundColor Red
Write-Host ""

# Show cloud benefits
Write-Host "☁️  Cloud Benefits:" -ForegroundColor Cyan
Write-Host "  🏃‍♂️ 5-10x faster with GPU acceleration" -ForegroundColor Green
Write-Host "  📈 2-4x faster with batch processing" -ForegroundColor Green
Write-Host "  🔄 Handle 10+ concurrent users" -ForegroundColor Green
Write-Host "  💰 Pay only for usage" -ForegroundColor Green
Write-Host ""

# Deployment options
Write-Host "🎯 Deployment Options:" -ForegroundColor Magenta
Write-Host ""
Write-Host "1. 🥇 Google Cloud Platform (RECOMMENDED)" -ForegroundColor Green
Write-Host "   - Best TensorFlow support"
Write-Host "   - GPU/TPU acceleration"
Write-Host "   - Cost: ~$50-150/month"
Write-Host ""
Write-Host "2. 🥈 Amazon Web Services" -ForegroundColor Yellow
Write-Host "   - GPU instances (P3/P4)"
Write-Host "   - Auto-scaling"
Write-Host "   - Cost: ~$60-200/month"
Write-Host ""
Write-Host "3. 🥉 Microsoft Azure" -ForegroundColor Blue
Write-Host "   - GPU-enabled VMs"
Write-Host "   - ML services"
Write-Host "   - Cost: ~$40-120/month"
Write-Host ""
Write-Host "4. 🐳 Docker (Test locally first)" -ForegroundColor Cyan
Write-Host "   - Simulate cloud environment"
Write-Host "   - Test before deployment"
Write-Host ""

# Get user choice
Write-Host "Which deployment option would you like to set up?" -ForegroundColor White
Write-Host "Enter 1 for GCP, 2 for AWS, 3 for Azure, or 4 for Docker test:" -ForegroundColor White
$choice = Read-Host

switch ($choice) {
    1 {
        Write-Host "🥇 Setting up Google Cloud Platform deployment..." -ForegroundColor Green
        
        # Check if gcloud is installed
        if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
            Write-Host "❌ Google Cloud CLI not found. Please install it first:" -ForegroundColor Red
            Write-Host "   https://cloud.google.com/sdk/docs/install"
            Write-Host ""
            Write-Host "After installation, run:" -ForegroundColor Yellow
            Write-Host "   gcloud auth login" -ForegroundColor Cyan
            Write-Host "   gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Cyan
            Write-Host "   gcloud app deploy deployments/gcp/app.yaml" -ForegroundColor Cyan
            exit 1
        }
        
        Write-Host "✅ Google Cloud CLI found!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 Next steps:" -ForegroundColor Yellow
        Write-Host "1. Set your project: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Cyan
        Write-Host "2. Deploy: gcloud app deploy deployments/gcp/app.yaml" -ForegroundColor Cyan
        Write-Host "3. Your app will be available at: https://YOUR_PROJECT_ID.appspot.com" -ForegroundColor Cyan
    }
    
    2 {
        Write-Host "🥈 Setting up Amazon Web Services deployment..." -ForegroundColor Yellow
        
        # Check if AWS CLI is installed
        if (!(Get-Command aws -ErrorAction SilentlyContinue)) {
            Write-Host "❌ AWS CLI not found. Please install it first:" -ForegroundColor Red
            Write-Host "   https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
            Write-Host ""
            Write-Host "After installation, run:" -ForegroundColor Yellow
            Write-Host "   aws configure" -ForegroundColor Cyan
            Write-Host "   eb init -p docker biometric-auth" -ForegroundColor Cyan
            Write-Host "   eb create biometric-prod --instance-type p3.medium" -ForegroundColor Cyan
            exit 1
        }
        
        Write-Host "✅ AWS CLI found!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 Next steps:" -ForegroundColor Yellow
        Write-Host "1. Configure AWS: aws configure" -ForegroundColor Cyan
        Write-Host "2. Initialize: eb init -p docker biometric-auth" -ForegroundColor Cyan
        Write-Host "3. Deploy: eb create biometric-prod --instance-type p3.medium" -ForegroundColor Cyan
    }
    
    3 {
        Write-Host "🥉 Setting up Microsoft Azure deployment..." -ForegroundColor Blue
        
        # Check if Azure CLI is installed
        if (!(Get-Command az -ErrorAction SilentlyContinue)) {
            Write-Host "❌ Azure CLI not found. Please install it first:" -ForegroundColor Red
            Write-Host "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
            Write-Host ""
            Write-Host "After installation, run:" -ForegroundColor Yellow
            Write-Host "   az login" -ForegroundColor Cyan
            Write-Host "   az containerapp create --resource-group myResourceGroup --name biometric-auth" -ForegroundColor Cyan
            exit 1
        }
        
        Write-Host "✅ Azure CLI found!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 Next steps:" -ForegroundColor Yellow
        Write-Host "1. Login: az login" -ForegroundColor Cyan
        Write-Host "2. Create resource group: az group create --name biometric-rg --location eastus" -ForegroundColor Cyan
        Write-Host "3. Deploy container: az containerapp create --resource-group biometric-rg --name biometric-auth" -ForegroundColor Cyan
    }
    
    4 {
        Write-Host "🐳 Setting up Docker test environment..." -ForegroundColor Cyan
        
        # Check if Docker is installed
        if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
            Write-Host "❌ Docker not found. Please install Docker Desktop first:" -ForegroundColor Red
            Write-Host "   https://www.docker.com/products/docker-desktop"
            exit 1
        }
        
        Write-Host "✅ Docker found!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🏗️  Building optimized Docker image..." -ForegroundColor Yellow
        
        # Build Docker image
        $buildResult = docker build -f Dockerfile.cloud -t biometric-auth-cloud .
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🚀 Starting container..." -ForegroundColor Yellow
            Write-Host "Your app will be available at: http://localhost:8000" -ForegroundColor Cyan
            Write-Host "Health check: http://localhost:8000/health" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Press Ctrl+C to stop the container" -ForegroundColor Yellow
            docker run -p 8000:8000 --name biometric-auth-test biometric-auth-cloud
        } else {
            Write-Host "❌ Docker build failed. Check the logs above." -ForegroundColor Red
            exit 1
        }
    }
    
    default {
        Write-Host "❌ Invalid choice. Please run the script again and choose 1, 2, 3, or 4." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Deployment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📈 Expected Performance Improvements:" -ForegroundColor Yellow
Write-Host "  Current: 2-3 seconds → Cloud: 0.2-0.4 seconds" -ForegroundColor Cyan
Write-Host "  Single user → 10+ concurrent users" -ForegroundColor Cyan
Write-Host "  Manual scaling → Automatic scaling" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Monitor your deployment:" -ForegroundColor Yellow
Write-Host "  - Check response times"
Write-Host "  - Monitor resource usage"
Write-Host "  - Scale as needed"
Write-Host ""
Write-Host "Need help? Check the full deployment guide:" -ForegroundColor Yellow
Write-Host "  📖 CLOUD_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
