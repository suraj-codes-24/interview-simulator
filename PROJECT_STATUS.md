# 🧠 AI Multimodal Interview Simulator
### Project Status & Complete Roadmap
**GitHub:** https://github.com/suraj-codes-24/interview-simulator  
**Stack:** FastAPI + PostgreSQL + sentence-transformers + React + Vite  
**Developer:** Suraj | PSIT Kanpur | B.Tech CSE (4th Sem)

---

## ✅ PHASE 1 — CORE TEXT ENGINE (COMPLETE)

### Backend
- [x] Project folder structure set up
- [x] PostgreSQL database connected (`interview_db`)
- [x] SQLAlchemy models created:
  - `users`, `interview_sessions`, `questions`, `answers`, `scores`, `subjects`, `topics`, `subtopics`
- [x] JWT Authentication (register + login)
- [x] Question bank seeded:
  - 7 subjects (DSA, OOPS, System Design, DBMS, OS & Networking, Machine Learning, Behavioral)
  - 52 topics
  - 129 subtopics
  - 133 questions with ideal answers
- [x] Subject type tagging (`technical` / `hr`)
- [x] Interview session creation (`POST /interview/start`)
- [x] Question fetching by subject + difficulty (`GET /interview/question`)
- [x] Answer submission (`POST /interview/answer`)
- [x] NLP Evaluation Engine (`ai_engine/nlp_engine.py`):
  - Semantic similarity using `sentence-transformers/all-MiniLM-L6-v2`
  - Keyword coverage with synonym map
  - Structure/length scoring
  - Calibrated final score formula:
    - 50% Semantic Similarity
    - 30% Keyword Coverage
    - 20% Structure Quality
- [x] Analytics endpoint (`GET /analytics/me`):
  - Total sessions, total answers
  - Average NLP score
  - Topic breakdown
  - Strongest / weakest topic

### Frontend
- [x] React + Vite setup
- [x] Login / Register page
- [x] Dashboard with Technical / HR tabs
- [x] Subject selection grid (fetched from API)
- [x] Difficulty selector (beginner / intermediate / advanced)
- [x] Interview room (question display + answer textarea)
- [x] Score breakdown after answer:
  - Semantic score
  - Keyword score
  - Structure score
  - Final NLP score + feedback
- [x] Analytics page with topic performance bars
- [x] Dark theme UI (Space Mono + Outfit fonts)

### DevOps
- [x] GitHub repo created and connected
- [x] All code pushed to `main` branch

---

## 🔄 PHASE 2 — CONVERSATION MEMORY + HR LLM (NEXT)

### Step 1 — Conversation Memory System
- [ ] Create `conversation_memory` table in DB:
  - `session_id`, `question_id`, `question_text`, `user_answer`, `score`, `topic`, `timestamp`
- [ ] Memory Manager service (`services/memory_service.py`):
  - Save each Q&A interaction to memory
  - Retrieve last 3 interactions (memory window)
- [ ] Connect memory to interview flow:
  - After each answer → update memory
  - Before next question → read memory

### Step 2 — Follow-Up Question Logic
- [ ] Add `follow_up_questions` field to questions table (list of question IDs)
- [ ] Follow-up trigger logic:
  - score >= 8 → ask follow-up on same topic
  - score 5–7 → next question same difficulty
  - score < 5 → reduce difficulty
- [ ] Update `GET /interview/question` to support follow-up mode

### Step 3 — Adaptive Interview Engine
- [ ] Create `ai_engine/adaptive_engine.py`
- [ ] Session state tracking:
  - current topic, current difficulty, question number
- [ ] Difficulty progression logic:
  - score >= 8 → upgrade difficulty
  - score 5–7 → keep same
  - score < 5 → downgrade
- [ ] Topic queue system (Arrays → Trees → Graphs etc.)
- [ ] Avoid question repetition within a session

### Step 4 — HR LLM Engine (Ollama + Llama)
- [ ] Install and configure Ollama locally
- [ ] Pull Llama model (`ollama pull llama3`)
- [ ] Create `ai_engine/hr_engine.py`:
  - Prompt design for behavioral evaluation
  - Parse JSON response (clarity, leadership, communication, structure)
  - Return HR score + feedback
- [ ] Connect HR engine to answer submission for Behavioral subject
- [ ] Update score aggregator for HR formula:
  - 40% LLM score
  - 30% Voice (placeholder until Phase 3)
  - 20% Face (placeholder until Phase 4)
  - 10% NLP

---

## 🎤 PHASE 3 — VOICE ANALYSIS

### Step 1 — Audio Capture (Frontend)
- [ ] Add `MediaRecorder` API to InterviewRoom
- [ ] Record audio while user types/speaks answer
- [ ] Send audio blob to backend (`POST /interview/voice`)

### Step 2 — Voice Analysis Engine (Backend)
- [ ] Install `librosa`, `parselmouth`, `SpeechRecognition`
- [ ] Create `ai_engine/voice_engine.py`:
  - Extract features:
    - Speaking rate (words per minute)
    - Pause frequency
    - Pitch variation / stability
    - Filler word detection (um, uh, like)
  - Voice score formula:
    - 30% Fluency
    - 25% Pace
    - 25% Pitch stability
    - 20% Filler word control

### Step 3 — Integrate Voice Score
- [ ] Add `voice_score` to answers table
- [ ] Update score aggregator:
  - Technical: 70% NLP + 20% Voice + 10% Face
  - HR: 40% LLM + 30% Voice + 20% Face + 10% NLP
- [ ] Show voice breakdown in frontend result card

---

## 👁️ PHASE 4 — FACE ANALYSIS

### Step 1 — Video Capture (Frontend)
- [ ] Add `WebRTC` / `getUserMedia` to InterviewRoom
- [ ] Show live camera feed during interview
- [ ] Capture frames and send to backend (`POST /interview/vision`)

### Step 2 — Face Analysis Engine (Backend)
- [ ] Install `opencv-python`, `mediapipe`
- [ ] Create `ai_engine/vision_engine.py`:
  - Detect features:
    - Eye contact ratio (frames with eye contact / total frames)
    - Head movement / stability
    - Emotion detection (calm, nervous, confident)
  - Face score formula:
- [x] Install `opencv-python`, `mediapipe`
- [x] Create `ai_engine/vision_engine.py`:
  - [x] Eye contact ratio
  - [x] Head stability
  - [x] Basic emotion detection (Calm/Confident/Nervous)

### Step 3 — Integrate Face Score
- [x] Add `face_score` to answers table
- [x] Aggregate vision scores on frontend and submit with answer
- [x] Update score aggregator:
  - Technical: 70% NLP + 20% Voice + 10% Face
  - HR: 40% LLM + 30% Voice + 20% Face + 10% NLP
- [x] Show face breakdown in frontend result card

---

## 🏗️ PHASE 5 — ADVANCED ANALYTICS & DASHBOARD (NEXT)

- [ ] Score progression chart over time (line chart)
- [ ] Per-topic radar chart (strengths vs weaknesses)
- [ ] Confidence trend tracking (voice + face over sessions)
- [ ] Interview history page (past sessions list)
- [ ] Session detail view (all Q&As with scores)
- [ ] Downloadable performance report (PDF)
- [ ] Recommendations engine:
  - "You should practice Dynamic Programming more"
  - "Your voice confidence improved by 12% this week"

---

## 🤖 PHASE 6 — AI AVATAR INTERVIEWER

- [ ] AI avatar UI component (`components/AIAvatar.jsx`)
  - Animated talking head or simple visual
- [ ] Text-to-speech for questions (browser Web Speech API or ElevenLabs)
- [ ] Context-aware follow-up generation using Ollama:
  - Send last answer → generate follow-up question
  - Prompt: "Based on this answer, ask a deeper follow-up"
- [ ] Conversation mode:
  - AI speaks question
  - User speaks answer
  - AI responds with feedback + next question
- [ ] Interview personality modes:
  - Friendly (campus interviews)
  - Strict (FAANG style)
  - HR (behavioral focused)

---

## 🚀 PHASE 7 — DEPLOYMENT

### Backend
- [ ] Dockerize FastAPI app
- [ ] Deploy on Render (free tier)
- [ ] Set up environment variables (DB, JWT secret)
- [ ] Configure CORS for production

### Frontend
- [ ] Build React app (`npm run build`)
- [ ] Deploy on Vercel
- [ ] Connect to production backend URL

### Database
- [ ] Migrate PostgreSQL to Render managed DB
  or use Supabase (free PostgreSQL hosting)

---

## 🗂️ CURRENT FILE STRUCTURE

```
interview_simulator/
│
├── main.py
├── database.py
├── requirements.txt
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
│
├── models/
│   ├── user.py
│   ├── subject.py
│   ├── topic.py
│   ├── subtopic.py
│   ├── interview_session.py
│   ├── question.py
│   ├── answer.py
│   └── score.py
│
├── routes/
│   ├── auth_routes.py
│   ├── interview_routes.py
│   └── analytics_routes.py
│
├── services/
│   ├── interview_service.py
│   └── analytics_service.py
│
├── ai_engine/
│   └── nlp_engine.py          ← DONE
│   (hr_engine.py)             ← Phase 2
│   (voice_engine.py)          ← Phase 3
│   (vision_engine.py)         ← Phase 4
│   (adaptive_engine.py)       ← Phase 2
│
├── scoring/
│   └── score_aggregator.py
│
├── data/
│   ├── seed.py
│   └── question_bank.py
│
└── frontend/
    └── src/
        ├── App.jsx             ← DONE
        └── main.jsx
```

---

## 📋 QUICK PHASE SUMMARY

| Phase | What | Status |
|-------|------|--------|
| Phase 1 | Auth + NLP Engine + Question Bank + Frontend | ✅ Complete |
| Phase 2 | Conversation Memory + Follow-ups + Adaptive Engine + Ollama HR | 🔲 Next |
| Phase 3 | Voice Analysis (librosa + parselmouth + Whisper) | ✅ Complete |
| Phase 4 | Face Analysis (OpenCV + MediaPipe) | ✅ Complete |
| Phase 5 | Advanced Analytics + Charts + Reports | 🔲 Pending |
| Phase 6 | AI Avatar + Conversation Mode + TTS | 🔲 Pending |
| Phase 7 | Docker + Render + Vercel Deployment | 🔲 Pending |

---

## 💡 NOTES

- Do phases in order — each builds on the previous
- Phase 2 has zero new library installs (except Ollama) — good starting point
- Voice and face need hardware testing — do locally first
- Keep question bank growing — more questions = better interviews
- Every phase = a new talking point in your placement interviews

---

*Last updated: Phase 1 complete — ready to begin Phase 2*
