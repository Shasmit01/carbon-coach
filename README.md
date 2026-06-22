# 🌍 AI Carbon Footprint Coach

A production-grade, **100% FREE** AI-powered platform that helps users track, understand, and reduce their carbon footprint using local LLMs and rule-based calculations.

**Monthly Cost: ₹0 (ZERO)** ✅

---

## 🎯 Project Overview

The AI Carbon Footprint Coach is a comprehensive web application that:

- **Tracks** user activities and calculates carbon emissions
- **Educates** users through AI-powered chatbot (local LLM)
- **Recommends** personalized reduction strategies
- **Gamifies** sustainability through goals and rewards
- **Analyzes** environmental impact with beautiful charts
- **Manages** emission factors through admin dashboard

---

## 📊 Cost Breakdown (Monthly: ₹0)

| Component | Solution | Cost |
|-----------|----------|------|
| **Frontend Hosting** | Vercel Free Tier | ₹0 |
| **Backend Hosting** | Render.com Free Tier | ₹0 |
| **Database** | Supabase Free Tier (500MB) | ₹0 |
| **File Storage** | Supabase Storage Free Tier | ₹0 |
| **AI Model** | Ollama (Self-Hosted Local) | ₹0 |
| **Email** | SMTP Gmail (Free) | ₹0 |
| **Authentication** | Supabase Auth Free Tier | ₹0 |
| **Analytics** | Self-Hosted | ₹0 |
| **Monitoring** | Open Source (Prometheus) | ₹0 |
| **Domain** | Freenom / Netlify Subdomain | ₹0 |
| **SSL Certificate** | Let's Encrypt (Free) | ₹0 |
| **TOTAL MONTHLY COST** | **₹0** | **₹0** |

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                      │
│  (React + TypeScript + Vite + Shadcn UI + Tailwind CSS)     │
│  - Dashboard                                                 │
│  - Activity Tracker                                          │
│  - AI Chatbot Interface                                      │
│  - Admin Dashboard                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│                    API GATEWAY LAYER                         │
│              (FastAPI + Python 3.11+)                        │
│  - Authentication & Authorization                           │
│  - Rate Limiting                                            │
│  - Request Validation                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼────┐  ┌──────▼──────┐  ┌──▼──────────┐
│  LLM API   │  │ Carbon API   │  │ Admin API   │
│ (Ollama    │  │ & Analytics │  │ (Users,     │
│  Local)    │  │             │  │  Settings)  │
└───────┬────┘  └──────┬──────┘  └──┬──────────┘
        │              │            │
        └──────────────┼────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              DATA & BUSINESS LOGIC LAYER                     │
│  - Emission Calculations                                    │
│  - User Management                                          │
│  - Goal Management                                          │
│  - Reward System                                            │
│  - Analytics Engine                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼────────────┐
        │              │            │
┌───────▼─────┐  ┌─────▼──────┐  ┌▼──────────┐
│ PostgreSQL  │  │  Supabase  │  │  Ollama   │
│  Database   │  │  Auth      │  │  Local    │
│             │  │  Storage   │  │  LLM      │
└─────────────┘  └────────────┘  └───────────┘
```

### Technology Stack

**Frontend:**
- React 18 + TypeScript
- Vite (Build Tool)
- Tailwind CSS (Styling)
- Shadcn UI (Component Library)
- Framer Motion (Animations)
- Recharts (Data Visualization)
- Zustand (State Management)
- Axios (HTTP Client)

**Backend:**
- FastAPI (Python Web Framework)
- Pydantic (Data Validation)
- SQLAlchemy (ORM)
- Alembic (Database Migrations)
- Python-Jose (JWT Authentication)
- Async PostgreSQL Driver
- Ollama Client

**Database:**
- PostgreSQL (Primary Database)
- Supabase (Managed PostgreSQL + Auth)

**AI/ML:**
- Ollama (Local LLM Engine)
- Gemma 3 / Llama 3 / DeepSeek (Models)

**Deployment:**
- Docker & Docker Compose
- Vercel (Frontend)
- Render.com (Backend)
- Supabase (Database)

**Monitoring & Logging:**
- Structured Logging (Python logging)
- Health Check Endpoints

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Ollama installed locally

### 1. Clone & Setup

```bash
# Navigate to project
cd carbon-coach

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Setup Local LLM (Ollama)

```bash
# Install Ollama from https://ollama.ai
# Then pull a model
ollama pull gemma:2b

# Start Ollama service
ollama serve
# Ollama runs on http://localhost:11434
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb carbon_coach

# Run migrations
cd backend
alembic upgrade head
```

### 4. Environment Variables

**Backend** (.env):
```env
DATABASE_URL=postgresql://user:password@localhost/carbon_coach
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
OLLAMA_API_URL=http://localhost:11434
JWT_SECRET=your-secret-key-change-this
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Frontend** (.env):
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_KEY=your-anon-key
```

### 5. Run Locally

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Ollama (if not already running)
ollama serve
```

Access at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
carbon-coach/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── emission_factor.py
│   │   │   ├── goal.py
│   │   │   └── analytics.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── emission_factor.py
│   │   │   └── analytics.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── activities.py
│   │   │   ├── chatbot.py
│   │   │   ├── analytics.py
│   │   │   ├── admin.py
│   │   │   └── health.py
│   │   ├── services/
│   │   │   ├── emission_calculator.py
│   │   │   ├── ollama_service.py
│   │   │   ├── user_service.py
│   │   │   └── analytics_service.py
│   │   ├── utils/
│   │   │   ├── jwt_handler.py
│   │   │   ├── email_service.py
│   │   │   └── validators.py
│   │   └── database.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_activities.py
│   │   ├── test_emissions.py
│   │   └── conftest.py
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              # Shadcn UI components
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── Stats.tsx
│   │   │   │   ├── Charts.tsx
│   │   │   │   └── ActivityCard.tsx
│   │   │   ├── chatbot/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   └── InputBox.tsx
│   │   │   ├── activities/
│   │   │   │   ├── ActivityForm.tsx
│   │   │   │   ├── ActivityList.tsx
│   │   │   │   └── ActivityStats.tsx
│   │   │   ├── goals/
│   │   │   │   ├── GoalForm.tsx
│   │   │   │   ├── GoalProgress.tsx
│   │   │   │   └── GoalList.tsx
│   │   │   ├── admin/
│   │   │   │   ├── AdminDashboard.tsx
│   │   │   │   ├── UserManagement.tsx
│   │   │   │   ├── EmissionFactors.tsx
│   │   │   │   ├── Analytics.tsx
│   │   │   │   └── Settings.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Admin.tsx
│   │   │   └── NotFound.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useActivities.ts
│   │   │   ├── useChatbot.ts
│   │   │   └── useAnalytics.ts
│   │   ├── store/
│   │   │   ├── authStore.ts
│   │   │   ├── activityStore.ts
│   │   │   ├── chatStore.ts
│   │   │   └── analyticsStore.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── activities.ts
│   │   │   ├── chatbot.ts
│   │   │   └── analytics.ts
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   ├── tailwind.css
│   │   │   └── animations.css
│   │   ├── types/
│   │   │   ├── index.ts
│   │   │   ├── auth.ts
│   │   │   ├── activity.ts
│   │   │   └── analytics.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── .env.example
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── package.json
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── API_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── OLLAMA_SETUP.md
│   ├── DEVELOPMENT.md
│   └── CONTRIBUTING.md
│
├── .gitignore
├── docker-compose.yml
└── .env.example
```

---

## 📚 Database Schema

### Core Tables

**users**
- id (UUID, PK)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- full_name (VARCHAR)
- avatar_url (TEXT)
- role (ENUM: user, admin)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**activities**
- id (UUID, PK)
- user_id (UUID, FK)
- activity_type (ENUM: transport, energy, food, waste, shopping)
- value (FLOAT)
- unit (VARCHAR)
- carbon_emissions (FLOAT)
- description (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**emission_factors**
- id (UUID, PK)
- category (VARCHAR)
- subcategory (VARCHAR)
- factor_value (FLOAT)
- unit (VARCHAR)
- source (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**goals**
- id (UUID, PK)
- user_id (UUID, FK)
- title (VARCHAR)
- target_reduction (FLOAT)
- deadline (DATE)
- status (ENUM: active, completed, failed)
- created_at (TIMESTAMP)

**rewards**
- id (UUID, PK)
- user_id (UUID, FK)
- earned_points (INTEGER)
- achievement (VARCHAR)
- created_at (TIMESTAMP)

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/me` - Get current user

### Activities
- `GET /api/activities` - List user activities
- `POST /api/activities` - Create activity
- `GET /api/activities/{id}` - Get activity
- `PUT /api/activities/{id}` - Update activity
- `DELETE /api/activities/{id}` - Delete activity
- `GET /api/activities/stats` - Get activity statistics

### Chatbot
- `POST /api/chatbot/chat` - Send message to AI coach
- `GET /api/chatbot/history` - Get chat history
- `DELETE /api/chatbot/history` - Clear chat history

### Analytics
- `GET /api/analytics/dashboard` - Dashboard data
- `GET /api/analytics/emissions/summary` - Emissions summary
- `GET /api/analytics/emissions/trends` - Emissions trends
- `GET /api/analytics/goals/progress` - Goals progress

### Admin
- `GET /api/admin/users` - List all users
- `GET /api/admin/users/{id}` - Get user details
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user
- `GET /api/admin/emission-factors` - List emission factors
- `POST /api/admin/emission-factors` - Create factor
- `PUT /api/admin/emission-factors/{id}` - Update factor
- `DELETE /api/admin/emission-factors/{id}` - Delete factor
- `GET /api/admin/analytics` - Global analytics
- `GET /api/admin/health` - System health

---

## 🤖 AI Chatbot Features

The AI Chatbot uses **Ollama** (100% free, runs locally) to provide:

1. **Carbon Footprint Advice** - Personalized recommendations
2. **Educational Content** - Sustainability tips
3. **Goal Setting** - Help users set reduction goals
4. **Progress Analysis** - Review user's emission trends
5. **Quick Tips** - Daily sustainability suggestions
6. **FAQs** - Common sustainability questions

### Chatbot Capabilities
- Natural language conversation
- Context-aware responses
- Multi-language support (optional)
- Offline operation (no API calls needed)
- Fast inference (~1-2 seconds)

---

## 🎨 UI Theme

Premium sustainability design matching PPT specifications:

**Color Palette:**
```css
--primary: #0F6D3B      (Deep Green)
--secondary: #2BAE66    (Vibrant Green)
--accent: #8BC34A       (Light Green)
--background: #F5FFF6   (Off-White)
--text-dark: #1F2937    (Dark Gray)
--text-light: #6B7280   (Medium Gray)
--success: #10B981
--warning: #F59E0B
--error: #EF4444
```

**Design Features:**
- Glassmorphism panels
- Smooth animations (Framer Motion)
- Responsive grid layouts
- Beautiful data visualizations (Recharts)
- Dark mode support
- Accessibility compliance (WCAG 2.1 AA)

---

## 🐳 Docker Setup

### Local Development

```bash
docker-compose up
```

### Production Deployment

```bash
docker-compose -f docker/docker-compose.prod.yml up
```

---

## 🚀 Deployment Guide

### Frontend (Vercel - FREE)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from frontend directory
cd frontend
vercel
```

### Backend (Render.com - FREE)

1. Push code to GitHub
2. Connect repository to Render.com
3. Set environment variables
4. Deploy

### Database (Supabase - FREE)

1. Create free account at supabase.com
2. Create new project
3. Note PostgreSQL connection URL
4. Run migrations
5. Get API keys for frontend

---

## 📖 Documentation Files

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Detailed system architecture
- **[DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)** - Complete DB schema
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - API reference
- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Step-by-step setup
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[OLLAMA_SETUP.md](docs/OLLAMA_SETUP.md)** - Local LLM setup
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Development guidelines

---

## ✅ Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Ollama model downloaded and tested
- [ ] Frontend build optimized
- [ ] Backend tests passing
- [ ] Authentication configured
- [ ] Email notifications tested
- [ ] Analytics data collection enabled
- [ ] Error logging configured
- [ ] SSL certificate configured
- [ ] Rate limiting enabled
- [ ] CORS configured properly
- [ ] Database backups scheduled
- [ ] Monitoring alerts set up
- [ ] Documentation completed

---

## 🐛 Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql postgresql://user:password@localhost/carbon_coach

# Check connection URL in .env
```

### Frontend API Connection
```bash
# Check CORS configuration in backend
# Verify VITE_API_URL in frontend .env
# Check network requests in browser DevTools
```

---

## 📝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🤝 Support

For issues, questions, or suggestions:
- Create GitHub Issue
- Check existing documentation
- Review API docs at `/docs`

---

## ⭐ Acknowledgments

- **Ollama** - Local LLM inference
- **FastAPI** - Python web framework
- **React** - UI framework
- **Supabase** - Backend-as-a-service
- **Vercel** - Frontend hosting
- **Render** - Backend hosting

---

**Made with ❤️ for sustainable future**

**Monthly Cost: ₹0** ✅
