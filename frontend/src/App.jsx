import { useState, useEffect, useRef } from "react";
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer,
  AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid,
} from "recharts";
import VoiceRecorder from "./VoiceRecorder";
import VisionRecorder from "./VisionRecorder";
import Editor from "@monaco-editor/react";

const API = "http://127.0.0.1:8000";

// ─── Global Styles ─────────────────────────────────────────────────────────────
const globalCss = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0B0F1E; color: #F1F5F9; font-family: 'Inter', sans-serif; min-height: 100vh; }
  button { font-family: 'Inter', sans-serif; cursor: pointer; border: none; outline: none; }
  input, select, textarea { font-family: 'Inter', sans-serif; outline: none; }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0B0F1E; }
  ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes ringPulse { 0%,100% { transform: scale(1); opacity:0.6; } 50% { transform: scale(1.08); opacity:0.3; } }
  .fade-in { animation: fadeIn 0.4s ease both; }
  .spin { animation: spin 0.8s linear infinite; display:inline-block; }
`;

// ─── Helpers ───────────────────────────────────────────────────────────────────
function Spinner() {
  return <span className="spin" style={{ fontSize: 16 }}>⟳</span>;
}

function Bar({ value, color = "#6366F1", height = 6 }) {
  return (
    <div style={{ background: "rgba(255,255,255,0.08)", borderRadius: 99, height, overflow: "hidden" }}>
      <div style={{ width: `${Math.min(100, Math.max(0, value))}%`, height: "100%", background: color, borderRadius: 99, transition: "width 0.6s ease" }} />
    </div>
  );
}

function buildWav(float32Array, sampleRate) {
  const n = float32Array.length;
  const buf = new ArrayBuffer(44 + n * 2);
  const v = new DataView(buf);
  const wr = (off, s) => { for (let i = 0; i < s.length; i++) v.setUint8(off + i, s.charCodeAt(i)); };
  wr(0, "RIFF"); v.setUint32(4, 36 + n * 2, true); wr(8, "WAVE"); wr(12, "fmt ");
  v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, sampleRate, true); v.setUint32(28, sampleRate * 2, true);
  v.setUint16(32, 2, true); v.setUint16(34, 16, true); wr(36, "data"); v.setUint32(40, n * 2, true);
  let maxA = 0;
  for (let i = 0; i < n; i++) { const a = Math.abs(float32Array[i]); if (a > maxA) maxA = a; }
  const gain = maxA > 0.001 ? 0.9 / maxA : 1.0;
  let off = 44;
  for (let i = 0; i < n; i++) {
    const s = Math.max(-1, Math.min(1, float32Array[i] * gain));
    v.setInt16(off, s < 0 ? s * 0x8000 : s * 0x7fff, true); off += 2;
  }
  return new Blob([buf], { type: "audio/wav" });
}

function CircularScore({ score, size = 160, strokeWidth = 10 }) {
  const r = (size - strokeWidth * 2) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (Math.min(100, score) / 100) * circ;
  const cx = size / 2;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#1E293B" strokeWidth={strokeWidth} />
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#6366F1" strokeWidth={strokeWidth}
        strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`} />
      <text x={cx} y={cx - 8} textAnchor="middle" fill="#fff" fontSize={size * 0.22} fontWeight="700" fontFamily="Inter">{score}</text>
      <text x={cx} y={cx + 14} textAnchor="middle" fill="#94A3B8" fontSize={size * 0.09} fontFamily="Inter" letterSpacing="2">SCORE</text>
    </svg>
  );
}

// ─── Sidebar ───────────────────────────────────────────────────────────────────
function Sidebar({ active, user, onNav, onLogout, showUser }) {
  const items = [
    { id: "dashboard", label: "Dashboard", icon: "⊞" },
    { id: "interview", label: "Interview", icon: "◉" },
    { id: "coding",    label: "Coding",    icon: "💻" },
    { id: "analytics", label: "Analytics", icon: "▦" },
    { id: "resume",    label: "Resume AI", icon: "📄" },
    { id: "profile",   label: "Profile",   icon: "○" },
    { id: "settings",  label: "Settings",  icon: "⚙" },
  ];
  return (
    <div style={{
      width: 220, minHeight: "100vh", background: "#0F1629",
      borderRight: "1px solid rgba(255,255,255,0.07)",
      display: "flex", flexDirection: "column",
      position: "fixed", left: 0, top: 0, zIndex: 100,
    }}>
      {/* Logo */}
      <div style={{ padding: "24px 20px 28px", display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{ width: 38, height: 38, background: "#6366F1", borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18, color: "#fff", fontWeight: 700 }}>◈</div>
        <div>
          <div style={{ color: "#fff", fontWeight: 700, fontSize: 14, lineHeight: 1.2 }}>Interview Pro</div>
          <div style={{ color: "#94A3B8", fontSize: 11 }}>AI Simulator</div>
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: "0 10px" }}>
        {items.map(item => (
          <button key={item.id} onClick={() => onNav(item.id)} style={{
            width: "100%", display: "flex", alignItems: "center", gap: 10,
            padding: "10px 12px", borderRadius: 8, marginBottom: 2, fontSize: 14,
            background: active === item.id ? "rgba(99,102,241,0.15)" : "transparent",
            color: active === item.id ? "#6366F1" : "#94A3B8",
            fontWeight: active === item.id ? 600 : 400,
            transition: "all 0.15s",
          }}>
            <span style={{ fontSize: 15, width: 18, textAlign: "center" }}>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Bottom */}
      <div style={{ padding: "16px 10px" }}>
        {showUser && user && (
          <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "12px", marginBottom: 8, borderRadius: 8, background: "rgba(255,255,255,0.04)" }}>
            <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#6366F1", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, color: "#fff", fontWeight: 700, flexShrink: 0 }}>
              {(user.name || "U")[0].toUpperCase()}
            </div>
            <div style={{ overflow: "hidden" }}>
              <div style={{ color: "#fff", fontSize: 13, fontWeight: 600, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{user.name?.split(" ")[0]}</div>
              <div style={{ color: "#6366F1", fontSize: 10 }}>Premium Member</div>
            </div>
          </div>
        )}
        <button onClick={onLogout} style={{
          width: "100%", display: "flex", alignItems: "center", gap: 10,
          padding: "10px 12px", borderRadius: 8,
          background: "transparent", color: "#94A3B8", fontSize: 14,
        }}>
          <span style={{ fontSize: 14 }}>↪</span> Logout
        </button>
      </div>
    </div>
  );
}

// ─── Page wrapper with sidebar ─────────────────────────────────────────────────
function SidebarLayout({ active, user, onNav, onLogout, children, showUser }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0B0F1E" }}>
      <Sidebar active={active} user={user} onNav={onNav} onLogout={onLogout} showUser={showUser} />
      <div style={{ marginLeft: 220, flex: 1, minHeight: "100vh" }}>
        {children}
      </div>
    </div>
  );
}

// ─── Landing Page ──────────────────────────────────────────────────────────────
function LandingPage({ onLogin, onGetStarted }) {
  return (
    <div style={{ background: "#0B0F1E", minHeight: "100vh", color: "#F1F5F9" }}>
      {/* Navbar */}
      <nav style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "18px 60px", borderBottom: "1px solid rgba(255,255,255,0.07)", position: "sticky", top: 0, background: "rgba(11,15,30,0.95)", backdropFilter: "blur(10px)", zIndex: 50 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 32, height: 32, background: "#6366F1", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700 }}>◈</div>
          <span style={{ fontWeight: 700, fontSize: 17, color: "#fff" }}>InterviewAI</span>
        </div>
        <div style={{ display: "flex", gap: 32, fontSize: 14, color: "#94A3B8" }}>
          <span style={{ cursor: "pointer" }} onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}>Features</span>
          <span style={{ cursor: "pointer" }} onClick={() => document.getElementById("cta")?.scrollIntoView({ behavior: "smooth" })}>Pricing</span>
          <span style={{ cursor: "pointer" }} onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}>Resources</span>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <button onClick={onLogin} style={{ background: "transparent", color: "#94A3B8", fontSize: 14, padding: "8px 16px", borderRadius: 8, border: "1px solid transparent" }}>Login</button>
          <button onClick={onGetStarted} style={{ background: "#6366F1", color: "#fff", fontSize: 14, fontWeight: 600, padding: "8px 20px", borderRadius: 8 }}>Get Started</button>
        </div>
      </nav>

      {/* Hero */}
      <section style={{ maxWidth: 1200, margin: "0 auto", padding: "80px 40px 60px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 60, alignItems: "center" }}>
        {/* Left */}
        <div className="fade-in">
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.3)", borderRadius: 99, padding: "6px 14px", fontSize: 11, color: "#A5B4FC", fontWeight: 600, letterSpacing: "0.05em", marginBottom: 28 }}>
            <span style={{ width: 6, height: 6, background: "#6366F1", borderRadius: "50%", display: "inline-block" }} />
            NEW: GPT-4O MULTIMODAL SUPPORT
          </div>
          <h1 style={{ fontSize: 58, fontWeight: 800, lineHeight: 1.1, marginBottom: 20 }}>
            AI Multimodal<br />
            <span style={{ background: "linear-gradient(135deg, #6366F1, #A78BFA)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Interview<br />Simulator</span>
          </h1>
          <p style={{ fontSize: 16, color: "#94A3B8", lineHeight: 1.7, marginBottom: 32, maxWidth: 420 }}>
            Practice technical &amp; HR interviews with AI-powered voice and facial analysis. Get instant feedback on body language, tone, and knowledge.
          </p>
          <div style={{ display: "flex", gap: 12, marginBottom: 32 }}>
            <button onClick={onGetStarted} style={{ background: "#6366F1", color: "#fff", fontWeight: 600, fontSize: 15, padding: "13px 28px", borderRadius: 10 }}>
              Start Interview →
            </button>
            <button onClick={onLogin} style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#F1F5F9", fontSize: 15, padding: "13px 24px", borderRadius: 10 }}>
              View Demo
            </button>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12, color: "#94A3B8", fontSize: 13 }}>
            <div style={{ display: "flex" }}>
              {["#6366F1","#22C55E","#F59E0B","#EF4444"].map((c, i) => (
                <div key={i} style={{ width: 28, height: 28, borderRadius: "50%", background: c, border: "2px solid #0B0F1E", marginLeft: i > 0 ? -8 : 0 }} />
              ))}
            </div>
            Joined by <strong style={{ color: "#fff" }}>2,000+</strong> aspiring candidates
          </div>
        </div>

        {/* Right — AI Interviewer Card */}
        <div className="fade-in" style={{ animationDelay: "0.15s" }}>
          <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 16, overflow: "hidden", position: "relative" }}>
            <div style={{ display: "flex", gap: 8, padding: "12px 16px", position: "absolute", top: 0, left: 0, right: 0, zIndex: 2 }}>
              <span style={{ background: "rgba(0,0,0,0.6)", padding: "4px 10px", borderRadius: 6, fontSize: 11, color: "#60A5FA", fontWeight: 600 }}>● EYE CONTACT: 98%</span>
              <span style={{ background: "rgba(0,0,0,0.6)", padding: "4px 10px", borderRadius: 6, fontSize: 11, color: "#22C55E", fontWeight: 600 }}>● TONE: CONFIDENT</span>
            </div>
            <div style={{ height: 320, background: "linear-gradient(160deg, #1E293B 0%, #0F172A 100%)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ width: 120, height: 120, borderRadius: "50%", background: "rgba(99,102,241,0.15)", border: "2px dashed rgba(99,102,241,0.4)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 48 }}>
                🤖
              </div>
            </div>
            <div style={{ padding: "14px 16px", background: "rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <div style={{ color: "#fff", fontWeight: 600, fontSize: 14 }}>AI Interviewer: Sarah</div>
                <div style={{ color: "#94A3B8", fontSize: 12 }}>Senior Technical Recruiter</div>
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <div style={{ width: 32, height: 32, borderRadius: "50%", background: "rgba(99,102,241,0.2)", border: "1px solid #6366F1", display: "flex", alignItems: "center", justifyContent: "center", color: "#6366F1", fontSize: 14 }}>🎙</div>
                <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#6366F1", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 14 }}>▶</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" style={{ maxWidth: 1200, margin: "0 auto", padding: "60px 40px" }}>
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <div style={{ fontSize: 12, color: "#6366F1", fontWeight: 600, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 12 }}>FEATURES</div>
          <h2 style={{ fontSize: 38, fontWeight: 800 }}>Everything you need to land the job</h2>
          <p style={{ color: "#94A3B8", marginTop: 12, fontSize: 15 }}>Our multimodal engine analyzes every nuance of your interview performance in real-time.</p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          {[
            { icon: "🎤", title: "Voice Confidence Analysis", desc: "AI analyzes pitch, speed, and filler words. Learn to sound more authoritative and clear during high-pressure questions." },
            { icon: "👁", title: "Face Tracking & Eye Contact", desc: "Our computer vision model ensures you're maintaining eye contact with the camera and tracks micro-expressions." },
            { icon: "📊", title: "AI Evaluation Score", desc: "Receive a detailed breakdown of your technical accuracy, behavioral alignment, and overall presence score after every session." },
            { icon: "🎯", title: "Real Interview Experience", desc: "Simulate stress with realistic interviewers from top tech companies. Adaptive questioning gets harder based on your performance." },
          ].map((f, i) => (
            <div key={i} className="fade-in" style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 28, animationDelay: `${i * 0.1}s` }}>
              <div style={{ width: 48, height: 48, background: "rgba(99,102,241,0.15)", borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22, marginBottom: 16 }}>{f.icon}</div>
              <h3 style={{ fontWeight: 700, fontSize: 16, marginBottom: 10 }}>{f.title}</h3>
              <p style={{ color: "#94A3B8", fontSize: 14, lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section id="cta" style={{ maxWidth: 1200, margin: "0 auto 80px", padding: "0 40px" }}>
        <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 20, padding: "48px 48px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 48, alignItems: "center" }}>
          <div>
            <h2 style={{ fontSize: 34, fontWeight: 800, marginBottom: 16 }}>Ready to ace your next big opportunity?</h2>
            <p style={{ color: "#94A3B8", fontSize: 15, lineHeight: 1.7, marginBottom: 24 }}>Start your first simulated interview today and discover the insights you've been missing.</p>
            <div style={{ display: "flex", gap: 12 }}>
              <button onClick={onGetStarted} style={{ background: "#6366F1", color: "#fff", fontWeight: 600, fontSize: 14, padding: "12px 24px", borderRadius: 8 }}>Start Free Trial</button>
              <button onClick={onGetStarted} style={{ background: "transparent", border: "1px solid rgba(255,255,255,0.15)", color: "#F1F5F9", fontSize: 14, padding: "12px 24px", borderRadius: 8 }}>Schedule Demo</button>
            </div>
          </div>
          <div style={{ background: "#1E293B", borderRadius: 14, padding: 24 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <span style={{ fontWeight: 600, fontSize: 14 }}>Recent Feedback</span>
              <span style={{ background: "rgba(34,197,94,0.15)", color: "#22C55E", fontSize: 11, padding: "3px 10px", borderRadius: 6, fontWeight: 600 }}>Analysis Complete</span>
            </div>
            {[
              { icon: "✅", text: "Technical depth was excellent, especially the explanation of distributed systems." },
              { icon: "⚠️", text: "You used \"Um\" 14 times. Try slowing down your speech for more impact." },
            ].map((item, i) => (
              <div key={i} style={{ display: "flex", gap: 10, marginBottom: 12, fontSize: 13, color: "#94A3B8", lineHeight: 1.5 }}>
                <span style={{ flexShrink: 0 }}>{item.icon}</span>
                {item.text}
              </div>
            ))}
            <div style={{ marginTop: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 6 }}>
                <span style={{ color: "#94A3B8" }}>Preparation Level</span>
                <span style={{ color: "#6366F1", fontWeight: 600 }}>82%</span>
              </div>
              <Bar value={82} />
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: "1px solid rgba(255,255,255,0.07)", padding: "24px 60px", display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: 13, color: "#94A3B8" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 24, height: 24, background: "#6366F1", borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 12, fontWeight: 700 }}>◈</div>
          <span style={{ color: "#fff", fontWeight: 600 }}>InterviewAI</span>
        </div>
        <div style={{ display: "flex", gap: 20 }}>
          <span>Privacy Policy</span><span>Terms of Service</span><span>Contact</span>
        </div>
        <span>© 2024 InterviewAI Corp. All rights reserved</span>
      </footer>
    </div>
  );
}

// ─── Login Page ────────────────────────────────────────────────────────────────
function LoginPage({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "", password: "", name: "", branch: "", year: "1" });
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [infoMsg, setInfoMsg] = useState("");

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  async function handleSubmit(e) {
    e.preventDefault();
    setError(""); setLoading(true);
    try {
      if (mode === "login") {
        const r = await fetch(`${API}/auth/login`, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: form.email, password: form.password }),
        });
        const d = await r.json();
        if (!r.ok) { setError(d.detail || "Login failed"); setLoading(false); return; }
        localStorage.setItem("token", d.access_token);
        localStorage.setItem("user", JSON.stringify(d.user));
        onLogin(d.access_token, d.user);
      } else {
        const r = await fetch(`${API}/auth/register`, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: form.name, email: form.email, password: form.password, branch: form.branch, year: parseInt(form.year) }),
        });
        const d = await r.json();
        if (!r.ok) { setError(d.detail || "Registration failed"); setLoading(false); return; }
        setMode("login"); setError(""); setForm(f => ({ ...f, password: "" }));
      }
    } catch { setError("Server error. Check that backend is running."); }
    setLoading(false);
  }

  return (
    <div style={{ minHeight: "100vh", background: "#0B0F1E", display: "grid", gridTemplateColumns: "1fr 1fr", fontFamily: "Inter" }}>
      {/* Left panel */}
      <div style={{ background: "#0F1629", padding: "40px 48px", display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 48 }}>
          <div style={{ width: 34, height: 34, background: "#6366F1", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700 }}>◈</div>
          <span style={{ fontWeight: 700, fontSize: 16, color: "#fff" }}>InterviewAI</span>
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ background: "#1E293B", borderRadius: 14, overflow: "hidden", border: "1px solid rgba(255,255,255,0.08)", marginBottom: 24 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "12px 16px", borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
              <span style={{ background: "#EF4444", color: "#fff", fontSize: 10, fontWeight: 700, padding: "3px 8px", borderRadius: 4 }}>● LIVE DEMO</span>
              <span style={{ color: "#94A3B8", fontSize: 12 }}>00:42 / 05:00</span>
            </div>
            <div style={{ height: 200, background: "linear-gradient(160deg, #1E293B, #0F172A)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ width: 80, height: 80, borderRadius: "50%", background: "rgba(99,102,241,0.2)", border: "2px dashed rgba(99,102,241,0.4)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 36 }}>🤖</div>
            </div>
            <div style={{ padding: "14px 16px" }}>
              <div style={{ fontSize: 11, color: "#6366F1", fontWeight: 600, letterSpacing: "0.05em", marginBottom: 6 }}>CURRENT QUESTION</div>
              <div style={{ color: "#fff", fontWeight: 700, fontSize: 15 }}>Explain the Quicksort algorithm.</div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 1, background: "rgba(255,255,255,0.06)" }}>
              {[{ label: "Voice Score", val: 82, color: "#6366F1" }, { label: "Face Analysis", val: 75, color: "#22C55E" }, { label: "Answer Quality", val: 90, color: "#F59E0B" }].map((s) => (
                <div key={s.label} style={{ background: "#1E293B", padding: "12px 14px" }}>
                  <div style={{ color: "#94A3B8", fontSize: 11, marginBottom: 4 }}>{s.label}</div>
                  <div style={{ color: "#fff", fontWeight: 700, fontSize: 20, marginBottom: 6 }}>{s.val}</div>
                  <Bar value={s.val} color={s.color} />
                </div>
              ))}
            </div>
          </div>
          <p style={{ color: "#94A3B8", fontSize: 13, display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ color: "#6366F1" }}>◈</span>
            Experience the world's most advanced AI multimodal interview trainer.
          </p>
        </div>
      </div>

      {/* Right panel */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: 40 }}>
        <div style={{ width: "100%", maxWidth: 400 }}>
          <h1 style={{ fontSize: 30, fontWeight: 800, color: "#fff", marginBottom: 8 }}>
            {mode === "login" ? "Welcome Back" : "Create Account"}
          </h1>
          <p style={{ color: "#94A3B8", fontSize: 14, marginBottom: 32 }}>
            {mode === "login" ? "Sign in to your account to continue" : "Join thousands of candidates improving daily"}
          </p>

          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {mode === "register" && (
              <div>
                <label style={{ fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" }}>Full Name</label>
                <input value={form.name} onChange={e => set("name", e.target.value)} required placeholder="Your full name"
                  style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#F1F5F9", fontSize: 14 }} />
              </div>
            )}
            <div>
              <label style={{ fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" }}>Email Address</label>
              <div style={{ position: "relative" }}>
                <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "#64748B", fontSize: 14 }}>✉</span>
                <input type="email" value={form.email} onChange={e => set("email", e.target.value)} required placeholder="name@company.com"
                  style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px 11px 36px", color: "#F1F5F9", fontSize: 14 }} />
              </div>
            </div>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <label style={{ fontSize: 13, color: "#94A3B8" }}>Password</label>
                <span style={{ fontSize: 12, color: "#6366F1", cursor: "pointer" }} onClick={() => setInfoMsg("Password reset is not available in local mode. Contact your admin.")}>Forgot password?</span>
              </div>
              <div style={{ position: "relative" }}>
                <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "#64748B", fontSize: 14 }}>🔒</span>
                <input type={showPw ? "text" : "password"} value={form.password} onChange={e => set("password", e.target.value)} required placeholder="••••••••"
                  style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 40px 11px 36px", color: "#F1F5F9", fontSize: 14 }} />
                <button type="button" onClick={() => setShowPw(p => !p)}
                  style={{ position: "absolute", right: 12, top: "50%", transform: "translateY(-50%)", background: "none", color: "#64748B", fontSize: 14 }}>
                  {showPw ? "🙈" : "👁"}
                </button>
              </div>
            </div>

            {mode === "register" && (
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <div>
                  <label style={{ fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" }}>Branch</label>
                  <input value={form.branch} onChange={e => set("branch", e.target.value)} placeholder="CSE" required
                    style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#F1F5F9", fontSize: 14 }} />
                </div>
                <div>
                  <label style={{ fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" }}>Year</label>
                  <select value={form.year} onChange={e => set("year", e.target.value)}
                    style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#F1F5F9", fontSize: 14 }}>
                    {[1,2,3,4].map(y => <option key={y} value={y}>{y}</option>)}
                  </select>
                </div>
              </div>
            )}

            {error && <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 8, padding: "10px 14px", color: "#FCA5A5", fontSize: 13 }}>{error}</div>}
            {infoMsg && <div style={{ background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.3)", borderRadius: 8, padding: "10px 14px", color: "#FDE68A", fontSize: 13 }}>{infoMsg}</div>}

            <button type="submit" disabled={loading}
              style={{ background: "#6366F1", color: "#fff", fontWeight: 600, fontSize: 15, padding: "13px", borderRadius: 8, marginTop: 4 }}>
              {loading ? <Spinner /> : mode === "login" ? "Sign In →" : "Create Account →"}
            </button>
          </form>

          {mode === "login" && (
            <>
              <div style={{ display: "flex", alignItems: "center", gap: 12, margin: "20px 0" }}>
                <div style={{ flex: 1, height: 1, background: "#334155" }} />
                <span style={{ color: "#64748B", fontSize: 12, fontWeight: 500 }}>OR CONTINUE WITH</span>
                <div style={{ flex: 1, height: 1, background: "#334155" }} />
              </div>
              <button onClick={() => setInfoMsg("Google login is not available in local mode. Use email + password.")} style={{ width: "100%", background: "#fff", color: "#1E293B", fontWeight: 600, fontSize: 14, padding: "12px", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", gap: 10 }}>
                <span style={{ fontSize: 18 }}>G</span> Google Account
              </button>
            </>
          )}

          <p style={{ textAlign: "center", marginTop: 24, fontSize: 14, color: "#94A3B8" }}>
            {mode === "login" ? "Don't have an account? " : "Already have an account? "}
            <span style={{ color: "#6366F1", cursor: "pointer", fontWeight: 600 }} onClick={() => { setMode(m => m === "login" ? "register" : "login"); setError(""); }}>
              {mode === "login" ? "Create Account" : "Sign In"}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}

// ─── Dashboard Page ────────────────────────────────────────────────────────────
function DashboardPage({ token, user, onNav, onLogout, onSelectSubject, onViewAnalytics }) {
  const [analytics, setAnalytics] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState("");
  const [loadingA, setLoadingA] = useState(true);

  useEffect(() => {
    fetch(`${API}/analytics/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => { if (r.status === 401) onLogout(); return r.json(); })
      .then(d => { setAnalytics(d); setLoadingA(false); })
      .catch(() => setLoadingA(false));

    fetch(`${API}/interview/subjects`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(d => { if (Array.isArray(d)) { setSubjects(d); if (d.length) setSelectedSubjectId(d[0].id); } })
      .catch(() => {});
  }, []);

  function handleStartInterview() {
    const sub = subjects.find(s => s.id === parseInt(selectedSubjectId) || s.id === selectedSubjectId);
    if (sub) onSelectSubject(sub);
  }

  const recent = analytics?.recent_sessions || [];
  const avgScore = analytics?.avg_nlp_score ?? 0;
  const bestScore = analytics?.best_score ?? analytics?.avg_nlp_score ?? 0;

  function statusBadge(score) {
    if (score >= 85) return { label: "Excellent", bg: "rgba(34,197,94,0.1)", color: "#22C55E" };
    if (score >= 65) return { label: "Passed", bg: "rgba(34,197,94,0.1)", color: "#22C55E" };
    return { label: "Needs Improvement", bg: "rgba(245,158,11,0.1)", color: "#F59E0B" };
  }

  return (
    <SidebarLayout active="dashboard" user={user} onNav={onNav} onLogout={onLogout}>
      <div style={{ padding: "32px 40px", minHeight: "100vh" }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 32 }}>
          <div>
            <h1 style={{ fontSize: 26, fontWeight: 700, color: "#fff", marginBottom: 4 }}>Welcome back, {user?.name?.split(" ")[0] || "there"}</h1>
            <p style={{ color: "#94A3B8", fontSize: 14 }}>Ready for your next session? Practice makes perfect.</p>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ width: 36, height: 36, borderRadius: "50%", background: "#1E293B", border: "1px solid #334155", display: "flex", alignItems: "center", justifyContent: "center", color: "#94A3B8", fontSize: 16 }}>🔔</div>
            <div onClick={() => onNav("profile")} style={{ width: 36, height: 36, borderRadius: "50%", background: "#6366F1", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 14, cursor: "pointer" }}>
              {(user?.name || "U")[0].toUpperCase()}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20, marginBottom: 28 }}>
          {[
            { label: "Interviews Completed", value: loadingA ? "…" : (analytics?.total_sessions ?? 0), badge: "+20%", icon: "✓", color: "#6366F1" },
            { label: "Avg Score", value: loadingA ? "…" : `${avgScore}%`, badge: "+5%", icon: "↗", color: "#22C55E" },
            { label: "Best Score", value: loadingA ? "…" : `${bestScore}%`, badge: "+2%", icon: "🏆", color: "#F59E0B" },
          ].map((s) => (
            <div key={s.label} className="fade-in" style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: "22px 24px", display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
              <div>
                <div style={{ color: "#94A3B8", fontSize: 13, marginBottom: 8 }}>{s.label}</div>
                <div style={{ color: "#fff", fontSize: 30, fontWeight: 700, marginBottom: 8 }}>{s.value}</div>
                <span style={{ background: "rgba(34,197,94,0.1)", color: "#22C55E", fontSize: 11, fontWeight: 600, padding: "3px 8px", borderRadius: 6 }}>{s.badge}</span>
              </div>
              <div style={{ color: s.color, fontSize: 22 }}>{s.icon}</div>
            </div>
          ))}
        </div>

        {/* Quick Start + Recent */}
        <div style={{ display: "grid", gridTemplateColumns: "420px 1fr", gap: 20 }}>
          {/* Quick Start */}
          <div className="fade-in" style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
              <div style={{ width: 42, height: 42, background: "#6366F1", borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }}>⚡</div>
              <div>
                <div style={{ color: "#fff", fontWeight: 700, fontSize: 16 }}>Quick Start</div>
                <div style={{ color: "#94A3B8", fontSize: 13 }}>Jump into a session</div>
              </div>
            </div>

            <label style={{ fontSize: 13, color: "#94A3B8", display: "block", marginBottom: 8 }}>Interview Subject</label>
            <select value={selectedSubjectId} onChange={e => setSelectedSubjectId(e.target.value)}
              style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#F1F5F9", fontSize: 14, marginBottom: 16 }}>
              {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
              {subjects.length === 0 && <option>Loading subjects...</option>}
            </select>

            <button onClick={handleStartInterview} disabled={!selectedSubjectId}
              style={{ width: "100%", background: "#6366F1", color: "#fff", fontWeight: 600, fontSize: 15, padding: "13px", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", gap: 8, opacity: selectedSubjectId ? 1 : 0.5 }}>
              Start Interview ▶
            </button>

            <div style={{ marginTop: 16, background: "rgba(99,102,241,0.08)", borderRadius: 8, padding: "12px 14px", display: "flex", gap: 10, alignItems: "flex-start" }}>
              <span style={{ color: "#6366F1", marginTop: 1 }}>ℹ</span>
              <p style={{ color: "#94A3B8", fontSize: 12, lineHeight: 1.5 }}>Practice sessions are AI-driven and adapt to your skill level. Audio and camera permissions may be required.</p>
            </div>
          </div>

          {/* Recent Interviews */}
          <div className="fade-in" style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
              <span style={{ color: "#fff", fontWeight: 700, fontSize: 16 }}>Recent Interviews</span>
              <span onClick={onViewAnalytics} style={{ color: "#6366F1", fontSize: 13, cursor: "pointer", fontWeight: 500 }}>View All</span>
            </div>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  {["Date", "Subject", "Score", "Status"].map(h => (
                    <th key={h} style={{ textAlign: "left", color: "#64748B", fontSize: 12, fontWeight: 500, paddingBottom: 12, borderBottom: "1px solid #1E293B" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {loadingA ? (
                  <tr><td colSpan={4} style={{ textAlign: "center", padding: 32, color: "#94A3B8" }}><Spinner /></td></tr>
                ) : recent.length === 0 ? (
                  <tr><td colSpan={4} style={{ textAlign: "center", padding: 32, color: "#64748B", fontSize: 14 }}>No sessions yet. Start your first interview!</td></tr>
                ) : recent.slice(0, 5).map((s, i) => {
                  const badge = statusBadge(s.avg_score || 0);
                  return (
                    <tr key={i} style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                      <td style={{ padding: "12px 0", color: "#94A3B8", fontSize: 13 }}>{s.date || "—"}</td>
                      <td style={{ padding: "12px 0", color: "#F1F5F9", fontSize: 13, fontWeight: 500 }}>{s.subject || "—"}</td>
                      <td style={{ padding: "12px 0" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                          <div style={{ flex: 1, maxWidth: 80 }}><Bar value={s.avg_score || 0} /></div>
                          <span style={{ color: "#6366F1", fontSize: 13, fontWeight: 600, minWidth: 28 }}>{s.avg_score ?? "—"}</span>
                        </div>
                      </td>
                      <td style={{ padding: "12px 0" }}>
                        <span style={{ background: badge.bg, color: badge.color, fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 6 }}>{badge.label}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </SidebarLayout>
  );
}

// ─── Subject Setup Page (topic / subtopic / difficulty) ────────────────────────
function SubjectPage({ token, subject, onBack, onStart, user, onNav, onLogout }) {
  const [topics, setTopics] = useState([]);
  const [loadingT, setLoadingT] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [subtopics, setSubtopics] = useState([]);
  const [loadingST, setLoadingST] = useState(false);
  const [form, setForm] = useState({ subtopic_id: "", difficulty: "medium", interview_type: subject.name === "Behavioral" ? "hr" : "technical" });
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/interview/topics?subject_id=${subject.id}`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setTopics(d); setLoadingT(false); }).catch(() => setLoadingT(false));
  }, [subject.id]);

  function handleSelectTopic(t) {
    setSelectedTopic(t); setSubtopics([]); setForm(f => ({ ...f, subtopic_id: "" })); setLoadingST(true);
    fetch(`${API}/interview/subtopics?topic_id=${t.id}`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setSubtopics(d); if (d.length > 0) setForm(f => ({ ...f, subtopic_id: d[0].id })); setLoadingST(false); })
      .catch(() => setLoadingST(false));
  }

  async function startInterview() {
    setError(""); setStarting(true);
    if (!selectedTopic) { setError("Please select a topic."); setStarting(false); return; }
    try {
      const payload = { interview_type: form.interview_type, subject_id: subject.id, topic_id: selectedTopic.id, subtopic_id: form.subtopic_id ? Number(form.subtopic_id) : null, difficulty: form.difficulty };
      const r = await fetch(`${API}/interview/start`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify(payload) });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Failed to start"); setStarting(false); return; }
      onStart({ sessionId: d.session_id, subjectId: subject.id, topicId: selectedTopic.id, subtopicId: payload.subtopic_id, difficulty: payload.difficulty, interviewType: payload.interview_type, subjectName: subject.name });
    } catch { setError("Server error"); }
    setStarting(false);
  }

  const diffColors = { beginner: "#22C55E", intermediate: "#F59E0B", advanced: "#6366F1", expert: "#EF4444" };

  return (
    <SidebarLayout active="interview" user={user} onNav={onNav} onLogout={onLogout}>
      <div style={{ padding: "32px 40px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 28 }}>
          <button onClick={onBack} style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#94A3B8", padding: "7px 14px", borderRadius: 8, fontSize: 13 }}>← Back</button>
          <div>
            <h1 style={{ fontSize: 22, fontWeight: 700, color: "#fff" }}>{subject.name}</h1>
            <p style={{ color: "#94A3B8", fontSize: 13 }}>Select a topic to focus your practice</p>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20 }}>
          {/* Topics */}
          <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
            <h2 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 16 }}>Topics</h2>
            {loadingT ? <div style={{ textAlign: "center", padding: 40 }}><Spinner /></div> :
              topics.length === 0 ? <div style={{ color: "#64748B", fontSize: 14 }}>No topics found.</div> :
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {topics.map(t => (
                    <div key={t.id} onClick={() => handleSelectTopic(t)} style={{
                      padding: "14px 16px", borderRadius: 10, cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center",
                      background: selectedTopic?.id === t.id ? "rgba(99,102,241,0.1)" : "rgba(255,255,255,0.03)",
                      border: `1px solid ${selectedTopic?.id === t.id ? "#6366F1" : "rgba(255,255,255,0.07)"}`,
                    }}>
                      <div>
                        <div style={{ color: "#F1F5F9", fontWeight: 500, fontSize: 14 }}>{t.name}</div>
                        <div style={{ color: "#64748B", fontSize: 12, marginTop: 2 }}>{t.subtopic_count} subtopics · {t.question_count} questions</div>
                      </div>
                      <span style={{ color: selectedTopic?.id === t.id ? "#6366F1" : "#334155" }}>→</span>
                    </div>
                  ))}
                </div>
            }
          </div>

          {/* Configure */}
          <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, position: "sticky", top: 24 }}>
            <h2 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 16 }}>Configure</h2>
            {!selectedTopic ? (
              <p style={{ color: "#64748B", fontSize: 13, lineHeight: 1.6 }}>Select a topic from the left to configure your session.</p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                <div style={{ background: "rgba(99,102,241,0.08)", borderRadius: 8, padding: "10px 14px" }}>
                  <div style={{ color: "#64748B", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Topic</div>
                  <div style={{ color: "#6366F1", fontWeight: 600, fontSize: 14 }}>{selectedTopic.name}</div>
                </div>

                <div>
                  <label style={{ fontSize: 12, color: "#94A3B8", display: "block", marginBottom: 6 }}>Subtopic (Optional)</label>
                  {loadingST ? <Spinner /> : (
                    <select value={form.subtopic_id} onChange={e => setForm(f => ({ ...f, subtopic_id: e.target.value }))}
                      style={{ width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "9px 12px", color: "#F1F5F9", fontSize: 13 }}>
                      <option value="">Any Subtopic</option>
                      {subtopics.map(st => <option key={st.id} value={st.id}>{st.name}</option>)}
                    </select>
                  )}
                </div>

                <div>
                  <label style={{ fontSize: 12, color: "#94A3B8", display: "block", marginBottom: 8 }}>Difficulty</label>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
                    {["beginner", "intermediate", "advanced", "expert"].map(d => (
                      <button key={d} onClick={() => setForm(f => ({ ...f, difficulty: d }))} style={{
                        padding: "8px 0", borderRadius: 6, fontSize: 12, fontWeight: 500, textTransform: "capitalize",
                        background: form.difficulty === d ? diffColors[d] : "rgba(255,255,255,0.04)",
                        border: `1px solid ${form.difficulty === d ? diffColors[d] : "rgba(255,255,255,0.08)"}`,
                        color: form.difficulty === d ? "#fff" : "#94A3B8",
                      }}>{d}</button>
                    ))}
                  </div>
                </div>

                {error && <div style={{ color: "#FCA5A5", fontSize: 13, background: "rgba(239,68,68,0.1)", padding: "8px 12px", borderRadius: 6 }}>{error}</div>}

                <button onClick={startInterview} disabled={starting}
                  style={{ background: "#6366F1", color: "#fff", fontWeight: 600, fontSize: 14, padding: "12px", borderRadius: 8, marginTop: 4 }}>
                  {starting ? <Spinner /> : "Start Interview →"}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </SidebarLayout>
  );
}

// ─── Interview Room Page ───────────────────────────────────────────────────────
function InterviewRoomPage({ token, user, sessionData, onResult, onBack }) {
  const [question, setQuestion]     = useState(null);
  const [answer, setAnswer]         = useState("");
  const [result, setResult]         = useState(null);
  const [loading, setLoading]       = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError]           = useState("");
  const [questionNum, setQuestionNum] = useState(1);
  const [elapsed, setElapsed]       = useState(0);

  // ── Voice recording ─────────────────────────────────────────────────
  const [recording, setRecording]     = useState(false);
  const [voiceLoading, setVoiceLoading] = useState(false);
  const [voiceResult, setVoiceResult] = useState(null);
  const audioCtxRef  = useRef(null);
  const processorRef = useRef(null);
  const samplesRef   = useRef([]);
  const srRef        = useRef(44100);

  // ── Vision ───────────────────────────────────────────────────────────
  const [visionDataPoints, setVisionDataPoints] = useState([]);
  const [latestVision, setLatestVision]         = useState(null);

  // ── Follow-up ────────────────────────────────────────────────────────
  const [followup, setFollowup]             = useState(null);   // { question }
  const [followupAnswer, setFollowupAnswer] = useState("");
  const [followupLoading, setFollowupLoading] = useState(false);
  const [followupSubmitting, setFollowupSubmitting] = useState(false);
  const [followupResult, setFollowupResult] = useState(null);

  const { sessionId, subjectId, topicId, subtopicId, difficulty, subjectName } = sessionData;

  useEffect(() => { fetchQuestion(); }, []);
  useEffect(() => {
    const t = setInterval(() => setElapsed(e => e + 1), 1000);
    return () => clearInterval(t);
  }, []);

  function fmtTime(s) {
    return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
  }

  async function fetchQuestion() {
    setLoading(true); setResult(null); setAnswer(""); setError("");
    setVoiceResult(null); setVisionDataPoints([]);
    setFollowup(null); setFollowupAnswer(""); setFollowupResult(null);
    try {
      let q = `subject_id=${subjectId}&difficulty=${difficulty}&session_id=${sessionId}`;
      if (topicId)    q += `&topic_id=${topicId}`;
      if (subtopicId) q += `&subtopic_id=${subtopicId}`;
      const r = await fetch(`${API}/interview/question?${q}`, { headers: { Authorization: `Bearer ${token}` } });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Failed to fetch question"); setLoading(false); return; }
      setQuestion(d);
    } catch { setError("Server error"); }
    setLoading(false);
  }

  async function submitAnswer() {
    const finalAnswer = answer.trim() || voiceResult?.transcript || "";
    if (!finalAnswer) { setError("Record or type your answer first."); return; }
    setError(""); setSubmitting(true);
    let avgFaceScore = 70;
    if (visionDataPoints.length > 0) {
      const sum = visionDataPoints.reduce((acc, p) => acc + (p.eye_contact * 0.5 + p.head_stability * 0.5), 0);
      avgFaceScore = sum / visionDataPoints.length;
    }
    try {
      const r = await fetch(`${API}/interview/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          session_id: sessionId, question_id: question.question_id,
          user_answer: finalAnswer,
          voice_score: voiceResult ? voiceResult.overall_voice_score : 0,
          face_score: avgFaceScore,
        }),
      });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Submission failed"); setSubmitting(false); return; }
      setResult(d);
      // Trigger follow-up for weak answers
      if (d.total_score < 70) {
        fetchFollowup(question.question_text, finalAnswer);
      }
    } catch { setError("Server error"); }
    setSubmitting(false);
  }

  async function fetchFollowup(questionText, userAnswer) {
    setFollowupLoading(true);
    try {
      const r = await fetch(`${API}/ai/followup`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ question_text: questionText, user_answer: userAnswer, session_id: sessionId }),
      });
      const d = await r.json();
      if (r.ok) setFollowup({ question: d.followup_question });
    } catch { /* silent — follow-up is optional */ }
    setFollowupLoading(false);
  }

  async function submitFollowupAnswer() {
    if (!followupAnswer.trim()) return;
    setFollowupSubmitting(true);
    try {
      const r = await fetch(`${API}/interview/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          session_id: sessionId, question_id: question.question_id,
          user_answer: followupAnswer, voice_score: 0, face_score: 0,
        }),
      });
      const d = await r.json();
      if (r.ok) setFollowupResult(d);
    } catch { /* silent */ }
    setFollowupSubmitting(false);
  }

  function handleVisionResult(data) {
    setLatestVision(data);
    setVisionDataPoints(prev => [...prev, data]);
  }

  async function startRecording() {
    setVoiceResult(null); samplesRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false, sampleRate: 44100 }
      });
      const ctx = new AudioContext();
      audioCtxRef.current = ctx;
      srRef.current = ctx.sampleRate;
      const src = ctx.createMediaStreamSource(stream);
      const proc = ctx.createScriptProcessor(4096, 1, 1);
      processorRef.current = proc;
      proc.onaudioprocess = (e) => samplesRef.current.push(new Float32Array(e.inputBuffer.getChannelData(0)));
      src.connect(proc); proc.connect(ctx.destination);
      ctx._stream = stream;
      setRecording(true);
    } catch { setError("Microphone access denied."); }
  }

  async function stopRecording() {
    if (!audioCtxRef.current) return;
    setRecording(false); setVoiceLoading(true);
    try {
      if (processorRef.current) { processorRef.current.disconnect(); processorRef.current = null; }
      if (audioCtxRef.current._stream) audioCtxRef.current._stream.getTracks().forEach(t => t.stop());
      await audioCtxRef.current.close(); audioCtxRef.current = null;
      const chunks = samplesRef.current;
      const total  = chunks.reduce((a, c) => a + c.length, 0);
      const merged = new Float32Array(total);
      let off = 0;
      for (const c of chunks) { merged.set(c, off); off += c.length; }
      const wav = buildWav(merged, srRef.current);
      const fd  = new FormData(); fd.append("audio", wav, "answer.wav");
      const res = await fetch(`${API}/api/voice/analyze`, { method: "POST", body: fd });
      if (res.ok) {
        const data = await res.json();
        setVoiceResult(data);
        if (data.transcript) setAnswer(data.transcript);
      }
    } catch (e) { setError(`Voice error: ${e.message}`); }
    setVoiceLoading(false);
  }

  // Derived display values
  const pace       = voiceResult?.details?.pace;
  const confidence = voiceResult?.details?.confidence;
  const fillers    = voiceResult?.details?.filler_words;
  const liveText   = voiceResult?.transcript || answer;
  const eyeVal     = latestVision ? Math.round(latestVision.eye_contact)     : null;
  const headVal    = latestVision ? Math.round(latestVision.head_stability)  : null;
  const emotion    = latestVision?.emotion || "Calm";
  const headLabel  = headVal === null ? "Good" : headVal >= 75 ? "Good" : headVal >= 50 ? "Fair" : "Low";

  return (
    <div style={{ height: "100vh", overflow: "hidden", display: "flex", flexDirection: "column", background: "#0B0F1E" }}>

      {/* ── Header (52px) ─────────────────────────────────────────────── */}
      <div style={{ flex: "0 0 52px", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 24px", background: "#0F1629", borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 32, height: 32, background: "#6366F1", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17 }}>🤖</div>
          <div>
            <div style={{ color: "#F1F5F9", fontWeight: 700, fontSize: 15 }}>Interview Room</div>
            <div style={{ color: "#475569", fontSize: 10, textTransform: "uppercase", letterSpacing: "0.1em" }}>SESSION: {(subjectName || "INTERVIEW").toUpperCase()}</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#94A3B8", padding: "7px 14px", borderRadius: 8, fontSize: 12, display: "flex", alignItems: "center", gap: 5 }}>
            ⚙ Settings
          </button>
          <button onClick={onBack} style={{ background: "rgba(239,68,68,0.15)", border: "1px solid rgba(239,68,68,0.3)", color: "#F87171", padding: "7px 16px", borderRadius: 8, fontSize: 12, fontWeight: 600, display: "flex", alignItems: "center", gap: 5 }}>
            📞 End Interview
          </button>
        </div>
      </div>

      {/* ── Content (flex 1, no overflow) ─────────────────────────────── */}
      <div style={{ flex: 1, minHeight: 0, display: "flex", flexDirection: "column", gap: 10, padding: "10px 24px" }}>

        {/* Row 1: Two columns (42%) */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, flex: "0 0 42%" }}>

          {/* Left — AI + Question */}
          <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, padding: "16px 18px", display: "flex", flexDirection: "column", overflow: "hidden" }}>
            <div style={{ fontSize: 10, color: "#6366F1", fontWeight: 700, letterSpacing: "0.1em", marginBottom: 10, display: "flex", alignItems: "center", gap: 6, flexShrink: 0 }}>
              <span style={{ width: 6, height: 6, background: "#6366F1", borderRadius: "50%", display: "inline-block" }} />
              AI INTERVIEWER
            </div>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 12, flexShrink: 0 }}>
              <div style={{ position: "relative", width: 80, height: 80, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <div style={{ position: "absolute", inset: 0, borderRadius: "50%", border: "1px dashed rgba(99,102,241,0.35)", animation: "ringPulse 3s ease-in-out infinite" }} />
                <div style={{ position: "absolute", inset: 10, borderRadius: "50%", border: "1px dashed rgba(99,102,241,0.2)", animation: "ringPulse 3s ease-in-out infinite 0.7s" }} />
                <div style={{ width: 52, height: 52, borderRadius: "50%", background: "rgba(99,102,241,0.2)", border: "2px solid rgba(99,102,241,0.5)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24 }}>🤖</div>
              </div>
            </div>
            <div style={{ flex: 1, overflow: "hidden" }}>
              {loading ? (
                <div style={{ textAlign: "center", paddingTop: 8 }}><Spinner /></div>
              ) : question ? (
                <>
                  <div style={{ fontSize: 10, color: "#6366F1", fontWeight: 700, letterSpacing: "0.1em", marginBottom: 6, textTransform: "uppercase" }}>Current Question</div>
                  <p style={{ color: "#F1F5F9", fontWeight: 600, fontSize: 14, lineHeight: 1.6, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 4, WebkitBoxOrient: "vertical" }}>
                    "{question.question_text}"
                  </p>
                  <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap" }}>
                    <span style={{ background: "rgba(99,102,241,0.12)", color: "#A5B4FC", fontSize: 10, padding: "2px 8px", borderRadius: 4, fontWeight: 600 }}>Q{questionNum}</span>
                    <span style={{ background: "rgba(255,255,255,0.04)", color: "#64748B", fontSize: 10, padding: "2px 8px", borderRadius: 4 }}>{question.difficulty}</span>
                    <span style={{ background: "rgba(255,255,255,0.04)", color: "#64748B", fontSize: 10, padding: "2px 8px", borderRadius: 4 }}>{question.type}</span>
                  </div>
                </>
              ) : (
                <div style={{ color: "#EF4444", fontSize: 13 }}>{error || "No more questions available."}</div>
              )}
            </div>
          </div>

          {/* Right — Live camera */}
          <div style={{ background: "#000", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, overflow: "hidden", display: "flex", flexDirection: "column" }}>
            <div style={{ flex: 1, minHeight: 0 }}>
              <VisionRecorder sessionId={sessionId} questionId={question?.question_id ?? 0} onVisionResult={handleVisionResult} />
            </div>
            <div style={{ flex: "0 0 40px", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", background: "rgba(0,0,0,0.6)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
              {[
                { label: "Eye Contact",    value: eyeVal !== null ? `${eyeVal}%` : "—",  color: "#22C55E" },
                { label: "Head Stability", value: headLabel,                               color: "#6366F1" },
                { label: "Emotion",        value: emotion,                                 color: "#F59E0B" },
              ].map((m, i) => (
                <div key={m.label} style={{ textAlign: "center", padding: "6px 4px", borderRight: i < 2 ? "1px solid rgba(255,255,255,0.06)" : "none" }}>
                  <div style={{ color: "#64748B", fontSize: 9, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 1 }}>{m.label}</div>
                  <div style={{ color: m.color, fontWeight: 700, fontSize: 13, textTransform: "capitalize" }}>{m.value}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Row 2: Live Transcript (17%) */}
        <div style={{ flex: "0 0 17%", background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, padding: "10px 16px", display: "flex", flexDirection: "column", overflow: "hidden" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 7, flexShrink: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 7, fontWeight: 600, color: "#F1F5F9", fontSize: 13 }}>
              <span style={{ fontSize: 14 }}>👤</span> Live Transcript
            </div>
            <span style={{ fontSize: 11, color: recording ? "#22C55E" : voiceLoading ? "#F59E0B" : voiceResult ? "#64748B" : "#475569", display: "flex", alignItems: "center", gap: 4, animation: recording ? "pulse 1.5s infinite" : "none" }}>
              {recording ? "● Recording..." : voiceLoading ? "⏳ Analyzing..." : voiceResult ? "Analysis complete" : "Capturing audio..."}
            </span>
          </div>
          <p style={{ color: "#94A3B8", fontSize: 13, lineHeight: 1.65, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" }}>
            {liveText ? `"${liveText}"` : "Press the 🎙 mic button below to start recording your answer..."}
          </p>
        </div>

        {/* Row 3: Voice Metrics OR Score Result (flex 1) */}
        {!result ? (
          <div style={{ flex: 1, minHeight: 0, background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, padding: "10px 18px", display: "flex", flexDirection: "column", overflow: "hidden" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 7, fontWeight: 600, color: "#F1F5F9", fontSize: 13, marginBottom: 10, flexShrink: 0 }}>
              <span style={{ fontSize: 14 }}>▦</span> Voice Metrics
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 18, flex: 1, alignItems: "start" }}>
              {[
                { label: "Pace",        value: pace ? `${pace.wpm} WPM` : "—",  bar: pace ? Math.min(100, (pace.wpm / 200) * 100) : 0, color: "#6366F1", desc: pace?.label || "Steady and clear delivery speed." },
                { label: "Confidence",  value: confidence ? (confidence.confidence_score >= 70 ? "High" : confidence.confidence_score >= 45 ? "Medium" : "Low") : "—", bar: confidence?.confidence_score || 0, color: "#22C55E", desc: "Low pitch variability and firm tone." },
                { label: "Filler Words",value: fillers ? `${fillers.count} Detected` : "—", bar: fillers ? Math.min(100, fillers.count * 15) : 0, color: "#F59E0B", desc: fillers?.count > 0 ? `${fillers.filler_ratio_percent}% of speech` : "Clean speech detected." },
              ].map(m => (
                <div key={m.label}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ color: "#94A3B8", fontSize: 12 }}>{m.label}</span>
                    <span style={{ color: m.color, fontSize: 12, fontWeight: 700 }}>{m.value}</span>
                  </div>
                  <Bar value={m.bar} color={m.color} height={5} />
                  <p style={{ color: "#475569", fontSize: 11, marginTop: 5, lineHeight: 1.4 }}>{m.desc}</p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="fade-in" style={{ flex: 1, minHeight: 0, background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, padding: "12px 18px", display: "flex", gap: 16, overflow: "hidden" }}>
            {/* Score ring */}
            <div style={{ flex: "0 0 72px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
              <div style={{ fontSize: 10, color: "#64748B", marginBottom: 4 }}>TOTAL</div>
              <div style={{ fontSize: 38, fontWeight: 800, color: result.total_score >= 70 ? "#22C55E" : result.total_score >= 45 ? "#F59E0B" : "#EF4444", lineHeight: 1 }}>{Math.round(result.total_score)}</div>
              <div style={{ fontSize: 10, color: "#475569", marginTop: 2 }}>/ 100</div>
            </div>
            {/* Score bars */}
            <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", gap: 7 }}>
              {[
                { label: "NLP Score", value: result.nlp_score, color: "#6366F1" },
                { label: "Voice", value: result.voice_score, color: "#F59E0B" },
                { label: "Eye Contact", value: result.face_score, color: "#22C55E" },
              ].map(s => (
                <div key={s.label}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3, fontSize: 11 }}>
                    <span style={{ color: "#94A3B8" }}>{s.label}</span>
                    <span style={{ color: s.color, fontWeight: 600 }}>{Math.round(s.value)}%</span>
                  </div>
                  <Bar value={s.value} color={s.color} height={4} />
                </div>
              ))}
            </div>
            {/* Feedback + buttons */}
            <div style={{ flex: 1.4, display: "flex", flexDirection: "column", justifyContent: "center", gap: 10 }}>
              <div style={{ background: "rgba(99,102,241,0.08)", borderRadius: 8, padding: "10px 12px", borderLeft: "3px solid #6366F1" }}>
                <p style={{ color: "#C7D2FE", fontSize: 11, lineHeight: 1.5, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical" }}>
                  💡 {result.feedback}
                </p>
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={() => { setQuestionNum(n => n + 1); fetchQuestion(); }} style={{ flex: 1, background: "#6366F1", color: "#fff", fontWeight: 600, padding: "9px", borderRadius: 8, fontSize: 13 }}>
                  → Next Question
                </button>
                <button onClick={() => onResult(result)} style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", color: "#94A3B8", padding: "9px 14px", borderRadius: 8, fontSize: 13 }}>
                  Summary
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Follow-up Question Panel ─────────────────────────────────────── */}
      {followupLoading && (
        <div className="fade-in" style={{ margin: "0 0 8px", background: "#0F1629", border: "1px solid rgba(99,102,241,0.25)", borderRadius: 10, padding: "12px 16px", display: "flex", alignItems: "center", gap: 10 }}>
          <span className="spin" style={{ fontSize: 14, color: "#6366F1" }}>⟳</span>
          <span style={{ color: "#94A3B8", fontSize: 13 }}>Generating follow-up question...</span>
        </div>
      )}
      {followup && !followupLoading && (
        <div className="fade-in" style={{ margin: "0 0 8px", background: "#0F1629", border: "1px solid rgba(245,158,11,0.3)", borderRadius: 10, padding: "14px 16px", display: "flex", flexDirection: "column", gap: 10 }}>
          <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
            <span style={{ fontSize: 16, flexShrink: 0 }}>🔎</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 11, color: "#F59E0B", fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Follow-up Question</div>
              <div style={{ color: "#F1F5F9", fontSize: 14, lineHeight: 1.5 }}>{followup.question}</div>
            </div>
          </div>
          {!followupResult ? (
            <div style={{ display: "flex", gap: 8 }}>
              <input
                value={followupAnswer}
                onChange={e => setFollowupAnswer(e.target.value)}
                placeholder="Type your answer..."
                style={{ flex: 1, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, padding: "8px 12px", color: "#F1F5F9", fontSize: 13, outline: "none" }}
              />
              <button
                onClick={submitFollowupAnswer}
                disabled={followupSubmitting || !followupAnswer.trim()}
                style={{ background: "#F59E0B", color: "#000", fontWeight: 700, fontSize: 13, padding: "8px 16px", borderRadius: 8, border: "none", cursor: "pointer", opacity: followupSubmitting ? 0.6 : 1 }}
              >
                {followupSubmitting ? "..." : "Submit"}
              </button>
            </div>
          ) : (
            <div style={{ background: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 8, padding: "8px 12px", display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ color: "#22C55E", fontWeight: 700, fontSize: 14 }}>{Math.round(followupResult.total_score)}</span>
              <span style={{ color: "#94A3B8", fontSize: 12 }}>/ 100 on follow-up · {followupResult.feedback?.slice(0, 80)}...</span>
            </div>
          )}
        </div>
      )}

      {/* ── Bottom bar (52px) ──────────────────────────────────────────── */}
      <div style={{ flex: "0 0 52px", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 24px", background: "#0F1629", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#6366F1", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 11 }}>
            {(user?.name || "U")[0].toUpperCase()}
          </div>
          <div style={{ width: 28, height: 28, borderRadius: "50%", background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14 }}>🤖</div>
          <span style={{ color: "#475569", fontSize: 12 }}>Interview in progress: {fmtTime(elapsed)} / 30:00</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {error && <span style={{ color: "#F87171", fontSize: 11, maxWidth: 220 }}>{error}</span>}
          {/* Mic button */}
          {question && !result && (
            <button
              onClick={recording ? stopRecording : startRecording}
              disabled={voiceLoading}
              title={recording ? "Stop Recording" : "Start Recording"}
              style={{
                width: 36, height: 36, borderRadius: "50%",
                background: recording ? "rgba(239,68,68,0.2)" : "rgba(99,102,241,0.15)",
                border: `1px solid ${recording ? "rgba(239,68,68,0.5)" : "rgba(99,102,241,0.35)"}`,
                color: recording ? "#F87171" : "#A5B4FC",
                display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
                animation: recording ? "pulse 1.2s infinite" : "none",
                cursor: voiceLoading ? "not-allowed" : "pointer",
              }}
            >
              {voiceLoading ? <Spinner /> : "🎙"}
            </button>
          )}
          {question && !result && (
            <button
              onClick={() => { setQuestionNum(n => n + 1); fetchQuestion(); }}
              style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#94A3B8", padding: "0 18px", height: 34, borderRadius: 8, fontSize: 13 }}
            >
              Skip Question
            </button>
          )}
          {question && !result && (
            <button
              onClick={submitAnswer}
              disabled={submitting}
              style={{ background: "#6366F1", color: "#fff", fontWeight: 600, padding: "0 22px", height: 34, borderRadius: 8, fontSize: 13, opacity: submitting ? 0.7 : 1 }}
            >
              {submitting ? <Spinner /> : "Submit Answer"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Results Page ──────────────────────────────────────────────────────────────
function ResultsPage({ token, user, lastResult, onBack, onRetake }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/analytics/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setAnalytics(d); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const score = lastResult?.total_score ?? analytics?.avg_nlp_score ?? 0;
  const answerQ = lastResult?.nlp_score ?? 0;
  const voiceC = lastResult?.voice_score ?? 0;
  const eyeC = lastResult?.face_score ?? 0;
  const feedback = lastResult?.feedback || "";

  const radarData = [
    { subject: "COMMUNICATION", A: Math.min(100, answerQ + 5) },
    { subject: "CONFIDENCE", A: voiceC },
    { subject: "CLARITY", A: Math.min(100, (answerQ + voiceC) / 2) },
    { subject: "TECHNICAL DEPTH", A: answerQ },
    { subject: "STRUCTURE", A: Math.min(100, answerQ - 5) },
  ];

  function parseStrengths() {
    if (answerQ >= 75) return [{ key: "Strong technical knowledge", desc: "Your answers showed solid understanding of core concepts." }];
    return [{ key: "Effort & thoroughness", desc: "You provided complete answers with good detail." }];
  }
  function parseImprovements() {
    const items = [];
    if (voiceC < 75) items.push({ key: "Filler words", desc: "Try to reduce use of \"um\" and \"like\" for clearer delivery." });
    if (eyeC < 75) items.push({ key: "Eye contact", desc: "Try to look directly into the camera lens more consistently." });
    if (items.length === 0) items.push({ key: "Pace", desc: "Maintain a steady speaking pace throughout your answers." });
    return items;
  }

  return (
    <div style={{ minHeight: "100vh", background: "#0B0F1E" }}>
      {/* Navbar */}
      <nav style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "14px 40px", background: "#0F1629", borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 30, height: 30, background: "#6366F1", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 14, fontWeight: 700 }}>◈</div>
          <span style={{ fontWeight: 700, color: "#fff", fontSize: 15 }}>InterviewAI</span>
        </div>
        <div style={{ display: "flex", gap: 12 }}>
          <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#1E293B", display: "flex", alignItems: "center", justifyContent: "center", color: "#94A3B8", fontSize: 14, cursor: "pointer" }}>🔔</div>
          <div onClick={onBack} style={{ width: 32, height: 32, borderRadius: "50%", background: "#6366F1", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>{(user?.name || "U")[0].toUpperCase()}</div>
        </div>
      </nav>

      <div style={{ maxWidth: 960, margin: "0 auto", padding: "40px 24px" }}>
        <h1 style={{ textAlign: "center", fontSize: 32, fontWeight: 800, color: "#fff", marginBottom: 32 }}>Performance Summary</h1>

        {loading ? (
          <div style={{ textAlign: "center", padding: 60 }}><Spinner /></div>
        ) : (
          <>
            {/* Score ring */}
            <div className="fade-in" style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: 32 }}>
              <CircularScore score={Math.round(score)} size={160} />
              <p style={{ color: "#94A3B8", fontSize: 14, marginTop: 16, textAlign: "center", maxWidth: 400, lineHeight: 1.6 }}>
                {score >= 80 ? "Impressive performance! Your technical answers were highly structured, showing strong domain knowledge." :
                  score >= 60 ? "Good performance! Keep practicing to strengthen your weak areas." :
                  "Keep going! Consistent practice will improve your scores significantly."}
              </p>
            </div>

            {/* 3 score cards */}
            <div className="fade-in" style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 24 }}>
              {[
                { label: "Answer Quality", value: Math.round(answerQ), color: "#22C55E", icon: "✓" },
                { label: "Voice Confidence", value: Math.round(voiceC), color: "#6366F1", icon: "🎙" },
                { label: "Eye Contact", value: Math.round(eyeC), color: "#F59E0B", icon: "👁" },
              ].map(s => (
                <div key={s.label} style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: "20px 22px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                    <span style={{ color: "#94A3B8", fontSize: 13 }}>{s.label}</span>
                    <span style={{ color: s.color, fontSize: 18 }}>{s.icon}</span>
                  </div>
                  <div style={{ color: "#fff", fontWeight: 700, fontSize: 28, marginBottom: 10 }}>{s.value}%</div>
                  <Bar value={s.value} color={s.color} />
                </div>
              ))}
            </div>

            {/* Radar + AI Feedback */}
            <div className="fade-in" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 }}>
              {/* Radar */}
              <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
                <h3 style={{ color: "#fff", fontWeight: 700, fontSize: 15, marginBottom: 20 }}>Skills Radar</h3>
                <ResponsiveContainer width="100%" height={240}>
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="rgba(255,255,255,0.08)" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: "#64748B", fontSize: 10 }} />
                    <Radar name="Score" dataKey="A" stroke="#6366F1" fill="#6366F1" fillOpacity={0.35} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              {/* AI Feedback */}
              <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
                <h3 style={{ color: "#fff", fontWeight: 700, fontSize: 15, marginBottom: 20 }}>AI Feedback Analysis</h3>
                <div style={{ marginBottom: 16 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 10, fontSize: 11, fontWeight: 700, color: "#22C55E", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    <span>✅</span> TOP STRENGTHS
                  </div>
                  {parseStrengths().map((s, i) => (
                    <div key={i} style={{ background: "rgba(34,197,94,0.06)", border: "1px solid rgba(34,197,94,0.15)", borderRadius: 8, padding: "10px 14px", marginBottom: 8, fontSize: 13, color: "#94A3B8", lineHeight: 1.5 }}>
                      <strong style={{ color: "#22C55E" }}>{s.key}:</strong> {s.desc}
                    </div>
                  ))}
                </div>
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 10, fontSize: 11, fontWeight: 700, color: "#F59E0B", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    <span>⚠</span> IMPROVEMENT AREAS
                  </div>
                  {parseImprovements().map((s, i) => (
                    <div key={i} style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.15)", borderRadius: 8, padding: "10px 14px", marginBottom: 8, fontSize: 13, color: "#94A3B8", lineHeight: 1.5 }}>
                      <strong style={{ color: "#F59E0B" }}>{s.key}:</strong> {s.desc}
                    </div>
                  ))}
                  {feedback && (
                    <div style={{ background: "rgba(99,102,241,0.06)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: 8, padding: "10px 14px", fontSize: 13, color: "#94A3B8", lineHeight: 1.5 }}>
                      {feedback}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Buttons */}
            <div className="fade-in" style={{ display: "flex", justifyContent: "center", gap: 16 }}>
              <button onClick={onBack} style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.12)", color: "#F1F5F9", padding: "12px 28px", borderRadius: 10, fontSize: 14, fontWeight: 500, display: "flex", alignItems: "center", gap: 8 }}>
                ⊞ Back to Dashboard
              </button>
              <button onClick={onRetake} style={{ background: "#6366F1", color: "#fff", fontWeight: 600, padding: "12px 28px", borderRadius: 10, fontSize: 14, display: "flex", alignItems: "center", gap: 8 }}>
                ↺ Retake Interview
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

// ─── Analytics Page ────────────────────────────────────────────────────────────
function AnalyticsPage({ token, user, onNav, onLogout }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pdfMsg, setPdfMsg] = useState("");
  const [showAllStreaks, setShowAllStreaks] = useState(false);

  useEffect(() => {
    fetch(`${API}/analytics/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => { setAnalytics(d); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const recent = analytics?.recent_sessions || [];
  const subjectBreakdown = analytics?.subject_breakdown || {};
  const topicBreakdown = analytics?.topic_breakdown || {};

  // Build chart data only from real sessions
  const chartData = recent.length > 0
    ? [...recent].reverse().map((s, i) => ({ name: `S${i + 1}`, score: s.avg_score || 0, target: 75 }))
    : null;

  // Radar built from real subject scores (at least 3 axes needed)
  const subjectEntries = Object.entries(subjectBreakdown);
  const radarData = subjectEntries.length >= 3
    ? subjectEntries.slice(0, 5).map(([k, v]) => ({ subject: k.toUpperCase(), A: v }))
    : null;

  const displayTopics = Object.entries(topicBreakdown).slice(0, 6).map(([k, v]) => ({ name: k, value: v }));
  const topSubject = analytics?.strongest_topic || subjectEntries.sort(([,a],[,b]) => b - a)[0]?.[0] || "—";

  function statusBadge(score) {
    if (score >= 85) return { label: "PASSED", bg: "rgba(34,197,94,0.1)", color: "#22C55E" };
    if (score >= 70) return { label: "IMPROVED", bg: "rgba(99,102,241,0.1)", color: "#6366F1" };
    return { label: "REVIEWED", bg: "rgba(100,116,139,0.1)", color: "#94A3B8" };
  }

  return (
    <SidebarLayout active="analytics" user={user} onNav={onNav} onLogout={onLogout} showUser>
      <div style={{ padding: "32px 40px" }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 28 }}>
          <div>
            <h1 style={{ fontSize: 26, fontWeight: 700, color: "#fff", marginBottom: 4 }}>Performance Analytics</h1>
            <p style={{ color: "#94A3B8", fontSize: 14 }}>Deep dive into your interview readiness and growth metrics.</p>
          </div>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <div style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#94A3B8", padding: "8px 14px", borderRadius: 8, fontSize: 13 }}>
              📅 Last 30 Days
            </div>
            <button onClick={() => setPdfMsg("PDF export coming soon!")} style={{ background: "#6366F1", color: "#fff", fontWeight: 600, padding: "8px 16px", borderRadius: 8, fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
              ⬇ Export PDF
            </button>
          </div>
        </div>

        {pdfMsg && (
          <div style={{ background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.3)", borderRadius: 8, padding: "10px 16px", marginBottom: 16, color: "#A5B4FC", fontSize: 13 }}>
            ℹ {pdfMsg}
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: "center", padding: 80 }}><Spinner /></div>
        ) : (
          <>
            {/* Stats */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 20 }}>
              {[
                { label: "Total Interviews", value: analytics?.total_sessions ?? 0, sub: `${analytics?.total_answers ?? 0} answers submitted`, icon: "📋" },
                { label: "Average Score", value: `${analytics?.avg_nlp_score ?? 0}%`, sub: `Best: ${analytics?.best_score ?? 0}%`, icon: "🏆" },
                { label: "Top Performance Area", value: topSubject, sub: analytics?.total_sessions ? "Based on your sessions" : "Complete sessions to unlock", icon: "⭐", small: true },
              ].map(s => (
                <div key={s.label} className="fade-in" style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: "20px 22px", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                  <div>
                    <div style={{ color: "#94A3B8", fontSize: 13, marginBottom: 8 }}>{s.label}</div>
                    <div style={{ color: "#fff", fontWeight: 700, fontSize: s.small ? 20 : 30, marginBottom: 6 }}>{s.value}</div>
                    <div style={{ color: "#22C55E", fontSize: 12, display: "flex", alignItems: "center", gap: 4 }}>↗ {s.sub}</div>
                  </div>
                  <span style={{ fontSize: 24, color: "#334155" }}>{s.icon}</span>
                </div>
              ))}
            </div>

            {/* Score chart + Topic mastery */}
            <div style={{ display: "grid", gridTemplateColumns: "1.5fr 1fr", gap: 16, marginBottom: 16 }}>
              {/* Chart */}
              <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                  <h3 style={{ color: "#fff", fontWeight: 700, fontSize: 15 }}>Interview Score Over Time</h3>
                  <div style={{ display: "flex", gap: 14, fontSize: 12, color: "#64748B" }}>
                    <span style={{ display: "flex", alignItems: "center", gap: 4 }}><span style={{ width: 8, height: 8, background: "#6366F1", borderRadius: "50%", display: "inline-block" }} /> Actual Score</span>
                    <span style={{ display: "flex", alignItems: "center", gap: 4 }}><span style={{ width: 8, height: 8, background: "#334155", borderRadius: "50%", display: "inline-block" }} /> Target</span>
                  </div>
                </div>
                <p style={{ color: "#64748B", fontSize: 12, marginBottom: 16 }}>Visualization of performance trends</p>
                {chartData ? (
                  <ResponsiveContainer width="100%" height={200}>
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#6366F1" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid stroke="rgba(255,255,255,0.04)" />
                      <XAxis dataKey="name" tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} />
                      <YAxis domain={[0, 100]} tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} />
                      <Tooltip contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: 8, color: "#F1F5F9", fontSize: 12 }} />
                      <Area type="monotone" dataKey="score" stroke="#6366F1" strokeWidth={2} fill="url(#scoreGrad)" dot={{ fill: "#6366F1", r: 3 }} />
                      <Area type="monotone" dataKey="target" stroke="#334155" strokeWidth={1.5} strokeDasharray="4 4" fill="none" dot={false} />
                    </AreaChart>
                  </ResponsiveContainer>
                ) : (
                  <div style={{ height: 200, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: "#64748B", gap: 8 }}>
                    <span style={{ fontSize: 32 }}>📈</span>
                    <span style={{ fontSize: 13 }}>Complete interviews to see your score trend</span>
                  </div>
                )}
              </div>

              {/* Topic Mastery */}
              <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
                <h3 style={{ color: "#fff", fontWeight: 700, fontSize: 15, marginBottom: 20 }}>Topic Mastery</h3>
                {displayTopics.length > 0 ? (
                  <>
                    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                      {displayTopics.map(t => (
                        <div key={t.name}>
                          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
                            <span style={{ color: "#F1F5F9" }}>{t.name}</span>
                            <span style={{ color: "#6366F1", fontWeight: 600 }}>{t.value}%</span>
                          </div>
                          <Bar value={t.value} color="#6366F1" />
                        </div>
                      ))}
                    </div>
                    {analytics?.weakest_topic && analytics.weakest_topic !== "N/A" && (
                      <div style={{ marginTop: 16, background: "rgba(99,102,241,0.08)", borderRadius: 8, padding: "10px 14px" }}>
                        <div style={{ fontSize: 10, color: "#6366F1", fontWeight: 600, letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: 6 }}>INSIGHT</div>
                        <p style={{ color: "#94A3B8", fontSize: 12, lineHeight: 1.5 }}>
                          Focus on <strong style={{ color: "#fff" }}>{analytics.weakest_topic}</strong> — it's your lowest-scoring topic. More practice here will raise your overall score.
                        </p>
                      </div>
                    )}
                  </>
                ) : (
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: 120, color: "#64748B", gap: 8 }}>
                    <span style={{ fontSize: 28 }}>🎯</span>
                    <span style={{ fontSize: 13 }}>Submit answers to see topic mastery</span>
                  </div>
                )}
              </div>
            </div>

            {/* Skills radar + Recent streaks */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
                <h3 style={{ color: "#fff", fontWeight: 700, fontSize: 15 }}>Skills Profile</h3>
                <p style={{ color: "#64748B", fontSize: 12, marginBottom: 4 }}>Performance by subject area</p>
                {radarData ? (
                  <ResponsiveContainer width="100%" height={240}>
                    <RadarChart data={radarData}>
                      <PolarGrid stroke="rgba(255,255,255,0.07)" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: "#64748B", fontSize: 9 }} />
                      <Radar name="Skills" dataKey="A" stroke="#6366F1" fill="#6366F1" fillOpacity={0.3} />
                    </RadarChart>
                  </ResponsiveContainer>
                ) : (
                  <div style={{ height: 220, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: "#64748B", gap: 8 }}>
                    <span style={{ fontSize: 32 }}>🕸</span>
                    <span style={{ fontSize: 13 }}>Practice across subjects to see your skills profile</span>
                  </div>
                )}
              </div>

              <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
                <h3 style={{ color: "#fff", fontWeight: 700, fontSize: 15, marginBottom: 20 }}>Recent Interview Streaks</h3>
                {recent.length === 0 ? (
                  <div style={{ textAlign: "center", padding: "24px 0", color: "#64748B", fontSize: 13 }}>No sessions yet. Start your first interview!</div>
                ) : (
                  <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    {(showAllStreaks ? recent : recent.slice(0, 3)).map((s, i) => {
                      const badge = statusBadge(s.avg_score || 0);
                      return (
                        <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 12px", background: "rgba(255,255,255,0.03)", borderRadius: 10 }}>
                          <div style={{ width: 36, height: 36, borderRadius: 8, background: badge.bg, display: "flex", alignItems: "center", justifyContent: "center", color: badge.color, fontSize: 16, flexShrink: 0 }}>
                            {badge.label === "PASSED" ? "✓" : badge.label === "IMPROVED" ? "↗" : "◎"}
                          </div>
                          <div style={{ flex: 1, overflow: "hidden" }}>
                            <div style={{ color: "#F1F5F9", fontWeight: 500, fontSize: 13, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{s.subject || "Interview Session"}</div>
                            <div style={{ color: "#64748B", fontSize: 11 }}>Score: {s.avg_score ?? "—"}/100 • {s.date || "Recently"} • {s.answer_count ?? 0} answers</div>
                          </div>
                          <span style={{ background: badge.bg, color: badge.color, fontSize: 10, fontWeight: 700, padding: "3px 8px", borderRadius: 4, flexShrink: 0 }}>{badge.label}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
                {recent.length > 3 && (
                  <button onClick={() => setShowAllStreaks(p => !p)} style={{ width: "100%", marginTop: 16, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", color: "#94A3B8", padding: "10px", borderRadius: 8, fontSize: 13 }}>
                    {showAllStreaks ? "Show Less" : `View All ${recent.length} Sessions`}
                  </button>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </SidebarLayout>
  );
}

// ─── Profile Page ─────────────────────────────────────────────────────────────
function ProfilePage({ token, user, onNav, onLogout, onUpdateUser }) {
  const [analytics, setAnalytics] = useState(null);

  // Edit form state — pre-filled from user object
  const [name, setName]       = useState(user?.name || "");
  const [branch, setBranch]   = useState(user?.branch || "");
  const [year, setYear]       = useState(user?.year || "");
  const [college, setCollege] = useState(user?.college || "");
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileMsg, setProfileMsg]       = useState("");
  const [profileError, setProfileError]   = useState("");

  // Password state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword]         = useState("");
  const [pwSaving, setPwSaving]   = useState(false);
  const [pwMsg, setPwMsg]         = useState("");
  const [pwError, setPwError]     = useState("");

  useEffect(() => {
    fetch(`${API}/analytics/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => setAnalytics(d)).catch(() => {});
  }, []);

  async function saveProfile() {
    setProfileSaving(true); setProfileMsg(""); setProfileError("");
    try {
      const r = await fetch(`${API}/auth/profile`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ name, branch, year: year ? parseInt(year) : null, college }),
      });
      const d = await r.json();
      if (!r.ok) { setProfileError(d.detail || "Update failed"); }
      else { onUpdateUser(d); setProfileMsg("Profile saved successfully."); }
    } catch { setProfileError("Server error. Please try again."); }
    setProfileSaving(false);
  }

  async function changePassword() {
    if (!currentPassword || !newPassword) { setPwError("Both fields are required."); return; }
    if (newPassword.length < 6) { setPwError("New password must be at least 6 characters."); return; }
    setPwSaving(true); setPwMsg(""); setPwError("");
    try {
      const r = await fetch(`${API}/auth/password`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
      });
      const d = await r.json();
      if (!r.ok) { setPwError(d.detail || "Password change failed"); }
      else { setPwMsg("Password updated successfully."); setCurrentPassword(""); setNewPassword(""); }
    } catch { setPwError("Server error. Please try again."); }
    setPwSaving(false);
  }

  const inputStyle = { width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#F1F5F9", fontSize: 14 };
  const labelStyle = { fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" };

  return (
    <SidebarLayout active="profile" user={user} onNav={onNav} onLogout={onLogout} showUser>
      <div style={{ padding: "32px 40px", maxWidth: 700 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 32 }}>
          <div>
            <h1 style={{ fontSize: 24, fontWeight: 700, color: "#fff", marginBottom: 4 }}>Profile Settings</h1>
            <p style={{ color: "#94A3B8", fontSize: 14 }}>Update your account information and password.</p>
          </div>
          <button onClick={saveProfile} disabled={profileSaving} style={{ background: "#6366F1", color: "#fff", fontWeight: 600, padding: "10px 22px", borderRadius: 8, fontSize: 14, opacity: profileSaving ? 0.7 : 1 }}>
            {profileSaving ? <Spinner /> : "Save Changes"}
          </button>
        </div>

        {/* Avatar card */}
        <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 24, background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24 }}>
          <div style={{ width: 72, height: 72, borderRadius: "50%", background: "#6366F1", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 28, flexShrink: 0 }}>
            {(name || user?.name || "U")[0].toUpperCase()}
          </div>
          <div>
            <div style={{ color: "#fff", fontWeight: 700, fontSize: 20 }}>{name || user?.name || "—"}</div>
            <div style={{ color: "#94A3B8", fontSize: 14, marginTop: 2 }}>{user?.email || "—"}</div>
            <div style={{ marginTop: 8 }}>
              <span style={{ background: "rgba(99,102,241,0.15)", color: "#A5B4FC", fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 6 }}>
                {branch || user?.branch || "Student"} • Year {year || user?.year || "—"}
              </span>
            </div>
          </div>
        </div>

        {/* Personal Info form */}
        <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, marginBottom: 20 }}>
          <h3 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 20 }}>Personal Information</h3>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <label style={labelStyle}>Full Name</label>
              <input value={name} onChange={e => setName(e.target.value)} placeholder="Your full name" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>Email</label>
              <input value={user?.email || ""} disabled style={{ ...inputStyle, color: "#64748B", cursor: "not-allowed" }} />
            </div>
            <div>
              <label style={labelStyle}>Branch</label>
              <input value={branch} onChange={e => setBranch(e.target.value)} placeholder="e.g. CSE" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>Year</label>
              <select value={year} onChange={e => setYear(e.target.value)} style={{ ...inputStyle, cursor: "pointer" }}>
                <option value="">Select year</option>
                {[1, 2, 3, 4].map(y => <option key={y} value={y}>Year {y}</option>)}
              </select>
            </div>
            <div style={{ gridColumn: "1 / -1" }}>
              <label style={labelStyle}>College</label>
              <input value={college} onChange={e => setCollege(e.target.value)} placeholder="e.g. PSIT Kanpur" style={inputStyle} />
            </div>
          </div>
          {profileMsg   && <div style={{ marginTop: 14, color: "#22C55E", fontSize: 13 }}>✓ {profileMsg}</div>}
          {profileError && <div style={{ marginTop: 14, color: "#F87171", fontSize: 13 }}>✗ {profileError}</div>}
        </div>

        {/* Change Password */}
        <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, marginBottom: 20 }}>
          <h3 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 20 }}>Change Password</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div>
              <label style={labelStyle}>Current Password</label>
              <input type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} placeholder="••••••••" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>New Password</label>
              <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} placeholder="••••••••" style={inputStyle} />
            </div>
          </div>
          {pwMsg   && <div style={{ marginTop: 14, color: "#22C55E", fontSize: 13 }}>✓ {pwMsg}</div>}
          {pwError && <div style={{ marginTop: 14, color: "#F87171", fontSize: 13 }}>✗ {pwError}</div>}
          <button onClick={changePassword} disabled={pwSaving} style={{ marginTop: 16, background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", color: "#A5B4FC", fontWeight: 600, padding: "10px 20px", borderRadius: 8, fontSize: 14, opacity: pwSaving ? 0.7 : 1 }}>
            {pwSaving ? <Spinner /> : "Update Password"}
          </button>
        </div>

        {/* Performance summary */}
        {analytics && analytics.total_sessions > 0 && (
          <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, marginBottom: 20 }}>
            <h3 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 20 }}>Performance Summary</h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
              {[
                { label: "Sessions", value: analytics.total_sessions, color: "#6366F1" },
                { label: "Avg Score", value: `${analytics.avg_total_score}%`, color: "#22C55E" },
                { label: "Best Score", value: `${analytics.best_score}%`, color: "#F59E0B" },
              ].map(s => (
                <div key={s.label} style={{ background: "rgba(255,255,255,0.03)", borderRadius: 10, padding: "14px 16px", textAlign: "center" }}>
                  <div style={{ color: "#64748B", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>{s.label}</div>
                  <div style={{ color: s.color, fontWeight: 700, fontSize: 22 }}>{s.value}</div>
                </div>
              ))}
            </div>
            {analytics.strongest_topic && analytics.strongest_topic !== "N/A" && (
              <div style={{ marginTop: 16, display: "flex", gap: 16 }}>
                <div style={{ flex: 1, background: "rgba(34,197,94,0.06)", border: "1px solid rgba(34,197,94,0.15)", borderRadius: 8, padding: "10px 14px", fontSize: 13, color: "#94A3B8" }}>
                  <strong style={{ color: "#22C55E" }}>Strongest:</strong> {analytics.strongest_topic}
                </div>
                {analytics.weakest_topic && analytics.weakest_topic !== "N/A" && (
                  <div style={{ flex: 1, background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.15)", borderRadius: 8, padding: "10px 14px", fontSize: 13, color: "#94A3B8" }}>
                    <strong style={{ color: "#F59E0B" }}>Needs Work:</strong> {analytics.weakest_topic}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        <button onClick={onLogout} style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", color: "#F87171", padding: "11px 24px", borderRadius: 8, fontSize: 14, fontWeight: 500 }}>
          Sign Out
        </button>
      </div>
    </SidebarLayout>
  );
}

// ─── Settings Page ─────────────────────────────────────────────────────────────
function SettingsPage({ user, onNav, onLogout }) {
  // Load saved values from localStorage on mount
  const [cameras,   setCameras]   = useState([]);
  const [mics,      setMics]      = useState([]);
  const [camera,    setCamera]    = useState(() => localStorage.getItem("selected_camera")    || "");
  const [mic,       setMic]       = useState(() => localStorage.getItem("selected_microphone") || "");
  const [whisper,   setWhisper]   = useState(() => localStorage.getItem("whisper_model")      || "base");
  const [difficulty, setDifficulty] = useState(() => localStorage.getItem("default_difficulty") || "intermediate");
  const [voiceOn,   setVoiceOn]   = useState(() => localStorage.getItem("enable_voice_analysis")  !== "false");
  const [cameraOn,  setCameraOn]  = useState(() => localStorage.getItem("enable_camera_analysis") !== "false");
  const [saved,     setSaved]     = useState(false);

  useEffect(() => {
    if (!navigator.mediaDevices) return;
    navigator.mediaDevices.enumerateDevices().then(devices => {
      setCameras(devices.filter(d => d.kind === "videoinput"));
      setMics(devices.filter(d => d.kind === "audioinput"));
    }).catch(() => {});
  }, []);

  function saveSettings() {
    localStorage.setItem("selected_camera",        camera);
    localStorage.setItem("selected_microphone",    mic);
    localStorage.setItem("whisper_model",          whisper);
    localStorage.setItem("default_difficulty",     difficulty);
    localStorage.setItem("enable_voice_analysis",  String(voiceOn));
    localStorage.setItem("enable_camera_analysis", String(cameraOn));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  }

  const inputStyle = { width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "10px 14px", color: "#F1F5F9", fontSize: 14, cursor: "pointer" };
  const labelStyle = { fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" };

  function Toggle({ on, onToggle }) {
    return (
      <div onClick={onToggle} style={{ width: 44, height: 24, borderRadius: 99, background: on ? "#6366F1" : "#334155", position: "relative", cursor: "pointer", flexShrink: 0, transition: "background 0.2s" }}>
        <div style={{ position: "absolute", top: 3, left: on ? 23 : 3, width: 18, height: 18, borderRadius: "50%", background: "#fff", transition: "left 0.2s" }} />
      </div>
    );
  }

  return (
    <SidebarLayout active="settings" user={user} onNav={onNav} onLogout={onLogout} showUser>
      <div style={{ padding: "32px 40px", maxWidth: 680 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 32 }}>
          <div>
            <h1 style={{ fontSize: 24, fontWeight: 700, color: "#fff", marginBottom: 4 }}>Settings</h1>
            <p style={{ color: "#94A3B8", fontSize: 14 }}>Configure your interview preferences and hardware.</p>
          </div>
          <button onClick={saveSettings} style={{ background: "#6366F1", color: "#fff", fontWeight: 600, padding: "10px 22px", borderRadius: 8, fontSize: 14 }}>
            Save Settings
          </button>
        </div>

        {saved && (
          <div style={{ marginBottom: 20, background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.25)", borderRadius: 10, padding: "12px 16px", color: "#22C55E", fontSize: 14 }}>
            ✓ Settings saved successfully.
          </div>
        )}

        {/* Hardware Settings */}
        <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, marginBottom: 20 }}>
          <h3 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 20 }}>Hardware Settings</h3>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <label style={labelStyle}>Camera Device</label>
              <select value={camera} onChange={e => setCamera(e.target.value)} style={inputStyle}>
                <option value="">Default Camera</option>
                {cameras.map(d => <option key={d.deviceId} value={d.deviceId}>{d.label || `Camera ${d.deviceId.slice(0, 8)}`}</option>)}
              </select>
            </div>
            <div>
              <label style={labelStyle}>Microphone</label>
              <select value={mic} onChange={e => setMic(e.target.value)} style={inputStyle}>
                <option value="">Default Microphone</option>
                {mics.map(d => <option key={d.deviceId} value={d.deviceId}>{d.label || `Microphone ${d.deviceId.slice(0, 8)}`}</option>)}
              </select>
            </div>
          </div>
          {cameras.length === 0 && mics.length === 0 && (
            <p style={{ marginTop: 12, color: "#64748B", fontSize: 13 }}>
              Allow camera and microphone permissions to see your devices here.
            </p>
          )}
        </div>

        {/* AI Preferences */}
        <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, marginBottom: 20 }}>
          <h3 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 20 }}>AI Preferences</h3>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <label style={labelStyle}>Whisper Model</label>
              <select value={whisper} onChange={e => setWhisper(e.target.value)} style={inputStyle}>
                <option value="tiny">Tiny — Fastest, lower accuracy</option>
                <option value="base">Base — Recommended (balanced)</option>
                <option value="small">Small — Most accurate, slower</option>
              </select>
            </div>
            <div>
              <label style={labelStyle}>Default Difficulty</label>
              <select value={difficulty} onChange={e => setDifficulty(e.target.value)} style={inputStyle}>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="expert">Expert</option>
              </select>
            </div>
          </div>
          <div style={{ marginTop: 12, padding: "10px 14px", background: "rgba(99,102,241,0.06)", borderRadius: 8, fontSize: 12, color: "#94A3B8" }}>
            Whisper model affects transcription speed. Base is recommended for most systems.
          </div>
        </div>

        {/* Privacy Controls */}
        <div style={{ background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 24, marginBottom: 20 }}>
          <h3 style={{ color: "#fff", fontWeight: 600, fontSize: 15, marginBottom: 20 }}>Privacy Controls</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
            {[
              { label: "Enable Voice Analysis", sub: "Record and analyse your speech during interviews", on: voiceOn, toggle: () => setVoiceOn(v => !v) },
              { label: "Enable Camera Analysis", sub: "Track eye contact and facial expressions during interviews", on: cameraOn, toggle: () => setCameraOn(v => !v) },
            ].map((item, i) => (
              <div key={item.label} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 0", borderBottom: i === 0 ? "1px solid rgba(255,255,255,0.05)" : "none" }}>
                <div>
                  <div style={{ color: "#F1F5F9", fontSize: 14, fontWeight: 500, marginBottom: 3 }}>{item.label}</div>
                  <div style={{ color: "#64748B", fontSize: 12 }}>{item.sub}</div>
                </div>
                <Toggle on={item.on} onToggle={item.toggle} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </SidebarLayout>
  );
}

// ─── Onboarding Page ───────────────────────────────────────────────────────────
function OnboardingPage({ user, onFinish }) {
  const [step, setStep]           = useState(1);
  const [micOk, setMicOk]         = useState(null);   // null=untested, true=ok, false=denied
  const [camOk, setCamOk]         = useState(null);
  const [companies, setCompanies] = useState("");
  const [role, setRole]           = useState("");
  const [weakTopics, setWeakTopics] = useState([]);

  const SUBJECTS = ["DSA", "OOPS", "System Design", "DBMS", "OS & Networking", "Machine Learning", "Behavioral"];

  async function testHardware() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: true });
      stream.getTracks().forEach(t => t.stop());
      setMicOk(true); setCamOk(true);
    } catch {
      // Try audio only
      try {
        const s = await navigator.mediaDevices.getUserMedia({ audio: true });
        s.getTracks().forEach(t => t.stop());
        setMicOk(true); setCamOk(false);
      } catch {
        setMicOk(false); setCamOk(false);
      }
    }
  }

  function toggleTopic(t) {
    setWeakTopics(prev => prev.includes(t) ? prev.filter(x => x !== t) : [...prev, t]);
  }

  function finish() {
    if (companies) localStorage.setItem("target_companies", companies);
    if (role)      localStorage.setItem("target_role", role);
    if (weakTopics.length) localStorage.setItem("weak_topics", JSON.stringify(weakTopics));
    onFinish();
  }

  const inputStyle = { width: "100%", background: "#1E293B", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#F1F5F9", fontSize: 14 };

  // ── Step dots ──
  function StepDots() {
    return (
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 32, justifyContent: "center" }}>
        {[1, 2, 3, 4].map(n => (
          <div key={n} style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: n === step ? 28 : 10, height: 10, borderRadius: 99, background: n === step ? "#6366F1" : n < step ? "rgba(99,102,241,0.5)" : "rgba(255,255,255,0.1)", transition: "all 0.2s" }} />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", background: "#0B0F1E", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24 }}>
      {/* Logo */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 40 }}>
        <div style={{ width: 34, height: 34, background: "#6366F1", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700 }}>◈</div>
        <span style={{ color: "#fff", fontWeight: 700, fontSize: 16 }}>InterviewAI</span>
        <span style={{ color: "#64748B", fontSize: 13, marginLeft: 8 }}>Step {step} / 4</span>
      </div>

      <div style={{ width: "100%", maxWidth: 520, background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 16, padding: "36px 40px" }}>
        <StepDots />

        {/* ── Step 1: Welcome ─────────────────────────────────────── */}
        {step === 1 && (
          <>
            <h2 style={{ color: "#fff", fontSize: 22, fontWeight: 700, marginBottom: 8, textAlign: "center" }}>
              Welcome{user?.name ? `, ${user.name.split(" ")[0]}` : ""}! 👋
            </h2>
            <p style={{ color: "#94A3B8", fontSize: 14, textAlign: "center", marginBottom: 28 }}>
              Let's set up your experience in 4 quick steps.
            </p>
            <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
              {[
                { icon: "🧠", title: "AI Answer Evaluation",   desc: "NLP engine scores your answers against ideal responses" },
                { icon: "🎙", title: "Voice Confidence Analysis", desc: "Whisper transcribes and rates your pace, filler words, and tone" },
                { icon: "👁", title: "Facial Behaviour Tracking", desc: "MediaPipe tracks eye contact, head stability, and emotion" },
                { icon: "📈", title: "Adaptive Difficulty",    desc: "Questions get harder or easier based on your performance" },
              ].map(f => (
                <div key={f.title} style={{ display: "flex", gap: 14, background: "rgba(255,255,255,0.03)", borderRadius: 10, padding: "12px 14px" }}>
                  <span style={{ fontSize: 20, flexShrink: 0 }}>{f.icon}</span>
                  <div>
                    <div style={{ color: "#F1F5F9", fontWeight: 600, fontSize: 13, marginBottom: 2 }}>{f.title}</div>
                    <div style={{ color: "#64748B", fontSize: 12 }}>{f.desc}</div>
                  </div>
                </div>
              ))}
            </div>
            <button onClick={() => setStep(2)} style={{ width: "100%", background: "#6366F1", color: "#fff", fontWeight: 600, padding: "12px", borderRadius: 8, fontSize: 14 }}>
              Get Started →
            </button>
          </>
        )}

        {/* ── Step 2: Hardware Test ────────────────────────────────── */}
        {step === 2 && (
          <>
            <h2 style={{ color: "#fff", fontSize: 20, fontWeight: 700, marginBottom: 8, textAlign: "center" }}>Test Your Hardware</h2>
            <p style={{ color: "#94A3B8", fontSize: 14, textAlign: "center", marginBottom: 28 }}>
              Grant camera and microphone access for the full experience.
            </p>
            <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 24 }}>
              {[
                { label: "Microphone", status: micOk, icon: "🎙" },
                { label: "Camera",     status: camOk, icon: "📷" },
              ].map(h => (
                <div key={h.label} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.03)", borderRadius: 10, padding: "14px 16px" }}>
                  <span style={{ color: "#F1F5F9", fontSize: 14 }}>{h.icon}  {h.label}</span>
                  <span style={{ fontSize: 13, fontWeight: 600, color: h.status === null ? "#64748B" : h.status ? "#22C55E" : "#F87171" }}>
                    {h.status === null ? "Not tested" : h.status ? "✓ Detected" : "✗ Permission denied"}
                  </span>
                </div>
              ))}
            </div>
            {micOk === null && (
              <button onClick={testHardware} style={{ width: "100%", background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", color: "#A5B4FC", fontWeight: 600, padding: "11px", borderRadius: 8, fontSize: 14, marginBottom: 12 }}>
                🎙 Test Camera & Microphone
              </button>
            )}
            <div style={{ display: "flex", gap: 10 }}>
              <button onClick={() => setStep(3)} style={{ flex: 1, background: "#6366F1", color: "#fff", fontWeight: 600, padding: "11px", borderRadius: 8, fontSize: 14 }}>
                Next →
              </button>
              <button onClick={() => setStep(3)} style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", color: "#64748B", padding: "11px 18px", borderRadius: 8, fontSize: 14 }}>
                Skip
              </button>
            </div>
          </>
        )}

        {/* ── Step 3: Goals ────────────────────────────────────────── */}
        {step === 3 && (
          <>
            <h2 style={{ color: "#fff", fontSize: 20, fontWeight: 700, marginBottom: 8, textAlign: "center" }}>Set Your Goals</h2>
            <p style={{ color: "#94A3B8", fontSize: 14, textAlign: "center", marginBottom: 28 }}>
              Tell us your targets so we can personalise your practice.
            </p>
            <div style={{ display: "flex", flexDirection: "column", gap: 16, marginBottom: 28 }}>
              <div>
                <label style={{ fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" }}>Target Companies</label>
                <input value={companies} onChange={e => setCompanies(e.target.value)} placeholder="e.g. Google, Amazon, Microsoft" style={inputStyle} />
              </div>
              <div>
                <label style={{ fontSize: 13, color: "#94A3B8", marginBottom: 6, display: "block" }}>Preferred Role</label>
                <input value={role} onChange={e => setRole(e.target.value)} placeholder="e.g. Software Engineer, ML Engineer" style={inputStyle} />
              </div>
            </div>
            <div style={{ display: "flex", gap: 10 }}>
              <button onClick={() => setStep(4)} style={{ flex: 1, background: "#6366F1", color: "#fff", fontWeight: 600, padding: "11px", borderRadius: 8, fontSize: 14 }}>
                Next →
              </button>
              <button onClick={() => setStep(4)} style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", color: "#64748B", padding: "11px 18px", borderRadius: 8, fontSize: 14 }}>
                Skip
              </button>
            </div>
          </>
        )}

        {/* ── Step 4: Weak Topics ──────────────────────────────────── */}
        {step === 4 && (
          <>
            <h2 style={{ color: "#fff", fontSize: 20, fontWeight: 700, marginBottom: 8, textAlign: "center" }}>Select Weak Topics</h2>
            <p style={{ color: "#94A3B8", fontSize: 14, textAlign: "center", marginBottom: 24 }}>
              We'll prioritise these in your practice sessions.
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 28 }}>
              {SUBJECTS.map(t => {
                const on = weakTopics.includes(t);
                return (
                  <div key={t} onClick={() => toggleTopic(t)} style={{ display: "flex", alignItems: "center", gap: 10, background: on ? "rgba(99,102,241,0.12)" : "rgba(255,255,255,0.03)", border: `1px solid ${on ? "rgba(99,102,241,0.4)" : "rgba(255,255,255,0.07)"}`, borderRadius: 10, padding: "12px 14px", cursor: "pointer", transition: "all 0.15s" }}>
                    <div style={{ width: 16, height: 16, borderRadius: 4, background: on ? "#6366F1" : "transparent", border: `2px solid ${on ? "#6366F1" : "#334155"}`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                      {on && <div style={{ width: 8, height: 8, background: "#fff", borderRadius: 2 }} />}
                    </div>
                    <span style={{ color: on ? "#A5B4FC" : "#94A3B8", fontSize: 13, fontWeight: on ? 600 : 400 }}>{t}</span>
                  </div>
                );
              })}
            </div>
            <button onClick={finish} style={{ width: "100%", background: "#6366F1", color: "#fff", fontWeight: 700, padding: "13px", borderRadius: 8, fontSize: 15 }}>
              Start Your First Interview 🚀
            </button>
            <button onClick={finish} style={{ width: "100%", marginTop: 10, background: "transparent", color: "#64748B", fontSize: 13, padding: "8px" }}>
              Skip Setup
            </button>
          </>
        )}
      </div>

      {/* Back button */}
      {step > 1 && (
        <button onClick={() => setStep(s => s - 1)} style={{ marginTop: 20, background: "transparent", color: "#64748B", fontSize: 13 }}>
          ← Back
        </button>
      )}
    </div>
  );
}

// ─── App Root ──────────────────────────────────────────────────────────────────
// ─── Coding Interview Page ─────────────────────────────────────────────────────
const SAMPLE_PROBLEM = {
  title: "Two Sum",
  difficulty: "Easy",
  difficultyColor: "#22C55E",
  description: `Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.`,
  examples: [
    { input: "nums = [2,7,11,15], target = 9", output: "[0,1]", explanation: "nums[0] + nums[1] = 2 + 7 = 9" },
    { input: "nums = [3,2,4], target = 6",     output: "[1,2]", explanation: "nums[1] + nums[2] = 2 + 4 = 6" },
  ],
  constraints: ["2 ≤ nums.length ≤ 10⁴", "-10⁹ ≤ nums[i] ≤ 10⁹", "Only one valid answer exists."],
};

const STARTER_CODE = {
  Python: `def twoSum(nums, target):\n    # Write your solution here\n    pass\n`,
  "C++":  `#include <vector>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    // Write your solution here\n    return {};\n}\n`,
  Java:   `class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n`,
};

const LANGUAGE_MAP = { Python: "python", "C++": "cpp", Java: "java" };

function CodingInterviewPage({ token, user, onNav, onLogout, onResult }) {
  const [language, setLanguage]   = useState("Python");
  const [code, setCode]           = useState(STARTER_CODE["Python"]);
  const [timer, setTimer]   = useState(30 * 60);
  const [results, setResults] = useState(null);
  const [running, setRunning]           = useState(false);
  const [runError, setRunError]         = useState("");
  const [submitting, setSubmitting]     = useState(false);
  const [submitPreview, setSubmitPreview] = useState(null);

  // countdown timer
  useEffect(() => {
    const id = setInterval(() => setTimer(t => (t > 0 ? t - 1 : 0)), 1000);
    return () => clearInterval(id);
  }, []);

  function formatTime(s) {
    const m = Math.floor(s / 60).toString().padStart(2, "0");
    const sec = (s % 60).toString().padStart(2, "0");
    return `${m}:${sec}`;
  }

  function handleLanguageChange(lang) {
    setLanguage(lang);
    setCode(STARTER_CODE[lang]);
    setResults(null);
    setRunError("");
  }

  async function runCode() {
    setRunning(true);
    setResults(null);
    setRunError("");
    try {
      const res = await fetch(`${API}/code/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: language.toLowerCase(), code, problem_id: 1 }),
      });
      const data = await res.json();
      if (!res.ok) {
        setRunError(data.detail || "Execution failed.");
      } else {
        setResults(data);
      }
    } catch (e) {
      setRunError("Could not reach server. Is the backend running?");
    } finally {
      setRunning(false);
    }
  }

  async function submitSolution() {
    // If no results yet, run tests first
    let currentResults = results;
    if (!currentResults) {
      setRunning(true);
      setRunError("");
      try {
        const res = await fetch(`${API}/code/run`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ language: language.toLowerCase(), code, problem_id: 1 }),
        });
        const data = await res.json();
        if (!res.ok) { setRunError(data.detail || "Run failed before submit."); setRunning(false); return; }
        setResults(data);
        currentResults = data;
      } catch (e) {
        setRunError("Could not reach server."); setRunning(false); return;
      } finally {
        setRunning(false);
      }
    }

    const passed = currentResults.passed_cases.filter(c => c.passed).length;
    const total  = currentResults.passed_cases.length;
    const score  = Math.round((passed / total) * 100);

    const preview = { passed, total, score, runtime: currentResults.runtime_ms };
    setSubmitPreview(preview);
    setSubmitting(true);

    // Brief 1.5s preview, then navigate to results
    setTimeout(() => {
      setSubmitting(false);
      onResult({
        problem: "Two Sum",
        language,
        runtime: currentResults.runtime_ms,
        passed,
        total,
        score,
        total_score: score,
        nlp_score: score,
        voice_score: 0,
        face_score: 0,
        feedback: `${passed}/${total} test cases passed in ${currentResults.runtime_ms}ms using ${language}.`,
        type: "coding",
      });
    }, 1500);
  }

  const card = { background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12 };
  const btn  = (bg, color = "#fff") => ({
    background: bg, color, border: "none", borderRadius: 8,
    padding: "10px 24px", fontWeight: 600, fontSize: 14, cursor: "pointer",
  });

  return (
    <SidebarLayout active="coding" user={user} onNav={onNav} onLogout={onLogout}>
      {/* ── Header ── */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: "#fff", margin: 0 }}>Coding Interview</h1>
          <p style={{ color: "#64748B", fontSize: 13, margin: "4px 0 0" }}>Solve the problem and submit your solution</p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ ...card, padding: "8px 18px", display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ fontSize: 16 }}>⏱</span>
            <span style={{ fontWeight: 700, fontSize: 18, color: timer < 300 ? "#EF4444" : "#F1F5F9", fontVariantNumeric: "tabular-nums" }}>
              {formatTime(timer)}
            </span>
          </div>
          <button onClick={() => onNav("dashboard")} style={{ ...btn("rgba(239,68,68,0.15)", "#EF4444"), border: "1px solid rgba(239,68,68,0.3)" }}>
            End Session
          </button>
        </div>
      </div>

      {/* ── Two Column Layout ── */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, height: "calc(100vh - 220px)", minHeight: 480 }}>

        {/* ── LEFT: Problem Panel ── */}
        <div style={{ ...card, padding: 24, overflowY: "auto", display: "flex", flexDirection: "column", gap: 20 }}>
          {/* Title + difficulty */}
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <h2 style={{ fontSize: 20, fontWeight: 700, color: "#fff", margin: 0 }}>{SAMPLE_PROBLEM.title}</h2>
            <span style={{ background: `${SAMPLE_PROBLEM.difficultyColor}18`, color: SAMPLE_PROBLEM.difficultyColor, fontSize: 12, fontWeight: 600, padding: "3px 10px", borderRadius: 99 }}>
              {SAMPLE_PROBLEM.difficulty}
            </span>
          </div>

          {/* Description */}
          <div>
            <p style={{ color: "#CBD5E1", fontSize: 14, lineHeight: 1.8, margin: 0, whiteSpace: "pre-line" }}>
              {SAMPLE_PROBLEM.description}
            </p>
          </div>

          {/* Examples */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <h3 style={{ color: "#94A3B8", fontSize: 12, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, margin: 0 }}>Examples</h3>
            {SAMPLE_PROBLEM.examples.map((ex, i) => (
              <div key={i} style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 8, padding: 14 }}>
                <div style={{ color: "#94A3B8", fontSize: 13, marginBottom: 4 }}>
                  <span style={{ color: "#6366F1", fontWeight: 600 }}>Input: </span>
                  <code style={{ fontFamily: "monospace", color: "#F1F5F9" }}>{ex.input}</code>
                </div>
                <div style={{ color: "#94A3B8", fontSize: 13, marginBottom: 4 }}>
                  <span style={{ color: "#22C55E", fontWeight: 600 }}>Output: </span>
                  <code style={{ fontFamily: "monospace", color: "#F1F5F9" }}>{ex.output}</code>
                </div>
                <div style={{ color: "#64748B", fontSize: 12 }}>
                  <span style={{ fontWeight: 500 }}>Explanation: </span>{ex.explanation}
                </div>
              </div>
            ))}
          </div>

          {/* Constraints */}
          <div>
            <h3 style={{ color: "#94A3B8", fontSize: 12, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, margin: "0 0 10px" }}>Constraints</h3>
            <ul style={{ paddingLeft: 18, margin: 0, display: "flex", flexDirection: "column", gap: 6 }}>
              {SAMPLE_PROBLEM.constraints.map((c, i) => (
                <li key={i} style={{ color: "#CBD5E1", fontSize: 13, fontFamily: "monospace" }}>{c}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* ── RIGHT: Editor Panel ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {/* Language selector */}
          <div style={{ ...card, padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span style={{ color: "#94A3B8", fontSize: 13, fontWeight: 500 }}>Language</span>
            <div style={{ display: "flex", gap: 8 }}>
              {["Python", "C++", "Java"].map(lang => (
                <button
                  key={lang}
                  onClick={() => handleLanguageChange(lang)}
                  style={{
                    padding: "5px 14px", borderRadius: 6, fontSize: 13, fontWeight: 600, cursor: "pointer",
                    background: language === lang ? "#6366F1" : "rgba(255,255,255,0.05)",
                    color: language === lang ? "#fff" : "#94A3B8",
                    border: language === lang ? "1px solid #6366F1" : "1px solid rgba(255,255,255,0.07)",
                  }}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>

          {/* Monaco Editor */}
          <div style={{ ...card, flex: 1, overflow: "hidden", display: "flex", flexDirection: "column" }}>
            <div style={{ padding: "8px 16px", borderBottom: "1px solid rgba(255,255,255,0.06)", display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#EF4444", display: "inline-block" }} />
              <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#F59E0B", display: "inline-block" }} />
              <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#22C55E", display: "inline-block" }} />
              <span style={{ color: "#475569", fontSize: 12, marginLeft: 8 }}>
                solution.{LANGUAGE_MAP[language] === "python" ? "py" : LANGUAGE_MAP[language] === "cpp" ? "cpp" : "java"}
              </span>
            </div>
            <div style={{ flex: 1 }}>
              <Editor
                height="100%"
                language={LANGUAGE_MAP[language]}
                theme="vs-dark"
                value={code}
                onChange={value => setCode(value || "")}
                options={{
                  fontSize: 14,
                  fontFamily: "'Fira Code', 'Consolas', monospace",
                  minimap: { enabled: false },
                  automaticLayout: true,
                  scrollBeyondLastLine: false,
                  lineNumbers: "on",
                  tabSize: 4,
                  wordWrap: "on",
                  padding: { top: 16 },
                }}
              />
            </div>
          </div>

          {/* Results Panel */}
          {runError && (
            <div style={{ ...card, padding: 14, border: "1px solid rgba(239,68,68,0.3)", background: "rgba(239,68,68,0.07)" }}>
              <span style={{ color: "#EF4444", fontSize: 13 }}>⚠ {runError}</span>
            </div>
          )}
          {results && (
            <div style={{ ...card, padding: 16 }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
                <span style={{ color: "#94A3B8", fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1 }}>Test Results</span>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 12, color: results.passed === results.total ? "#22C55E" : "#F59E0B", fontWeight: 600 }}>
                    {results.passed}/{results.total} Passed
                  </span>
                  <span style={{ fontSize: 12, color: "#475569" }}>Runtime: {results.runtime_ms} ms</span>
                </div>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                {results.passed_cases.map((tc, i) => (
                  <div key={i} style={{
                    display: "grid", gridTemplateColumns: "1fr 1fr 1fr auto",
                    gap: 8, padding: "8px 12px", borderRadius: 6, fontSize: 12,
                    background: tc.passed ? "rgba(34,197,94,0.07)" : "rgba(239,68,68,0.07)",
                    border: `1px solid ${tc.passed ? "rgba(34,197,94,0.2)" : "rgba(239,68,68,0.2)"}`,
                  }}>
                    <div>
                      <div style={{ color: "#475569", fontSize: 10, marginBottom: 2 }}>INPUT</div>
                      <code style={{ color: "#CBD5E1", fontFamily: "monospace" }}>{tc.input}</code>
                    </div>
                    <div>
                      <div style={{ color: "#475569", fontSize: 10, marginBottom: 2 }}>EXPECTED</div>
                      <code style={{ color: "#22C55E", fontFamily: "monospace" }}>{tc.expected}</code>
                    </div>
                    <div>
                      <div style={{ color: "#475569", fontSize: 10, marginBottom: 2 }}>OUTPUT</div>
                      <code style={{ color: tc.passed ? "#22C55E" : "#EF4444", fontFamily: "monospace" }}>{tc.actual}</code>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", fontSize: 16 }}>
                      {tc.passed ? "✓" : "✗"}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Submit Score Preview ── */}
      {submitPreview && submitting && (
        <div style={{ ...card, padding: "14px 20px", marginTop: 12, display: "flex", alignItems: "center", justifyContent: "space-between", border: "1px solid rgba(99,102,241,0.4)", background: "rgba(99,102,241,0.08)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 24 }}>{submitPreview.score === 100 ? "🎉" : submitPreview.score >= 60 ? "👍" : "💪"}</span>
            <div>
              <div style={{ color: "#F1F5F9", fontWeight: 700, fontSize: 16 }}>
                Score: <span style={{ color: submitPreview.score >= 80 ? "#22C55E" : submitPreview.score >= 50 ? "#F59E0B" : "#EF4444" }}>{submitPreview.score}%</span>
              </div>
              <div style={{ color: "#94A3B8", fontSize: 13 }}>{submitPreview.passed}/{submitPreview.total} test cases passed · {submitPreview.runtime}ms</div>
            </div>
          </div>
          <span style={{ color: "#6366F1", fontSize: 13, fontWeight: 500 }}>Loading results...</span>
        </div>
      )}

      {/* ── Bottom Action Bar ── */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 16, ...card, padding: "14px 20px" }}>
        <span style={{ color: "#64748B", fontSize: 13 }}>
          💡 Tip: Think about time complexity before coding
        </span>
        <div style={{ display: "flex", gap: 10 }}>
          <button
            onClick={runCode}
            disabled={running}
            style={{ ...btn("rgba(255,255,255,0.06)", "#CBD5E1"), border: "1px solid rgba(255,255,255,0.1)", opacity: running ? 0.6 : 1 }}
          >
            {running ? "Running..." : "▶ Run Code"}
          </button>
          <button
            onClick={() => { console.log("Skip clicked"); onNav("dashboard"); }}
            style={{ ...btn("transparent", "#94A3B8") }}
          >
            Skip
          </button>
          <button
            onClick={submitSolution}
            disabled={submitting || running}
            style={{ ...btn("#6366F1"), opacity: submitting ? 0.7 : 1 }}
          >
            {submitting ? "Submitting..." : "✓ Submit"}
          </button>
        </div>
      </div>
    </SidebarLayout>
  );
}

// ─── Resume Analyser Page ────────────────────────────────────────────────────
function ResumeAnalyserPage({ token, user, onNav, onLogout }) {
  const [dragging, setDragging]   = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult]       = useState(null);
  const [error, setError]         = useState("");
  const fileInputRef              = useRef(null);

  const card = { background: "#0F1629", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12 };

  async function uploadFile(file) {
    if (!file || !file.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are supported."); return;
    }
    setError(""); setUploading(true); setResult(null);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const r = await fetch(`${API}/resume/analyse`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: fd,
      });
      const d = await r.json();
      if (!r.ok) { setError(d.detail || "Analysis failed."); }
      else { setResult(d); }
    } catch { setError("Could not reach server. Is the backend running?"); }
    setUploading(false);
  }

  function onDrop(e) {
    e.preventDefault(); setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) uploadFile(file);
  }

  const atsColor = result
    ? result.ats_score >= 75 ? "#22C55E" : result.ats_score >= 50 ? "#F59E0B" : "#EF4444"
    : "#6366F1";

  return (
    <SidebarLayout active="resume" user={user} onNav={onNav} onLogout={onLogout}>
      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ fontSize: 22, fontWeight: 700, color: "#fff", margin: 0 }}>Resume Analyser</h1>
        <p style={{ color: "#64748B", fontSize: 13, margin: "4px 0 0" }}>Upload your resume — get ATS score, skill tags, and AI-generated interview questions</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: result ? "1fr 1.6fr" : "1fr", gap: 16 }}>
        {/* Upload zone */}
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div
            onDragOver={e => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
            style={{
              ...card, padding: 40, textAlign: "center", cursor: "pointer",
              border: `2px dashed ${dragging ? "#6366F1" : "rgba(255,255,255,0.12)"}`,
              background: dragging ? "rgba(99,102,241,0.06)" : "#0F1629",
              transition: "all 0.2s",
            }}
          >
            <input ref={fileInputRef} type="file" accept=".pdf" style={{ display: "none" }} onChange={e => uploadFile(e.target.files[0])} />
            <div style={{ fontSize: 40, marginBottom: 12 }}>📄</div>
            {uploading ? (
              <>
                <span className="spin" style={{ fontSize: 20, color: "#6366F1" }}>⟳</span>
                <p style={{ color: "#6366F1", marginTop: 10, fontSize: 14, fontWeight: 600 }}>Analysing with AI...</p>
                <p style={{ color: "#475569", fontSize: 12 }}>This may take 20–60 seconds</p>
              </>
            ) : (
              <>
                <p style={{ color: "#F1F5F9", fontWeight: 600, fontSize: 15, marginBottom: 6 }}>Drop your resume here</p>
                <p style={{ color: "#64748B", fontSize: 13 }}>or click to upload · PDF only · max 5 MB</p>
              </>
            )}
          </div>
          {error && (
            <div style={{ ...card, padding: 12, border: "1px solid rgba(239,68,68,0.3)", background: "rgba(239,68,68,0.07)" }}>
              <span style={{ color: "#EF4444", fontSize: 13 }}>⚠ {error}</span>
            </div>
          )}
          {/* ATS score ring */}
          {result && (
            <div style={{ ...card, padding: 24, textAlign: "center" }}>
              <div style={{ fontSize: 11, color: "#64748B", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>ATS Compatibility</div>
              <div style={{ fontSize: 56, fontWeight: 800, color: atsColor, lineHeight: 1 }}>{result.ats_score}</div>
              <div style={{ fontSize: 12, color: "#475569", marginTop: 4 }}>/ 100</div>
              <div style={{ marginTop: 12, fontSize: 13, color: atsColor, fontWeight: 600 }}>
                {result.ats_score >= 75 ? "Strong resume ✓" : result.ats_score >= 50 ? "Needs improvement" : "Major gaps found"}
              </div>
            </div>
          )}
        </div>

        {/* Results panel */}
        {result && (
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }} className="fade-in">
            {/* Skills */}
            <div style={{ ...card, padding: 20 }}>
              <div style={{ fontSize: 11, color: "#94A3B8", fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>Detected Skills</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {result.skills.length > 0 ? result.skills.map((s, i) => (
                  <span key={i} style={{ background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", color: "#A5B4FC", fontSize: 12, fontWeight: 500, padding: "4px 12px", borderRadius: 99 }}>
                    {s}
                  </span>
                )) : <span style={{ color: "#475569", fontSize: 13 }}>No skills detected</span>}
              </div>
            </div>

            {/* Suggestions */}
            <div style={{ ...card, padding: 20 }}>
              <div style={{ fontSize: 11, color: "#94A3B8", fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>💡 Improvement Suggestions</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {result.suggestions.map((s, i) => (
                  <div key={i} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                    <span style={{ color: "#F59E0B", flexShrink: 0, marginTop: 1 }}>▸</span>
                    <span style={{ color: "#CBD5E1", fontSize: 13, lineHeight: 1.5 }}>{s}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Questions */}
            <div style={{ ...card, padding: 20 }}>
              <div style={{ fontSize: 11, color: "#94A3B8", fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>🤖 AI-Generated Interview Questions</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {result.questions.map((q, i) => (
                  <div key={i} style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 8, padding: "12px 14px", display: "flex", gap: 12, alignItems: "flex-start" }}>
                    <span style={{ color: "#6366F1", fontWeight: 700, fontSize: 13, flexShrink: 0 }}>Q{i + 1}</span>
                    <span style={{ color: "#E2E8F0", fontSize: 13, lineHeight: 1.6 }}>{q}</span>
                  </div>
                ))}
              </div>
              <button
                onClick={() => onNav("interview")}
                style={{ marginTop: 14, width: "100%", background: "#6366F1", color: "#fff", fontWeight: 700, fontSize: 14, padding: "12px", borderRadius: 8, border: "none", cursor: "pointer" }}
              >
                Start Interview Now →
              </button>
            </div>
          </div>
        )}
      </div>
    </SidebarLayout>
  );
}

export default function App() {
  const [page, setPage] = useState("landing");
  const [token, setToken] = useState(() => localStorage.getItem("token") || "");
  const [user, setUser] = useState(() => { try { return JSON.parse(localStorage.getItem("user")) || null; } catch { return null; } });
  const [activeSubject, setActiveSubject] = useState(null);
  const [sessionData, setSessionData] = useState(null);
  const [lastResult, setLastResult] = useState(null);

  useEffect(() => {
    if (token && user) setPage("dashboard");
  }, []);

  function handleLogin(t, u) {
    setToken(t); setUser(u);
    if (localStorage.getItem("onboarding_complete")) {
      setPage("dashboard");
    } else {
      setPage("onboarding");
    }
  }

  function handleLogout() {
    localStorage.removeItem("token"); localStorage.removeItem("user");
    setToken(""); setUser(null); setPage("landing");
  }

  function handleNav(dest) {
    if (dest === "dashboard") setPage("dashboard");
    else if (dest === "analytics") setPage("analytics");
    else if (dest === "interview") setPage(activeSubject ? "subject" : "dashboard");
    else if (dest === "profile") setPage("profile");
    else if (dest === "settings") setPage("settings");
    else if (dest === "coding")   setPage("coding");
    else if (dest === "resume")   setPage("resume");
  }

  function handleUpdateUser(updatedUser) {
    const merged = { ...user, ...updatedUser };
    setUser(merged);
    localStorage.setItem("user", JSON.stringify(merged));
  }

  const sidebarProps = { user, onNav: handleNav, onLogout: handleLogout };

  return (
    <>
      <style>{globalCss}</style>
      {page === "landing" && <LandingPage onLogin={() => setPage("login")} onGetStarted={() => setPage("login")} />}
      {page === "login" && <LoginPage onLogin={handleLogin} />}
      {page === "onboarding" && <OnboardingPage user={user} onFinish={() => { localStorage.setItem("onboarding_complete", "true"); setPage("dashboard"); }} />}
      {page === "dashboard" && <DashboardPage token={token} {...sidebarProps} onSelectSubject={s => { setActiveSubject(s); setPage("subject"); }} onViewAnalytics={() => setPage("analytics")} />}
      {page === "subject" && activeSubject && <SubjectPage token={token} subject={activeSubject} onBack={() => setPage("dashboard")} onStart={sd => { setSessionData(sd); setPage("interview"); }} {...sidebarProps} />}
      {page === "interview" && sessionData && <InterviewRoomPage token={token} user={user} sessionData={sessionData} onResult={r => { setLastResult(r); setPage("result"); }} onBack={() => setPage("dashboard")} />}
      {page === "result" && <ResultsPage token={token} user={user} lastResult={lastResult} onBack={() => setPage("dashboard")} onRetake={() => setPage(activeSubject ? "subject" : "dashboard")} />}
      {page === "analytics" && <AnalyticsPage token={token} {...sidebarProps} />}
      {page === "profile" && <ProfilePage token={token} {...sidebarProps} onUpdateUser={handleUpdateUser} />}
      {page === "settings" && <SettingsPage {...sidebarProps} />}
      {page === "coding"   && <CodingInterviewPage token={token} {...sidebarProps} onResult={r => { setLastResult(r); setPage("result"); }} />}
      {page === "resume"   && <ResumeAnalyserPage token={token} {...sidebarProps} />}
    </>
  );
}
