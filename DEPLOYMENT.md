# Cloud Deployment Guide

This guide covers deploying the Biometric Authentication System to various cloud platforms.

## Quick Deploy Options

### 1. Railway (Recommended - Easiest)

Railway is the fastest way to deploy your application.

#### Prerequisites:
- GitHub account
- Railway account (free tier available)

#### Steps:
1. **Fork/Clone this repository to GitHub**
2. **Go to [Railway.app](https://railway.app)**
3. **Connect your GitHub account**
4. **Click "New Project" → "Deploy from GitHub repo"**
5. **Select your repository**
6. **Railway will automatically detect the Dockerfile and deploy**

#### Environment Variables (set in Railway dashboard):
```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
CORS_ORIGINS=https://your-frontend-domain.com
```

### 2. Render

#### Steps:
1. **Go to [Render.com](https://render.com)**
2. **Connect your GitHub account**
3. **Click "New Web Service"**
4. **Select your repository**
5. **Configure:**
   - **Name:** biometric-auth-backend
   - **Environment:** Docker
   - **Branch:** main
   - **Root Directory:** backend
   - **Dockerfile Path:** Dockerfile.prod

### 3. Fly.io

#### Prerequisites:
- Fly CLI installed: `curl -L https://fly.io/install.sh | sh`

#### Steps:
1. **Login to Fly:** `fly auth login`
2. **Create app:** `fly apps create biometric-auth`
3. **Deploy:** `fly deploy --dockerfile backend/Dockerfile.prod`

### 4. Google Cloud Run

#### Prerequisites:
- Google Cloud CLI installed
- Project created in Google Cloud Console

#### Steps:
1. **Build image:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/biometric-auth
   ```
2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy biometric-auth \
     --image gcr.io/PROJECT_ID/biometric-auth \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### 5. AWS ECS/Fargate

#### Prerequisites:
- AWS CLI configured
- ECR repository created

#### Steps:
1. **Build and push to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   docker build -t biometric-auth .
   docker tag biometric-auth:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/biometric-auth:latest
   docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/biometric-auth:latest
   ```
2. **Create ECS service using AWS Console or CLI**

## Database Setup

### Option 1: Cloud Database (Recommended)

#### Railway PostgreSQL:
- Railway provides managed PostgreSQL
- Automatically handles backups and scaling

#### Supabase:
- Free tier available
- PostgreSQL with real-time features
- Easy to set up

#### Neon:
- Serverless PostgreSQL
- Auto-scaling
- Free tier available

### Option 2: Self-hosted Database

If using a cloud platform without managed databases:

1. **Deploy PostgreSQL container separately**
2. **Use connection pooling (PgBouncer)**
3. **Set up automated backups**

## Environment Configuration

### Required Environment Variables:

```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
SECRET_KEY=your-very-secure-secret-key-here
JWT_SECRET=your-jwt-secret-key-here

# CORS
CORS_ORIGINS=https://your-frontend-domain.com,https://your-admin-domain.com

# Optional: Redis for caching
REDIS_URL=redis://host:port

# Optional: Email service
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Frontend Deployment

### Deploy Frontend to:

1. **Vercel** (Recommended):
   - Connect GitHub repository
   - Automatic deployments
   - Free tier available

2. **Netlify**:
   - Drag and drop deployment
   - Free tier available

3. **GitHub Pages**:
   - Free hosting
   - Requires build step

### Frontend Environment Variables:

```bash
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_ENVIRONMENT=production
```

## SSL/HTTPS Setup

### Automatic SSL (Recommended):
- Railway, Render, Fly.io provide automatic SSL
- Vercel and Netlify provide automatic SSL

### Manual SSL:
- Use Let's Encrypt
- Configure nginx with SSL certificates

## Monitoring and Logs

### Built-in Monitoring:
- Railway: Built-in monitoring dashboard
- Render: Logs and metrics available
- Fly.io: Built-in monitoring

### External Monitoring:
- Sentry for error tracking
- LogRocket for user session replay
- Google Analytics for usage analytics

## Scaling Considerations

### Horizontal Scaling:
- Use load balancers
- Implement session management
- Use Redis for session storage

### Database Scaling:
- Use read replicas
- Implement connection pooling
- Consider database sharding for large scale

## Security Best Practices

1. **Environment Variables**: Never commit secrets to code
2. **HTTPS**: Always use HTTPS in production
3. **CORS**: Configure CORS properly
4. **Rate Limiting**: Implement API rate limiting
5. **Input Validation**: Validate all inputs
6. **SQL Injection**: Use parameterized queries
7. **XSS Protection**: Sanitize user inputs

## Troubleshooting

### Common Issues:

1. **Port Issues**: Ensure PORT environment variable is set
2. **Database Connection**: Check DATABASE_URL format
3. **CORS Errors**: Verify CORS_ORIGINS configuration
4. **Build Failures**: Check Dockerfile syntax
5. **Memory Issues**: Optimize container resources

### Debug Commands:

```bash
# Check container logs
docker logs container_name

# Check application health
curl https://your-domain.com/health

# Test database connection
python -c "from app.database import engine; print('DB OK')"
```

## Cost Optimization

### Free Tiers Available:
- Railway: $5/month free tier
- Render: Free tier available
- Fly.io: Free tier available
- Vercel: Free tier available
- Netlify: Free tier available

### Cost Saving Tips:
1. Use free tiers where possible
2. Implement proper resource limits
3. Use serverless where appropriate
4. Monitor usage and optimize
5. Use CDN for static assets

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review logs for error messages
3. Verify environment variables
4. Test locally before deploying 