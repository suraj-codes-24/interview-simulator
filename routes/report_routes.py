import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database import get_db
from models.user import User
from models.interview_session import InterviewSession
from models.answer import Answer
from models.question import Question
from services.session_feedback_service import generate_session_feedback
from services.report_service import generate_session_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/session/{session_id}")
def download_session_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate and return a PDF report for a completed interview session."""
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    # Build answers list joined with question text
    raw_answers = db.query(Answer).filter(Answer.session_id == session_id).all()
    if not raw_answers:
        raise HTTPException(status_code=404, detail="No answers found for this session.")

    answers = []
    for a in raw_answers:
        q = db.query(Question).filter(Question.id == a.question_id).first()
        answers.append({
            "question_text": q.question_text if q else "Unknown question",
            "user_answer":   (a.user_answer or "")[:500],
            "nlp_score":     a.nlp_score   or 0,
            "voice_score":   a.voice_score or 0,
            "face_score":    a.face_score  or 0,
            "total_score":   a.total_score or 0,
            "feedback":      a.feedback    or "",
        })

    # AI coaching summary
    coaching_payload = [
        {"question": a["question_text"], "answer": a["user_answer"], "score": a["total_score"]}
        for a in answers
    ]
    coaching = generate_session_feedback(coaching_payload)

    # Subject name for the report header
    subject_name = "—"
    if session.subject_id:
        from models.subject import Subject
        subj = db.query(Subject).filter(Subject.id == session.subject_id).first()
        if subj:
            subject_name = subj.name

    session_dict = {
        "subject_name":       subject_name,
        "difficulty":         session.difficulty,
        "start_time":         session.start_time,
        "final_score":        session.final_score,
        "questions_answered": session.questions_answered,
    }

    pdf_bytes = generate_session_report(
        session=session_dict,
        answers=answers,
        coaching=coaching,
        candidate_name=current_user.name or "Candidate",
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="interview_report_{session_id}.pdf"'
        },
    )
