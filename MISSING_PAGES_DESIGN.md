# Frontend Feature Design Spec
> AI Interview Simulator | UI wireframes for pages not yet fully implemented
> Design System: bg #0B0F1E | cards #0F1629 | accent #6366F1 | font Inter

> **NOTE:**
> Some pages listed here may already exist in `App.jsx` in a display-only form.
> This document describes the **full intended UI** for each page, including features not yet built.
> Refer to `CONTEXT.md` → *Frontend Pages — Real Status* for the actual implementation state.

---

## Shared Layout Rules
- Same sidebar as Dashboard: logo, nav items with icons, user section at bottom
- Top content area: page title left, action buttons right
- All cards: dark bg + rgba(255,255,255,0.07) border + 12px radius
- Primary: #6366F1 | Success: #22C55E | Warning: #F59E0B | Danger: #EF4444

---

## 1. ProfilePage
> Status: Display-only version exists in App.jsx. Edit form, password change, and danger zone NOT yet built.

Layout:
- Sidebar + main content
- Header: "Profile Settings" + [Save Changes] button (indigo)

Sections:
1. **Avatar card** — initials circle (indigo gradient), name, email, branch/year, [Change Photo]
2. **Stats row** — Interviews (total_sessions), Avg Score (avg_total_score), Streak (5 🔥) — fetched from GET /analytics/me
3. **Personal Information form** — Full Name, Email (read-only), Branch, Year (select), College
4. **Change Password** — Current Password, New Password, Confirm Password + [Update Password]
5. **Danger Zone** — red border card — [Delete All Data] + [Delete Account]

Backend needed:
- `PUT /auth/profile` — update name, branch, year, college
- `PUT /auth/password` — change password (verify current first)

---

## 2. CodingInterviewPage

Layout:
- Full screen (no sidebar), same header style as InterviewRoomPage
- Header: logo + "Coding Round" + timer (counts down 30min) + [End] button

Two-column main area:
- **Left panel** (problem):
  - Title + difficulty badge (Easy/Medium/Hard)
  - Description text
  - Input/Output examples
  - Constraints list
  - Collapsible hints (> Hint 1, > Hint 2)
- **Right panel** (editor + test cases):
  - Language selector dropdown [Python / C++ / Java]
  - Monaco Editor (npm install @monaco-editor/react)
  - Test Cases panel below editor:
    - Case 1: input / expected / your output + ✅/❌ badge
    - Case 2: same

Bottom bar: [Skip] + [▶ Run Code] + [✓ Submit]

After submit:
- AI feedback card slides in (via Ollama): time complexity, code quality, edge cases

Backend:
- `POST /code/run` — execute code in subprocess sandbox, return {output, error, runtime_ms, passed_cases}
- DB table: `coding_problems` (id, title, difficulty, description, examples JSON, constraints, starter_code JSON, test_cases JSON)

---

## 3. ResumeAnalyserPage

Layout: Sidebar + main content

Sections:
1. **Upload card** — dashed border, drag & drop or click, "Supports PDF, DOCX", [Upload Resume] button
2. **After upload (results):**
   - Left: ATS score ring (green/amber/red, 0-100%) + "Compatibility" label
   - Right: Extracted skills as tags (Python, React, FastAPI, etc.)
3. **Improvement suggestions card** — ✅ good items (green) + ⚠ improvement items (amber)
4. **AI Generated Questions card** — 5 questions personalized to resume content
   - [Start Interview with These Questions] button — indigo, full width

Backend:
- `POST /resume/analyse` — multipart PDF → PyMuPDF extract → Ollama → {skills, ats_score, suggestions, questions}

Install: `pip install PyMuPDF`

---

## 4. JDAnalyserPage

Layout: Sidebar + main content

Sections:
1. **JD Input card** — large textarea "Paste Job Description here...", [🔍 Analyse Gap] button
2. **Results (after analyse):**
   - **Skill Match card** — overall match % badge + per-skill bars:
     - Green (≥70%): Data Structures 92%
     - Amber (40-70%): System Design 62%
     - Red (<40%): Distributed Systems 30%
   - **7-Day Prep Plan card** — Day 1-2: weakest topic, Day 3-4: next topic... [Start Prep] button

Backend:
- `POST /jd/analyse` — {jd_text} → Ollama extracts skills → cross-reference /analytics/me → {required_skills, match_scores, missing_skills, prep_plan}

---

## 5. ReplayPage

Layout: Sidebar + main content
Header: "Interview Replay" + session selector dropdown (past 10 sessions)

Two-column main:
- **Left** (70%):
  - Session info bar: date, subject, avg score
  - Q&A timeline — for each question:
    - Question card (indigo left border)
    - Your answer card (dark)
    - Score row: NLP / Voice / Face / Total bars
    - Feedback text (collapsible)
- **Right** (30%):
  - Score trend chart (recharts LineChart across questions)
  - Behaviour summary:
    - Avg eye contact %
    - Total filler words
    - Avg pace (WPM)
    - Emotion distribution

Note: No video storage yet — transcript + scores only. Video replay is Phase 13+.

Backend needed:
- `GET /interview/sessions` — list user's sessions with answer count + avg score
- `GET /interview/sessions/{id}/answers` — all Q&A + scores for that session

---

## 6. SettingsPage

Layout: Sidebar + main content

Sections:
1. **Hardware card**
   - Camera Device [dropdown from navigator.mediaDevices]
   - Microphone [dropdown]
   - [Test Camera] [Test Mic] buttons

2. **AI Preferences card**
   - Whisper Model: [tiny / base (recommended) / small] dropdown → saved to localStorage
   - Default Difficulty: [Beginner / Intermediate / Advanced] → localStorage
   - AI Interviewer Mode: [Friendly / Neutral / Strict] → localStorage

3. **Notifications card**
   - Daily practice reminder [toggle]
   - Weekly report email [toggle]

4. **Privacy & Data card** (red border)
   - Store voice recordings [toggle]
   - [Delete All My Data] red button

[Save Settings] button — indigo, bottom right

No backend needed — all stored in localStorage.

---

## 7. OnboardingPage

Shown ONCE after first registration. Check `localStorage.getItem('onboarding_complete')`.

Layout: Full screen centered (no sidebar), step indicator at top

Step indicator: 4 dots connected by line — highlight current step

**Step 1 — Welcome**
- "Welcome to InterviewAI, [name]!" heading
- Brief description of what the app does
- [Allow Camera & Microphone] button → requests permissions
- Status indicators: Camera ✅ / Mic ✅

**Step 2 — Test Hardware**
- Small camera preview box (live)
- [🎙 Start 5s Test Recording] button
- Audio quality bar after recording
- Status: Camera: ✅ Detected | Audio Quality: Good

**Step 3 — Set Goals**
- "Target Companies" checkboxes: Google / Microsoft / Amazon / Startup / Other
- "Target Role" radio: SDE / Frontend / Backend / ML / Fullstack

**Step 4 — Weak Topics**
- Checklist: DSA / System Design / HR / OS / DBMS / Networks / Machine Learning
- [Start Your First Interview] CTA button (indigo, large)

Navigation: [← Back] on left, [Continue →] on right, [Skip Setup] below Continue

On finish/skip:
```js
localStorage.setItem('onboarding_complete', 'true')
```
Navigate to dashboard.

---

## Build Priority

| # | Page | Effort | Backend? |
|---|---|---|---|
| 1 | ProfilePage | Medium | Yes — 2 new PUT routes |
| 2 | SettingsPage | Easy | No — localStorage only |
| 3 | OnboardingPage | Medium | No — localStorage only |
| 4 | CodingInterviewPage | Hard | Yes — code runner + DB table |
| 5 | ResumeAnalyserPage | Medium | Yes — PyMuPDF + Ollama |
| 6 | JDAnalyserPage | Medium | Yes — Ollama analysis |
| 7 | ReplayPage | Medium | Yes — 2 new GET routes |

---

*Frontend Feature Design Spec | AI Interview Simulator | Updated March 12, 2026*
