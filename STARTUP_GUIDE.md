# Biometric Authentication System

A comprehensive biometric authentication system with FastAPI backend and React frontend.

## Quick Start

### Option 1: Windows Batch Script (Recommended for Windows)
```bash
start_servers.bat
```

### Option 2: PowerShell Script
```powershell
./start_servers.ps1
```

### Option 3: Cross-Platform Node.js Script
```bash
node start_servers.js
```

### Option 4: Unix/Linux/macOS Script
```bash
chmod +x start_servers.sh
./start_servers.sh
```

## Manual Start

### Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm start
```

## Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## Features

- Multi-modal biometric authentication (face, fingerprint, palmprint)
- Advanced TensorFlow-powered feature extraction
- Modern React interface with Material-UI
- Real-time biometric capture and processing
- Admin dashboard and user management
- Comprehensive security layers

## System Requirements

- Python 3.8+
- Node.js 14+
- Modern web browser with camera access
- TensorFlow dependencies (automatically installed)

## Default Credentials

- **Admin Login**: admin / admin123

Enjoy your biometric authentication system! 🚀
