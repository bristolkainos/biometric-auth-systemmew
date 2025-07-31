# ☁️ Google Cloud Platform Deployment Guide

## 🎯 **Why GCP is Perfect for Your Biometric System**

### **✅ GCP Advantages:**

1. **GPU Support** - Perfect for PyTorch ResNet50 processing
2. **Auto-scaling** - Handles varying biometric processing loads
3. **Global CDN** - Fast access worldwide
4. **Enterprise Security** - Perfect for biometric data
5. **Managed Services** - Database, monitoring, logging
6. **Cost Effective** - Pay only for what you use
7. **Free Tier** - Generous free tier available

### **🎯 GCP Services You'll Use:**

- **App Engine** - Host your FastAPI backend
- **Cloud Storage** - Store ML models and large files
- **Cloud SQL** - PostgreSQL database
- **Cloud Run** - Containerized deployment (alternative)
- **Cloud Build** - Automated deployments

## 🚀 **Quick Start: Deploy to GCP**

### **Option 1: Automated Deployment**
```bash
# Windows
deploy.bat
# Choose option 5: "Google Cloud Platform"

# PowerShell
.\deploy_gcp.ps1
```

### **Option 2: Manual Deployment**
```bash
# Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# Login and configure
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud config set compute/region us-central1

# Deploy
gcloud app deploy app.yaml
```

## 📋 **Step-by-Step GCP Setup**

### **Step 1: Create GCP Project**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Enter project name: `biometric-auth-system`
4. Click "Create"

### **Step 2: Enable Required APIs**

```bash
# Enable App Engine API
gcloud services enable appengine.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable Cloud SQL Admin API
gcloud services enable sqladmin.googleapis.com

# Enable Cloud Storage API
gcloud services enable storage.googleapis.com
```

### **Step 3: Set Up Billing**

1. Go to [Billing](https://console.cloud.google.com/billing)
2. Link billing account to your project
3. GCP offers $300 free credit for new users

### **Step 4: Configure App Engine**

Your `app.yaml` is already configured! It includes:

```yaml
runtime: python310
service: default

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

resources:
  cpu: 2
  memory_gb: 4
  disk_size_gb: 20

env_variables:
  TENSORFLOW_OPTIMIZATION: "true"
  GPU_ACCELERATION: "auto"
  BATCH_PROCESSING: "true"
  CLOUD_PROVIDER: "gcp"
```

## 🗄️ **Database Setup (Cloud SQL)**

### **Step 1: Create PostgreSQL Instance**

```bash
# Create Cloud SQL instance
gcloud sql instances create biometric-auth-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_SECURE_PASSWORD
```

### **Step 2: Create Database**

```bash
# Create database
gcloud sql databases create biometric_auth \
  --instance=biometric-auth-db
```

### **Step 3: Get Connection String**

```bash
# Get connection info
gcloud sql instances describe biometric-auth-db
```

Update your `app.yaml` with the connection string:
```yaml
env_variables:
  DATABASE_URL: "postgresql://postgres:YOUR_PASSWORD@YOUR_IP:5432/biometric_auth"
```

## 📦 **Model Storage (Cloud Storage)**

### **Step 1: Create Storage Bucket**

```bash
# Create bucket for models
gsutil mb gs://biometric-auth-models

# Make bucket publicly readable (or use signed URLs)
gsutil iam ch allUsers:objectViewer gs://biometric-auth-models
```

### **Step 2: Upload Models**

```bash
# Upload model files
gsutil cp models/face_cnn.h5 gs://biometric-auth-models/
gsutil cp models/fingerprint_cnn.h5 gs://biometric-auth-models/
gsutil cp models/palmprint_cnn.h5 gs://biometric-auth-models/
```

### **Step 3: Update Download Script**

Update `download_models.py` with GCP URLs:
```python
models = {
    "face_cnn.h5": "https://storage.googleapis.com/biometric-auth-models/face_cnn.h5",
    "fingerprint_cnn.h5": "https://storage.googleapis.com/biometric-auth-models/fingerprint_cnn.h5",
    "palmprint_cnn.h5": "https://storage.googleapis.com/biometric-auth-models/palmprint_cnn.h5",
}
```

## 🚀 **Deploy Backend**

### **Step 1: Deploy to App Engine**

```bash
# Deploy your application
gcloud app deploy app.yaml --promote --stop-previous-version
```

### **Step 2: Access Your App**

Your app will be available at:
```
https://YOUR_PROJECT_ID.uc.r.appspot.com
```

### **Step 3: Test Deployment**

```bash
# Test health endpoint
curl https://YOUR_PROJECT_ID.uc.r.appspot.com/health

# View logs
gcloud app logs tail -s default
```

## 🎨 **Deploy Frontend**

### **Option 1: Firebase Hosting (Recommended)**

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase project
firebase init hosting

# Build frontend
cd frontend
npm run build

# Deploy
firebase deploy
```

### **Option 2: Cloud Storage Static Website**

```bash
# Create bucket for website
gsutil mb gs://biometric-auth-frontend

# Configure bucket for website
gsutil web set -m index.html -e 404.html gs://biometric-auth-frontend

# Upload frontend files
gsutil -m cp -r frontend/build/* gs://biometric-auth-frontend/

# Make files publicly readable
gsutil iam ch allUsers:objectViewer gs://biometric-auth-frontend
```

### **Option 3: App Engine Static Files**

Create a separate service for frontend in `app.yaml`:
```yaml
runtime: python310
service: frontend

handlers:
- url: /(.*)
  static_files: frontend/build/\1
  upload: frontend/build/(.*)
```

## 🔧 **Environment Configuration**

### **Required Environment Variables**

Update your `app.yaml`:
```yaml
env_variables:
  DATABASE_URL: "postgresql://postgres:YOUR_PASSWORD@YOUR_IP:5432/biometric_auth"
  SECRET_KEY: "your-very-secure-secret-key-here"
  JWT_SECRET: "your-jwt-secret-key-here"
  CORS_ORIGINS: "https://your-frontend-domain.com"
  TENSORFLOW_OPTIMIZATION: "true"
  GPU_ACCELERATION: "auto"
  BATCH_PROCESSING: "true"
  CLOUD_PROVIDER: "gcp"
```

### **Generate Secure Keys**

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

## 📊 **Monitoring & Management**

### **View Logs**

```bash
# Real-time logs
gcloud app logs tail -s default

# Historical logs
gcloud app logs read

# Filter logs
gcloud app logs read --filter="severity>=ERROR"
```

### **Monitor Performance**

```bash
# List instances
gcloud app instances list

# View app info
gcloud app describe

# Check versions
gcloud app versions list
```

### **Scale Application**

```bash
# Update scaling configuration
gcloud app deploy app.yaml

# Manual scaling (if needed)
gcloud app versions migrate v1 --min-instances=2 --max-instances=20
```

## 💰 **Cost Optimization**

### **Free Tier Benefits**

- **App Engine**: 28 instance hours/day free
- **Cloud SQL**: db-f1-micro instance free
- **Cloud Storage**: 5GB free
- **Cloud Build**: 120 build-minutes/day free

### **Cost Optimization Tips**

1. **Use free tier limits**
2. **Set reasonable instance limits**
3. **Use Cloud Storage for large files**
4. **Enable automatic scaling**
5. **Monitor usage with billing alerts**

### **Estimated Monthly Costs**

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| App Engine | $0 | $0.05/hour |
| Cloud SQL | $0 | $7.50/month |
| Cloud Storage | $0 | $0.02/GB |
| **Total** | **$0** | **~$15-25/month** |

## 🔒 **Security Best Practices**

### **1. IAM (Identity and Access Management)**

```bash
# Create service account
gcloud iam service-accounts create biometric-auth-sa

# Grant minimal permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:biometric-auth-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/appengine.deployer"
```

### **2. Network Security**

```bash
# Configure Cloud SQL for private access
gcloud sql instances patch biometric-auth-db \
  --authorized-networks=YOUR_APP_ENGINE_IP
```

### **3. Data Encryption**

- Cloud SQL: Encryption at rest (automatic)
- Cloud Storage: Encryption at rest (automatic)
- App Engine: HTTPS by default

## 🚀 **Advanced Features**

### **GPU Support (Optional)**

Uncomment in `app.yaml`:
```yaml
accelerators:
  - type: nvidia-tesla-t4
    count: 1
```

### **Custom Domain**

```bash
# Map custom domain
gcloud app domain-mappings create YOUR_DOMAIN
```

### **Load Balancing**

```bash
# Create load balancer
gcloud compute backend-services create biometric-auth-backend
```

## ✅ **Deployment Checklist**

After deployment, verify:

- [ ] Backend is accessible via HTTPS
- [ ] Database connection works
- [ ] Models are downloadable
- [ ] Frontend loads correctly
- [ ] User registration works
- [ ] Biometric capture works
- [ ] Admin panel is accessible
- [ ] Logs are being generated
- [ ] Monitoring is set up
- [ ] Billing alerts are configured

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **Deployment fails**
   ```bash
   # Check logs
   gcloud app logs tail
   
   # Check requirements
   pip install -r requirements.txt
   ```

2. **Database connection fails**
   ```bash
   # Test connection
   gcloud sql connect biometric-auth-db
   
   # Check firewall rules
   gcloud sql instances describe biometric-auth-db
   ```

3. **Models not found**
   ```bash
   # Check Cloud Storage
   gsutil ls gs://biometric-auth-models/
   
   # Test download
   curl https://storage.googleapis.com/biometric-auth-models/face_cnn.h5
   ```

### **Debug Commands:**

```bash
# Check app status
gcloud app describe

# View instance details
gcloud app instances list

# Check database status
gcloud sql instances describe biometric-auth-db

# Monitor costs
gcloud billing accounts list
```

## 🎉 **Success!**

Your biometric authentication system is now running on Google Cloud Platform with:

- ✅ **Enterprise-grade infrastructure**
- ✅ **Auto-scaling capabilities**
- ✅ **Global CDN**
- ✅ **Managed database**
- ✅ **Built-in monitoring**
- ✅ **Cost optimization**

**Your app is live at: https://YOUR_PROJECT_ID.uc.r.appspot.com 🚀**
