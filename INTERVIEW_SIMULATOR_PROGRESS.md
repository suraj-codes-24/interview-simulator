# 🧠 AI Multimodal Interview Simulator — Project Progress

## 📌 Project Location
```
C:\Users\suraj\Desktop\interview_simulator
```

## 🔗 GitHub Repo
```
https://github.com/suraj-codes-24/interview-simulator
```

---

## ✅ COMPLETED SO FAR

### Environment
- Python 3.11.8
- Node v24.11.0 + npm 11.6.1
- Git 2.51.2
- PostgreSQL 18.3 (password: `admin123`)
- Virtual environment: `venv/`
- Database name: `interview_db`

### Installed Packages
```
fastapi, uvicorn, sqlalchemy, psycopg2-binary,
python-jose[cryptography], passlib, bcrypt==4.0.1,
python-dotenv, sentence-transformers, email-validator
```

### .env File (already created)
```
DATABASE_URL=postgresql://postgres:admin123@localhost:5432/interview_db
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Files Written ✅
```
main.py                         ✅
database.py                     ✅
core/config.py                  ✅
core/security.py                ✅
core/dependencies.py            ✅
models/user.py                  ✅
models/interview_session.py     ✅
models/question.py              ✅
models/answer.py                ✅
models/score.py                 ✅
models/analytics.py             ✅
schemas/user_schema.py          ✅
services/auth_service.py        ✅
routes/auth_routes.py           ✅
```

### Database Tables Created ✅
```
users
interview_sessions
questions
answers
scores
analytics
```

### API Endpoints Working ✅
```
GET  /              → API health check
POST /auth/register → Register new user
POST /auth/login    → Login + returns JWT token
```

---

## 🏗️ FULL FOLDER STRUCTURE
```
interview_simulator/
├── main.py
├── database.py
├── .env
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── interview_session.py
│   ├── question.py
│   ├── answer.py
│   ├── score.py
│   └── analytics.py
├── schemas/
│   ├── __init__.py
│   └── user_schema.py
├── routes/
│   ├── __init__.py
│   └── auth_routes.py
├── services/
│   ├── __init__.py
│   └── auth_service.py
├── ai_engine/
│   ├── base_engine.py
│   ├── nlp_engine.py
│   ├── voice_engine.py
│   └── vision_engine.py
├── scoring/
│   └── score_aggregator.py
└── utils/
    ├── embeddings.py
    └── helpers.py
```

---

## 🗄️ DATABASE DESIGN

### users
- id, name, email, password_hash, branch, year

### interview_sessions
- id, user_id, interview_type, topic, difficulty, start_time, end_time, final_score

### questions
- id, topic, difficulty, type, question_text, ideal_answer

### answers
- id, session_id, question_id, user_answer, nlp_score, voice_score, face_score, total_score

### scores
- id, session_id, nlp_score, voice_score, face_score, final_score

### analytics
- id, user_id, avg_technical_score, avg_hr_score, weakest_topic, strongest_topic

---

## 🗓️ DEVELOPMENT ROADMAP

### ✅ Day 1 — Environment Setup (DONE)
- Installed all tools
- Created folder structure
- Set up GitHub repo
- Configured .env

### ✅ Day 2 — Database + Models (DONE)
- SQLAlchemy connection
- All 6 models written
- All 6 tables created in PostgreSQL

### ✅ Day 3 — Auth System (DONE)
- JWT token generation
- Password hashing with bcrypt
- Register endpoint
- Login endpoint
- Swagger UI working at http://localhost:8000/docs

### 🔄 Day 4 — Interview Session + Questions (NEXT)
**Files to build:**
- `schemas/interview_schema.py`
- `services/interview_service.py`
- `routes/interview_routes.py`

**Endpoints to build:**
- POST `/interview/start` → create session
- GET `/interview/question` → fetch question by topic + difficulty
- Seed 20-30 questions into DB

### 📅 Day 5 — NLP Evaluation Engine
**Files to build:**
- `ai_engine/nlp_engine.py`

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Scoring Formula:**
```
Final Score =
  50% Semantic Similarity
+ 30% Keyword Coverage
+ 20% Structure Quality
```

### 📅 Day 6 — Answer Submission + Scoring
**Files to build:**
- `services/evaluation_service.py`
- `scoring/score_aggregator.py`

**Endpoints:**
- POST `/interview/answer` → submit answer → trigger NLP → store score

### 📅 Day 7 — Analytics + Dashboard API
**Files to build:**
- `services/analytics_service.py`
- `routes/analytics_routes.py`

**Endpoints:**
- GET `/analytics/me` → get user performance summary

### 📅 Day 8 — React Frontend (Basic)
**Pages:**
- Login.jsx
- Dashboard.jsx
- InterviewRoom.jsx
- Result.jsx

---

## 🛠️ HOW TO START THE SERVER

```bash
cd C:\Users\suraj\Desktop\interview_simulator
venv\Scripts\activate
uvicorn main:app --reload
```

Then open: http://localhost:8000/docs

---

## 💡 IMPORTANT NOTES
- Use **me (Claude)** for writing all code — saves Antigravity credits
- Use **Antigravity** only for complex multi-file debugging
- In Antigravity use **Gemini 3.1 Pro (Low)** for daily tasks
- Use **Claude Sonnet 4.6 (Thinking)** only for hard logic problems
- PostgreSQL password: `admin123`
- JWT tokens expire in 30 minutes

---

## 🎯 TECH STACK
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Auth:** JWT + bcrypt
- **AI/NLP:** HuggingFace sentence-transformers
- **Frontend (Day 8):** React + Tailwind
- **Version Control:** GitHub

---

## 📊 SCORING FORMULAS (for reference)

### NLP Score (Phase 1)
```
Final Score = 50% Semantic Similarity
            + 30% Keyword Coverage
            + 20% Structure Quality
```

### Voice Score (Phase 2)
```
Voice Score = 30% Fluency + 25% Pace + 25% Volume + 20% Filler Control
```

### Face Score (Phase 3)
```
Face Score = 40% Eye Contact + 30% Stability + 30% Emotional Consistency
```

### Final HR Score (Phase 4)
```
Final HR Score = 40% NLP + 30% Voice + 20% Face + 10% Behavioral Structure
```
