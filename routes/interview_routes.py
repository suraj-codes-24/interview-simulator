from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from core.dependencies import get_current_user
from database import get_db
from models.user import User
from schemas.interview_schema import (
    SubjectResponse,
    StartInterviewRequest,
    StartInterviewResponse,
    QuestionResponse,
    QuestionListItem,
)
from services.interview_service import (
    get_subjects,
    get_topics,
    get_subtopics,
    get_questions_list,
    create_session,
    get_random_question,
    seed_questions,
)

router = APIRouter(prefix="/interview", tags=["Interview"])


# ── Hierarchy endpoints ──────────────────────────────────────────────────────

@router.get("/subjects", response_model=List[SubjectResponse])
def list_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all subjects with topic and question counts."""
    return get_subjects(db)


@router.get("/topics")
def list_topics(
    subject_id: int = Query(..., description="Subject ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all topics for a subject."""
    return get_topics(db, subject_id)


@router.get("/subtopics")
def list_subtopics(
    topic_id: int = Query(..., description="Topic ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all subtopics for a topic."""
    return get_subtopics(db, topic_id)


@router.get("/questions")
def list_questions(
    subject_id: Optional[int] = Query(None),
    topic_id: Optional[int] = Query(None),
    subtopic_id: Optional[int] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get filtered question list."""
    return get_questions_list(db, subject_id, topic_id, subtopic_id, difficulty)


# ── Interview flow ───────────────────────────────────────────────────────────

@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    body: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start a new interview session."""
    from models.subject import Subject

    subject = db.query(Subject).filter(Subject.id == body.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    session = create_session(
        db=db,
        user_id=current_user.id,
        interview_type=body.interview_type,
        subject_id=body.subject_id,
        difficulty=body.difficulty,
        topic_id=body.topic_id,
        subtopic_id=body.subtopic_id,
    )

    topic_name = None
    if session.topic_id:
        from models.topic import Topic
        topic = db.query(Topic).filter(Topic.id == session.topic_id).first()
        topic_name = topic.name if topic else None

    return StartInterviewResponse(
        session_id=session.id,
        interview_type=session.interview_type,
        subject_name=subject.name,
        topic_name=topic_name,
        difficulty=session.difficulty,
        start_time=session.start_time,
        message=f"Interview started! Subject: {subject.name} | Difficulty: {session.difficulty}",
    )


@router.get("/question", response_model=QuestionResponse)
def get_question(
    subject_id: int = Query(...),
    difficulty: str = Query(...),
    topic_id: Optional[int] = Query(None),
    subtopic_id: Optional[int] = Query(None),
    session_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a random question — adaptive difficulty, no repeats."""
    question = get_random_question(
        db=db,
        subject_id=subject_id,
        difficulty=difficulty,
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        session_id=session_id,
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="No more questions available for this session.",
        )

    return QuestionResponse(
        question_id=question.id,
        title=question.title,
        question_text=question.question_text,
        type=question.type,
        subject_name=question.subject.name,
        topic_name=question.topic.name,
        subtopic_name=question.subtopic.name,
        difficulty=question.difficulty,
    )


@router.post("/seed-questions")
def seed_db_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Seed the full Subject → Topic → Subtopic → Question hierarchy."""
    result = seed_questions(db)
    return result
