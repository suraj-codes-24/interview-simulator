from sqlalchemy.orm import Session

from models.answer import Answer
from models.question import Question
from models.interview_session import InterviewSession
from ai_engine.nlp_engine import evaluate_answer


def submit_and_score_answer(
    db: Session,
    session_id: int,
    question_id: int,
    user_answer: str,
    user_id: int
) -> dict:
    """
    Main evaluation flow:
    1. Validate session and question exist
    2. Run NLP scoring
    3. Save answer + scores to DB
    4. Return full result
    """

    # --- Validate session belongs to this user ---
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id
    ).first()

    if not session:
        return {"error": "Session not found or does not belong to you."}

    # --- Validate question exists ---
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        return {"error": "Question not found."}

    # --- Run NLP evaluation ---
    result = evaluate_answer(user_answer, question.ideal_answer)

    # --- Save answer to DB ---
    answer = Answer(
        session_id=session_id,
        question_id=question_id,
        user_answer=user_answer,
        nlp_score=result["nlp_score"],
        voice_score=0.0,   # Phase 2 — not built yet
        face_score=0.0,    # Phase 3 — not built yet
        total_score=result["nlp_score"]  # For now total = nlp score
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)

    return {
        "answer_id": answer.id,
        "session_id": session_id,
        "question_id": question_id,
        "user_answer": user_answer,
        "semantic_score": result["semantic_score"],
        "keyword_score": result["keyword_score"],
        "structure_score": result["structure_score"],
        "nlp_score": result["nlp_score"],
        "feedback": result["feedback"]
    }
