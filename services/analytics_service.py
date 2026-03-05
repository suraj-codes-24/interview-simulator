from sqlalchemy.orm import Session
from sqlalchemy import func

from models.answer import Answer
from models.interview_session import InterviewSession
from models.question import Question


def get_user_analytics(db: Session, user_id: int) -> dict:
    """
    Returns a full performance summary for the user.
    Covers: overall scores, topic breakdown, strongest/weakest topic.
    """

    # --- Get all sessions for this user ---
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == user_id
    ).all()

    if not sessions:
        return {
            "message": "No interview sessions found. Start an interview first!",
            "total_sessions": 0
        }

    session_ids = [s.id for s in sessions]

    # --- Get all answers across all sessions ---
    answers = db.query(Answer).filter(
        Answer.session_id.in_(session_ids)
    ).all()

    if not answers:
        return {
            "message": "No answers submitted yet.",
            "total_sessions": len(sessions),
            "total_answers": 0
        }

    # --- Overall stats ---
    total_answers = len(answers)
    avg_nlp_score = round(sum(a.nlp_score for a in answers) / total_answers, 2)
    avg_total_score = round(sum(a.total_score for a in answers) / total_answers, 2)

    # --- Topic-wise breakdown ---
    topic_scores = {}
    topic_counts = {}

    for answer in answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        if not question:
            continue

        topic = question.topic
        if topic not in topic_scores:
            topic_scores[topic] = 0.0
            topic_counts[topic] = 0

        topic_scores[topic] += answer.nlp_score
        topic_counts[topic] += 1

    # Calculate average per topic
    topic_averages = {}
    for topic in topic_scores:
        topic_averages[topic] = round(topic_scores[topic] / topic_counts[topic], 2)

    # --- Strongest and weakest topic ---
    strongest_topic = max(topic_averages, key=topic_averages.get) if topic_averages else "N/A"
    weakest_topic = min(topic_averages, key=topic_averages.get) if topic_averages else "N/A"

    # --- Performance label ---
    if avg_nlp_score >= 75:
        performance = "Excellent 🔥"
    elif avg_nlp_score >= 55:
        performance = "Good 👍"
    elif avg_nlp_score >= 35:
        performance = "Average 📈 — Keep practicing!"
    else:
        performance = "Needs Improvement 💪 — Don't give up!"

    return {
        "total_sessions": len(sessions),
        "total_answers": total_answers,
        "avg_nlp_score": avg_nlp_score,
        "avg_total_score": avg_total_score,
        "strongest_topic": strongest_topic,
        "weakest_topic": weakest_topic,
        "topic_breakdown": topic_averages,
        "performance": performance
    }
