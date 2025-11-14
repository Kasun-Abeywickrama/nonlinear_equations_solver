# Railway Deployment Guide

## Quick Deploy to Railway

### Option 1: One-Click Deploy (Recommended)
1. Fork this repository to your GitHub account
2. Visit [Railway](https://railway.app)
3. Sign up/in with your GitHub account  
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your forked repository
6. Railway will automatically detect it's a Django app and deploy it

### Option 2: Railway CLI Deploy
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Environment Variables to Set in Railway

Go to your Railway project → Variables tab and set:

```
SECRET_KEY=your-very-long-secret-key-here-make-it-random-and-secure
DEBUG=False
```

Railway will automatically provide:
- `DATABASE_URL` (PostgreSQL database)
- `PORT` (application port)

## Free Tier Limits
- Railway provides $5 in free credits monthly
- Enough for small to medium Django apps
- Automatic HTTPS certificates
- Custom domains supported

## Alternative Free Platforms

### 1. Render.com
- True free tier (with limitations)
- Automatic deploys from GitHub
- Built-in PostgreSQL database

### 2. PythonAnywhere  
- Free tier available
- Good for Django apps
- Manual deployment process

### 3. Vercel (with serverless)
- Free for small projects
- Requires Django adaptation for serverless

## Post-Deployment Steps

1. **Run migrations**: Railway will auto-run them, or use Railway CLI:
   ```bash
   railway run python manage.py migrate
   ```

2. **Create superuser** (optional):
   ```bash
   railway run python manage.py createsuperuser
   ```

3. **Test your app**: Visit the provided Railway URL

## Troubleshooting

- Check Railway logs in the dashboard
- Ensure all environment variables are set
- Verify your requirements.txt includes all dependencies
- Make sure DEBUG=False in production

Your nonlinear equations solver will be live and accessible worldwide! 🚀