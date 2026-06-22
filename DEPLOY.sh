#!/bin/bash
# Quick Deployment Setup Script for Carbon Coach

echo "🚀 Carbon Coach - Deployment Setup"
echo "===================================="
echo ""

# Step 1: Initialize Git
echo "Step 1: Initializing Git repository..."
git init
git add .
git commit -m "Initial commit - Carbon Coach App"
echo "✅ Git initialized"
echo ""

# Step 2: Create .gitignore if not exists
echo "Step 2: Setting up .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Frontend
node_modules/
dist/
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
carbon_coach.db

# OS
.DS_Store
Thumbs.db
EOF
echo "✅ .gitignore created"
echo ""

echo "📋 DEPLOYMENT CHECKLIST:"
echo "========================"
echo ""
echo "1️⃣  GITHUB SETUP (2 min):"
echo "   [ ] Create GitHub account: https://github.com"
echo "   [ ] Create new repository: https://github.com/new"
echo "   [ ] Name it: carbon-coach"
echo "   [ ] Push code:"
echo "       git remote add origin https://github.com/YOUR_USERNAME/carbon-coach.git"
echo "       git branch -M main"
echo "       git push -u origin main"
echo ""

echo "2️⃣  SUPABASE DATABASE (5 min):"
echo "   [ ] Create Supabase account: https://supabase.com"
echo "   [ ] New project → carbon-coach"
echo "   [ ] Copy connection string from Settings > Database"
echo "   [ ] Save it: postgresql://postgres:PASSWORD@host:5432/postgres"
echo ""

echo "3️⃣  BACKEND DEPLOYMENT (10 min):"
echo "   [ ] Create Render account: https://render.com"
echo "   [ ] New Web Service"
echo "   [ ] Connect GitHub repo: carbon-coach"
echo "   [ ] Settings:"
echo "       - Name: carbon-coach-backend"
echo "       - Runtime: Python 3"
echo "       - Build: pip install -r backend/requirements.txt"
echo "       - Start: cd backend && uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "   [ ] Environment Variables (copy from .env.example):"
echo "       - ENVIRONMENT=production"
echo "       - DATABASE_URL=<from Supabase>"
echo "       - JWT_SECRET=<generate random>"
echo "       - DEBUG=False"
echo "   [ ] Deploy"
echo "   [ ] Copy your backend URL (e.g., https://carbon-coach-backend.onrender.com)"
echo ""

echo "4️⃣  FRONTEND DEPLOYMENT (5 min):"
echo "   [ ] Create Vercel account: https://vercel.com"
echo "   [ ] New Project"
echo "   [ ] Import GitHub repository: carbon-coach"
echo "   [ ] Settings:"
echo "       - Framework: Vite"
echo "       - Root Directory: ./frontend"
echo "       - Build Command: npm run build"
echo "       - Output Directory: dist"
echo "   [ ] Environment Variables:"
echo "       - VITE_API_URL=<your-backend-url>"
echo "   [ ] Deploy"
echo "   [ ] Copy your frontend URL (e.g., https://carbon-coach.vercel.app)"
echo ""

echo "5️⃣  VERIFICATION (3 min):"
echo "   [ ] Open frontend: https://carbon-coach.vercel.app"
echo "   [ ] Test API: https://carbon-coach-backend.onrender.com/docs"
echo "   [ ] Create account and test features"
echo ""

echo "✨ Total time: ~25 minutes"
echo ""
echo "Need help? Check DEPLOYMENT.md for detailed instructions"
