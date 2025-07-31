# Frontend Deployment Configuration for GCP
# React App Deployment to Firebase Hosting

## Firebase Hosting Setup Commands:

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase in frontend directory
cd frontend
firebase init hosting

# Build and deploy
npm run build
firebase deploy --only hosting
```

## Production Environment Variables for Frontend:
REACT_APP_API_URL=https://biometric-auth-system.uc.r.appspot.com/api/v1
REACT_APP_ENVIRONMENT=production
PUBLIC_URL=https://biometric-auth-frontend.web.app

## Firebase Configuration:
{
  "hosting": {
    "public": "build",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "/static/**",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=31536000"
          }
        ]
      }
    ]
  }
}
