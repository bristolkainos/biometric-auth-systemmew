# Biometric Authentication System

A comprehensive multi-modal biometric authentication system for enterprise use with fingerprint, face ID, and palmprint recognition.

## 🚀 Quick Start

### 🚀 Deploy to Cloud (Recommended)

**Choose your deployment platform:**

1. **Railway** (Fastest - 5 minutes) - **RECOMMENDED**:
   ```bash
   # Windows
   deploy.bat
   # Then choose option 1
   
   # PowerShell
   .\deploy_railway.ps1
   
   # Python
   python package_and_deploy.py --deploy railway
   ```

2. **Render** (Easy - 10 minutes):
   ```bash
   # Windows
   deploy.bat
   # Then choose option 2
   
   # PowerShell
   .\deploy_all_platforms.ps1 -Platform render
   ```

3. **Fly.io** (Global - 15 minutes):
   ```bash
   # Windows
   deploy.bat
   # Then choose option 3
   
   # PowerShell
   .\deploy_all_platforms.ps1 -Platform fly
   ```

4. **Docker Local** (Development - 2 minutes):
   ```bash
   # Windows
   deploy.bat
   # Then choose option 6
   
   # PowerShell
   .\deploy_all_platforms.ps1 -Platform docker
   ```

### 🏃‍♂️ Local Development

**Easy Startup Scripts (Choose One):**

1. **Windows Batch Script** (Recommended for Windows):
   ```bash
   start_servers.bat
   ```

2. **PowerShell Script**:
   ```powershell
   ./start_servers.ps1
   ```

3. **Cross-Platform Node.js Script**:
   ```bash
   npm start
   ```

4. **Unix/Linux/macOS Script**:
   ```bash
   ./start_servers.sh
   ```

All scripts will start both backend (port 8000) and frontend (port 3000) servers automatically.

## Features

- **Multi-modal Biometric Authentication**: Fingerprint, Face ID, and Palmprint
- **Registration**: Password + at least 2 biometric methods required
- **Login**: Password + any biometric method
- **Admin Management**: Backend admin can manage users
- **Enterprise Security**: Designed for intranet deployment
- **Audit Trail**: Complete login attempt logging

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Enterprise-grade database
- **SQLAlchemy** - Database ORM
- **JWT** - Token authentication
- **OpenCV** - Image processing
- **NumPy/Scikit-learn** - Machine learning operations

### Frontend
- **React** - User interface
- **TypeScript** - Type safety
- **Material-UI** - Professional components
- **WebRTC** - Camera access

### Infrastructure
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **PostgreSQL** - Database (cloud-hosted)

## Project Structure

```
Biometric_Login_auth/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── database/
│   ├── migrations/
│   └── init.sql
├── docker-compose.yml
└── README.md
```

## Setup Instructions

1. **Clone the repository**
2. **Set up environment variables**
3. **Run with Docker Compose**
4. **Access the application**

## Security Features

- Encrypted biometric data storage
- Rate limiting on login attempts
- IP address logging
- Session management
- Admin audit trails

## 🚀 Deployment Options

### Cloud Deployment (Recommended)

| Platform | Speed | Cost | Features | Best For |
|----------|-------|------|----------|----------|
| **Railway** | ⚡ 5 min | Free tier | Auto-scaling, SSL, DB | Quick deployment |
| **Render** | ⚡ 10 min | Free tier | Auto-scaling, SSL, DB | Easy setup |
| **Fly.io** | ⚡ 15 min | Free tier | Global CDN, Edge | Global reach |
| **Google Cloud** | ⚡ 20 min | Pay per use | GPU, Enterprise | High performance |
| **AWS** | ⚡ 25 min | Pay per use | Enterprise, HA | Enterprise use |

### Local Deployment

Designed for intranet deployment with:
- Internal network access only
- Database encryption at rest
- Secure API endpoints
- Admin-only user management

### Deployment Scripts

- **`deploy.bat`** - Windows deployment wizard
- **`deploy_railway.ps1`** - Railway-specific deployment
- **`deploy_all_platforms.ps1`** - Multi-platform deployment
- **`package_and_deploy.py`** - Python deployment script

### Documentation

- **`DEPLOYMENT_GUIDE.md`** - Complete deployment guide
- **`QUICK_DEPLOY.md`** - Quick deployment instructions
- **`DEPLOYMENT.md`** - Detailed deployment options

## License

Enterprise License - All rights reserved 