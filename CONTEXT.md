# AI Multimodal Interview Simulator — Project Context
> Synced with real codebase: March 12, 2026 | Read this at the start of every session

---

## Project Info

| Field | Value |
|---|---|
| Location | `C:\Users\suraj\Desktop\interview_simulator` |
| GitHub | https://github.com/suraj-codes-24/interview-simulator |
| Backend | FastAPI — `http://localhost:8000` |
| Frontend | React + Vite — `http://localhost:5173` |
| API Docs | `http://localhost:8000/docs` |
| Database | PostgreSQL — `interview_db` (user: `postgres`, pass: `admin123`) |
| Test Login | `suraj@test.com` / `test123` |
| GPU | NVIDIA RTX 4050 Laptop (Ollama on CUDA) |
| Stack | Python 3.11 + FastAPI + PostgreSQL + React + Vite |

---

## Start Every Session

```bash
# Terminal 1 — Backend
cd C:\Users\suraj\Desktop\interview_simulator
uvicorn main:app --reload

# Terminal 2 — Frontend
cd C:\Users\suraj\Desktop\interview_simulator\frontend
npm run dev
```

---

## Phases Completed

| Phase | What Was Built |
|---|---|
| Phase 1 | JWT auth, PostgreSQL models, NLP engine with CONCEPT_MAP, 133 questions seeded across 7 subjects / 52 topics / 129 subtopics |
| Phase 2 | Ollama HR engine (qwen2.5-coder:7b on local GPU), adaptive difficulty, no-repeat questions per session |
| Phase 3 | Voice analysis: Whisper (local, CPU), librosa, parselmouth — pace / filler words / confidence / silence / energy |
| Phase 4 | Face analysis: MediaPipe FaceMesh 0.10.11 — eye contact / head stability / emotion detection. Multimodal scoring. |
| Phase 5 | Frontend redesign: 9 pages in App.jsx, recharts, Figma-matched layouts |
| Phase 5b | DB redesign: dropped 3 dead tables, added full NLP breakdown columns to answers, added college/avatar_url/created_at to users |
| Phase 5c | Interview Room: no-scroll 100vh layout, inline audio recording, mic button in bottom bar |
| Phase 6 | Profile edit form (PUT /auth/profile + PUT /auth/password), SettingsPage (localStorage), OnboardingPage (4-step wizard) |
| Phase 7 | Coding Interview: CodingInterviewPage + Monaco Editor + POST /code/run (sandboxed Python) + Run/Submit flow |

---

## Frontend Pages — Real Status

All pages live in `frontend/src/App.jsx` (~1600 lines). State-based routing (no React Router).

| Page Function | In Sidebar | Page State | Status |
|---|---|---|---|
| `LandingPage` | No (pre-login) | `landing` | Complete |
| `LoginPage` | No (pre-login) | `login` | Complete |
| `DashboardPage` | Yes — "Dashboard" | `dashboard` | Complete |
| `SubjectPage` | Yes — "Interview" | `subject` | Complete |
| `InterviewRoomPage` | No (full-screen) | `interview` | Complete — no-scroll redesign, inline mic |
| `ResultsPage` | No (post-interview) | `result` | Complete |
| `AnalyticsPage` | Yes — "Analytics" | `analytics` | Complete |
| `ProfilePage` | Yes — "Profile" | `profile` | Complete — edit form + change password connected to API |
| `SettingsPage` | Yes — "Settings" | `settings` | Complete — hardware/AI/privacy toggles, all localStorage |
| `OnboardingPage` | No (post-register, once) | `onboarding` | Complete — 4-step wizard, shown once after first login |
| `CodingInterviewPage` | Yes — "Coding" | `coding` | Complete — Monaco Editor, Run Code, Submit, results panel |

**Page navigation flow:**
`landing` → `login` → `onboarding` (first time) or `dashboard` (returning) → `subject` → `interview` → `result`
Sidebar nav: `dashboard` ↔ `interview` ↔ `coding` ↔ `analytics` ↔ `profile` ↔ `settings`

**Pages NOT yet built:**

| Page | Page State | Priority |
|---|---|---|
| ResumeAnalyserPage | `resume` | Phase 9 |
| JDAnalyserPage | `jd` | Phase 10 |
| ReplayPage | `replay` | Phase 11 |

---

## Real Database Schema

Verified directly from PostgreSQL on March 12, 2026.

### `users`
```
id            integer  PK
name          varchar
email         varchar  UNIQUE
password_hash varchar
branch        varchar
year          integer
avatar_url    varchar        ← added Phase 5b
college       varchar        ← added Phase 5b
created_at    timestamp      DEFAULT NOW()
```

### `subjects`
```
id    integer  PK
name  varchar  UNIQUE
type  varchar  DEFAULT 'technical'   (values: 'technical' | 'hr')
```
Data: 7 subjects — DSA, OOPS, System Design, DBMS, OS & Networking, Machine Learning, Behavioral (hr)

### `topics`
```
id          integer  PK
subject_id  integer  FK → subjects.id
name        varchar
```
Data: 52 topics total

### `subtopics`
```
id        integer  PK
topic_id  integer  FK → topics.id
name      varchar
```
Data: 129 subtopics total

### `questions`
```
id               integer  PK
subject_id       integer  FK → subjects.id
topic_id         integer  FK → topics.id
subtopic_id      integer  FK → subtopics.id
title            varchar
difficulty       varchar       (beginner | intermediate | advanced | expert)
type             varchar       (technical | hr)
question_text    text
ideal_answer     text
tags             varchar
companies        varchar
time_complexity  varchar
space_complexity varchar
```
Data: 133 questions — 30 beginner, 58 intermediate, 38 advanced, 7 expert. 127 technical, 6 hr.

### `interview_sessions`
```
id                integer   PK
user_id           integer   FK → users.id
interview_type    varchar   (technical | hr)
subject_id        integer   FK → subjects.id
topic_id          integer   FK → topics.id
subtopic_id       integer   FK → subtopics.id
difficulty        varchar
status            varchar   DEFAULT 'active'   (active | completed | abandoned)
total_questions   integer   DEFAULT 0
questions_answered integer  DEFAULT 0
start_time        timestamp
end_time          timestamp
final_score       float
```

### `answers`
```
id              integer  PK
session_id      integer  FK → interview_sessions.id
question_id     integer  FK → questions.id
user_answer     text
semantic_score  float    ← added Phase 5b
keyword_score   float    ← added Phase 5b
depth_score     float    ← added Phase 5b
structure_score float    ← added Phase 5b
nlp_score       float    (weighted NLP total, 0–100)
voice_score     float    (0–100)
face_score      float    (0–100)
total_score     float    (weighted final, 0–100)
feedback        text     ← added Phase 5b
```

### `user_preferences`
```
id                        integer   PK
user_id                   integer   FK → users.id
preferred_topics          text
difficulty_level          varchar
interview_type_preference varchar
created_at                timestamp
updated_at                timestamp
```
⚠️ This table exists in the DB but has NO SQLAlchemy model file and is never written to by any route.

### Dropped Tables (removed Phase 5b)
- `scores` — was duplicate of answers columns
- `analytics` — was never written to
- `conversation_memory` — was duplicate of answers + question FK

---

## Real Backend API

All registered in `main.py`. Verified against actual route files.

| Method | Full Endpoint | Route File | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | auth_routes.py | No |
| POST | `/auth/login` | auth_routes.py | No |
| PUT | `/auth/profile` | auth_routes.py | Yes |
| PUT | `/auth/password` | auth_routes.py | Yes |
| GET | `/interview/subjects` | interview_routes.py | Yes |
| GET | `/interview/topics?subject_id=X` | interview_routes.py | Yes |
| GET | `/interview/subtopics?topic_id=X` | interview_routes.py | Yes |
| GET | `/interview/questions` | interview_routes.py | Yes |
| POST | `/interview/start` | interview_routes.py | Yes |
| GET | `/interview/question` | interview_routes.py | Yes |
| POST | `/interview/seed-questions` | interview_routes.py | Yes |
| POST | `/interview/answer` | answer_routes.py | Yes |
| GET | `/analytics/me` | analytics_routes.py | Yes |
| POST | `/api/voice/analyze` | voice_routes.py | No |
| POST | `/api/vision/analyze` | vision_routes.py | No |

**Exact request/response shapes:**

`POST /auth/login` → `{email, password}` → `{access_token, token_type, user: {id, name, email, branch, year, college, avatar_url}}`
`POST /auth/register` → `{name, email, password, branch?, year?}` → user object
`POST /interview/start` → `{interview_type, subject_id, difficulty, topic_id?, subtopic_id?}` → `{session_id, subject_name, topic_name, difficulty, start_time, message}`
`GET /interview/question` → `?subject_id=X&difficulty=X&session_id=X&topic_id=X&subtopic_id=X` → `{question_id, title, question_text, type, subject_name, topic_name, subtopic_name, difficulty}`
`POST /interview/answer` → `{session_id, question_id, user_answer, voice_score?, face_score?}` → `{answer_id, session_id, question_id, user_answer, semantic_score, keyword_score, depth_score, structure_score, nlp_score, voice_score, face_score, total_score, feedback, engine}`
`GET /analytics/me` → `{total_sessions, total_answers, avg_nlp_score, avg_total_score, best_score, strongest_topic, weakest_topic, subject_breakdown, topic_breakdown, recent_sessions, performance}`
`POST /api/voice/analyze` → multipart `audio` file → `{overall_voice_score, transcript, duration_seconds, feedback, details: {pace, filler_words, confidence, silence, energy}}`
`POST /api/vision/analyze` → `{image: base64, session_id, question_id}` → `{eye_contact, head_stability, emotion}`

**Backend endpoints NOT yet built (needed for future phases):**

| Endpoint | Phase | Purpose |
|---|---|---|
| `POST /ai/followup` | Phase 8 | Generate AI follow-up question |
| `POST /resume/analyse` | Phase 9 | PDF upload → extract + AI questions |
| `POST /jd/analyse` | Phase 10 | JD text → gap analysis + prep plan |
| `GET /interview/sessions` | Phase 11 | List user's past sessions |
| `GET /interview/sessions/{id}/answers` | Phase 11 | Full Q&A for a session |
| `GET /reports/session/{id}` | Phase 12 | Generate + download PDF report |

---

## Score Formulas (verified against evaluation_service.py)

```
Technical: 70% NLP + 20% Voice + 10% Face

HR:        50% NLP(LLM) + 30% Voice + 20% Face
           (NOTE: CLAUDE.md says 40/30/20/10 — code actually does 50/30/20)

NLP:       45% semantic + 25% keyword + 20% depth + 10% structure
Voice:     25% pace + 25% filler + 20% confidence + 15% silence + 15% energy
```

---

## Key Files Reference

| File | Purpose | Note |
|---|---|---|
| `main.py` | FastAPI entry, all routers registered | |
| `database.py` | PostgreSQL engine + Base | |
| `ai_engine/nlp_engine.py` | NLP scoring + CONCEPT_MAP (7 subjects) | Returns `overall_score` key (not `nlp_score`) |
| `ai_engine/hr_engine.py` | Ollama qwen2.5-coder:7b HR evaluation | |
| `ai_engine/voice_engine.py` | Whisper + librosa + parselmouth | Running on CPU |
| `ai_engine/vision_engine.py` | MediaPipe FaceMesh 0.10.11 | DO NOT upgrade mediapipe |
| `services/evaluation_service.py` | Routes hr vs technical, saves full breakdown | |
| `services/analytics_service.py` | Computes analytics on-the-fly | |
| `services/interview_service.py` | Adaptive difficulty + no-repeat | |
| `services/auth_service.py` | Register + login logic | |
| `schemas/user_schema.py` | UserRegister, UserLogin, UserResponse, TokenResponse | Includes college, avatar_url |
| `schemas/answer_schema.py` | SubmitAnswerRequest, SubmitAnswerResponse | Includes depth_score |
| `frontend/src/App.jsx` | All 9 React pages in one file | ~1600 lines |
| `frontend/src/VoiceRecorder.jsx` | Audio recording + WAV builder + Whisper call | DO NOT modify |
| `frontend/src/VisionRecorder.jsx` | Camera capture + MediaPipe call | DO NOT modify |
| `front_idea/` | 6 Figma design PNG screenshots | Reference for UI matching |
| `MISSING_PAGES_DESIGN.md` | ASCII wireframes for 7 unbuilt pages | Reference for Phase 6+ |

---

## Known Issues

| Issue | Severity | Fix |
|---|---|---|
| Whisper runs on CPU (torch.cuda not detecting GPU) | Low — works, just slower | Fix in Phase 13 |
| Parselmouth pitch occasionally 0 Hz | Low — librosa fallback covers it | No action needed |
| mediapipe MUST be 0.10.11 on Windows | Constraint | DO NOT upgrade |
| `user_preferences` table has no SQLAlchemy model file and is never written to | Low | Add model or drop table when needed |

---

## Do NOT

- Upgrade mediapipe beyond 0.10.11
- Modify `VoiceRecorder.jsx` or `VisionRecorder.jsx`
- Change multimodal score weights without being asked
- Add features outside current phase scope
- Auto-commit or auto-push to git

---

## Full Roadmap

### Phase 6 — Profile Edit + Settings + Onboarding — COMPLETED

**All tasks done:**
- Deleted dead service files: `memory_service.py`, `vision_service.py`, `voice_service.py`
- `UserResponse` now includes `college` and `avatar_url`
- `SubmitAnswerResponse` now includes `depth_score`
- `interview_sessions.status` default aligned to `"active"`
- `PUT /auth/profile` — update name, branch, year, college
- `PUT /auth/password` — verify current password + update hash
- `ProfilePage` — full edit form + change password section wired to API, updates root user state + localStorage
- `SettingsPage` — hardware dropdowns, Whisper model, difficulty, privacy toggles, all localStorage
- `OnboardingPage` — 4-step wizard (Welcome, Hardware, Goals, Weak Topics), shown once after first login

---

### Phase 7 — Coding Interview Round — COMPLETED

**What was built:**
- `schemas/code_schema.py` — CodeRunRequest, TestCaseResult, CodeRunResponse
- `services/code_service.py` — sandboxed subprocess execution, safety blocklist (no os/sys/subprocess/eval/exec), 5s timeout, JSON output comparison, Two Sum problem with 3 test cases hardcoded
- `routes/code_routes.py` — `POST /code/run` (Python only, C++/Java planned)
- `CodingInterviewPage` — Monaco Editor (`@monaco-editor/react@4.7.0`), language selector (Python/C++/Java) with starter code, 30-min timer, Run Code → results table, Submit → score preview → ResultsPage
- Sidebar: "Coding" nav item added

---

### Phase 8 — AI Follow-up Questions

**New backend route:**
`POST /ai/followup` — `{question_text, user_answer, session_id}` → Ollama → `{followup_question}`

**InterviewRoomPage change:**
- After submit answer + show score: if score < 70, fetch and show follow-up question
- Follow-up answer submitted as a separate answer record
- Adds 1–2 dynamic turns per question

---

### Phase 9 — Resume-Based Questions

**Install:** `pip install PyMuPDF`

**New backend route:**
`POST /resume/analyse` — multipart PDF → PyMuPDF extract → Ollama → `{skills, ats_score, suggestions, questions: [5 items]}`

**New frontend page:** `ResumeAnalyserPage`
- Drag-and-drop PDF upload zone
- After upload: ATS score ring + skill tags + suggestions list + 5 AI questions
- [Start Interview with These Questions] → passes custom questions to InterviewRoomPage

---

### Phase 10 — JD Gap Analyser

**New backend route:**
`POST /jd/analyse` — `{jd_text}` → Ollama extracts skills → cross-reference with `/analytics/me` → `{required_skills, match_scores, missing_skills, prep_plan}`

**New frontend page:** `JDAnalyserPage`
- Large textarea + [Analyse Gap] button
- Per-skill progress bars: green ≥70% / amber 40–70% / red <40%
- 7-day personalised prep plan card
- [Start Prep] → launches interview with weakest topics pre-selected

---

### Phase 11 — Interview Replay

**New backend routes:**
`GET /interview/sessions` → list user's sessions with answer count + avg score
`GET /interview/sessions/{id}/answers` → all Q&A + scores + feedback for a session

**New frontend page:** `ReplayPage`
- Session selector dropdown (past 10 sessions)
- Q&A timeline: question card → answer card → score bars → feedback
- Score trend chart across questions (recharts LineChart)
- Behaviour summary (avg eye contact, total fillers, avg pace)

---

### Phase 12 — PDF Reports

**New backend route:**
`GET /reports/session/{id}` → generate PDF (reportlab or weasyprint) → return as file download

PDF contents: session info, full Q&A transcript, per-question score breakdown, AI feedback summary, improvement tips

---

### Phase 13 — Docker + Deploy

- Dockerfile (Python 3.11, all AI deps, CUDA drivers for Whisper GPU)
- docker-compose.yml (backend + postgres + volumes)
- Fix `torch.cuda` detection for Whisper GPU acceleration
- Frontend → Vercel (static build, `npm run build`)
- Backend → Render or Railway
- `.env` for `DATABASE_URL`, `JWT_SECRET`, `OLLAMA_URL`

---

## Frontend Design System

```
bg:      #0B0F1E   page background
cards:   #0F1629   card background
border:  rgba(255,255,255,0.07)
primary: #6366F1   indigo
success: #22C55E   green
warning: #F59E0B   amber
danger:  #EF4444   red
text:    #F1F5F9   primary
muted:   #94A3B8   secondary
faint:   #475569   labels
font:    Inter (Google Fonts)
routing: state-based (no React Router)
charts:  recharts (RadarChart, AreaChart)
```

---

*Last updated: March 12, 2026 — Phase 7 complete*
*Next: Phase 8 — AI Follow-up Questions (POST /ai/followup via Ollama, InterviewRoomPage integration)*
