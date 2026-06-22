# 🚀 CARBON COACH - DEPLOYMENT GUIDE (Option 1 - Direct Deployment)

**Total Time: ~25 minutes | Cost: ₹0/month forever ✅**

---

## 📋 What You Need:

1. **GitHub Account** (free at https://github.com)
2. **Supabase Account** (free at https://supabase.com)
3. **Render Account** (free at https://render.com)
4. **Vercel Account** (free at https://vercel.com)

---

## 🔧 PRE-DEPLOYMENT SETUP (2 minutes)

### Git Commands to Run:

Open PowerShell in `d:\hackathon 12\carbon-coach` and run:

```powershell
# Check git is initialized
git status

# Stage all files
git add .

# First commit
git commit -m "Initial commit - Carbon Coach hackathon project"

# Verify
git log --oneline
```

Expected output:
```
✅ On branch master
✅ nothing to commit, working tree clean
✅ Shows 1 commit in log
```

---

## 🌐 STEP 1: GitHub Setup (2 minutes)

### 1.1 Create GitHub Account (if needed)
- Go to: https://github.com/signup
- Fill in: username, email, password
- Verify email
- Done! ✅

### 1.2 Create New Repository
- Go to: https://github.com/new
- **Repository name**: `carbon-coach`
- **Description**: "AI-powered carbon footprint tracking app"
- **Visibility**: Public (or Private)
- Click: **Create repository**
- Copy the URL shown: `https://github.com/YOUR_USERNAME/carbon-coach.git`

### 1.3 Push Code to GitHub

In PowerShell at `d:\hackathon 12\carbon-coach`, run:

```powershell
# Add remote (replace YOUR_USERNAME and URL)
git remote add origin https://github.com/YOUR_USERNAME/carbon-coach.git

# Rename branch to main
git branch -M main

# Push code
git push -u origin main
```

Expected output:
```
✅ Enumerating objects...
✅ Delta compression...
✅ ... [new branch] main → origin/main
```

---

## 💾 STEP 2: Database Setup on Supabase (5 minutes)

### 2.1 Create Supabase Account
- Go to: https://supabase.com
- Click: **Start your project**
- Sign up with GitHub (easiest)
- Create organization

### 2.2 Create Database Project
1. Click: **New Project**
2. Fill in:
   - **Project name**: `carbon-coach`
   - **Database password**: `GenerateStrongPassword123!`
   - **Region**: Pick closest to your location
3. Click: **Create new project**
4. ⏳ Wait 2-3 minutes for creation

### 2.3 Get Connection String
1. Go to: **Settings** → **Database** (left sidebar)
2. Scroll to: **Connection Pooling**
3. Copy the connection string that looks like:
   ```
   postgresql://postgres:PASSWORD@db.XXXXX.supabase.co:6543/postgres?sslmode=require
   ```
4. **Save this somewhere!** You'll need it in Step 3 ⬇️

---

## 🚀 STEP 3: Deploy Backend on Render.com (10 minutes)

### 3.1 Create Render Account
- Go to: https://render.com
- Click: **Get Started**
- Sign up with GitHub (paste your GitHub email)

### 3.2 Create Web Service
1. Dashboard → Click: **New +**
2. Select: **Web Service**
3. **Connect GitHub**
   - Click: **Connect account**
   - Authorize Render to access GitHub
   - Select repository: `carbon-coach`
   - Click: **Connect**

### 3.3 Configure Deployment
Fill in the following fields:

```
Name:                 carbon-coach-backend
Environment:          Python 3
Build Command:        pip install -r backend/requirements.txt
Start Command:        cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
Plan:                 Free
Region:               (pick closest)
```

### 3.4 Add Environment Variables
Click: **Advanced** → **Add Environment Variable**

Add these variables one by one:

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | `production` |
| `DATABASE_URL` | (Paste from Supabase Step 2.3) |
| `JWT_SECRET` | `your-super-secret-key-change-this-123456` |
| `DEBUG` | `False` |
| `CORS_ORIGINS` | `["https://carbon-coach-XXXX.vercel.app"]` |
| `OLLAMA_API_URL` | `http://localhost:11434` |

**Note:** Update CORS_ORIGINS later with actual Vercel URL

### 3.5 Deploy
1. Click: **Create Web Service**
2. ⏳ Wait 3-5 minutes for deployment
3. When done, you'll see: **Live** ✅
4. **Copy your backend URL**: `https://carbon-coach-backend.onrender.com`
5. ⬇️ You'll need this for Vercel in Step 4

---

## 🎨 STEP 4: Deploy Frontend on Vercel (5 minutes)

### 4.1 Create Vercel Account
- Go to: https://vercel.com
- Click: **Sign Up**
- Sign up with GitHub (easiest)

### 4.2 Import Project
1. Dashboard → Click: **Add New** → **Project**
2. Click: **Continue with GitHub**
3. Find: `carbon-coach` repo
4. Click: **Import**

### 4.3 Configure Build Settings
Vercel auto-detects, but verify:

```
Framework:           Vite
Root Directory:      ./frontend
Build Command:       npm run build
Output Directory:    dist
```

### 4.4 Add Environment Variables
Before deploying, click: **Environment Variables**

Add:
| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://carbon-coach-backend.onrender.com` |

### 4.5 Deploy
1. Click: **Deploy**
2. ⏳ Wait 1-2 minutes
3. When done, you'll see: **Ready** ✅
4. **Copy your frontend URL**: `https://carbon-coach-XXXX.vercel.app`

---

## 🧪 STEP 5: Test Your Deployment (3 minutes)

### 5.1 Test Frontend
1. Open: `https://carbon-coach-XXXX.vercel.app`
2. Should see the Carbon Coach login page ✅
3. Try to register a new account

### 5.2 Test Backend API
1. Open: `https://carbon-coach-backend.onrender.com/docs`
2. Should see **Swagger UI** with API endpoints ✅
3. Try the health check: `GET /health`

### 5.3 Test Database Connection
1. Login with your Supabase account
2. Check: **SQL Editor**
3. Should see tables: `users`, `activities`, `goals`, etc. ✅

---

## ✅ YOU'RE LIVE! 🎉

Your app is now deployed and accessible worldwide!

| Component | URL |
|-----------|-----|
| **Frontend** | `https://carbon-coach-XXXX.vercel.app` |
| **Backend API** | `https://carbon-coach-backend.onrender.com` |
| **API Documentation** | `https://carbon-coach-backend.onrender.com/docs` |
| **Database Dashboard** | `https://app.supabase.com` |

**Share your live link with friends! 🌍**

---

## 🔄 Making Changes (Auto-Deploy)

After deployment, any changes you push to GitHub automatically deploy!

### Local Development:
```powershell
# Make changes
git add .
git commit -m "Feature description"
git push origin main

# Your changes are live in 2-3 minutes! ✅
```

---

## 📊 Deployment Architecture

```
Your GitHub Repo
      ↓
   (push)
   ↙   ↘
Render    Vercel      Supabase
(Backend) (Frontend)  (Database)
  ↓         ↓           ↓
https://carbon-coach-backend.onrender.com
https://carbon-coach-XXXX.vercel.app
(Connected automatically with DATABASE_URL & VITE_API_URL)
```

---

## 💰 Monthly Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Vercel** | 100 GB bandwidth/month | ₹0 |
| **Render** | 750 hours/month (auto-sleep) | ₹0 |
| **Supabase** | 500 MB database | ₹0 |
| **Total** | **Everything included** | **₹0** |

---

## 🆘 Troubleshooting

### Backend won't start
```
Error: "Connection refused"
→ Check DATABASE_URL env var on Render
→ Verify Supabase database is running
→ Check Render deployment logs
```

### Frontend can't connect to API
```
Error: "API request failed"
→ Check VITE_API_URL is set in Vercel
→ Verify backend URL doesn't end with "/"
→ Wait 2 min after backend restart
```

### 504 Error on Render
```
Solution: Backend is waking up (free tier auto-sleeps)
→ Wait 30 seconds and refresh
→ First request always slow on free tier
```

---

## 📱 Share Your App!

Once live, share the link:
- **For others to use**: `https://carbon-coach-XXXX.vercel.app`
- **For developers**: Point to GitHub repo: `https://github.com/YOUR_USERNAME/carbon-coach`

---

## 🎓 What You Just Did

1. ✅ Set up version control (Git)
2. ✅ Hosted code on GitHub
3. ✅ Deployed backend API to Render
4. ✅ Deployed frontend to Vercel
5. ✅ Set up production database on Supabase
6. ✅ Configured auto-deployment pipelines
7. ✅ Created a live production app

**You're now a DevOps engineer! 🚀**

---

## 📞 Need Help?

| Issue | Solution |
|-------|----------|
| GitHub push fails | Run `git remote -v` to verify remote URL |
| Supabase connection fails | Check password doesn't have `@` unencoded |
| Render won't deploy | Check build log in Render dashboard |
| Vercel shows 404 | Check root directory is `./frontend` |

---

**Congratulations! Your app is live on the internet! 🌍✨**
