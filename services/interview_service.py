from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from models.interview_session import InterviewSession
from models.question import Question
from models.answer import Answer
from models.score import Score
from data.question_bank import QUESTION_BANK


def create_session(db: Session, user_id: int, interview_type: str, topic: str, difficulty: str) -> InterviewSession:
    session = InterviewSession(
        user_id=user_id,
        interview_type=interview_type,
        topic=topic,
        difficulty=difficulty,
        start_time=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_random_question(db: Session, topic: str, difficulty: str) -> Question | None:
    question = (
        db.query(Question)
        .filter(Question.topic == topic, Question.difficulty == difficulty)
        .order_by(func.random())
        .first()
    )
    return question


def get_topics_list(db: Session) -> dict:
    """Return all available topics and their question counts."""
    from sqlalchemy import func as sqlfunc
    results = (
        db.query(Question.topic, Question.difficulty, sqlfunc.count(Question.id))
        .group_by(Question.topic, Question.difficulty)
        .all()
    )
    topics = {}
    for topic, difficulty, count in results:
        if topic not in topics:
            topics[topic] = {}
        topics[topic][difficulty] = count
    return topics


def seed_questions(db: Session):
    """Seed the full question bank into DB. Clears old questions first."""
    existing = db.query(Question).count()
    if existing >= len(QUESTION_BANK):
        return {"message": f"Questions already seeded. Total: {existing}"}

    # Clear old questions to avoid duplicates
    from models.answer import Answer
    from models.score import Score
    db.query(Answer).delete()
    db.query(Score).delete()
    db.query(Question).delete()
    db.commit()

    count = 0
    for q in QUESTION_BANK:
        question = Question(
            topic=q["topic"],
            subtopic=q.get("subtopic", "general"),
            difficulty=q["difficulty"],
            type=q["type"],
            question_text=q["question_text"],
            ideal_answer=q["ideal_answer"],
            tags=q.get("tags", ""),
            companies=q.get("companies", ""),
            time_complexity=q.get("time_complexity", "N/A"),
            space_complexity=q.get("space_complexity", "N/A"),
        )
        db.add(question)
        count += 1

    db.commit()
    return {"message": f"Successfully seeded {count} questions across all topics."}
