from sqlalchemy.orm import Session

from models.answer import Answer
from models.interview_session import InterviewSession
from models.question import Question
from models.subject import Subject
from models.topic import Topic


def get_user_analytics(db: Session, user_id: int) -> dict:
    """Full performance summary for the user."""

    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == user_id
    ).order_by(InterviewSession.start_time.desc()).all()

    if not sessions:
        return {
            "total_sessions": 0,
            "total_answers": 0,
            "avg_nlp_score": 0,
            "avg_total_score": 0,
            "best_score": 0,
            "strongest_topic": "N/A",
            "weakest_topic": "N/A",
            "subject_breakdown": {},
            "topic_breakdown": {},
            "recent_sessions": [],
            "performance": "No data yet",
        }

    session_ids = [s.id for s in sessions]

    answers = db.query(Answer).filter(
        Answer.session_id.in_(session_ids)
    ).all()

    if not answers:
        return {
            "total_sessions": len(sessions),
            "total_answers": 0,
            "avg_nlp_score": 0,
            "avg_total_score": 0,
            "best_score": 0,
            "strongest_topic": "N/A",
            "weakest_topic": "N/A",
            "subject_breakdown": {},
            "topic_breakdown": {},
            "recent_sessions": [],
            "performance": "No data yet",
        }

    # ── Overall stats ─────────────────────────────────────────────────────
    total_answers = len(answers)
    nlp_scores    = [a.nlp_score or 0.0 for a in answers]
    total_scores  = [a.total_score or 0.0 for a in answers]
    avg_nlp       = round(sum(nlp_scores) / total_answers, 1)
    avg_total     = round(sum(total_scores) / total_answers, 1)
    best_score    = round(max(total_scores), 1)

    # ── Subject & topic breakdown (by total_score) ────────────────────────
    subject_scores = {}
    subject_counts = {}
    topic_scores   = {}
    topic_counts   = {}

    for answer in answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        if not question:
            continue

        score = answer.total_score or 0.0

        subject = db.query(Subject).filter(Subject.id == question.subject_id).first()
        if subject:
            sname = subject.name
            subject_scores[sname] = subject_scores.get(sname, 0.0) + score
            subject_counts[sname] = subject_counts.get(sname, 0) + 1

        topic = db.query(Topic).filter(Topic.id == question.topic_id).first()
        if topic:
            tname = topic.name
            topic_scores[tname] = topic_scores.get(tname, 0.0) + score
            topic_counts[tname] = topic_counts.get(tname, 0) + 1

    subject_averages = {
        s: round(subject_scores[s] / subject_counts[s], 1) for s in subject_scores
    }
    topic_averages = {
        t: round(topic_scores[t] / topic_counts[t], 1) for t in topic_scores
    }

    strongest_topic = max(topic_averages, key=topic_averages.get) if topic_averages else "N/A"
    weakest_topic   = min(topic_averages, key=topic_averages.get) if topic_averages else "N/A"

    # ── Performance label ─────────────────────────────────────────────────
    if avg_total >= 75:
        performance = "Excellent"
    elif avg_total >= 55:
        performance = "Good"
    elif avg_total >= 35:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    # ── Recent sessions (last 5) ──────────────────────────────────────────
    recent_sessions = []
    for session in sessions[:5]:
        sess_answers = [a for a in answers if a.session_id == session.id]
        if sess_answers:
            avg_s = round(sum(a.total_score or 0 for a in sess_answers) / len(sess_answers), 1)
        else:
            avg_s = None

        subject = db.query(Subject).filter(Subject.id == session.subject_id).first()
        recent_sessions.append({
            "session_id":     session.id,
            "date":           session.start_time.strftime("%b %d, %Y") if session.start_time else "—",
            "subject":        subject.name if subject else "—",
            "difficulty":     session.difficulty,
            "total_answered": session.total_answered or len(sess_answers),
            "avg_score":      avg_s,
            "status":         session.status or "completed",
        })

    return {
        "total_sessions":    len(sessions),
        "total_answers":     total_answers,
        "avg_nlp_score":     avg_nlp,
        "avg_total_score":   avg_total,
        "best_score":        best_score,
        "strongest_topic":   strongest_topic,
        "weakest_topic":     weakest_topic,
        "subject_breakdown": subject_averages,
        "topic_breakdown":   topic_averages,
        "recent_sessions":   recent_sessions,
        "performance":       performance,
    }
