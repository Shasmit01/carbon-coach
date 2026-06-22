# Database Schema Documentation

## Overview

The AI Carbon Footprint Coach uses PostgreSQL to store all application data. This document provides a complete reference for the database schema.

---

## Entity-Relationship Diagram (ERD)

```
┌─────────────────────┐
│      users          │
├─────────────────────┤
│ id (PK)             │◄──────────┐
│ email (UNIQUE)      │           │
│ password_hash       │           │
│ full_name           │           │
│ avatar_url          │           │
│ role (user/admin)   │           │
│ is_active           │           │
│ created_at          │           │
│ updated_at          │           │
└─────────────────────┘           │
         │                        │
         ├──────────────┬─────────┼────────┐
         │              │         │        │
         ▼              ▼         ▼        ▼
    ┌────────────┐ ┌────────┐ ┌─────┐ ┌──────────┐
    │ activities │ │ goals  │ │rewards│ │chat_     │
    └────────────┘ └────────┘ └─────┘ │histories │
                                       └──────────┘

┌──────────────────────┐
│ emission_factors     │
├──────────────────────┤
│ id (PK)              │
│ category             │
│ subcategory          │
│ factor_value         │
│ unit                 │
│ source               │
│ created_at           │
│ updated_at           │
└──────────────────────┘
```

---

## Detailed Schema

### 1. USERS Table

**Purpose:** Store user account information and authentication data.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    bio TEXT,
    role VARCHAR(50) DEFAULT 'user' NOT NULL CHECK (role IN ('user', 'admin')),
    is_active BOOLEAN DEFAULT true NOT NULL,
    email_verified BOOLEAN DEFAULT false NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK, Default | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (login identifier) |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| full_name | VARCHAR(255) | NULL | User's full name |
| avatar_url | TEXT | NULL | Profile picture URL |
| bio | TEXT | NULL | User biography |
| role | VARCHAR(50) | NOT NULL, CHECK | 'user' or 'admin' |
| is_active | BOOLEAN | DEFAULT true | Account active status |
| email_verified | BOOLEAN | DEFAULT false | Email verification status |
| last_login | TIMESTAMP | NULL | Last login timestamp |
| preferences | JSONB | DEFAULT {} | User preferences (dark mode, etc) |
| created_at | TIMESTAMP | NOT NULL | Account creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

---

### 2. ACTIVITIES Table

**Purpose:** Track user activities and their associated carbon emissions.

```sql
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    value DECIMAL(10, 2) NOT NULL CHECK (value > 0),
    unit VARCHAR(50) NOT NULL,
    carbon_emissions DECIMAL(10, 4) NOT NULL DEFAULT 0,
    data JSONB DEFAULT '{}',
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_activities_user_id ON activities(user_id);
CREATE INDEX idx_activities_type ON activities(activity_type);
CREATE INDEX idx_activities_created ON activities(created_at DESC);
CREATE INDEX idx_activities_user_date ON activities(user_id, created_at DESC);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Activity identifier |
| user_id | UUID | FK, NOT NULL | Reference to user |
| activity_type | VARCHAR(50) | NOT NULL | transport, energy, food, waste, shopping |
| category | VARCHAR(100) | NULL | Subcategory (e.g., car, bus, etc) |
| description | TEXT | NULL | Activity notes |
| value | DECIMAL(10,2) | NOT NULL | Numeric value (km, kWh, kg, etc) |
| unit | VARCHAR(50) | NOT NULL | Measurement unit |
| carbon_emissions | DECIMAL(10,4) | NOT NULL | Calculated CO2 equivalent in kg |
| data | JSONB | DEFAULT {} | Additional metadata |
| is_verified | BOOLEAN | DEFAULT false | Admin verification flag |
| created_at | TIMESTAMP | NOT NULL | When activity was logged |
| updated_at | TIMESTAMP | NOT NULL | Last modification time |

**Activity Types:**
- `transport` - Car, bus, train, flight, bicycle
- `energy` - Electricity, gas, heating
- `food` - Meat, dairy, plant-based
- `waste` - Recycling, composting, landfill
- `shopping` - New purchases, clothing, electronics

---

### 3. EMISSION_FACTORS Table

**Purpose:** Store conversion factors for calculating carbon emissions.

```sql
CREATE TABLE emission_factors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) NOT NULL,
    description TEXT,
    factor_value DECIMAL(10, 6) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    source VARCHAR(255),
    region VARCHAR(100),
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE UNIQUE INDEX idx_factors_category_subcategory 
    ON emission_factors(category, subcategory, region) 
    WHERE is_active = true;
CREATE INDEX idx_factors_category ON emission_factors(category);
CREATE INDEX idx_factors_active ON emission_factors(is_active);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Factor identifier |
| category | VARCHAR(100) | NOT NULL | Activity type |
| subcategory | VARCHAR(100) | NOT NULL | Specific sub-type |
| description | TEXT | NULL | What this factor covers |
| factor_value | DECIMAL(10,6) | NOT NULL | kg CO2 per unit |
| unit | VARCHAR(50) | NOT NULL | Input unit (km, kWh, kg, etc) |
| source | VARCHAR(255) | NULL | Data source (EPA, IPCC, etc) |
| region | VARCHAR(100) | NULL | Geographic region |
| is_active | BOOLEAN | DEFAULT true | Currently used |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

**Sample Data:**

```sql
-- Transportation
INSERT INTO emission_factors (category, subcategory, factor_value, unit, source)
VALUES 
    ('transport', 'car_petrol', 0.21, 'km', 'EPA 2024'),
    ('transport', 'car_diesel', 0.18, 'km', 'EPA 2024'),
    ('transport', 'car_electric', 0.05, 'km', 'IPCC 2023'),
    ('transport', 'bus', 0.089, 'km', 'EPA 2024'),
    ('transport', 'train', 0.041, 'km', 'EPA 2024'),
    ('transport', 'flight_domestic', 0.255, 'km', 'ICAO 2024'),
    ('transport', 'flight_international', 0.195, 'km', 'ICAO 2024');

-- Energy
INSERT INTO emission_factors (category, subcategory, factor_value, unit, source)
VALUES 
    ('energy', 'electricity_grid_avg', 0.42, 'kWh', 'IEA 2024'),
    ('energy', 'electricity_renewable', 0.05, 'kWh', 'IPCC 2023'),
    ('energy', 'natural_gas', 2.04, 'm3', 'EPA 2024'),
    ('energy', 'heating_oil', 3.15, 'liter', 'EPA 2024');

-- Food
INSERT INTO emission_factors (category, subcategory, factor_value, unit, source)
VALUES 
    ('food', 'beef', 27.0, 'kg', 'Oxford Study 2023'),
    ('food', 'pork', 12.1, 'kg', 'Oxford Study 2023'),
    ('food', 'chicken', 6.9, 'kg', 'Oxford Study 2023'),
    ('food', 'fish', 11.7, 'kg', 'Oxford Study 2023'),
    ('food', 'dairy', 3.2, 'kg', 'Oxford Study 2023'),
    ('food', 'vegetables', 2.0, 'kg', 'Oxford Study 2023'),
    ('food', 'fruits', 1.5, 'kg', 'Oxford Study 2023');

-- Waste
INSERT INTO emission_factors (category, subcategory, factor_value, unit, source)
VALUES 
    ('waste', 'landfill', 0.5, 'kg', 'EPA 2024'),
    ('waste', 'recycling', 0.1, 'kg', 'EPA 2024'),
    ('waste', 'composting', 0.02, 'kg', 'EPA 2024');

-- Shopping
INSERT INTO emission_factors (category, subcategory, factor_value, unit, source)
VALUES 
    ('shopping', 'clothing', 10.0, 'item', 'Ellen MacArthur Foundation'),
    ('shopping', 'electronics', 50.0, 'item', 'IVL Swedish Research'),
    ('shopping', 'furniture', 100.0, 'item', 'European Commission');
```

---

### 4. GOALS Table

**Purpose:** Track user reduction goals and achievements.

```sql
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_reduction DECIMAL(10, 2) NOT NULL,
    baseline_emissions DECIMAL(10, 2) NOT NULL,
    target_emissions DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) DEFAULT 'kg_CO2' NOT NULL,
    category VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active' NOT NULL CHECK (status IN ('active', 'completed', 'failed', 'paused')),
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    deadline DATE NOT NULL,
    actual_reduction DECIMAL(10, 2) DEFAULT 0,
    progress_percentage DECIMAL(5, 2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_goals_deadline ON goals(deadline);
CREATE INDEX idx_goals_user_status ON goals(user_id, status);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Goal identifier |
| user_id | UUID | FK, NOT NULL | User creating goal |
| title | VARCHAR(255) | NOT NULL | Goal name |
| description | TEXT | NULL | Goal description |
| target_reduction | DECIMAL(10,2) | NOT NULL | % reduction target |
| baseline_emissions | DECIMAL(10,2) | NOT NULL | Starting emissions |
| target_emissions | DECIMAL(10,2) | NOT NULL | Target emissions level |
| unit | VARCHAR(50) | DEFAULT 'kg_CO2' | Measurement unit |
| category | VARCHAR(100) | NULL | Goal category |
| status | VARCHAR(50) | NOT NULL, CHECK | active/completed/failed/paused |
| start_date | DATE | NOT NULL | Goal start |
| deadline | DATE | NOT NULL | Goal deadline |
| actual_reduction | DECIMAL(10,2) | DEFAULT 0 | Achieved reduction |
| progress_percentage | DECIMAL(5,2) | DEFAULT 0 | % progress (0-100) |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update |

---

### 5. REWARDS Table

**Purpose:** Track achievements and points earned by users.

```sql
CREATE TABLE rewards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reward_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    points INTEGER NOT NULL DEFAULT 0,
    points_multiplier DECIMAL(3, 2) DEFAULT 1.0,
    icon_url TEXT,
    badge_name VARCHAR(100),
    criteria JSONB,
    unlocked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_rewards_user_id ON rewards(user_id);
CREATE INDEX idx_rewards_type ON rewards(reward_type);
CREATE INDEX idx_rewards_unlocked ON rewards(unlocked_at);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Reward identifier |
| user_id | UUID | FK, NOT NULL | User earning reward |
| reward_type | VARCHAR(100) | NOT NULL | achievement, milestone, streak |
| title | VARCHAR(255) | NOT NULL | Reward name |
| description | TEXT | NULL | What was achieved |
| points | INTEGER | NOT NULL | Points earned |
| points_multiplier | DECIMAL(3,2) | DEFAULT 1.0 | Bonus multiplier |
| icon_url | TEXT | NULL | Badge image URL |
| badge_name | VARCHAR(100) | NULL | Badge identifier |
| criteria | JSONB | NULL | How reward was earned |
| unlocked_at | TIMESTAMP | NULL | When earned |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Reward Types:**
- `first_activity` - 50 points
- `activity_streak` - 10 points per day
- `goal_completed` - 200 points
- `eco_warrior` - 100 points (30 days consistent)
- `carbon_reduction` - Variable points based on reduction %

---

### 6. CHAT_HISTORIES Table

**Purpose:** Store conversation history with AI chatbot.

```sql
CREATE TABLE chat_histories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID NOT NULL,
    message_index INTEGER NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    response_tokens INTEGER,
    ai_model VARCHAR(100) DEFAULT 'gemma:2b',
    response_time_ms INTEGER,
    helpful BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_chat_user_id ON chat_histories(user_id);
CREATE INDEX idx_chat_session ON chat_histories(user_id, session_id);
CREATE INDEX idx_chat_created ON chat_histories(created_at DESC);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Message identifier |
| user_id | UUID | FK, NOT NULL | User in conversation |
| session_id | UUID | NOT NULL | Chat session identifier |
| message_index | INTEGER | NOT NULL | Message order in session |
| user_message | TEXT | NOT NULL | User's question/input |
| ai_response | TEXT | NOT NULL | AI's response |
| response_tokens | INTEGER | NULL | Tokens in response |
| ai_model | VARCHAR(100) | DEFAULT 'gemma:2b' | Model used |
| response_time_ms | INTEGER | NULL | Generation time |
| helpful | BOOLEAN | NULL | User feedback |
| created_at | TIMESTAMP | NOT NULL | Message timestamp |

---

### 7. ANALYTICS_SNAPSHOTS Table

**Purpose:** Store pre-calculated daily analytics for fast queries.

```sql
CREATE TABLE analytics_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    daily_emissions DECIMAL(10, 4) NOT NULL DEFAULT 0,
    weekly_emissions DECIMAL(10, 4) NOT NULL DEFAULT 0,
    monthly_emissions DECIMAL(10, 4) NOT NULL DEFAULT 0,
    yearly_emissions DECIMAL(10, 4) NOT NULL DEFAULT 0,
    activity_count INTEGER DEFAULT 0,
    daily_change DECIMAL(10, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE UNIQUE INDEX idx_analytics_user_date ON analytics_snapshots(user_id, snapshot_date);
CREATE INDEX idx_analytics_user ON analytics_snapshots(user_id);
CREATE INDEX idx_analytics_date ON analytics_snapshots(snapshot_date DESC);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Snapshot identifier |
| user_id | UUID | FK, NOT NULL | User data |
| snapshot_date | DATE | NOT NULL | Date of snapshot |
| daily_emissions | DECIMAL(10,4) | NOT NULL | That day's emissions |
| weekly_emissions | DECIMAL(10,4) | NOT NULL | Last 7 days |
| monthly_emissions | DECIMAL(10,4) | NOT NULL | Last 30 days |
| yearly_emissions | DECIMAL(10,4) | NOT NULL | Last 365 days |
| activity_count | INTEGER | DEFAULT 0 | Activities that day |
| daily_change | DECIMAL(10,4) | NULL | % change from previous day |
| created_at | TIMESTAMP | NOT NULL | Record creation |

---

## Calculated/Derived Fields

### Daily Emissions Calculation

```sql
-- Calculate daily emissions for a user on a given date
SELECT SUM(carbon_emissions) as daily_total
FROM activities
WHERE user_id = $1
  AND DATE(created_at) = $2
  AND is_verified = true;
```

### Monthly Emissions Calculation

```sql
-- Calculate monthly emissions
SELECT DATE_TRUNC('month', created_at) as month,
       SUM(carbon_emissions) as monthly_total,
       COUNT(*) as activity_count
FROM activities
WHERE user_id = $1
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;
```

### Goal Progress Calculation

```sql
-- Calculate goal progress percentage
UPDATE goals
SET progress_percentage = (
    SELECT CASE 
        WHEN baseline_emissions = target_emissions THEN 100
        ELSE MIN(100, (baseline_emissions - COALESCE(SUM(a.carbon_emissions), 0)) / 
                       (baseline_emissions - target_emissions) * 100)
    END
    FROM activities a
    WHERE a.user_id = goals.user_id
      AND a.created_at >= goals.start_date
      AND a.created_at <= goals.deadline
),
actual_reduction = baseline_emissions - COALESCE(
    (SELECT SUM(carbon_emissions) 
     FROM activities 
     WHERE user_id = goals.user_id
       AND created_at >= goals.start_date
       AND created_at <= goals.deadline),
    0
)
WHERE id = $1;
```

---

## Indexes Strategy

### Performance Indexes

```sql
-- User Queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Activity Queries
CREATE INDEX idx_activities_user_id ON activities(user_id);
CREATE INDEX idx_activities_type ON activities(activity_type);
CREATE INDEX idx_activities_created ON activities(created_at DESC);
CREATE INDEX idx_activities_user_date ON activities(user_id, created_at DESC);

-- Goal Queries
CREATE INDEX idx_goals_user_status ON goals(user_id, status);
CREATE INDEX idx_goals_deadline ON goals(deadline);

-- Reward Queries
CREATE INDEX idx_rewards_user_unlocked ON rewards(user_id, unlocked_at);

-- Chat Queries
CREATE INDEX idx_chat_user_session ON chat_histories(user_id, session_id);

-- Analytics Queries
CREATE INDEX idx_analytics_user_date ON analytics_snapshots(user_id, snapshot_date DESC);
```

---

## Constraints & Validation

### Table Constraints

1. **users**
   - email must be unique and valid
   - password_hash must not be empty
   - role must be 'user' or 'admin'

2. **activities**
   - user_id must exist in users table
   - value must be positive
   - carbon_emissions >= 0

3. **emission_factors**
   - category + subcategory must be unique (when is_active=true)
   - factor_value must be >= 0

4. **goals**
   - user_id must exist in users table
   - target_reduction must be between 0-100
   - deadline must be > start_date

---

## Migration Strategy

### Initial Setup

```bash
# Using Alembic (Python migration tool)
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Data Migration

```python
# Load initial emission factors
from sqlalchemy import insert
from app.models import EmissionFactor

factors = [
    # ... emission factor data
]

db.execute(insert(EmissionFactor), factors)
db.commit()
```

---

## Backup Strategy

### PostgreSQL Backups

```bash
# Full database backup
pg_dump carbon_coach > backup.sql

# Compressed backup
pg_dump carbon_coach | gzip > backup.sql.gz

# Restore from backup
psql carbon_coach < backup.sql
```

### Supabase Backups (Automatic)

Supabase automatically backs up data:
- Daily snapshots (7 days retained)
- Point-in-time recovery available
- No manual backup needed

---

## Performance Metrics

### Expected Query Times

| Query | Indexed | Time |
|-------|---------|------|
| Get user activities | Yes | <50ms |
| Calculate daily emissions | Yes | <100ms |
| List emission factors | Yes | <20ms |
| Get goal progress | Yes | <150ms |
| Search chat history | Yes | <200ms |

