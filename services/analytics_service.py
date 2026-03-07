from sqlalchemy.orm import Session
from sqlalchemy import func

from models.answer import Answer
from models.interview_session import InterviewSession
from models.question import Question
from models.subject import Subject
from models.topic import Topic


def get_user_analytics(db: Session, user_id: int) -> dict:
    """
    Full performance summary for the user.
    Now tracks by subject and topic.
    """

    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == user_id
    ).all()

    if not sessions:
        return {
            "message": "No interview sessions found. Start an interview first!",
            "total_sessions": 0,
        }

    session_ids = [s.id for s in sessions]

    answers = db.query(Answer).filter(
        Answer.session_id.in_(session_ids)
    ).all()

    if not answers:
        return {
            "message": "No answers submitted yet.",
            "total_sessions": len(sessions),
            "total_answers": 0,
        }

    # ── Overall stats ────────────────────────────────────────────────────
    total_answers = len(answers)
    avg_nlp = round(sum(a.nlp_score for a in answers) / total_answers, 2)
    avg_total = round(sum(a.total_score for a in answers) / total_answers, 2)

    # ── Subject-level breakdown ──────────────────────────────────────────
    subject_scores = {}
    subject_counts = {}

    # ── Topic-level breakdown ────────────────────────────────────────────
    topic_scores = {}
    topic_counts = {}

    for answer in answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        if not question:
            continue

        # Subject level
        subject = db.query(Subject).filter(Subject.id == question.subject_id).first()
        if subject:
            sname = subject.name
            subject_scores[sname] = subject_scores.get(sname, 0.0) + answer.nlp_score
            subject_counts[sname] = subject_counts.get(sname, 0) + 1

        # Topic level
        topic = db.query(Topic).filter(Topic.id == question.topic_id).first()
        if topic:
            tname = topic.name
            topic_scores[tname] = topic_scores.get(tname, 0.0) + answer.nlp_score
            topic_counts[tname] = topic_counts.get(tname, 0) + 1

    subject_averages = {
        s: round(subject_scores[s] / subject_counts[s], 2)
        for s in subject_scores
    }
    topic_averages = {
        t: round(topic_scores[t] / topic_counts[t], 2)
        for t in topic_scores
    }

    strongest_topic = max(topic_averages, key=topic_averages.get) if topic_averages else "N/A"
    weakest_topic = min(topic_averages, key=topic_averages.get) if topic_averages else "N/A"

    if avg_nlp >= 75:
        performance = "Excellent 🔥"
    elif avg_nlp >= 55:
        performance = "Good 👍"
    elif avg_nlp >= 35:
        performance = "Average 📈 — Keep practicing!"
    else:
        performance = "Needs Improvement 💪 — Don't give up!"

    return {
        "total_sessions": len(sessions),
        "total_answers": total_answers,
        "avg_nlp_score": avg_nlp,
        "avg_total_score": avg_total,
        "strongest_topic": strongest_topic,
        "weakest_topic": weakest_topic,
        "subject_breakdown": subject_averages,
        "topic_breakdown": topic_averages,
        "performance": performance,
    }
