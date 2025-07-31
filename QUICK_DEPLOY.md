# 🚀 Quick Deploy to Cloud

## Option 1: Railway (Fastest - 5 minutes)

### Step 1: Prepare Your Code
```bash
# Make sure your code is in a GitHub repository
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect and deploy

### Step 3: Set Environment Variables
In Railway dashboard, add these variables:
```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-super-secret-key-here
JWT_SECRET=your-jwt-secret-here
CORS_ORIGINS=https://your-frontend-domain.com
```

### Step 4: Add Database
1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically link it to your app

## Option 2: Render (Alternative)

### Step 1: Deploy Backend
1. Go to [Render.com](https://render.com)
2. Connect GitHub account
3. Click "New Web Service"
4. Select your repository
5. Configure:
   - **Name:** biometric-auth-backend
   - **Environment:** Docker
   - **Root Directory:** backend
   - **Dockerfile Path:** Dockerfile.prod

### Step 2: Deploy Frontend
1. In Render, click "New Static Site"
2. Connect to your GitHub repo
3. Configure:
   - **Name:** biometric-auth-frontend
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/build`

## Option 3: Fly.io (Global Deployment)

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Deploy
```bash
# Login
fly auth login

# Create app
fly apps create biometric-auth

# Deploy
fly deploy --dockerfile backend/Dockerfile.prod
```

## Environment Variables for All Platforms

### Required Variables:
```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-very-secure-secret-key-here
JWT_SECRET=your-jwt-secret-key-here
CORS_ORIGINS=https://your-frontend-domain.com
```

### Optional Variables:
```bash
REDIS_URL=redis://host:port
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Database Setup

### Railway (Automatic):
- Railway provides managed PostgreSQL
- Automatically handles backups

### Render (Automatic):
- Render provides managed PostgreSQL
- Easy to set up

### External Database Options:
1. **Supabase** (Free tier):
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Get connection string

2. **Neon** (Free tier):
   - Go to [neon.tech](https://neon.tech)
   - Create new project
   - Get connection string

3. **PlanetScale** (Free tier):
   - Go to [planetscale.com](https://planetscale.com)
   - Create new database
   - Get connection string

## Frontend Deployment

### Vercel (Recommended):
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set build settings:
   - **Framework Preset:** Create React App
   - **Root Directory:** frontend
   - **Build Command:** `npm run build`
   - **Output Directory:** build

### Environment Variables for Frontend:
```bash
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_ENVIRONMENT=production
```

## Testing Your Deployment

### 1. Check Backend Health:
```bash
curl https://your-backend-domain.com/health
```

### 2. Test API Endpoints:
```bash
# Test registration endpoint
curl -X POST https://your-backend-domain.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### 3. Check Frontend:
- Visit your frontend URL
- Try to register a new user
- Test biometric capture

## Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Check Dockerfile syntax
   - Verify all dependencies are in requirements.txt
   - Check platform-specific logs

2. **Database Connection:**
   - Verify DATABASE_URL format
   - Check if database is accessible
   - Ensure SSL is configured if required

3. **CORS Errors:**
   - Update CORS_ORIGINS with your frontend domain
   - Include both http and https versions

4. **Port Issues:**
   - Ensure PORT environment variable is set
   - Check if platform uses different port variable

### Debug Commands:
```bash
# Check application logs
railway logs
# or
fly logs
# or
render logs

# Test database connection
python -c "from app.database import engine; print('DB OK')"

# Check environment variables
railway variables
```

## Next Steps

After successful deployment:

1. **Set up monitoring** (Sentry, LogRocket)
2. **Configure SSL certificates** (usually automatic)
3. **Set up backups** for database
4. **Configure custom domain** (optional)
5. **Set up CI/CD** for automatic deployments

## Support

- **Railway:** [docs.railway.app](https://docs.railway.app)
- **Render:** [render.com/docs](https://render.com/docs)
- **Fly.io:** [fly.io/docs](https://fly.io/docs)
- **Vercel:** [vercel.com/docs](https://vercel.com/docs) 