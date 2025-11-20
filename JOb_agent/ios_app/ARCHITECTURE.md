# 🏗️ JobTracker Architecture - Complete System

## 📱 **System Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                         iOS App (SwiftUI)                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
│  │   Home   │   Apps   │   Jobs   │ Analytics│  Profile │      │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
│                              │                                   │
│                              │ HTTP/REST                         │
│                              ▼                                   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │
┌──────────────────────────────┼──────────────────────────────────┐
│                              │                                   │
│                    FastAPI Backend                               │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    API Routes                           │    │
│  │  /auth  /applications  /jobs  /analytics  /resume      │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    Services Layer                       │    │
│  │  ┌──────────┬──────────┬──────────┬──────────┐        │    │
│  │  │ LinkedIn │  Google  │  Indeed  │   Logo   │        │    │
│  │  │ Service  │  Service │ Service  │ Service  │        │    │
│  │  └──────────┴──────────┴──────────┴──────────┘        │    │
│  │  ┌──────────┬──────────┬──────────┐                   │    │
│  │  │   Auth   │  Resume  │ Semantic │                   │    │
│  │  │ Service  │  Parser  │ Matcher  │                   │    │
│  │  └──────────┴──────────┴──────────┘                   │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
└──────────────────────────────┼──────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  PostgreSQL   │    │     Redis     │    │  External APIs │
│   Database    │    │     Cache     │    │                │
│               │    │               │    │  • RapidAPI    │
│ • Users       │    │ • Sessions    │    │  • SerpAPI     │
│ • Apps        │    │ • Job Cache   │    │  • Clearbit    │
│ • Resumes     │    │ • Rate Limits │    │  • OpenAI      │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## 🔄 **Data Flow: Job Recommendations**

```
1. User opens Jobs tab
         │
         ▼
2. iOS App → GET /api/v1/jobs/external/aggregate
         │
         ▼
3. Backend checks Redis cache
         │
         ├─ Cache Hit → Return cached jobs
         │
         └─ Cache Miss ↓
                │
                ▼
4. Parallel API calls:
         │
         ├─→ LinkedIn Service → RapidAPI → LinkedIn Jobs
         │
         ├─→ Google Service → SerpAPI → Google Jobs
         │
         └─→ Indeed Service → Indeed API → Indeed Jobs
                │
                ▼
5. Aggregate results
         │
         ▼
6. For each job:
         │
         └─→ Logo Service → Clearbit → Company Logo
                │
                ▼
7. If user has resume:
         │
         └─→ Semantic Matcher → OpenAI → Match Score
                │
                ▼
8. Cache results in Redis (1 hour)
         │
         ▼
9. Return to iOS app
         │
         ▼
10. Display jobs with logos and match scores
```

---

## 🔐 **Authentication Flow**

```
1. User signs up/in
         │
         ▼
2. iOS App → POST /api/v1/auth/signin
         │
         ▼
3. Backend validates credentials
         │
         ▼
4. Generate JWT tokens
         │
         ├─ Access Token (30 min)
         └─ Refresh Token (7 days)
         │
         ▼
5. iOS stores in Keychain
         │
         ▼
6. All requests include:
   Authorization: Bearer <access_token>
```

---

## 📄 **Resume Processing Flow**

```
1. User uploads resume (PDF/DOC)
         │
         ▼
2. iOS App → POST /api/v1/resume/upload
         │
         ▼
3. Backend receives file
         │
         ▼
4. Extract text:
         │
         ├─ PDF → PyPDF2
         └─ DOC → python-docx
         │
         ▼
5. Parse resume:
         │
         ├─→ Extract skills (NLP/OpenAI)
         ├─→ Extract experience
         └─→ Extract education
         │
         ▼
6. Create embeddings:
         │
         └─→ OpenAI Embeddings API
                │
                ▼
7. Store in database:
         │
         ├─ Resume text
         ├─ Parsed data
         └─ Embeddings
         │
         ▼
8. Return resume ID to iOS
```

---

## 🎯 **Semantic Matching Flow**

```
1. User has resume uploaded
         │
         ▼
2. Fetch jobs from APIs
         │
         ▼
3. For each job:
         │
         ├─ Get job description
         │
         ├─→ Create job embedding (OpenAI)
         │
         ├─→ Get resume embedding (from DB)
         │
         ├─→ Calculate cosine similarity
         │      similarity = dot(resume_vec, job_vec) / 
         │                   (norm(resume_vec) * norm(job_vec))
         │
         ├─→ Convert to match score (0-100%)
         │
         └─→ Generate match reasons (OpenAI)
                │
                ▼
4. Sort jobs by match score
         │
         ▼
5. Return top matches to iOS
```

---

## 🗄️ **Database Schema**

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Resumes table
CREATE TABLE resumes (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    parsed_text TEXT,
    skills JSONB,
    experience JSONB,
    education JSONB,
    embedding VECTOR(1536),  -- OpenAI embedding
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Applications table
CREATE TABLE applications (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    role_title VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    applied_date TIMESTAMP NOT NULL,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Saved Jobs table
CREATE TABLE saved_jobs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    job_id VARCHAR(255) NOT NULL,
    job_data JSONB,
    saved_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔧 **Technology Stack**

### **iOS App**
- **Language:** Swift 5.9+
- **UI Framework:** SwiftUI
- **Architecture:** MVVM
- **Reactive:** Combine
- **Networking:** URLSession (async/await)
- **Security:** Keychain
- **Deployment:** iOS 17.0+

### **Backend**
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.11+
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7+
- **Task Queue:** Celery
- **Authentication:** JWT (python-jose)
- **Password:** bcrypt (passlib)

### **External APIs**
- **LinkedIn Jobs:** RapidAPI
- **Google Jobs:** SerpAPI
- **Indeed Jobs:** Indeed Publisher API
- **Company Logos:** Clearbit Logo API
- **AI Matching:** OpenAI Embeddings API

---

## 📊 **API Endpoints**

### **Authentication**
```
POST   /api/v1/auth/signup
POST   /api/v1/auth/signin
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me
POST   /api/v1/auth/password-reset
```

### **Applications**
```
GET    /api/v1/applications
POST   /api/v1/applications
GET    /api/v1/applications/{id}
PUT    /api/v1/applications/{id}
DELETE /api/v1/applications/{id}
```

### **Jobs** ⭐ NEW
```
GET    /api/v1/jobs/external/linkedin
GET    /api/v1/jobs/external/google
GET    /api/v1/jobs/external/indeed
GET    /api/v1/jobs/external/aggregate
GET    /api/v1/jobs/company-logo
POST   /api/v1/jobs/{job_id}/save
DELETE /api/v1/jobs/{job_id}/save
GET    /api/v1/jobs/saved
```

### **Resume** ⭐ NEW
```
POST   /api/v1/resume/upload
GET    /api/v1/resume
DELETE /api/v1/resume
```

### **Semantic Search** ⭐ NEW
```
GET    /api/v1/jobs/recommendations/semantic
```

---

## 🚀 **Deployment Architecture**

```
┌─────────────────────────────────────────────┐
│              App Store                       │
│         (iOS App Distribution)               │
└─────────────────────────────────────────────┘
                    │
                    │ Users download
                    ▼
┌─────────────────────────────────────────────┐
│           User's iPhone/iPad                 │
│            (JobTracker App)                  │
└─────────────────────────────────────────────┘
                    │
                    │ HTTPS
                    ▼
┌─────────────────────────────────────────────┐
│              Load Balancer                   │
│            (AWS ALB / Nginx)                 │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│  FastAPI      │       │  FastAPI      │
│  Instance 1   │       │  Instance 2   │
│  (Docker)     │       │  (Docker)     │
└───────────────┘       └───────────────┘
        │                       │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│  PostgreSQL   │       │     Redis     │
│   (RDS)       │       │  (ElastiCache)│
└───────────────┘       └───────────────┘
```

---

## 📈 **Performance Optimizations**

### **Caching Strategy**
```python
# Cache job results for 1 hour
@cache(ttl=3600)
def get_jobs(query, location):
    # Expensive API calls
    pass

# Cache company logos indefinitely
@cache(ttl=None)
def get_logo(company):
    # Logo URLs don't change
    pass
```

### **Rate Limiting**
```python
# Limit to 100 requests per hour per user
@rate_limit(limit=100, period=3600)
async def get_jobs():
    pass
```

### **Pagination**
```python
# Load 20 jobs at a time
limit = 20
offset = page * limit
```

---

## 🎉 **Complete!**

You now have a **full-stack, production-ready application** with:

✅ iOS app with 5 tabs  
✅ Backend API with FastAPI  
✅ Real job data from LinkedIn/Google/Indeed  
✅ AI-powered semantic matching  
✅ Company logos  
✅ Resume parsing  
✅ Secure authentication  
✅ Scalable architecture  

**Ready to ship!** 🚀
