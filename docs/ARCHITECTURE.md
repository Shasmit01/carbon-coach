# AI Carbon Footprint Coach - Architecture Documentation

## 🏗️ System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                      │
│  React App (Vite) → Deployed on Vercel (FREE)              │
│  - Dashboard UI                                              │
│  - Activity Tracker                                          │
│  - AI Chatbot UI                                             │
│  - Admin Panel                                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS / WSS
                       │ (Stateless API Calls)
┌──────────────────────▼──────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  FastAPI Server → Deployed on Render.com (FREE)            │
│  - Request Routing & Validation                             │
│  - Authentication & Authorization                           │
│  - Business Logic                                           │
│  - Rate Limiting & Security                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼─────────┐ ┌▼──────────────┐
│   DATABASE   │ │  OLLAMA LLM   │ │  FILE STORAGE │
│ Supabase     │ │   (Local)     │ │  Supabase     │
│ PostgreSQL   │ │               │ │  (Free Tier)  │
└──────────────┘ └───────────────┘ └───────────────┘
```

---

## 🔄 Component Architecture

### 1. Frontend Architecture (React)

```
Frontend/
├── Pages (Route-based)
│   ├── Home.tsx (Landing)
│   ├── Login.tsx (Authentication)
│   ├── Dashboard.tsx (Main App)
│   ├── Admin.tsx (Admin Dashboard)
│   └── NotFound.tsx
│
├── Components (Reusable UI)
│   ├── Layout/ (Navigation, Sidebar)
│   ├── Dashboard/ (Stats, Charts, Cards)
│   ├── Activities/ (Forms, Lists)
│   ├── Chatbot/ (Chat UI)
│   ├── Goals/ (Goal Management)
│   └── Admin/ (Admin Panels)
│
├── Hooks (State & Logic)
│   ├── useAuth() - Authentication state
│   ├── useActivities() - Activity data
│   ├── useChatbot() - Chat state
│   └── useAnalytics() - Analytics data
│
├── Store (Zustand State)
│   ├── authStore - User & tokens
│   ├── activityStore - Activities data
│   ├── chatStore - Chat history
│   └── analyticsStore - Analytics state
│
└── Services (API Communication)
    ├── api.ts - Base axios config
    ├── auth.ts - Auth endpoints
    ├── activities.ts - Activity endpoints
    ├── chatbot.ts - Chatbot endpoints
    └── analytics.ts - Analytics endpoints
```

### 2. Backend Architecture (FastAPI)

```
Backend/
├── main.py
│   ├── Initialize FastAPI app
│   ├── Setup middleware
│   ├── Setup CORS
│   ├── Register routers
│   └── Setup error handlers
│
├── Routers (API Endpoints)
│   ├── auth.py - Authentication
│   ├── activities.py - Activity CRUD
│   ├── chatbot.py - AI Chat
│   ├── analytics.py - Analytics
│   ├── admin.py - Admin operations
│   └── health.py - Health checks
│
├── Models (Database ORM)
│   ├── user.py - User model
│   ├── activity.py - Activity model
│   ├── emission_factor.py - Factors
│   ├── goal.py - Goal model
│   ├── reward.py - Reward model
│   └── chat_history.py - Chat logs
│
├── Schemas (Pydantic)
│   ├── user.py - User validation
│   ├── activity.py - Activity validation
│   ├── emission_factor.py - Factor validation
│   └── analytics.py - Analytics validation
│
├── Services (Business Logic)
│   ├── emission_calculator.py - Carbon calculation
│   ├── ollama_service.py - LLM integration
│   ├── user_service.py - User management
│   ├── analytics_service.py - Analytics engine
│   └── reward_service.py - Reward logic
│
├── Utils
│   ├── jwt_handler.py - JWT tokens
│   ├── email_service.py - Email via SMTP
│   ├── validators.py - Custom validators
│   └── constants.py - App constants
│
├── Database
│   ├── database.py - Connection pool
│   ├── dependencies.py - Dependency injection
│   └── config.py - Configuration
│
└── Tests
    ├── test_auth.py
    ├── test_activities.py
    ├── test_emissions.py
    └── conftest.py
```

### 3. Database Architecture

```sql
-- User Management
users (id, email, password_hash, full_name, role, is_active, created_at)
├── One-to-Many: activities
├── One-to-Many: goals
├── One-to-Many: rewards
└── One-to-Many: chat_histories

-- Activity Tracking
activities (id, user_id, activity_type, value, unit, carbon_emissions, created_at)
├── Foreign Key: users.id
└── Calculated Field: carbon_emissions

-- Emission Data
emission_factors (id, category, subcategory, factor_value, unit, source, created_at)
├── Pre-loaded data
└── Admin editable

-- Goal Management
goals (id, user_id, title, target_reduction, deadline, status, created_at)
├── Foreign Key: users.id
└── One-to-Many: goal_progress

-- Reward System
rewards (id, user_id, earned_points, achievement, created_at)
├── Foreign Key: users.id
└── Linked to goals/activities

-- Chat History
chat_histories (id, user_id, message, response, created_at)
├── Foreign Key: users.id
└── Stores conversation logs

-- Analytics
analytics_snapshots (id, user_id, daily_emissions, weekly_emissions, monthly_emissions, created_at)
├── Foreign Key: users.id
└── Daily aggregate data
```

---

## 🔐 Security Architecture

### Authentication Flow

```
1. User Registration
   ↓
   POST /api/auth/register
   ↓
   Hash password with bcrypt
   ↓
   Store in database (Supabase Auth)
   ↓
   Send verification email (SMTP)
   ↓
   Return JWT token

2. User Login
   ↓
   POST /api/auth/login
   ↓
   Verify email & password
   ↓
   Generate JWT token
   ↓
   Return access & refresh tokens
   ↓
   Client stores in localStorage

3. API Request Protection
   ↓
   Client sends JWT in Authorization header
   ↓
   FastAPI middleware verifies JWT
   ↓
   Extract user_id from token claims
   ↓
   Check user roles for authorization
   ↓
   Proceed with request or return 401/403
```

### JWT Token Structure

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "role": "user",
  "iat": 1234567890,
  "exp": 1234571490,
  "type": "access"
}
```

### Security Measures

1. **JWT Tokens**
   - Access tokens: 1 hour expiry
   - Refresh tokens: 7 days expiry
   - Signed with HS256 algorithm

2. **Password Security**
   - Bcrypt hashing (cost factor: 12)
   - No plaintext storage
   - Salted hashes

3. **CORS**
   - Configured for Vercel domain
   - Allows authenticated requests only
   - Restricts HTTP methods

4. **Rate Limiting**
   - 100 requests/minute per user
   - 1000 requests/minute per IP
   - Sliding window algorithm

5. **Input Validation**
   - Pydantic schemas validate all inputs
   - Email format validation
   - Activity value range checking

6. **SQL Injection Prevention**
   - SQLAlchemy ORM prevents injections
   - Parameterized queries
   - No raw SQL queries

---

## 📊 Data Flow Diagrams

### Activity Creation Flow

```
User Input
↓
Frontend Form Validation
↓
POST /api/activities
{
  activity_type: "transport",
  value: 50,
  unit: "km",
  description: "Daily commute"
}
↓
Backend Validation (Pydantic)
↓
Lookup emission_factors
  category = activity_type
↓
Calculate carbon_emissions
  = value × factor_value
↓
Create activity record
↓
Update user analytics
↓
Check goals & achievements
↓
Return 201 with activity data
↓
Update frontend state
↓
Display in dashboard
```

### Chatbot Interaction Flow

```
User Message
↓
Frontend sends to API
  POST /api/chatbot/chat
  { message: "How can I reduce emissions?" }
↓
Backend receives message
↓
Get user's activity history
↓
Prepare context prompt
↓
Call Ollama API
  POST http://localhost:11434/api/generate
  {
    model: "gemma:2b",
    prompt: "Based on user's activities...",
    stream: false
  }
↓
Ollama inference (GPU/CPU)
↓
Return generated response
↓
Save to chat_history table
↓
Return response to frontend
↓
Display in chat interface
↓
Update suggestion based on emissions
```

### Analytics Aggregation

```
Daily Trigger (Scheduled Job)
↓
Get all users with activities today
↓
For each user:
  Calculate daily emissions
  ↓
  Calculate weekly emissions
  ↓
  Calculate monthly emissions
  ↓
  Check goal progress
  ↓
  Award points if goals met
  ↓
  Create analytics snapshot
↓
Store aggregated data
↓
Trigger notifications (optional)
↓
Update admin dashboard
```

---

## 🔌 API Architecture

### API Layers

```
REQUEST
  ↓
MIDDLEWARE
  ├── CORS Handler
  ├── JWT Verification
  ├── Rate Limiting
  └── Request Logging
  ↓
ROUTING LAYER
  ├── /api/auth/
  ├── /api/activities/
  ├── /api/chatbot/
  ├── /api/analytics/
  └── /api/admin/
  ↓
VALIDATION LAYER
  ├── Pydantic Schema
  ├── Field Validation
  └── Business Rule Validation
  ↓
SERVICE LAYER
  ├── EmissionCalculator
  ├── OllamaService
  ├── UserService
  ├── AnalyticsService
  └── RewardService
  ↓
DATABASE LAYER
  ├── SQLAlchemy ORM
  ├── Connection Pooling
  └── Transaction Management
  ↓
RESPONSE FORMATTING
  ├── JSON Serialization
  ├── Error Handling
  └── Status Codes
  ↓
RESPONSE
```

### Request/Response Pattern

```javascript
// Frontend Request
{
  headers: {
    "Authorization": "Bearer JWT_TOKEN",
    "Content-Type": "application/json"
  },
  body: {
    "activity_type": "transport",
    "value": 50,
    "unit": "km"
  }
}

// Backend Response (Success)
{
  status: 200,
  body: {
    "id": "uuid",
    "user_id": "uuid",
    "activity_type": "transport",
    "value": 50,
    "unit": "km",
    "carbon_emissions": 12.5,
    "created_at": "2024-06-22T10:30:00Z"
  }
}

// Backend Response (Error)
{
  status: 422,
  body: {
    "detail": [
      {
        "loc": ["body", "value"],
        "msg": "Value must be between 0 and 1000",
        "type": "value_error"
      }
    ]
  }
}
```

---

## 🤖 AI/LLM Architecture

### Ollama Integration

```
Frontend Chat
↓
Send message to Backend
↓
Backend receives /api/chatbot/chat
↓
Get user context:
  - Recent activities
  - Current emissions
  - Active goals
  - Achievement history
↓
Build prompt template:
  "User's carbon data: {...}
   Recent activities: {...}
   User question: {...}"
↓
Call Ollama Service
  ├── Connect to localhost:11434
  ├── Send POST request
  ├── Model: gemma:2b / llama2 / deepseek
  └── Wait for generation
↓
Ollama runs inference
  ├── Tokenization
  ├── Forward pass
  ├── Token generation
  └── Stream or batch output
↓
Backend receives response
↓
Parse & format response
↓
Store in chat_history
↓
Return to frontend
↓
Display in UI
```

### Model Selection

| Model | Size | Speed | Quality | VRAM |
|-------|------|-------|---------|------|
| Gemma 2b | 2GB | Fast | Good | 4GB |
| Mistral 7b | 7GB | Medium | Very Good | 8GB |
| Llama 2 7b | 7GB | Medium | Excellent | 8GB |
| DeepSeek 6.7b | 6.7GB | Medium | Excellent | 8GB |

**Recommended:** Gemma 2b (balance of speed & quality)

---

## 🐳 Container Architecture

### Docker Services

```yaml
services:
  backend:
    image: carbon-coach-backend
    ports: 8000:8000
    environment:
      - DATABASE_URL
      - OLLAMA_API_URL=http://ollama:11434
    depends_on:
      - postgres
      - ollama

  frontend:
    image: carbon-coach-frontend
    ports: 3000:3000
    environment:
      - VITE_API_URL=http://backend:8000

  postgres:
    image: postgres:15-alpine
    ports: 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ollama:
    image: ollama/ollama
    ports: 11434:11434
    volumes:
      - ollama_data:/root/.ollama
    # Note: GPU support requires additional config
```

---

## 📈 Scalability Considerations

### Current Architecture (Development)

- Single FastAPI instance
- Local PostgreSQL
- Local Ollama
- File-based state

### Production Architecture (Render + Supabase)

- FastAPI on Render (automatic scaling)
- Supabase PostgreSQL (managed, scalable)
- Ollama on separate machine (or local)
- Distributed cache (optional)

### Future Scalability

1. **Horizontal Scaling**
   - Multiple API instances behind load balancer
   - Database read replicas
   - Redis cache layer

2. **LLM Optimization**
   - Model quantization
   - Batch inference
   - Caching common responses

3. **Analytics Optimization**
   - Time-series database (InfluxDB)
   - Materialized views
   - Pre-aggregated metrics

---

## 🔄 Deployment Architecture

### Local Development

```
Laptop
├── Frontend (npm run dev)
├── Backend (uvicorn --reload)
├── PostgreSQL (local)
└── Ollama (ollama serve)
```

### Production (FREE Tier)

```
Internet
  ↓
Vercel (Frontend)
  ├── Automatic deployment from GitHub
  ├── Global CDN
  └── Free tier: 100GB bandwidth/month
  ↓
Render.com (Backend API)
  ├── Auto deployment from GitHub
  ├── PostgreSQL connection
  └── Free tier: 750 hours/month
  ↓
Supabase (Database)
  ├── PostgreSQL managed service
  ├── Built-in Auth
  └── Free tier: 500MB storage
  ↓
Local/VPS (Ollama)
  ├── Local LLM inference
  ├── No API costs
  └── Can run on laptop
```

---

## 🧪 Testing Architecture

### Test Pyramid

```
        /\
       /  \
      / E2E \ (5%)
     /────────\
    /  \      /
   /    \    /
  / API  \  / Integration (15%)
 /────────\/
/          \
/ Unit Tests \ (80%)
/──────────────\
```

### Testing Strategy

1. **Unit Tests (80%)**
   - Services: emission_calculator, user_service, reward_service
   - Utils: validators, jwt_handler
   - No database, use mocks

2. **Integration Tests (15%)**
   - API endpoints with test database
   - Database transactions
   - External service mocks

3. **E2E Tests (5%)**
   - Full user flows
   - UI interactions (Playwright)
   - Real database

---

## 📊 Performance Architecture

### Frontend Optimization

- Code splitting with Vite
- Lazy loading of components
- Image optimization
- CSS minification
- Caching strategies

### Backend Optimization

- Connection pooling (5-20 connections)
- Query optimization with indexes
- Response caching
- Gzip compression
- Async operations

### Database Optimization

- Indexed columns: user_id, activity_type, created_at
- Partitioned tables (optional): activities by year
- Regular VACUUM & ANALYZE
- Connection limits

---

## 🔧 Configuration Architecture

### Environment Variables

**Backend**
```env
# Database
DATABASE_URL=postgresql://...

# Supabase
SUPABASE_URL=https://...
SUPABASE_KEY=...

# Ollama
OLLAMA_API_URL=http://localhost:11434

# JWT
JWT_SECRET=random-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=...
SMTP_PASSWORD=...

# Environment
DEBUG=False
ENVIRONMENT=production
```

**Frontend**
```env
VITE_API_URL=https://backend-api.com
VITE_SUPABASE_URL=https://...
VITE_SUPABASE_KEY=...
VITE_ENVIRONMENT=production
```

---

## 📡 External Services Integration

### 100% FREE Integrations

1. **Ollama** - Local LLM (No API key needed)
2. **Supabase Auth** - Free authentication
3. **Supabase Database** - Free PostgreSQL
4. **Supabase Storage** - Free file storage
5. **Gmail SMTP** - Free email sending
6. **Vercel** - Free frontend hosting
7. **Render.com** - Free backend hosting
8. **GitHub** - Free code repository

### No Paid Services

❌ OpenAI API (Paid)
❌ AWS Services (Paid)
❌ Google Cloud (Paid)
❌ SendGrid (Paid after free tier)
❌ Stripe (Transaction fees)
❌ Sentry (Paid plans only)

---

## ✅ Architecture Validation

- [x] 100% free components
- [x] Local LLM (no API costs)
- [x] Scalable to production
- [x] Responsive frontend
- [x] Secure authentication
- [x] Efficient calculations
- [x] Beautiful UI/UX
- [x] Well-documented
- [x] Docker ready
- [x] Auto-deployable

