# 📌 DEPLOYMENT QUICK REFERENCE

## 🎯 5-Step Deployment Checklist (25 min total)

```
[ ] Step 1: GitHub Setup (2 min)
    → Create repo at https://github.com/new
    → Run: git remote add origin <URL>
    → Run: git push -u origin main
    
[ ] Step 2: Database (5 min)
    → Create Supabase project at https://supabase.com
    → Copy connection string (CONNECTION_STRING)
    
[ ] Step 3: Backend (10 min)
    → New Web Service at https://render.com
    → Connect GitHub repo
    → Start command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    → Add env: DATABASE_URL=CONNECTION_STRING
    → Get backend URL (BACKEND_URL)
    
[ ] Step 4: Frontend (5 min)
    → Import project at https://vercel.com
    → Add env: VITE_API_URL=BACKEND_URL
    → Get frontend URL (FRONTEND_URL)
    
[ ] Step 5: Test (3 min)
    → Visit FRONTEND_URL
    → Visit BACKEND_URL/docs
```

---

## 🔗 Important Links

| Action | URL |
|--------|-----|
| Create GitHub account | https://github.com/signup |
| New GitHub repo | https://github.com/new |
| Supabase dashboard | https://supabase.com |
| Render dashboard | https://render.com |
| Vercel dashboard | https://vercel.com |
| GitHub settings | https://github.com/settings |

---

## 💻 Git Commands

```powershell
# From: d:\hackathon 12\carbon-coach

# Initialize (if not done)
git init

# Stage all files
git add .

# Commit
git commit -m "Initial commit - Carbon Coach"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/carbon-coach.git

# Push to main
git branch -M main
git push -u origin main

# After deployment, any changes auto-deploy:
git add .
git commit -m "Your change description"
git push origin main
```

---

## 📝 Environment Variables

### Backend (Render)
```
ENVIRONMENT=production
DATABASE_URL=postgresql://postgres:PASSWORD@db.XXXXX.supabase.co:5432/postgres?sslmode=require
JWT_SECRET=your-secret-key-123456
DEBUG=False
CORS_ORIGINS=["https://carbon-coach-XXXX.vercel.app"]
OLLAMA_API_URL=http://localhost:11434
```

### Frontend (Vercel)
```
VITE_API_URL=https://carbon-coach-backend.onrender.com
```

---

## 🏗️ Build/Start Commands

### Backend
- **Build**: `pip install -r backend/requirements.txt`
- **Start**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend
- **Build**: `npm run build`
- **Root**: `./frontend`
- **Output**: `dist`

---

## ✅ Live URLs (After Deployment)

```
Frontend:       https://carbon-coach-XXXX.vercel.app
Backend API:    https://carbon-coach-backend.onrender.com
API Docs:       https://carbon-coach-backend.onrender.com/docs
Database:       https://app.supabase.com (your project)
GitHub Repo:    https://github.com/YOUR_USERNAME/carbon-coach
```

---

## 🧪 Testing

| Test | URL |
|------|-----|
| Frontend loads | Visit `FRONTEND_URL` |
| API works | Visit `BACKEND_URL/docs` |
| DB connected | Check Supabase dashboard |
| Health check | `GET BACKEND_URL/health` |

---

## 🚨 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `fatal: remote origin already exists` | Remote already added | Run `git remote -v` to check |
| `Connection refused` (backend) | DB not connected | Verify DATABASE_URL in Render |
| `CORS error` in frontend | Wrong API URL | Check VITE_API_URL in Vercel |
| `504 Gateway Timeout` | Backend sleeping | Wait 30s, first request wakes it |
| `404 on frontend` | Wrong root directory | Set to `./frontend` in Vercel |

---

## ⏱️ Deployment Timeline

| Step | Time | Status |
|------|------|--------|
| GitHub setup | 2 min | Quick |
| Supabase setup | 5 min | Requires wait |
| Render deploy | 10 min | Longest |
| Vercel deploy | 5 min | Quick |
| Testing | 3 min | Verify |
| **TOTAL** | **~25 min** | **Done!** |

---

## 📊 Your Deployment Stack

```
┌─────────────────────────────────────────┐
│      🌐 Frontend (Vercel)                │
│  React + Vite + Tailwind CSS             │
│  Auto-deploys on GitHub push             │
└──────────────┬──────────────────────────┘
               │ HTTPS
┌──────────────▼──────────────────────────┐
│      🖥️ Backend (Render)                 │
│  FastAPI + Python 3.11                   │
│  Auto-deploys on GitHub push             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     💾 Database (Supabase)               │
│  PostgreSQL + 500MB Free Storage         │
│  Managed, automatic backups              │
└──────────────────────────────────────────┘
```

---

## 🎯 Success Indicators

After deployment, you should see:

```
✅ Frontend loads without errors
✅ API docs available at /docs
✅ Can create user account
✅ Can track activities
✅ Dashboard loads with data
✅ Database tables populated
✅ No CORS errors in console
✅ Backend URL accessible from anywhere
```

---

## 📞 Support Resources

- **Render Support**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **GitHub Help**: https://docs.github.com

---

**You've got this! 🚀**
