# 🚀 Carbon Coach - Deployment Summary

## Your Deployment Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    CARBON COACH DEPLOYMENT                       │
└─────────────────────────────────────────────────────────────────┘

Frontend Layer                Backend Layer              Database Layer
┌──────────────────┐         ┌──────────────────┐       ┌──────────────┐
│  React + Vite    │         │  FastAPI         │       │  PostgreSQL  │
│  (TypeScript)    │◄────────│  (Python 3.11)   │◄──────│  (Supabase)  │
│                  │         │                  │       │              │
│  Vercel.app      │         │  Render.com      │       │  Free 500MB  │
│  (Free Tier)     │         │  (Free Tier)     │       │              │
└──────────────────┘         └──────────────────┘       └──────────────┘
       ↓                            ↓                           ↓
  Auto-deploys              Auto-deploys                   Managed
  on GitHub push            on GitHub push
```

---

## ⚡ Quick Start Deployment (25 minutes)

### Step 1: GitHub Setup (2 min)

```bash
cd d:\hackathon 12\carbon-coach

# Initialize git
git init
git add .
git commit -m "Initial commit - Carbon Coach App"

# Create repo at https://github.com/new (name: carbon-coach)

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/carbon-coach.git
git branch -M main
git push -u origin main
```

---

### Step 2: Database (Supabase) - 5 min

1. **Create Account**: https://supabase.com (Free)
2. **New Project**:
   - Name: `carbon-coach`
   - Password: Generate strong one
   - Region: Pick closest to you
3. **Get Connection String**:
   - Settings → Database → Connection Pooling
   - Copy: `postgresql://postgres:PASSWORD@host:6543/postgres?sslmode=require`
   - Save this! ⬇️

---

### Step 3: Backend (Render.com) - 10 min

1. **Create Account**: https://render.com (Free)
2. **New Web Service**:
   - Connect GitHub
   - Select: `carbon-coach` repo
   
3. **Configure**:
   ```
   Name:           carbon-coach-backend
   Environment:    Python 3
   Build Command:  pip install -r backend/requirements.txt
   Start Command:  cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan:           Free
   ```

4. **Environment Variables**:
   ```
   ENVIRONMENT           = production
   DATABASE_URL          = (paste from Supabase step)
   JWT_SECRET            = generate-random-key-here
   DEBUG                 = False
   CORS_ORIGINS          = ["https://carbon-coach.vercel.app"]
   ```

5. **Deploy** → Wait 3-5 min
6. **Get URL**: Copy the deployed URL (e.g., `https://carbon-coach-backend.onrender.com`)

---

### Step 4: Frontend (Vercel) - 5 min

1. **Create Account**: https://vercel.com (Free)
2. **Import Project**:
   - Connect GitHub
   - Select: `carbon-coach` repo
   
3. **Configure**:
   ```
   Framework:         Vite
   Root Directory:    ./frontend
   Build Command:     npm run build
   Output Directory:  dist
   ```

4. **Environment Variables**:
   ```
   VITE_API_URL = https://carbon-coach-backend.onrender.com
   ```

5. **Deploy** → Instant
6. **Get URL**: Your frontend is live at `https://carbon-coach-XXXX.vercel.app`

---

## ✅ You're Live!

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | `https://carbon-coach-XXXX.vercel.app` | ✅ Live |
| **Backend API** | `https://carbon-coach-backend.onrender.com` | ✅ Live |
| **API Docs** | `https://carbon-coach-backend.onrender.com/docs` | ✅ Live |
| **Database** | Supabase PostgreSQL | ✅ Live |

---

## 🔄 Making Updates

After deployment, any push to GitHub auto-deploys to both Vercel and Render!

```bash
# Make changes locally
git add .
git commit -m "Feature description"
git push origin main

# Automatically deploys to production! 🎉
```

---

## 🆘 Troubleshooting

### Backend won't start
- [ ] Check DATABASE_URL is correct in Render settings
- [ ] Verify Supabase database is running
- [ ] Check Render build logs for errors

### Frontend can't connect to API
- [ ] Verify VITE_API_URL is set in Vercel
- [ ] Ensure backend URL ends WITHOUT `/`
- [ ] Wait 1-2 min after backend deploy

### Database connection timeout
- [ ] Verify connection string format
- [ ] Check password doesn't have special chars (or URL encode them)
- [ ] Ensure Supabase project is running

---

## 📊 Total Cost: ₹0/month

- **Vercel**: Free tier (up to 100 GB bandwidth)
- **Render**: Free tier (auto-sleep after 15 min inactivity)
- **Supabase**: Free tier (500 MB database)
- **Total**: **₹0 forever** ✅

---

## 🎯 Next Steps

1. ✅ Deploy using steps above
2. ✅ Test the live app
3. ✅ Share the link with friends: `https://carbon-coach-XXXX.vercel.app`
4. 📈 Monitor at Render/Vercel dashboards
5. 🚀 Add features and auto-deploy!

---

**Happy Deploying! 🚀**
