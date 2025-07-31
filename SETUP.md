# Biometric Authentication System - Setup Guide

## Prerequisites

Before setting up the system, ensure you have the following installed:

- **Docker** and **Docker Compose** (latest version)
- **Git** (for cloning the repository)
- **Node.js** (v18 or higher) - for local development
- **Python** (v3.11 or higher) - for local development

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd Biometric_Login_auth

# Copy environment file
cp env.example .env

# Edit environment variables (optional for development)
nano .env
```

### 2. Add Your Pretrained Models

Place your pretrained models in the `models/` directory:

```
models/
├── fingerprint_model.pkl
├── face_model.pkl
└── palmprint_model.pkl
```

### 3. Start the System

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## Default Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Email**: admin@company.com

## Configuration

### Environment Variables

Edit the `.env` file to customize the system:

```bash
# Database
DB_PASSWORD=your_secure_password
DATABASE_URL=postgresql://biometric_user:your_secure_password@localhost:5432/biometric_auth

# Security
SECRET_KEY=your-very-secure-secret-key
JWT_SECRET=your-very-secure-jwt-secret

# Biometric Settings
MIN_BIOMETRIC_METHODS=2
MAX_LOGIN_ATTEMPTS=5
FACE_RECOGNITION_TOLERANCE=0.6
FINGERPRINT_MATCH_THRESHOLD=0.8
PALMPRINT_MATCH_THRESHOLD=0.8
```

### Database Configuration

The system uses PostgreSQL with the following default settings:

- **Database**: biometric_auth
- **User**: biometric_user
- **Password**: Set via DB_PASSWORD environment variable
- **Port**: 5432

## Development Setup

### Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Production Deployment

### 1. Environment Configuration

```bash
# Set production environment
ENVIRONMENT=production
DEBUG=false

# Use strong secrets
SECRET_KEY=your-production-secret-key
JWT_SECRET=your-production-jwt-secret

# Configure CORS for your domain
CORS_ORIGINS=https://yourdomain.com
```

### 2. Database Setup

For production, consider using a managed PostgreSQL service:

- **AWS RDS**
- **Google Cloud SQL**
- **Azure Database for PostgreSQL**
- **DigitalOcean Managed Databases**

### 3. SSL Configuration

Configure SSL certificates in the nginx configuration:

```bash
# Copy SSL certificates to nginx/ssl/
cp your-cert.pem nginx/ssl/cert.pem
cp your-key.pem nginx/ssl/key.pem
```

### 4. Deploy

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Security Considerations

### 1. Network Security

- Deploy on a secure intranet network
- Use VPN for remote access
- Configure firewall rules appropriately

### 2. Database Security

- Use strong passwords
- Enable SSL connections
- Regular backups
- Access control and monitoring

### 3. Application Security

- Regular security updates
- Monitor login attempts
- Implement rate limiting
- Audit logging

### 4. Biometric Data Security

- Encrypt biometric data at rest
- Secure transmission of biometric data
- Regular model updates
- Compliance with privacy regulations

## Monitoring and Maintenance

### 1. Health Checks

```bash
# Check system health
curl http://localhost:8000/health

# Check database connection
docker-compose exec postgres pg_isready
```

### 2. Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### 3. Database Maintenance

```bash
# Access database
docker-compose exec postgres psql -U biometric_user -d biometric_auth

# Backup database
docker-compose exec postgres pg_dump -U biometric_user biometric_auth > backup.sql

# Restore database
docker-compose exec -T postgres psql -U biometric_user -d biometric_auth < backup.sql
```

### 4. Updates

```bash
# Update system
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database connection errors**: Check DB_PASSWORD and DATABASE_URL
3. **Model loading errors**: Ensure models are in the correct format and location
4. **CORS errors**: Update CORS_ORIGINS in environment variables

### Support

For issues and questions:
1. Check the logs: `docker-compose logs`
2. Verify configuration in `.env` file
3. Ensure all prerequisites are installed
4. Check network connectivity

## API Documentation

Once the system is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

This system is licensed for enterprise use. All rights reserved. 