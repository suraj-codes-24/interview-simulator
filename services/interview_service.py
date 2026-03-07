from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional, List

from models.subject import Subject
from models.topic import Topic
from models.subtopic import Subtopic
from models.interview_session import InterviewSession
from models.question import Question


# ── Hierarchy queries ────────────────────────────────────────────────────────

def get_subjects(db: Session) -> list[dict]:
    """Return all subjects with topic and question counts."""
    subjects = db.query(Subject).all()
    result = []
    for s in subjects:
        topic_count = db.query(Topic).filter(Topic.subject_id == s.id).count()
        question_count = db.query(Question).filter(Question.subject_id == s.id).count()
        result.append({
            "id": s.id,
            "name": s.name,
            "type": s.type,
            "topic_count": topic_count,
            "question_count": question_count,
        })
    return result


def get_topics(db: Session, subject_id: int) -> list[dict]:
    """Return all topics for a subject with subtopic and question counts."""
    topics = db.query(Topic).filter(Topic.subject_id == subject_id).all()
    result = []
    for t in topics:
        subtopic_count = db.query(Subtopic).filter(Subtopic.topic_id == t.id).count()
        question_count = db.query(Question).filter(Question.topic_id == t.id).count()
        result.append({
            "id": t.id,
            "name": t.name,
            "subject_id": t.subject_id,
            "subtopic_count": subtopic_count,
            "question_count": question_count,
        })
    return result


def get_subtopics(db: Session, topic_id: int) -> list[dict]:
    """Return all subtopics for a topic with question counts."""
    subtopics = db.query(Subtopic).filter(Subtopic.topic_id == topic_id).all()
    result = []
    for st in subtopics:
        question_count = db.query(Question).filter(Question.subtopic_id == st.id).count()
        result.append({
            "id": st.id,
            "name": st.name,
            "topic_id": st.topic_id,
            "question_count": question_count,
        })
    return result


def get_questions_list(
    db: Session,
    subject_id: Optional[int] = None,
    topic_id: Optional[int] = None,
    subtopic_id: Optional[int] = None,
    difficulty: Optional[str] = None,
) -> list[dict]:
    """Return filtered question list."""
    query = db.query(Question)
    if subject_id:
        query = query.filter(Question.subject_id == subject_id)
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if subtopic_id:
        query = query.filter(Question.subtopic_id == subtopic_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    questions = query.all()
    return [
        {
            "question_id": q.id,
            "title": q.title,
            "difficulty": q.difficulty,
            "type": q.type,
            "companies": q.companies,
            "tags": q.tags,
        }
        for q in questions
    ]


# ── Interview session ────────────────────────────────────────────────────────

def create_session(
    db: Session,
    user_id: int,
    interview_type: str,
    subject_id: int,
    difficulty: str,
    topic_id: Optional[int] = None,
    subtopic_id: Optional[int] = None,
) -> InterviewSession:
    session = InterviewSession(
        user_id=user_id,
        interview_type=interview_type,
        subject_id=subject_id,
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        difficulty=difficulty,
        start_time=datetime.utcnow(),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_random_question(
    db: Session,
    subject_id: int,
    difficulty: str,
    topic_id: Optional[int] = None,
    subtopic_id: Optional[int] = None,
) -> Question | None:
    query = db.query(Question).filter(
        Question.subject_id == subject_id,
        Question.difficulty == difficulty,
    )
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if subtopic_id:
        query = query.filter(Question.subtopic_id == subtopic_id)
    return query.order_by(func.random()).first()


# ── Seeder (delegates to data/seed.py) ───────────────────────────────────────

def seed_questions(db: Session) -> dict:
    from data.seed import seed_all
    return seed_all(db)
