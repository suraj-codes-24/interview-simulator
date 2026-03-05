from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database import get_db
from models.user import User
from schemas.interview_schema import (
    StartInterviewRequest,
    StartInterviewResponse,
    QuestionResponse,
)
from services.interview_service import create_session, get_random_question, seed_questions

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    body: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start a new interview session for the logged-in user."""

    # Validate inputs
    valid_types = ["technical", "hr"]
    valid_difficulties = ["easy", "medium", "hard"]

    if body.interview_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"interview_type must be one of {valid_types}")

    if body.difficulty not in valid_difficulties:
        raise HTTPException(status_code=400, detail=f"difficulty must be one of {valid_difficulties}")

    session = create_session(
        db=db,
        user_id=current_user.id,
        interview_type=body.interview_type,
        topic=body.topic,
        difficulty=body.difficulty,
    )

    return StartInterviewResponse(
        session_id=session.id,
        interview_type=session.interview_type,
        topic=session.topic,
        difficulty=session.difficulty,
        start_time=session.start_time,
        message=f"Interview session started! Topic: {session.topic} | Difficulty: {session.difficulty}",
    )


@router.get("/question", response_model=QuestionResponse)
def get_question(
    topic: str,
    difficulty: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a random question by topic and difficulty."""

    question = get_random_question(db=db, topic=topic, difficulty=difficulty)

    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"No question found for topic='{topic}' and difficulty='{difficulty}'. Try seeding the DB first."
        )

    return QuestionResponse(
        question_id=question.id,
        question_text=question.question_text,
        type=question.type,
        topic=question.topic,
        difficulty=question.difficulty,
    )


@router.post("/seed-questions")
def seed_db_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Seed 25 sample questions into the database (run once)."""
    result = seed_questions(db)
    return result


@router.get("/topics")
def get_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available topics and question counts."""
    from services.interview_service import get_topics_list
    return get_topics_list(db)
