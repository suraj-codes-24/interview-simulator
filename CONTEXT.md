# Interview Simulator — Project Context

*Last updated: March 13, 2026 | Phase 14 Complete | All features built except Docker/Deploy*

---

## Phase Status

| Phase | Task | Status |
|-------|------|--------|
| Phase 1 | Core Backend: JWT, PostgreSQL, NLP, questions seeded | DONE |
| Phase 2 | Intelligence: Ollama HR, adaptive difficulty, no-repeat | DONE |
| Phase 3 | Voice: Whisper, librosa, parselmouth | DONE |
| Phase 4 | Face: MediaPipe 0.10.11, multimodal scoring | DONE |
| Phase 5 | Frontend: 14 pages, recharts, state-based routing | DONE |
| Phase 5b | DB Redesign: dropped dead tables, enriched schema | DONE |
| Phase 6 | ProfilePage + SettingsPage + OnboardingPage | DONE |
| Phase 7 | Coding Interview: Monaco Editor + sandboxed execution | DONE |
| Phase 8 | AI Follow-up Questions via Ollama | DONE |
| Phase 9 | Resume Analyser: PyMuPDF + Ollama | DONE |
| Phase 10 | JD Gap Analyser: Ollama + difflib fuzzy matching | DONE |
| Phase 11 | Interview Replay: transcript timeline + coaching | DONE |
| Phase 12 | PDF Reports: reportlab session download | DONE |
| Phase 12.5 | UX & stability improvements | DONE |
| Phase 14 | Question Bank: 133 → 482, NLP CONCEPT_MAP 74 → 79 | DONE |
| Phase 13 | Docker + Deploy | PLANNED |

---

## Question Bank (as of Phase 14)

| Subject | Questions | Difficulty Mix |
|---------|-----------|----------------|
| DSA | 280 | beginner/intermediate/advanced/expert |
| OOPS | 37 | beginner/intermediate/advanced |
| DBMS | 36 | beginner/intermediate/advanced |
| OS & Networking | 33 | beginner/intermediate/advanced |
| System Design | 26 | intermediate/advanced |
| Machine Learning | 40 | beginner/intermediate/advanced |
| Behavioral | 30 | beginner/intermediate/advanced |
| **Total** | **482** | **20 expert, 120 advanced, 239 intermediate, 103 beginner** |

- 7 subjects, 52 topics, 129 subtopics
- All subtopics have >= 3 questions
- NLP CONCEPT_MAP: 79 concepts
- Difficulty values: `beginner`, `intermediate`, `advanced`, `expert`

---

## Frontend Pages (all in App.jsx)

| # | Page | Purpose | Backend |
|---|------|---------|---------|
| 1 | LandingPage | Marketing/hero page | None |
| 2 | LoginPage | Login + Register forms | `/auth/login`, `/auth/register` |
| 3 | DashboardPage | Subject cards + analytics preview | `/interview/subjects`, `/analytics/me` |
| 4 | SubjectPage | Topic/subtopic/difficulty selector | `/interview/topics`, `/interview/subtopics` |
| 5 | InterviewRoomPage | Full-screen Q&A with voice/face | `/interview/question`, `/interview/answer` |
| 6 | ResultsPage | Session score breakdown | Session data from state |
| 7 | AnalyticsPage | Performance charts + history | `/analytics/me` |
| 8 | ProfilePage | Edit profile + change password | `/auth/profile`, `/auth/password` |
| 9 | SettingsPage | Hardware/AI/privacy toggles | localStorage only |
| 10 | OnboardingPage | 4-step wizard (shown once) | localStorage only |
| 11 | CodingInterviewPage | Monaco Editor + test cases | `/code/run` |
| 12 | ResumeAnalyserPage | PDF upload + AI analysis | `/resume/analyse` |
| 13 | JDAnalyserPage | JD paste + gap analysis | `/jd/analyse` |
| 14 | ReplayPage | Session transcript timeline | `/analytics/me` (sessions) |

---

## Backend Architecture

### Routes (11 routers in main.py)

| Router | Prefix | Endpoints |
|--------|--------|-----------|
| auth_router | `/auth` | POST login, register; PUT profile, password |
| interview_router | `/interview` | GET subjects, topics, subtopics, question; POST start |
| answer_router | `/interview` | POST answer |
| analytics_router | `/analytics` | GET me |
| voice_router | `/api/voice` | POST analyze |
| vision_router | `/api/vision` | POST analyze |
| code_router | `/code` | POST run |
| ai_router | `/ai` | POST followup |
| resume_router | `/resume` | POST analyse |
| jd_router | `/jd` | POST analyse |
| report_router | `/reports` | GET session/{id} |

### Services (11 files)

| Service | Purpose |
|---------|---------|
| auth_service.py | Register, login, profile/password update |
| interview_service.py | Adaptive difficulty, no-repeat question selection |
| evaluation_service.py | Multimodal scoring (NLP + voice + face) |
| analytics_service.py | Performance stats, topic breakdown, recent sessions |
| code_service.py | Sandboxed Python execution, safety blocklist, 5s timeout |
| ollama_utils.py | Centralized Ollama API with timeout/error handling |
| followup_service.py | AI follow-up question generation |
| resume_service.py | PyMuPDF text extraction + Ollama analysis |
| jd_service.py | JD skill extraction + gap analysis |
| report_service.py | PDF report generation (reportlab) |
| session_feedback_service.py | AI coaching summary |

### AI Engines (4 files)

| Engine | Purpose |
|--------|---------|
| nlp_engine.py | NLP scoring (semantic + keyword + depth + structure) + CONCEPT_MAP |
| hr_engine.py | Ollama HR evaluation |
| voice_engine.py | Whisper transcription + librosa + parselmouth analysis |
| vision_engine.py | MediaPipe FaceMesh emotion/engagement detection |

---

## Database Schema

### Active Tables

| Table | Key Columns |
|-------|-------------|
| users | id, name, email, password_hash, branch, year, college, avatar_url, created_at |
| subjects | id, name, type (technical/hr) |
| topics | id, subject_id, name |
| subtopics | id, topic_id, name |
| questions | id, subject_id, topic_id, subtopic_id, title, difficulty, type, question_text, ideal_answer, tags, companies |
| interview_sessions | id, user_id, interview_type, subject_id, topic_id, subtopic_id, difficulty, status, total_questions, questions_answered, start_time, end_time, final_score |
| answers | id, session_id, question_id, user_answer, semantic_score, keyword_score, depth_score, structure_score, nlp_score, voice_score, face_score, total_score, feedback |

### Dropped Tables
- `scores` — merged into answers columns (Phase 5b)
- `analytics` — never written to (Phase 5b)
- `conversation_memory` — redundant with answers (Phase 5b)
- `user_preferences` — never used, no model (Phase 14)

---

## Score Formulas

```
Technical: 70% NLP + 20% Voice + 10% Face
HR:        50% NLP + 30% Voice + 20% Face

NLP:   45% semantic + 25% keyword + 20% depth + 10% structure
Voice: 25% pace + 25% filler + 20% confidence + 15% silence + 15% energy
```

---

## File Structure

```
interview_simulator/
├── main.py                    <- FastAPI entry, 11 routers
├── database.py                <- PostgreSQL engine
├── CLAUDE.md                  <- Claude instructions
├── CONTEXT.md                 <- This file
├── requirements.txt
├── .env                       <- DB_URL, SECRET_KEY
├── .gitignore
│
├── ai_engine/
│   ├── base_engine.py
│   ├── nlp_engine.py          <- NLP + CONCEPT_MAP (79 concepts)
│   ├── hr_engine.py           <- Ollama qwen2.5-coder:7b
│   ├── voice_engine.py        <- Whisper + librosa + parselmouth
│   └── vision_engine.py       <- MediaPipe FaceMesh 0.10.11
│
├── core/
│   ├── config.py              <- Load .env variables
│   ├── security.py            <- JWT + bcrypt
│   └── dependencies.py        <- get_db, get_current_user
│
├── models/                    <- SQLAlchemy ORM (7 models)
│   ├── user.py, subject.py, topic.py, subtopic.py
│   ├── question.py, interview_session.py, answer.py
│
├── routes/                    <- FastAPI routers (11 files)
│   ├── auth_routes.py, interview_routes.py, answer_routes.py
│   ├── analytics_routes.py, voice_routes.py, vision_routes.py
│   ├── code_routes.py, ai_routes.py, resume_routes.py
│   ├── jd_routes.py, report_routes.py
│
├── schemas/                   <- Pydantic models
│   ├── user_schema.py, interview_schema.py, answer_schema.py
│   ├── score_schema.py, code_schema.py
│
├── services/                  <- Business logic (11 files)
│   ├── auth_service.py, interview_service.py, evaluation_service.py
│   ├── analytics_service.py, code_service.py, ollama_utils.py
│   ├── followup_service.py, resume_service.py, jd_service.py
│   ├── report_service.py, session_feedback_service.py
│
├── data/
│   ├── question_bank.py       <- Master question data
│   └── seed.py                <- Hierarchy + seeding logic
│
├── seed_v2.py                 <- Phase 14 question expansion
├── seed_v2_dsa_fill.py        <- Phase 14 DSA fill + expert questions
│
└── frontend/
    └── src/
        ├── App.jsx            <- ~3200 lines, all 14 pages
        ├── VoiceRecorder.jsx  <- Audio recording (DO NOT MODIFY)
        ├── VisionRecorder.jsx <- Camera + MediaPipe (DO NOT MODIFY)
        └── main.jsx
```

---

## Known Issues

| Issue | Status |
|-------|--------|
| Whisper on CPU (torch.cuda not detected) | Open - fix in Phase 13 |
| Parselmouth pitch = 0 Hz occasionally | Covered (librosa fallback) |
| mediapipe MUST be 0.10.11 on Windows | Constraint - do NOT upgrade |
| user_preferences table dropped | Fixed |

---

## Start Servers

```bash
# Terminal 1 - Backend
cd C:\Users\suraj\Desktop\interview_simulator
uvicorn main:app --reload

# Terminal 2 - Frontend
cd C:\Users\suraj\Desktop\interview_simulator\frontend
npm run dev
```

Login: `suraj@test.com` / `test123`
Frontend: http://localhost:5173
Backend docs: http://localhost:8000/docs

---

## Next: Phase 13 - Docker + Deploy

- Dockerfile for backend (Python 3.11, FastAPI, all AI deps)
- docker-compose.yml (backend + postgres)
- Frontend -> Vercel (static build)
- Backend -> Render or Railway
- Fix Whisper GPU (torch CUDA detection issue)
