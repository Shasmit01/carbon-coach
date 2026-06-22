# Deployment Instructions - Carbon Coach

## Step-by-Step Deployment Guide

### 1️⃣ Frontend Deployment on Vercel (5 minutes)

**Prerequisites:**
- Vercel account (free at https://vercel.com)

**Steps:**
```bash
# Install Vercel CLI
npm i -g vercel

# From project root, deploy frontend
cd d:\hackathon 12\carbon-coach
vercel --prod
```

**During Vercel Setup:**
- Choose "Scope": Create team (or use existing)
- Link to existing project: No
- Project name: `carbon-coach`
- Framework: `Vite`
- Root directory: `./frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Environment Variables:
  - Key: `VITE_API_URL`
  - Value: `https://carbon-coach-backend.onrender.com` (we'll set backend first)

---

### 2️⃣ Backend Deployment on Render.com (10 minutes)

**Prerequisites:**
- Render account (free at https://render.com)
- GitHub account (we'll push code there)

**Steps:**

#### Step 2a: Push to GitHub
```bash
# Initialize git
cd d:\hackathon 12\carbon-coach
git init
git add .
git commit -m "Initial commit - Carbon Coach App"

# Create GitHub repo at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/carbon-coach.git
git branch -M main
git push -u origin main
```

#### Step 2b: Deploy Backend on Render
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select `carbon-coach` repo
4. Fill in details:
   - **Name**: `carbon-coach-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Add Environment Variables:
   ```
   ENVIRONMENT=production
   DATABASE_URL=postgresql://... (from Supabase below)
   JWT_SECRET=(generate random secret)
   DEBUG=False
   OLLAMA_API_URL=http://localhost:11434
   ```
6. Click "Create Web Service"
7. Wait for deployment (~3-5 min)
8. Copy the URL: `https://carbon-coach-backend.onrender.com`

---

### 3️⃣ Database Setup on Supabase (5 minutes)

**Prerequisites:**
- Supabase account (free at https://supabase.com)

**Steps:**
1. Go to https://app.supabase.com
2. Click "New Project"
3. Fill in:
   - **Project name**: `carbon-coach`
   - **Database password**: Generate strong password
   - **Region**: Choose closest to you
4. Wait for database creation (~2 min)
5. Go to "Settings" → "Database" → "Connection Pooling"
6. Copy the connection string:
   ```
   postgresql://postgres:[PASSWORD]@[HOST]:6543/postgres?sslmode=require
   ```
7. Update on Render:
   - Add env var `DATABASE_URL` with the connection string

---

### 4️⃣ Update Frontend Environment (2 minutes)

1. In Vercel Dashboard for your project
2. Go to "Settings" → "Environment Variables"
3. Add:
   - Key: `VITE_API_URL`
   - Value: `https://carbon-coach-backend.onrender.com`
   - Select: Production
4. Trigger new deployment

---

## ✅ Your App is Live!

| Component | URL |
|-----------|-----|
| **Frontend** | `https://carbon-coach.vercel.app` |
| **Backend API** | `https://carbon-coach-backend.onrender.com` |
| **API Docs** | `https://carbon-coach-backend.onrender.com/docs` |
| **Database** | Supabase PostgreSQL |

---

## 📝 Post-Deployment Checklist

- [ ] Test frontend: Visit https://carbon-coach.vercel.app
- [ ] Test API: Visit https://carbon-coach-backend.onrender.com/docs
- [ ] Try registering a new user
- [ ] Test activity tracking
- [ ] Check database via Supabase dashboard

---

## 🔄 Making Updates After Deployment

```bash
# After making changes locally:
git add .
git commit -m "Update description"
git push origin main

# Render & Vercel auto-deploy on push!
```

---

## 💡 Troubleshooting

**Backend won't start:**
- Check logs on Render dashboard
- Verify DATABASE_URL env var is set correctly
- Check Supabase database is running

**Frontend won't connect to API:**
- Ensure VITE_API_URL is set correctly in Vercel
- Verify backend is running on Render
- Check CORS settings in backend/app/main.py

**Database connection fails:**
- Verify connection string format
- Check Supabase IP whitelist (should be empty for free tier)
- Ensure database user password is correct

---

## 🎉 Total Deployment Time: ~20 minutes
