#!/usr/bin/env python3
"""
Automated Deployment Setup for Carbon Coach
Handles all cloud service configuration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class DeploymentSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config = {}
    
    def check_git(self):
        """Verify git is configured"""
        print("🔍 Checking Git configuration...")
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            print(f"✅ {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"❌ Git not found: {e}")
            return False
    
    def verify_github(self):
        """Verify GitHub repo is set up"""
        print("\n🔍 Checking GitHub repository...")
        try:
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, cwd=self.project_root)
            if 'github.com' in result.stdout:
                print("✅ GitHub repository connected")
                print(result.stdout)
                return True
            else:
                print("⚠️  No GitHub remote found")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def check_requirements(self):
        """Verify all requirements are met"""
        print("\n📋 Checking Requirements...")
        
        checks = {
            "Git": self.check_git(),
            "GitHub": self.verify_github(),
            "Frontend package.json": (self.project_root / "frontend" / "package.json").exists(),
            "Backend requirements.txt": (self.project_root / "backend" / "requirements.txt").exists(),
        }
        
        print("\n📊 Requirements Status:")
        for check, status in checks.items():
            symbol = "✅" if status else "❌"
            print(f"  {symbol} {check}")
        
        return all(checks.values())
    
    def display_deployment_guide(self):
        """Display next steps"""
        print("\n" + "="*60)
        print("🚀 CARBON COACH - DEPLOYMENT NEXT STEPS")
        print("="*60)
        
        steps = """
1️⃣  DATABASE SETUP (Supabase) - 5 minutes
   • Go to: https://supabase.com
   • Create new project "carbon-coach"
   • Get connection string from Settings > Database
   • Save: DATABASE_URL environment variable

2️⃣  BACKEND DEPLOYMENT (Render) - 10 minutes
   • Go to: https://render.com
   • New Web Service
   • Connect your GitHub repo: Shasmit01/carbon-coach
   • Configure:
     - Name: carbon-coach-backend
     - Runtime: Python 3
     - Build: pip install -r backend/requirements.txt
     - Start: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   • Add Environment Variables (from .env.example)
   • Deploy!

3️⃣  FRONTEND DEPLOYMENT (Vercel) - 5 minutes
   • Go to: https://vercel.com
   • Import project from GitHub
   • Select repository: Shasmit01/carbon-coach
   • Framework: Vite
   • Root Directory: ./frontend
   • Add Environment Variables:
     - VITE_API_URL=<your-render-backend-url>
   • Deploy!

4️⃣  CONFIGURE AUTO-DEPLOYMENT
   • Add GitHub Secrets:
     - RENDER_API_KEY (from Render account)
     - RENDER_SERVICE_ID (from Render dashboard)
     - VERCEL_TOKEN (from Vercel account)
   • Push to GitHub and workflows auto-run!

✅ YOUR APP WILL BE LIVE!
   Frontend: https://carbon-coach-XXXX.vercel.app
   Backend:  https://carbon-coach-backend.onrender.com
   Docs:     https://carbon-coach-backend.onrender.com/docs
"""
        print(steps)
    
    def create_deployment_summary(self):
        """Create deployment summary file"""
        summary = {
            "project": "Carbon Coach",
            "status": "Ready for Deployment",
            "github_repo": "https://github.com/Shasmit01/carbon-coach",
            "services": {
                "frontend": {
                    "platform": "Vercel",
                    "framework": "React + Vite",
                    "url": "https://vercel.com/import"
                },
                "backend": {
                    "platform": "Render",
                    "framework": "FastAPI + Python 3.11",
                    "url": "https://render.com"
                },
                "database": {
                    "platform": "Supabase",
                    "type": "PostgreSQL",
                    "url": "https://supabase.com"
                }
            },
            "estimated_time": "20-25 minutes",
            "cost": "₹0/month"
        }
        
        summary_path = self.project_root / "DEPLOYMENT_STATUS.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Deployment summary saved to: DEPLOYMENT_STATUS.json")
        return summary
    
    def run(self):
        """Run complete setup"""
        print("\n" + "="*60)
        print("🚀 CARBON COACH - AUTOMATED DEPLOYMENT SETUP")
        print("="*60 + "\n")
        
        if self.check_requirements():
            print("\n✅ All requirements met!")
            self.create_deployment_summary()
            self.display_deployment_guide()
        else:
            print("\n❌ Some requirements are missing")
            print("Please resolve issues above and try again")
            sys.exit(1)

if __name__ == "__main__":
    setup = DeploymentSetup()
    setup.run()
