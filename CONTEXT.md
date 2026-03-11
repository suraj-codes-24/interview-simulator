# 🤖 AI Multimodal Interview Simulator — Project Context
> Use this file to continue development in a new session

---

## 📍 Project Info
| Field | Value |
|-------|-------|
| **Location** | `C:\Users\suraj\Desktop\interview_simulator` |
| **GitHub** | https://github.com/suraj-codes-24/interview-simulator |
| **Backend** | FastAPI on `http://localhost:8000` |
| **Frontend** | React + Vite on `http://localhost:5173` |
| **Database** | PostgreSQL — `interview_db` |
| **DB User** | `postgres` |
| **Test Login** | `suraj@test.com` / `test123` |
| **GPU** | NVIDIA RTX 4050 Laptop (Ollama on CUDA) |
| **Stack** | FastAPI + PostgreSQL + React + Vite + Tailwind |

---

## ⚠️ FIRST THING TO DO IN A NEW SESSION
```bash
cd C:\Users\suraj\Desktop\interview_simulator
git reset --hard HEAD
git clean -fd
git status  # should say "nothing to commit, working tree clean"
```

Then start both servers:
```bash
# Terminal 1 - Backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## ✅ PHASES COMPLETED

### Phase 1 — Core Backend ✅
- JWT Authentication (login + register)
- PostgreSQL models — users, sessions, questions, answers
- 7 subjects, 52 topics, 129 subtopics, 133 questions seeded
- Subject types: `technical` / `hr`
- NLP Engine with full CONCEPT_MAP covering:
  - DSA (arrays, linked lists, trees, graphs, sorting, DP...)
  - OOP (encapsulation, inheritance, polymorphism...)
  - OS (processes, threads, deadlock, scheduling...)
  - DBMS (normalization, ACID, indexing, joins...)
  - Networks (TCP/IP, HTTP, DNS, OSI...)
  - System Design (load balancer, caching, CAP theorem...)
  - ML (supervised, neural networks, transformers...)
- Score formula: 45% semantic + 25% keyword + 20% depth + 10% structure
- Analytics endpoint (`GET /analytics/me`)

### Phase 2 — Intelligence Layer ✅
- Conversation memory (`models/conversation_memory.py`)
- Adaptive difficulty engine — adjusts based on last score
- No-repeat questions within a session
- HR Engine via Ollama `qwen2.5-coder:7b` (local GPU)
- Routing: `question.type == "hr"` → HR engine, else → NLP engine

### Phase 3 — Voice Analysis ✅
- **Recording:** `ScriptProcessorNode` in browser — raw PCM float32 (no ffmpeg needed)
- **Transcription:** OpenAI Whisper (local, ~1s on CPU)
- **Pace:** WPM calculation, scored 50-100
- **Filler words:** detects um/uh/like/basically etc.
- **Pitch/Confidence:** parselmouth with multi-floor detection + librosa fallback
- **Silence ratio:** librosa voice activity detection (top_db=15)
- **Energy:** librosa RMS energy
- **Score weights:** pace 25% + filler 25% + confidence 20% + silence 15% + energy 15%
- **Endpoint:** `POST /api/voice/analyze`
- **Key files:** `ai_engine/voice_engine.py`, `routes/voice_routes.py`, `VoiceRecorder.jsx`

### Phase 4 — Face Analysis + Multimodal Scoring ✅
- **MediaPipe FaceMesh** — 468 facial landmarks
- **Eye contact** — iris centering in eye sockets
- **Head stability** — nose tip position tracking
- **Emotion detection** — calm / confident / nervous
- **Multimodal scoring formula:**
  - Technical: 70% NLP + 20% Voice + 10% Face
  - HR: 40% LLM + 30% Voice + 20% Face + 10% NLP
- Live camera sidebar in interview room
- Score breakdown card (NLP + Voice + Face)
- **Key files:** `ai_engine/vision_engine.py`, `routes/vision_routes.py`, `VisionRecorder.jsx`
- **Note:** mediapipe 0.10.11 required on Windows (not latest)

---

## 📁 Key File Structure
```
interview_simulator/
├── main.py                          ← FastAPI app entry point
├── database.py                      ← PostgreSQL connection
├── requirements.txt
├── ai_engine/
│   ├── nlp_engine.py               ← NLP scoring + CONCEPT_MAP
│   ├── hr_engine.py                ← Ollama HR evaluation
│   ├── voice_engine.py             ← Whisper + librosa + parselmouth
│   └── vision_engine.py            ← MediaPipe face analysis
├── models/
│   └── conversation_memory.py
├── services/
│   ├── interview_service.py        ← adaptive difficulty + no-repeat
│   ├── evaluation_service.py       ← routes hr vs technical + multimodal
│   ├── memory_service.py
│   └── vision_service.py
├── routes/
│   ├── interview_routes.py
│   ├── answer_routes.py
│   ├── voice_routes.py
│   └── vision_routes.py
├── schemas/
└── frontend/                       ← React + Vite (Figma design)
    └── src/app/components/pages/
        ├── LandingPage.tsx
        ├── LoginPage.tsx
        ├── DashboardPage.tsx
        ├── InterviewRoomPage.tsx
        ├── ResultsPage.tsx
        └── AnalyticsPage.tsx
```

---

## 🎨 Frontend Design System
- **Background:** `#0F172A` (dark navy)
- **Cards:** `#1E293B` with border `#334155`
- **Primary accent:** `#6366F1` (indigo)
- **Secondary:** `#22C55E` (green), `#F59E0B` (amber), `#EC4899` (pink)
- **Text:** `#F1F5F9` primary, `#94A3B8` secondary
- **Font:** Inter
- **Style:** Glassmorphism cards, framer-motion animations

### Target Page Designs:
1. **Landing** — split layout, feature cards 2x2, How It Works steps, stats bar
2. **Login** — split panel, left has live AI demo card, right has form + OAuth
3. **Interview Room** — AI avatar left, live camera right, circular metrics, live transcript
4. **Results** — overall ring score, 4 score cards, radar chart, per-question timeline, AI summary
5. **Analytics** — stat cards with sparklines, score progression chart, skills radar, topic mastery tags

---

## 🚀 NEXT SESSION PLAN

### Step 1 — Fix & Push
- [ ] `git reset --hard HEAD && git clean -fd`
- [ ] Verify backend + frontend both start cleanly
- [ ] `git push origin main`

### Step 2 — Frontend Redesign
- [ ] Rebuild all 5 pages to match Figma screenshots exactly
- [ ] Install recharts for Analytics + Results charts
- [ ] Navbar: Dashboard | Analytics | Interview tabs + user avatar
- [ ] Keep all existing API connections working

### Step 3 — Phase 5: Coding Interview Round
- [ ] Monaco Editor integration (VS Code in browser)
- [ ] LeetCode-style problems in DB
- [ ] Auto test case execution (backend sandboxed Python runner)
- [ ] AI reviews code quality + time complexity

### Step 4 — Phase 6: Interview Realism
- [ ] AI follow-up questions based on your answer
- [ ] Silence detection — AI prompts if you pause too long
- [ ] AI interviewer personality modes (strict / friendly / neutral)
- [ ] Per-answer detailed feedback with ideal answer comparison

### Step 5 — Phase 7: PDF Reports
- [ ] Downloadable PDF after every session
- [ ] Full session report: scores, transcript, feedback, action items

### Step 6 — Phase 8: Deployment
- [ ] Docker containerization
- [ ] Backend → Render
- [ ] Frontend → Vercel

---

## 🔧 Known Issues to Fix
- Whisper running on CPU (torch.cuda not detecting GPU) — needs fix
- Parselmouth pitch occasionally returns 0 Hz — librosa fallback works but improve
- mediapipe must be version `0.10.11` on Windows (not latest)
- Frontend needs full redesign to match Figma screenshots

---

## 💡 Feature Ideas Backlog
- AI follow-up questions (most important)
- Session video recording + replay
- Silence detection with AI prompts
- Company-specific question modes (Google, Amazon, Microsoft)
- Body language timestamp report
- Speaking pattern heatmap
- Daily practice streaks + badges
- Peer mock interview matching

---

## 🌟 Future Enhancements (Portfolio-Level)

### 1️⃣ Coding Interview Round
Full LeetCode-style coding environment inside the interview room.

**Backend Endpoint:**
```
POST /code/run
→ Receive user code
→ Execute in sandbox environment
→ Return output, runtime, errors
```

**AI Evaluation will analyze:** Time complexity, code quality, edge case handling, readability

---

### 2️⃣ AI Follow-Up Questions
Make the interviewer dynamic — generates follow-ups based on candidate's response.

**Example Flow:**
```
Question: Explain Binary Search
User answers →
AI follow-ups:
- What happens if the array contains duplicates?
- Can binary search work on a rotated array?
- What is the time complexity?
```

**Backend Endpoint:**
```
POST /ai/followup
Prompt: "The candidate answered: {answer}
Generate a realistic technical follow-up question."
```

---

### 3️⃣ Resume-Based Personalized Questions
User uploads resume → AI reads it → generates questions specific to their projects/skills.

**Implementation:** PyMuPDF to extract resume text → send to Ollama → generate questions → inject into interview flow.

---

### 4️⃣ Job Description Gap Analyser
User pastes a JD → AI compares it to their analytics → tells them exactly what to practice.

**Implementation:** Ollama extracts skills from JD → cross-reference with `GET /analytics/me` → generate gap report + 7-day prep plan.

---

### 5️⃣ Interview Replay System
Video playback of full interview with transcript timeline, score timeline, and behavior overlays.

---

## 🎯 Final Vision

| Feature | Status |
|---------|--------|
| NLP answer evaluation | ✅ Done |
| Voice confidence analysis | ✅ Done |
| Face behavior tracking | ✅ Done |
| Adaptive difficulty engine | ✅ Done |
| HR engine via Ollama | ✅ Done |
| Frontend redesign (Figma) | 🔄 Next |
| Coding interview + Monaco | 📋 Planned |
| AI follow-up questions | 📋 Planned |
| Resume-based questions | 📋 Planned |
| JD gap analyser | 📋 Planned |
| Interview replay system | 📋 Planned |
| PDF session reports | 📋 Planned |
| Docker + Deployment | 📋 Planned |

**Goal: A realistic AI-powered mock interview platform that feels like a real interview — not a quiz app.**

---

## 🛠️ Backend API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | `{email, password}` → `{access_token}` |
| POST | `/auth/register` | `{full_name, email, password, branch, year}` |
| GET | `/interview/subjects` | List all subjects |
| GET | `/interview/topics?subject_id=X` | Topics for subject |
| GET | `/interview/subtopics?topic_id=X` | Subtopics for topic |
| POST | `/interview/start` | Start session → `{session_id}` |
| GET | `/interview/question` | Get next question |
| POST | `/answer/submit` | Submit answer with scores |
| POST | `/api/voice/analyze` | Analyze audio file |
| POST | `/api/vision/analyze` | Analyze video frame |
| GET | `/analytics/me` | User analytics data |

---

## 🏗️ Score Formulas
```
Technical: 70% NLP + 20% Voice + 10% Face
HR:        40% LLM + 30% Voice + 20% Face + 10% NLP

NLP:   45% semantic + 25% keywords + 20% depth + 10% structure
Voice: 25% pace + 25% filler + 20% confidence + 15% silence + 15% energy
```

---

## 📅 Recommended Build Order

| Week | Task |
|------|------|
| Week 1 | Fix issues + Frontend redesign |
| Week 2 | Coding interview round (Monaco) |
| Week 3 | AI follow-up questions |
| Week 4 | Resume-based questions + JD analyser |
| Week 5 | Replay system + PDF reports |
| Week 6 | Docker + Deploy |

---

*Last updated: March 2026 | Phase 4 Complete | Ready for Claude Code session*
