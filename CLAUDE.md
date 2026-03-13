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
- React + Vite (CSS-in-JSX, no Tailwind classes — inline styles)
- Ollama (`qwen2.5-coder:7b`) on local GPU (NVIDIA RTX 4050)
- Whisper (local, CPU), librosa, parselmouth, MediaPipe 0.10.11
- Monaco Editor (`@monaco-editor/react@4.7.0`) for coding interviews
- recharts for analytics charts
- reportlab for PDF report generation
- PyMuPDF for resume PDF parsing

## Key Files
| File | Purpose |
|------|---------|
| `main.py` | FastAPI entry point, all 11 routers registered |
| `database.py` | PostgreSQL engine + Base |
| `ai_engine/nlp_engine.py` | NLP scoring + CONCEPT_MAP (79 concepts) |
| `ai_engine/hr_engine.py` | Ollama HR evaluation |
| `ai_engine/voice_engine.py` | Whisper + librosa + parselmouth |
| `ai_engine/vision_engine.py` | MediaPipe FaceMesh |
| `services/evaluation_service.py` | Routes hr vs technical + multimodal scoring |
| `services/interview_service.py` | Adaptive difficulty + no-repeat questions |
| `services/code_service.py` | Sandboxed Python code execution |
| `services/ollama_utils.py` | Centralized Ollama API wrapper |
| `services/followup_service.py` | AI follow-up question generation |
| `services/resume_service.py` | Resume PDF analysis via Ollama |
| `services/jd_service.py` | JD gap analysis via Ollama |
| `services/report_service.py` | PDF report generation |
| `services/session_feedback_service.py` | AI coaching summary |
| `frontend/src/App.jsx` | All 14 pages in one file (~3200 lines) |
| `frontend/src/VoiceRecorder.jsx` | Audio recording (do NOT modify) |
| `frontend/src/VisionRecorder.jsx` | Camera + MediaPipe (do NOT modify) |

## Score Formulas
```
Technical: 70% NLP + 20% Voice + 10% Face
HR:        50% NLP + 30% Voice + 20% Face

NLP:   45% semantic + 25% keywords + 20% depth + 10% structure
Voice: 25% pace + 25% filler + 20% confidence + 15% silence + 15% energy
```

## API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | `{email, password}` → `{access_token, user}` |
| POST | `/auth/register` | `{name, email, password, branch, year}` |
| PUT | `/auth/profile` | Update user profile |
| PUT | `/auth/password` | Change password |
| GET | `/interview/subjects` | List all subjects |
| GET | `/interview/topics?subject_id=X` | Topics for subject |
| GET | `/interview/subtopics?topic_id=X` | Subtopics |
| POST | `/interview/start` | Start session → `{session_id}` |
| GET | `/interview/question` | Next adaptive question |
| POST | `/interview/answer` | Submit answer with multimodal scores |
| POST | `/api/voice/analyze` | Analyze audio file |
| POST | `/api/vision/analyze` | Analyze video frame |
| GET | `/analytics/me` | User analytics |
| POST | `/code/run` | Execute code in sandbox |
| POST | `/ai/followup` | Generate AI follow-up question |
| POST | `/resume/analyse` | Analyze resume PDF |
| POST | `/jd/analyse` | JD gap analysis |
| GET | `/reports/session/{id}` | Download PDF report |

## Coding Conventions
- Use explicit if-blocks — no lambdas
- Follow existing patterns in each file before adding new code
- No over-engineering — keep additions minimal and focused
- Backend: Python snake_case; Frontend: React camelCase/PascalCase
- Difficulty levels: `beginner`, `intermediate`, `advanced`, `expert`

## Frontend Design System
- Background: `#0B0F1E` | Cards: `#0F1629` | Border: `rgba(255,255,255,0.07)`
- Primary: `#6366F1` (indigo) | Success: `#22C55E` | Warning: `#F59E0B`
- Text: `#F1F5F9` primary, `#94A3B8` secondary | Font: Inter
- Style: Glassmorphism cards, CSS keyframe animations

## Current Phase Status
- Phase 1 — Core Backend (JWT, PostgreSQL, NLP, 133 questions): DONE
- Phase 2 — Intelligence Layer (Ollama HR + adaptive difficulty): DONE
- Phase 3 — Voice Analysis (Whisper + librosa + parselmouth): DONE
- Phase 4 — Face Analysis (MediaPipe + multimodal scoring): DONE
- Phase 5 — Frontend Redesign (14 pages, recharts, state-based routing): DONE
- Phase 5b — DB Redesign (drop dead tables, enrich answers/users/sessions): DONE
- Phase 6 — Profile + Settings + Onboarding pages: DONE
- Phase 7 — Coding Interview (Monaco Editor + sandboxed execution): DONE
- Phase 8 — AI Follow-up Questions (Ollama): DONE
- Phase 9 — Resume Analyser (PyMuPDF + Ollama): DONE
- Phase 10 — JD Gap Analyser (Ollama + difflib): DONE
- Phase 11 — Interview Replay (transcript timeline): DONE
- Phase 12 — PDF Reports (reportlab): DONE
- Phase 12.5 — UX & stability improvements: DONE
- Phase 14 — Question Bank Expansion (133 → 482 questions, NLP CONCEPT_MAP extended): DONE
- Phase 13 — Docker + Deploy: PLANNED

## Known Issues
- Whisper runs on CPU (torch.cuda not detecting GPU) — needs fix in Phase 13
- Parselmouth pitch occasionally returns 0 Hz (librosa fallback covers it)
- mediapipe MUST be version `0.10.11` on Windows — do not upgrade

## Do NOT
- Upgrade mediapipe beyond 0.10.11
- Change the multimodal score weights without being asked
- Add features outside the scope of the current request
- Auto-commit or auto-push to git
