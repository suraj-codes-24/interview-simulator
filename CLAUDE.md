# Interview Simulator — Claude Instructions

## Project Overview
AI-powered multimodal mock interview platform. FastAPI backend + React/Vite frontend.

## Locations
- **Root:** `C:\Users\suraj\Desktop\interview_simulator`
- **Backend:** `http://localhost:8000` — run with `uvicorn main:app --reload`
- **Frontend:** `http://localhost:5173` — run with `cd frontend && npm run dev`
- **API Docs:** `http://localhost:8000/docs`
- **Database:** PostgreSQL — `interview_db`, user `postgres`
- **Test Login:** `suraj@test.com` / `test123`

## Tech Stack
- Python 3.11.8, Node v24
- FastAPI + SQLAlchemy + PostgreSQL (psycopg2)
- React + Vite + Tailwind (CSS-in-JSX)
- Ollama (`qwen2.5-coder:7b`) on local GPU (NVIDIA RTX 4050)
- Whisper (local, CPU), librosa, parselmouth, MediaPipe 0.10.11

## Key Files
| File | Purpose |
|------|---------|
| `main.py` | FastAPI entry point, all routers registered |
| `database.py` | PostgreSQL engine + Base |
| `ai_engine/nlp_engine.py` | NLP scoring + CONCEPT_MAP |
| `ai_engine/hr_engine.py` | Ollama HR evaluation |
| `ai_engine/voice_engine.py` | Whisper + librosa + parselmouth |
| `ai_engine/vision_engine.py` | MediaPipe FaceMesh |
| `services/evaluation_service.py` | Routes hr vs technical + multimodal scoring |
| `services/interview_service.py` | Adaptive difficulty + no-repeat questions |
| `routes/interview_routes.py` | Session, question endpoints |
| `routes/answer_routes.py` | Answer submission |
| `routes/voice_routes.py` | `/api/voice/analyze` |
| `routes/vision_routes.py` | `/api/vision/analyze` |
| `frontend/src/` | React pages + components |

## Score Formulas
```
Technical: 70% NLP + 20% Voice + 10% Face
HR:        40% LLM + 30% Voice + 20% Face + 10% NLP

NLP:   45% semantic + 25% keywords + 20% depth + 10% structure
Voice: 25% pace + 25% filler + 20% confidence + 15% silence + 15% energy
```

## API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | `{email, password}` → `{access_token}` |
| POST | `/auth/register` | `{full_name, email, password, branch, year}` |
| GET | `/interview/subjects` | List all subjects |
| GET | `/interview/topics?subject_id=X` | Topics for subject |
| GET | `/interview/subtopics?topic_id=X` | Subtopics |
| POST | `/interview/start` | Start session → `{session_id}` |
| GET | `/interview/question` | Next adaptive question |
| POST | `/answer/submit` | Submit answer with multimodal scores |
| POST | `/api/voice/analyze` | Analyze audio file |
| POST | `/api/vision/analyze` | Analyze video frame |
| GET | `/analytics/me` | User analytics |

## Coding Conventions
- Use explicit if-blocks — no lambdas
- Follow existing patterns in each file before adding new code
- No over-engineering — keep additions minimal and focused
- Backend: Python snake_case; Frontend: React camelCase/PascalCase

## Frontend Design System
- Background: `#0F172A` | Cards: `#1E293B` | Border: `#334155`
- Primary: `#6366F1` (indigo) | Success: `#22C55E` | Warning: `#F59E0B`
- Text: `#F1F5F9` primary, `#94A3B8` secondary | Font: Inter
- Style: Glassmorphism cards

## Current Phase Status
- Phase 1 — Core Backend: DONE
- Phase 2 — Intelligence Layer (Ollama HR + adaptive difficulty): DONE
- Phase 3 — Voice Analysis (Whisper + librosa + parselmouth): DONE
- Phase 4 — Face Analysis (MediaPipe + multimodal scoring): DONE
- Phase 5 — Frontend Redesign: IN PROGRESS (next priority)
- Phase 6 — Coding Interview (Monaco Editor): PLANNED
- Phase 7 — AI Follow-ups + Resume questions: PLANNED
- Phase 8 — PDF Reports + Deployment: PLANNED

## Known Issues
- Whisper runs on CPU (CUDA not detected by torch) — needs fix
- Parselmouth pitch occasionally returns 0 Hz (librosa fallback covers it)
- mediapipe MUST be version `0.10.11` on Windows — do not upgrade
- Frontend needs full redesign to match Figma

## Do NOT
- Upgrade mediapipe beyond 0.10.11
- Change the multimodal score weights without being asked
- Add features outside the scope of the current request
- Auto-commit or auto-push to git
