import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const theme = {
  bg: "#0a0e1a",
  card: "#0f1525",
  border: "#1e2d4a",
  accent: "#00e5ff",
  green: "#00ff88",
  red: "#ff4d6d",
  yellow: "#ffd166",
  text: "#c8d8f0",
  muted: "#4a6080",
  font: "'JetBrains Mono', 'Fira Code', monospace",
  display: "'Syne', sans-serif",
};

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@300;400;600&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: ${theme.bg};
    color: ${theme.text};
    font-family: ${theme.font};
    min-height: 100vh;
  }

  .page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    position: relative;
    overflow: hidden;
  }

  .grid-bg {
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  .glow {
    position: fixed;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,229,255,0.06) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .card {
    background: ${theme.card};
    border: 1px solid ${theme.border};
    border-radius: 12px;
    position: relative;
    z-index: 1;
  }

  .card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,229,255,0.04) 0%, transparent 60%);
    pointer-events: none;
  }

  .btn {
    font-family: ${theme.font};
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    padding: 12px 24px;
  }

  .btn-primary {
    background: ${theme.accent};
    color: ${theme.bg};
  }

  .btn-primary:hover {
    background: #33eaff;
    box-shadow: 0 0 20px rgba(0,229,255,0.4);
    transform: translateY(-1px);
  }

  .btn-secondary {
    background: transparent;
    color: ${theme.accent};
    border: 1px solid ${theme.border};
  }

  .btn-secondary:hover {
    border-color: ${theme.accent};
    background: rgba(0,229,255,0.05);
  }

  .btn-green {
    background: ${theme.green};
    color: ${theme.bg};
  }

  .btn-green:hover {
    box-shadow: 0 0 20px rgba(0,255,136,0.4);
    transform: translateY(-1px);
  }

  .input {
    width: 100%;
    background: rgba(0,0,0,0.3);
    border: 1px solid ${theme.border};
    border-radius: 8px;
    padding: 12px 16px;
    font-family: ${theme.font};
    font-size: 13px;
    color: ${theme.text};
    outline: none;
    transition: border-color 0.2s;
  }

  .input:focus {
    border-color: ${theme.accent};
    box-shadow: 0 0 0 3px rgba(0,229,255,0.08);
  }

  .input::placeholder { color: ${theme.muted}; }

  .label {
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: ${theme.muted};
    margin-bottom: 8px;
  }

  .tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .tag-technical { background: rgba(0,229,255,0.12); color: ${theme.accent}; }
  .tag-hr { background: rgba(255,209,102,0.12); color: ${theme.yellow}; }
  .tag-easy { background: rgba(0,255,136,0.12); color: ${theme.green}; }
  .tag-medium { background: rgba(255,209,102,0.12); color: ${theme.yellow}; }
  .tag-hard { background: rgba(255,77,109,0.12); color: ${theme.red}; }

  .score-bar-bg {
    height: 6px;
    background: ${theme.border};
    border-radius: 99px;
    overflow: hidden;
  }

  .score-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 1s ease;
  }

  .title {
    font-family: ${theme.display};
    font-weight: 800;
    letter-spacing: -0.02em;
  }

  select.input option { background: ${theme.card}; }

  .fade-in {
    animation: fadeIn 0.4s ease forwards;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .pulse {
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  textarea.input { resize: vertical; min-height: 120px; line-height: 1.6; }

  .nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 100;
    background: rgba(10,14,26,0.9);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid ${theme.border};
    padding: 0 32px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .error-msg {
    background: rgba(255,77,109,0.1);
    border: 1px solid rgba(255,77,109,0.3);
    border-radius: 8px;
    padding: 12px 16px;
    color: ${theme.red};
    font-size: 13px;
  }

  .success-msg {
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.3);
    border-radius: 8px;
    padding: 12px 16px;
    color: ${theme.green};
    font-size: 13px;
  }
`;

// ─── Helpers ───────────────────────────────────────────────────────────────────

function ScoreBar({ value, color }) {
  const col = value >= 70 ? theme.green : value >= 45 ? theme.yellow : theme.red;
  return (
    <div className="score-bar-bg">
      <div className="score-bar-fill" style={{ width: `${value}%`, background: color || col }} />
    </div>
  );
}

function Loader() {
  return (
    <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
      {[0, 1, 2].map(i => (
        <div key={i} style={{
          width: 6, height: 6, borderRadius: "50%",
          background: theme.accent,
          animation: `pulse 1s ease-in-out ${i * 0.2}s infinite`
        }} />
      ))}
    </div>
  );
}

// ─── Login Page ────────────────────────────────────────────────────────────────

function LoginPage({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ name: "", email: "", password: "", branch: "CSE", year: 2 });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  async function submit() {
    setError(""); setLoading(true);
    try {
      if (mode === "register") {
        const r = await fetch(`${API}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...form, year: Number(form.year) })
        });
        const d = await r.json();
        if (!r.ok) { setError(d.detail || "Registration failed"); setLoading(false); return; }
        setMode("login"); setError(""); 
      }
      const r = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: form.email, password: form.password })
      });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Login failed"); setLoading(false); return; }
      localStorage.setItem("token", d.access_token);
      localStorage.setItem("user", JSON.stringify(d.user));
      onLogin(d.access_token, d.user);
    } catch {
      setError("Cannot connect to server. Is uvicorn running?");
    }
    setLoading(false);
  }

  return (
    <div className="page">
      <div className="grid-bg" />
      <div className="glow" style={{ top: "-200px", left: "50%", transform: "translateX(-50%)" }} />

      <div className="card fade-in" style={{ width: "100%", maxWidth: 440, padding: 40 }}>
        {/* Logo */}
        <div style={{ marginBottom: 32, textAlign: "center" }}>
          <div style={{ fontSize: 11, letterSpacing: "0.2em", color: theme.muted, textTransform: "uppercase", marginBottom: 8 }}>
            ◈ Interview Simulator
          </div>
          <h1 className="title" style={{ fontSize: 32, color: "#fff" }}>
            Crack the <span style={{ color: theme.accent }}>Interview</span>
          </h1>
          <p style={{ fontSize: 13, color: theme.muted, marginTop: 8 }}>
            AI-powered mock interviews with real scoring
          </p>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 4, background: "rgba(0,0,0,0.3)", borderRadius: 8, padding: 4, marginBottom: 28 }}>
          {["login", "register"].map(m => (
            <button key={m} className="btn" onClick={() => setMode(m)} style={{
              flex: 1, padding: "8px 0", fontSize: 12,
              background: mode === m ? theme.accent : "transparent",
              color: mode === m ? theme.bg : theme.muted,
              borderRadius: 6,
            }}>{m === "login" ? "Sign In" : "Register"}</button>
          ))}
        </div>

        {/* Fields */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {mode === "register" && (
            <>
              <div>
                <label className="label">Full Name</label>
                <input className="input" name="name" placeholder="Suraj Kumar" value={form.name} onChange={handle} />
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <div>
                  <label className="label">Branch</label>
                  <input className="input" name="branch" placeholder="CSE" value={form.branch} onChange={handle} />
                </div>
                <div>
                  <label className="label">Year</label>
                  <select className="input" name="year" value={form.year} onChange={handle}>
                    {[1,2,3,4].map(y => <option key={y} value={y}>Year {y}</option>)}
                  </select>
                </div>
              </div>
            </>
          )}
          <div>
            <label className="label">Email</label>
            <input className="input" name="email" type="email" placeholder="suraj@test.com" value={form.email} onChange={handle} />
          </div>
          <div>
            <label className="label">Password</label>
            <input className="input" name="password" type="password" placeholder="••••••••" value={form.password} onChange={handle}
              onKeyDown={e => e.key === "Enter" && submit()} />
          </div>

          {error && <div className="error-msg">{error}</div>}

          <button className="btn btn-primary" onClick={submit} disabled={loading}
            style={{ width: "100%", marginTop: 4, padding: "14px", fontSize: 13 }}>
            {loading ? <Loader /> : mode === "login" ? "→ Sign In" : "→ Create Account"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Dashboard Page ────────────────────────────────────────────────────────────

function DashboardPage({ token, user, onStart, onLogout }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ interview_type: "technical", topic: "arrays", difficulty: "medium" });
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");

  const topics = {
    technical: ["arrays", "linked_list", "trees", "sorting", "dp", "oops", "system_design"],
    hr: ["behavioral"]
  };

  useEffect(() => {
    fetch(`${API}/analytics/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setAnalytics(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  async function startInterview() {
    setError(""); setStarting(true);
    try {
      const r = await fetch(`${API}/interview/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Failed to start"); setStarting(false); return; }
      onStart(d.session_id, form.topic, form.difficulty, form.interview_type);
    } catch { setError("Server error"); }
    setStarting(false);
  }

  const perf = analytics?.avg_nlp_score;
  const perfColor = perf >= 70 ? theme.green : perf >= 45 ? theme.yellow : theme.red;

  return (
    <div style={{ minHeight: "100vh", background: theme.bg, paddingTop: 60 }}>
      <div className="grid-bg" />

      {/* Nav */}
      <nav className="nav">
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ color: theme.accent, fontSize: 16 }}>◈</span>
          <span className="title" style={{ fontSize: 18, color: "#fff" }}>Interview Simulator</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <span style={{ fontSize: 12, color: theme.muted }}>
            {user?.name} · {user?.branch} Y{user?.year}
          </span>
          <button className="btn btn-secondary" onClick={onLogout} style={{ padding: "6px 14px", fontSize: 11 }}>
            Sign Out
          </button>
        </div>
      </nav>

      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "40px 24px", position: "relative", zIndex: 1 }}>

        {/* Header */}
        <div className="fade-in" style={{ marginBottom: 36 }}>
          <p style={{ fontSize: 12, color: theme.accent, letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: 6 }}>
            Welcome back
          </p>
          <h1 className="title" style={{ fontSize: 36, color: "#fff" }}>
            Ready to practice, <span style={{ color: theme.accent }}>{user?.name?.split(" ")[0]}?</span>
          </h1>
        </div>

        {/* Stats Row */}
        <div className="fade-in" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, marginBottom: 32 }}>
          {[
            { label: "Sessions", value: analytics?.total_sessions ?? "—", color: theme.accent },
            { label: "Answers", value: analytics?.total_answers ?? "—", color: theme.yellow },
            { label: "Avg Score", value: analytics?.avg_nlp_score ? `${analytics.avg_nlp_score}%` : "—", color: perfColor },
            { label: "Best Topic", value: analytics?.strongest_topic ?? "—", color: theme.green },
          ].map(s => (
            <div key={s.label} className="card" style={{ padding: "20px 24px" }}>
              <div style={{ fontSize: 11, color: theme.muted, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 8 }}>{s.label}</div>
              <div className="title" style={{ fontSize: 26, color: s.color }}>{loading ? "…" : s.value}</div>
            </div>
          ))}
        </div>

        {/* Two Columns */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>

          {/* Start Interview */}
          <div className="card fade-in" style={{ padding: 28 }}>
            <h2 className="title" style={{ fontSize: 20, color: "#fff", marginBottom: 20 }}>
              Start Interview
            </h2>
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div>
                <label className="label">Type</label>
                <select className="input" value={form.interview_type}
                  onChange={e => setForm(f => ({ ...f, interview_type: e.target.value, topic: topics[e.target.value][0] }))}>
                  <option value="technical">Technical</option>
                  <option value="hr">HR / Behavioral</option>
                </select>
              </div>
              <div>
                <label className="label">Topic</label>
                <select className="input" value={form.topic}
                  onChange={e => setForm(f => ({ ...f, topic: e.target.value }))}>
                  {topics[form.interview_type].map(t => (
                    <option key={t} value={t}>{t.replace("_", " ").toUpperCase()}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="label">Difficulty</label>
                <div style={{ display: "flex", gap: 8 }}>
                  {["easy", "medium", "hard"].map(d => (
                    <button key={d} className="btn" onClick={() => setForm(f => ({ ...f, difficulty: d }))} style={{
                      flex: 1, padding: "10px 0", fontSize: 11,
                      background: form.difficulty === d
                        ? d === "easy" ? theme.green : d === "medium" ? theme.yellow : theme.red
                        : "transparent",
                      color: form.difficulty === d ? theme.bg : theme.muted,
                      border: `1px solid ${form.difficulty === d ? "transparent" : theme.border}`,
                      borderRadius: 6,
                    }}>{d}</button>
                  ))}
                </div>
              </div>

              {error && <div className="error-msg">{error}</div>}

              <button className="btn btn-primary" onClick={startInterview} disabled={starting}
                style={{ width: "100%", padding: "14px", marginTop: 4 }}>
                {starting ? <Loader /> : "→ Start Interview"}
              </button>
            </div>
          </div>

          {/* Topic Breakdown */}
          <div className="card fade-in" style={{ padding: 28 }}>
            <h2 className="title" style={{ fontSize: 20, color: "#fff", marginBottom: 20 }}>
              Topic Performance
            </h2>
            {loading ? (
              <div style={{ display: "flex", justifyContent: "center", padding: 40 }}><Loader /></div>
            ) : analytics?.topic_breakdown && Object.keys(analytics.topic_breakdown).length > 0 ? (
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                {Object.entries(analytics.topic_breakdown).map(([topic, score]) => (
                  <div key={topic}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                      <span style={{ fontSize: 12, color: theme.text }}>{topic.replace("_", " ")}</span>
                      <span style={{ fontSize: 12, color: score >= 70 ? theme.green : score >= 45 ? theme.yellow : theme.red, fontWeight: 600 }}>
                        {score}%
                      </span>
                    </div>
                    <ScoreBar value={score} />
                  </div>
                ))}
                <div style={{ marginTop: 8, padding: "12px 16px", background: "rgba(0,0,0,0.3)", borderRadius: 8 }}>
                  <span style={{ fontSize: 12, color: theme.muted }}>Weakest: </span>
                  <span style={{ fontSize: 12, color: theme.red }}>{analytics.weakest_topic}</span>
                  <span style={{ fontSize: 12, color: theme.muted }}> · Strongest: </span>
                  <span style={{ fontSize: 12, color: theme.green }}>{analytics.strongest_topic}</span>
                </div>
              </div>
            ) : (
              <div style={{ textAlign: "center", padding: "40px 0", color: theme.muted }}>
                <div style={{ fontSize: 32, marginBottom: 12 }}>📊</div>
                <p style={{ fontSize: 13 }}>No data yet — complete your first interview!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Interview Room Page ────────────────────────────────────────────────────────

function InterviewRoomPage({ token, sessionId, topic, difficulty, interviewType, onResult, onBack }) {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [questionNum, setQuestionNum] = useState(1);

  useEffect(() => { fetchQuestion(); }, []);

  async function fetchQuestion() {
    setLoading(true); setResult(null); setAnswer(""); setError("");
    try {
      const r = await fetch(`${API}/interview/question?topic=${topic}&difficulty=${difficulty}`,
        { headers: { Authorization: `Bearer ${token}` } });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Failed to fetch question"); setLoading(false); return; }
      setQuestion(d);
    } catch { setError("Server error"); }
    setLoading(false);
  }

  async function submitAnswer() {
    if (!answer.trim()) { setError("Please write an answer first."); return; }
    setError(""); setSubmitting(true);
    try {
      const r = await fetch(`${API}/interview/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ session_id: sessionId, question_id: question.question_id, user_answer: answer })
      });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Submission failed"); setSubmitting(false); return; }
      setResult(d);
    } catch { setError("Server error"); }
    setSubmitting(false);
  }

  function nextQuestion() {
    setQuestionNum(n => n + 1);
    fetchQuestion();
  }

  const scoreColor = result ? (result.nlp_score >= 70 ? theme.green : result.nlp_score >= 45 ? theme.yellow : theme.red) : theme.accent;

  return (
    <div style={{ minHeight: "100vh", background: theme.bg, paddingTop: 60 }}>
      <div className="grid-bg" />

      <nav className="nav">
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <button className="btn btn-secondary" onClick={onBack} style={{ padding: "6px 14px", fontSize: 11 }}>← Dashboard</button>
          <span style={{ fontSize: 12, color: theme.muted }}>
            Session #{sessionId} · Q{questionNum}
          </span>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <span className={`tag tag-${interviewType}`}>{interviewType}</span>
          <span className={`tag tag-${difficulty}`}>{difficulty}</span>
          <span className="tag" style={{ background: "rgba(0,229,255,0.08)", color: theme.accent }}>
            {topic.replace("_", " ")}
          </span>
        </div>
      </nav>

      <div style={{ maxWidth: 800, margin: "0 auto", padding: "40px 24px", position: "relative", zIndex: 1 }}>

        {/* Question Card */}
        <div className="card fade-in" style={{ padding: 32, marginBottom: 20 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
            <span style={{ fontSize: 11, color: theme.muted, letterSpacing: "0.1em", textTransform: "uppercase" }}>
              Question {questionNum}
            </span>
            {question && <span className={`tag tag-${question.type}`}>{question.type}</span>}
          </div>

          {loading ? (
            <div style={{ display: "flex", justifyContent: "center", padding: 32 }}><Loader /></div>
          ) : question ? (
            <p style={{ fontSize: 18, color: "#fff", lineHeight: 1.6, fontFamily: theme.display, fontWeight: 600 }}>
              {question.question_text}
            </p>
          ) : (
            <div className="error-msg">Could not load question. Try a different topic/difficulty.</div>
          )}
        </div>

        {/* Answer Box */}
        {question && !result && (
          <div className="card fade-in" style={{ padding: 28, marginBottom: 20 }}>
            <label className="label" style={{ marginBottom: 12 }}>Your Answer</label>
            <textarea
              className="input"
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              placeholder="Type your answer here... Be thorough — explain concepts, give examples, mention time/space complexity where relevant."
              style={{ minHeight: 160 }}
            />
            {error && <div className="error-msg" style={{ marginTop: 12 }}>{error}</div>}
            <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
              <button className="btn btn-primary" onClick={submitAnswer} disabled={submitting}
                style={{ flex: 1, padding: "13px" }}>
                {submitting ? <Loader /> : "→ Submit Answer"}
              </button>
              <button className="btn btn-secondary" onClick={onBack} style={{ padding: "13px 20px" }}>
                End Session
              </button>
            </div>
          </div>
        )}

        {/* Result Card */}
        {result && (
          <div className="card fade-in" style={{ padding: 28 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
              <h2 className="title" style={{ fontSize: 22, color: "#fff" }}>Score Breakdown</h2>
              <div className="title" style={{ fontSize: 36, color: scoreColor }}>{result.nlp_score}%</div>
            </div>

            {/* Score bars */}
            <div style={{ display: "flex", flexDirection: "column", gap: 16, marginBottom: 24 }}>
              {[
                { label: "Semantic Understanding", value: result.semantic_score, color: theme.accent },
                { label: "Keyword Coverage", value: result.keyword_score, color: theme.yellow },
                { label: "Answer Structure", value: result.structure_score, color: theme.green },
              ].map(s => (
                <div key={s.label}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ fontSize: 12, color: theme.text }}>{s.label}</span>
                    <span style={{ fontSize: 12, color: s.color, fontWeight: 600 }}>{s.value}%</span>
                  </div>
                  <ScoreBar value={s.value} color={s.color} />
                </div>
              ))}
            </div>

            {/* Feedback */}
            <div style={{ background: "rgba(0,0,0,0.3)", borderRadius: 8, padding: "14px 16px", marginBottom: 20, borderLeft: `3px solid ${scoreColor}` }}>
              <p style={{ fontSize: 13, color: theme.text, lineHeight: 1.6 }}>💡 {result.feedback}</p>
            </div>

            <div style={{ display: "flex", gap: 12 }}>
              <button className="btn btn-green" onClick={nextQuestion} style={{ flex: 1, padding: "13px" }}>
                → Next Question
              </button>
              <button className="btn btn-secondary" onClick={() => onResult(result)} style={{ padding: "13px 20px" }}>
                View Summary
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Result Page ───────────────────────────────────────────────────────────────

function ResultPage({ token, onBack }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/analytics/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setAnalytics(d); setLoading(false); });
  }, []);

  const score = analytics?.avg_nlp_score;
  const scoreColor = score >= 70 ? theme.green : score >= 45 ? theme.yellow : theme.red;

  return (
    <div style={{ minHeight: "100vh", background: theme.bg, paddingTop: 60 }}>
      <div className="grid-bg" />
      <div className="glow" style={{ top: "0", left: "50%", transform: "translateX(-50%)" }} />

      <nav className="nav">
        <button className="btn btn-secondary" onClick={onBack} style={{ padding: "6px 14px", fontSize: 11 }}>
          ← Back to Dashboard
        </button>
        <span style={{ fontSize: 12, color: theme.muted }}>Session Summary</span>
      </nav>

      <div style={{ maxWidth: 700, margin: "0 auto", padding: "40px 24px", position: "relative", zIndex: 1 }}>
        {loading ? (
          <div style={{ display: "flex", justifyContent: "center", padding: 80 }}><Loader /></div>
        ) : (
          <>
            {/* Big Score */}
            <div className="card fade-in" style={{ padding: 40, textAlign: "center", marginBottom: 20 }}>
              <p style={{ fontSize: 11, color: theme.muted, letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: 12 }}>
                Overall Performance
              </p>
              <div className="title" style={{ fontSize: 72, color: scoreColor, lineHeight: 1 }}>
                {score ?? "—"}%
              </div>
              <p style={{ fontSize: 16, color: theme.text, marginTop: 12, fontFamily: theme.display }}>
                {analytics?.performance}
              </p>
              <div style={{ display: "flex", justifyContent: "center", gap: 24, marginTop: 24 }}>
                <div style={{ textAlign: "center" }}>
                  <div className="title" style={{ fontSize: 28, color: theme.accent }}>{analytics?.total_sessions}</div>
                  <div style={{ fontSize: 11, color: theme.muted, textTransform: "uppercase", letterSpacing: "0.1em" }}>Sessions</div>
                </div>
                <div style={{ width: 1, background: theme.border }} />
                <div style={{ textAlign: "center" }}>
                  <div className="title" style={{ fontSize: 28, color: theme.yellow }}>{analytics?.total_answers}</div>
                  <div style={{ fontSize: 11, color: theme.muted, textTransform: "uppercase", letterSpacing: "0.1em" }}>Answers</div>
                </div>
              </div>
            </div>

            {/* Topic Breakdown */}
            {analytics?.topic_breakdown && Object.keys(analytics.topic_breakdown).length > 0 && (
              <div className="card fade-in" style={{ padding: 28, marginBottom: 20 }}>
                <h2 className="title" style={{ fontSize: 20, color: "#fff", marginBottom: 20 }}>Topic Breakdown</h2>
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  {Object.entries(analytics.topic_breakdown)
                    .sort(([,a],[,b]) => b - a)
                    .map(([topic, score]) => (
                    <div key={topic}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                        <span style={{ fontSize: 13, color: theme.text }}>{topic.replace("_", " ").toUpperCase()}</span>
                        <span style={{ fontSize: 13, fontWeight: 600,
                          color: score >= 70 ? theme.green : score >= 45 ? theme.yellow : theme.red }}>
                          {score}%
                        </span>
                      </div>
                      <ScoreBar value={score} />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Advice */}
            <div className="card fade-in" style={{ padding: 24, borderLeft: `3px solid ${theme.accent}` }}>
              <p style={{ fontSize: 13, color: theme.muted, marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.1em" }}>
                Focus Area
              </p>
              <p style={{ fontSize: 15, color: theme.text, lineHeight: 1.6 }}>
                Practice more on <span style={{ color: theme.red }}>{analytics?.weakest_topic?.replace("_", " ")}</span>.
                Your strongest area is <span style={{ color: theme.green }}>{analytics?.strongest_topic?.replace("_", " ")}</span> — keep it up!
              </p>
            </div>

            <button className="btn btn-primary" onClick={onBack}
              style={{ width: "100%", marginTop: 20, padding: "14px" }}>
              → Practice Again
            </button>
          </>
        )}
      </div>
    </div>
  );
}

// ─── App Root ──────────────────────────────────────────────────────────────────

export default function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState(() => localStorage.getItem("token") || "");
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("user")) || null; } catch { return null; }
  });
  const [session, setSession] = useState(null);

  useEffect(() => {
    if (token && user) setPage("dashboard");
  }, []);

  function handleLogin(t, u) {
    setToken(t); setUser(u); setPage("dashboard");
  }

  function handleLogout() {
    localStorage.removeItem("token"); localStorage.removeItem("user");
    setToken(""); setUser(null); setPage("login");
  }

  function handleStart(sessionId, topic, difficulty, interviewType) {
    setSession({ sessionId, topic, difficulty, interviewType });
    setPage("interview");
  }

  return (
    <>
      <style>{css}</style>
      {page === "login" && <LoginPage onLogin={handleLogin} />}
      {page === "dashboard" && <DashboardPage token={token} user={user} onStart={handleStart} onLogout={handleLogout} />}
      {page === "interview" && session && (
        <InterviewRoomPage
          token={token}
          sessionId={session.sessionId}
          topic={session.topic}
          difficulty={session.difficulty}
          interviewType={session.interviewType}
          onResult={() => setPage("result")}
          onBack={() => setPage("dashboard")}
        />
      )}
      {page === "result" && <ResultPage token={token} onBack={() => setPage("dashboard")} />}
    </>
  );
}
