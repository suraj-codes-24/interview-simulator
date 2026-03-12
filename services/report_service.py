"""
Generate a PDF interview report using reportlab.
"""
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)

# ── Colour palette ────────────────────────────────────────────────────────────
INDIGO  = colors.HexColor("#6366F1")
GREEN   = colors.HexColor("#22C55E")
AMBER   = colors.HexColor("#F59E0B")
RED     = colors.HexColor("#EF4444")
DARK    = colors.HexColor("#0F172A")
GREY    = colors.HexColor("#64748B")
LIGHT   = colors.HexColor("#F1F5F9")


def _score_color(score: float):
    if score >= 70: return GREEN
    if score >= 45: return AMBER
    return RED


def generate_session_report(
    session: dict,
    answers: list[dict],
    coaching: dict,
    candidate_name: str = "Candidate",
) -> bytes:
    """
    Build a PDF report and return it as bytes.

    session  : dict with keys subject_name, difficulty, start_time, final_score
    answers  : list of answer dicts (question_text, user_answer, scores, feedback)
    coaching : dict with strengths, weaknesses, advice lists
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm,
    )

    styles  = getSampleStyleSheet()
    story   = []

    # ── Helper styles ─────────────────────────────────────────────────────────
    h1 = ParagraphStyle("h1", fontSize=22, fontName="Helvetica-Bold",
                        textColor=INDIGO,  spaceAfter=4)
    h2 = ParagraphStyle("h2", fontSize=14, fontName="Helvetica-Bold",
                        textColor=DARK,    spaceAfter=6, spaceBefore=14)
    h3 = ParagraphStyle("h3", fontSize=11, fontName="Helvetica-Bold",
                        textColor=INDIGO,  spaceAfter=4, spaceBefore=8)
    body = ParagraphStyle("body", fontSize=10, fontName="Helvetica",
                          textColor=DARK,    spaceAfter=4, leading=15)
    small = ParagraphStyle("small", fontSize=9, fontName="Helvetica",
                           textColor=GREY,   spaceAfter=2, leading=13)
    label = ParagraphStyle("label", fontSize=8, fontName="Helvetica-Bold",
                           textColor=GREY,   spaceAfter=2, leading=10)
    def divider():
        return HRFlowable(width="100%", thickness=0.5,
                          color=colors.HexColor("#E2E8F0"), spaceAfter=10)

    # ── Title block ───────────────────────────────────────────────────────────
    story.append(Paragraph("AI Interview Report", h1))
    story.append(divider())

    # ── Metadata table ────────────────────────────────────────────────────────
    date_str = ""
    if session.get("start_time"):
        try:
            dt = datetime.fromisoformat(str(session["start_time"]))
            date_str = dt.strftime("%d %b %Y, %H:%M")
        except Exception:
            date_str = str(session["start_time"])[:16]

    avg_score = session.get("final_score")
    if avg_score is None and answers:
        scores = [a.get("total_score") or 0 for a in answers]
        avg_score = round(sum(scores) / len(scores), 1)

    meta_data = [
        ["Candidate",    candidate_name,
         "Subject",      session.get("subject_name", session.get("subject_id", "—"))],
        ["Date",         date_str,
         "Difficulty",   str(session.get("difficulty", "—")).title()],
        ["Questions",    str(session.get("questions_answered", len(answers))),
         "Overall Score", f"{round(avg_score, 1) if avg_score else '—'} / 100"],
    ]
    meta_table = Table(meta_data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME",  (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",  (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE",  (0,0), (-1,-1), 9),
        ("TEXTCOLOR", (0,0), (0,-1), GREY),
        ("TEXTCOLOR", (2,0), (2,-1), GREY),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#E2E8F0")),
        ("PADDING",   (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 16))

    # ── Coaching summary ──────────────────────────────────────────────────────
    story.append(Paragraph("AI Coaching Summary", h2))
    story.append(divider())

    for section, color in [
        ("strengths",  GREEN),
        ("weaknesses", AMBER),
        ("advice",     INDIGO),
    ]:
        items = (coaching or {}).get(section, [])
        if not items:
            continue
        icon = {"strengths": "✓ Strengths", "weaknesses": "⚠ Weaknesses", "advice": "💡 Advice"}[section]
        story.append(Paragraph(icon, ParagraphStyle(
            f"sec_{section}", fontSize=10, fontName="Helvetica-Bold",
            textColor=color, spaceAfter=3, spaceBefore=8,
        )))
        for item in items:
            story.append(Paragraph(f"• {item}", body))

    story.append(Spacer(1, 16))

    # ── Q&A timeline ─────────────────────────────────────────────────────────
    story.append(Paragraph("Question & Answer Breakdown", h2))
    story.append(divider())

    for i, ans in enumerate(answers, 1):
        total  = ans.get("total_score")  or 0
        nlp    = ans.get("nlp_score")    or 0
        voice  = ans.get("voice_score")  or 0
        face   = ans.get("face_score")   or 0
        q_text = ans.get("question_text", "—")
        a_text = ans.get("user_answer",   "—")
        fb     = ans.get("feedback",      "")

        # Question header row
        header_data = [[
            Paragraph(f"Q{i}", ParagraphStyle("qnum", fontSize=10, fontName="Helvetica-Bold",
                                               textColor=INDIGO)),
            Paragraph(q_text, ParagraphStyle("qtxt", fontSize=10, fontName="Helvetica",
                                              textColor=DARK, leading=14)),
            Paragraph(f"Score: {round(total)}/100", ParagraphStyle(
                "qscore", fontSize=10, fontName="Helvetica-Bold",
                textColor=_score_color(total), alignment=2)),
        ]]
        hdr_table = Table(header_data, colWidths=[1*cm, 13*cm, 3*cm])
        hdr_table.setStyle(TableStyle([
            ("VALIGN",     (0,0), (-1,-1), "TOP"),
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ("BOX",        (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ("PADDING",    (0,0), (-1,-1), 6),
        ]))
        story.append(hdr_table)

        # Answer text
        story.append(Paragraph(
            f"<b>Answer:</b> {a_text[:600]}{'…' if len(a_text) > 600 else ''}",
            ParagraphStyle("ans", fontSize=9, fontName="Helvetica",
                           textColor=colors.HexColor("#374151"), leading=14,
                           leftIndent=8, spaceAfter=3, spaceBefore=3)
        ))

        # Scores mini-row
        scores_data = [[
            f"NLP: {round(nlp)}%",
            f"Voice: {round(voice)}%",
            f"Face: {round(face)}%",
        ]]
        sc_table = Table(scores_data, colWidths=[5.67*cm, 5.67*cm, 5.66*cm])
        sc_table.setStyle(TableStyle([
            ("FONTNAME",   (0,0), (-1,-1), "Helvetica"),
            ("FONTSIZE",   (0,0), (-1,-1), 8),
            ("TEXTCOLOR",  (0,0), (-1,-1), GREY),
            ("ALIGN",      (0,0), (-1,-1), "CENTER"),
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ("BOX",        (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
            ("PADDING",    (0,0), (-1,-1), 4),
        ]))
        story.append(sc_table)

        # Feedback
        if fb:
            story.append(Paragraph(
                f"<i>💡 {fb[:300]}</i>",
                ParagraphStyle("fb", fontSize=8, fontName="Helvetica-Oblique",
                               textColor=GREY, leftIndent=8, spaceAfter=3,
                               spaceBefore=2, leading=12)
            ))

        story.append(Spacer(1, 8))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 10))
    story.append(divider())
    story.append(Paragraph(
        "Generated by AI Interview Simulator · Keep practising!",
        ParagraphStyle("footer", fontSize=8, fontName="Helvetica",
                       textColor=GREY, alignment=1)
    ))

    doc.build(story)
    return buf.getvalue()
