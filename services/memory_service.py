from sqlalchemy.orm import Session
from models.conversation_memory import ConversationMemory


def save_memory(
    db: Session,
    session_id: int,
    question_id: int,
    question_text: str,
    user_answer: str,
    score: float,
    topic: str,
    subtopic: str,
    difficulty: str,
):
    entry = ConversationMemory(
        session_id=session_id,
        question_id=question_id,
        question_text=question_text,
        user_answer=user_answer,
        score=score,
        topic=topic,
        subtopic=subtopic,
        difficulty=difficulty,
    )
    db.add(entry)
    db.commit()
    return entry


def get_memory_window(db: Session, session_id: int, limit: int = 3):
    return (
        db.query(ConversationMemory)
        .filter(ConversationMemory.session_id == session_id)
        .order_by(ConversationMemory.timestamp.desc())
        .limit(limit)
        .all()
    )


def get_last_score(db: Session, session_id: int):
    last = (
        db.query(ConversationMemory)
        .filter(ConversationMemory.session_id == session_id)
        .order_by(ConversationMemory.timestamp.desc())
        .first()
    )
    return last.score if last else None


def get_used_question_ids(db: Session, session_id: int):
    rows = (
        db.query(ConversationMemory.question_id)
        .filter(ConversationMemory.session_id == session_id)
        .all()
    )
    return [r.question_id for r in rows]
