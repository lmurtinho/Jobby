# 🚀 AI Job Tracker Deployment Guide

**Date:** August 1, 2025  
**Status:** Ready for Production Deployment  
**Platforms:** Railway (Backend) + Vercel (Frontend)

## 📋 Pre-Deployment Checklist

✅ **Code Ready:**
- Health endpoint implemented (`/health`)
- Config status endpoint implemented (`/api/v1/config/status`)
- Railway configuration file (`railway.toml`) present
- Frontend builds successfully
- Core functionality tested (90%+ backend coverage)

✅ **Deployment Requirements:**
- Railway account and CLI installed
- Vercel account and CLI installed  
- GitHub repository up to date
- Environment variables ready

## 🔧 Step 1: Deploy Backend to Railway

### 1.1 Railway Setup
```bash
# Login to Railway (interactive)
railway login

# Create new project
railway new ai-job-tracker-backend

# Link to existing project (if already created)
railway link

# Add PostgreSQL database
railway add postgresql
```

### 1.2 Configure Environment Variables

**Required Environment Variables for Railway:**
```bash
railway variables:set DATABASE_URL=${{RAILWAY_DATABASE_URL}}
railway variables:set SECRET_KEY="your-super-secret-production-key-here"
railway variables:set JWT_SECRET_KEY="your-jwt-secret-production-key-here"
railway variables:set ANTHROPIC_API_KEY="your-claude-api-key-here"
railway variables:set FRONTEND_URL="https://your-app.vercel.app"
railway variables:set ENVIRONMENT="production"
```

### 1.3 Deploy Backend
```bash
# Deploy from current directory (backend)
cd backend
railway up

# Or deploy from root with specific backend path
railway up --detach
```

### 1.4 Verify Backend Deployment
```bash
# Get deployment URL
railway domain

# Test health endpoint
curl https://your-backend.railway.app/health

# Test config status
curl https://your-backend.railway.app/api/v1/config/status

# Test API docs
curl https://your-backend.railway.app/docs
```

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Vercel Setup
```bash
# Login to Vercel (interactive)
vercel login

# Navigate to frontend directory
cd frontend

# Deploy to production
vercel --prod
```

### 2.2 Configure Frontend Environment Variables

**Add via Vercel Dashboard or CLI:**
```bash
vercel env add REACT_APP_API_URL
# Enter: https://your-backend.railway.app

vercel env add REACT_APP_ENVIRONMENT  
# Enter: production
```

### 2.3 Verify Frontend Deployment
```bash
# Get deployment URL from vercel output
# Test frontend
curl https://your-app.vercel.app

# Test frontend → backend connection
# (Check browser console for API calls)
```

## ⚙️ Step 3: Production Configuration

### 3.1 Update Railway Environment Variables

After getting Vercel URL, update Railway:
```bash
railway variables:set FRONTEND_URL="https://your-actual-vercel-url.vercel.app"
```

### 3.2 Required Environment Variables

**Backend (Railway):**
```env
DATABASE_URL=${{RAILWAY_DATABASE_URL}}
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-secret-key  
ANTHROPIC_API_KEY=your-claude-api-key
FRONTEND_URL=https://your-frontend.vercel.app
ENVIRONMENT=production
```

**Frontend (Vercel):**
```env
REACT_APP_API_URL=https://your-backend.railway.app
REACT_APP_ENVIRONMENT=production
```

### 3.3 Security Considerations

- ✅ Use strong, unique secret keys
- ✅ Never commit API keys to repository
- ✅ Use environment-specific database URLs
- ✅ Enable HTTPS only in production
- ✅ Configure CORS for specific frontend domain

## 🧪 Step 4: Verify Deployment

### 4.1 Backend Health Checks
```bash
# Health endpoint
curl https://your-backend.railway.app/health
# Expected: {"status": "healthy", "database": "connected", ...}

# Config status
curl https://your-backend.railway.app/api/v1/config/status  
# Expected: All configurations should be true

# API documentation
curl https://your-backend.railway.app/docs
# Expected: FastAPI Swagger UI
```

### 4.2 Frontend Verification
```bash
# Frontend loads
curl -I https://your-frontend.vercel.app
# Expected: 200 OK

# API connectivity (check browser dev tools)
# Navigate to: https://your-frontend.vercel.app
# Check console for successful API calls
```

### 4.3 Integration Testing
1. **User Registration:** Create account via frontend
2. **Authentication:** Login/logout functionality  
3. **Resume Upload:** Upload PDF and parse
4. **Job Browsing:** View job listings
5. **Job Matching:** See match scores
6. **Save Jobs:** Save/unsave functionality

## 🚨 Troubleshooting

### Common Backend Issues

**Health Check Failing:**
```bash
# Check Railway logs
railway logs

# Verify database connection
railway connect

# Check environment variables
railway variables
```

**Database Connection Error:**
```bash
# Ensure PostgreSQL service is added
railway add postgresql

# Verify DATABASE_URL is set
railway variables:get DATABASE_URL
```

**CORS Errors:**
```bash
# Verify FRONTEND_URL is set correctly
railway variables:set FRONTEND_URL="https://your-exact-vercel-url.vercel.app"
```

### Common Frontend Issues

**API Connection Failed:**
```bash
# Check environment variables
vercel env ls

# Verify API URL is correct
vercel env get REACT_APP_API_URL

# Check browser developer console for CORS errors
```

**Build Failures:**
```bash
# Check build logs in Vercel dashboard
# Fix any TypeScript/ESLint errors
cd frontend
npm run build
```

## 📊 Expected Performance

### Backend (Railway)
- **Startup Time:** < 30 seconds
- **Health Check Response:** < 2 seconds
- **API Response Time:** < 500ms
- **Database Queries:** < 100ms

### Frontend (Vercel)
- **Build Time:** < 2 minutes
- **Page Load Speed:** < 3 seconds
- **Bundle Size:** ~100KB gzipped
- **Lighthouse Score:** 90+ Performance

## 🔐 Environment Variables Reference

### Railway Backend Variables
| Variable | Example | Required |
|----------|---------|----------|
| `DATABASE_URL` | `${{RAILWAY_DATABASE_URL}}` | ✅ |
| `SECRET_KEY` | `super-secret-production-key` | ✅ |
| `JWT_SECRET_KEY` | `jwt-secret-production-key` | ✅ |
| `ANTHROPIC_API_KEY` | `sk-ant-api-key` | ✅ |
| `FRONTEND_URL` | `https://app.vercel.app` | ✅ |
| `ENVIRONMENT` | `production` | ✅ |

### Vercel Frontend Variables  
| Variable | Example | Required |
|----------|---------|----------|
| `REACT_APP_API_URL` | `https://backend.railway.app` | ✅ |
| `REACT_APP_ENVIRONMENT` | `production` | ⚠️ |

## 🎯 Post-Deployment Tasks

1. **Monitor Logs:** Check Railway + Vercel logs
2. **Performance Testing:** Run load tests
3. **Security Scan:** Check for vulnerabilities
4. **User Testing:** Validate all features work
5. **Analytics Setup:** Configure monitoring
6. **Backup Strategy:** Database backup schedule
7. **CI/CD Pipeline:** Automate future deployments

## 📈 Scaling Considerations

### Railway Backend Scaling
- **Horizontal Scaling:** Railway auto-scales based on traffic
- **Database Scaling:** PostgreSQL can handle moderate load
- **Memory Usage:** Monitor for memory leaks
- **Background Jobs:** Consider Celery + Redis for heavy processing

### Vercel Frontend Scaling  
- **Global CDN:** Vercel provides automatic global distribution
- **Edge Functions:** For server-side rendering if needed
- **Build Optimization:** Code splitting and lazy loading

---

## 🚀 Quick Deploy Commands

**One-time setup:**
```bash
# Backend
cd backend
railway login
railway new ai-job-tracker-backend
railway add postgresql
railway up

# Frontend  
cd ../frontend
vercel login
vercel --prod
```

**Future deployments:**
```bash
# Backend
cd backend
railway up

# Frontend
cd ../frontend
vercel --prod
```

**Current Status:** Ready for production deployment! 🎉