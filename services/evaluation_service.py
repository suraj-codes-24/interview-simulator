from sqlalchemy.orm import Session

from models.answer import Answer
from models.question import Question
from models.interview_session import InterviewSession
from ai_engine.nlp_engine import evaluate_answer
from ai_engine.hr_engine import evaluate_hr_answer
from services.memory_service import save_memory


def submit_and_score_answer(
    db: Session,
    session_id: int,
    question_id: int,
    user_answer: str,
    user_id: int
) -> dict:

    # --- Validate session ---
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id
    ).first()
    if not session:
        return {"error": "Session not found or does not belong to you."}

    # --- Validate question ---
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return {"error": "Question not found."}

    # --- Route to correct engine ---
    if question.type == "hr":
        result = evaluate_hr_answer(question.question_text, user_answer)
        final_score = result["hr_score"]
        response = {
            "answer_id":      None,
            "session_id":     session_id,
            "question_id":    question_id,
            "user_answer":    user_answer,
            "semantic_score": result["clarity"],
            "keyword_score":  result["structure"],
            "structure_score":result["communication"],
            "nlp_score":      final_score,
            "feedback":       result["feedback"],
            "engine":         "hr"
        }
    else:
        result = evaluate_answer(user_answer, question.ideal_answer)
        final_score = result["nlp_score"]
        response = {
            "answer_id":      None,
            "session_id":     session_id,
            "question_id":    question_id,
            "user_answer":    user_answer,
            "semantic_score": result["semantic_score"],
            "keyword_score":  result["keyword_score"],
            "structure_score":result["structure_score"],
            "nlp_score":      final_score,
            "feedback":       result["feedback"],
            "engine":         "nlp"
        }

    # --- Save answer to DB ---
    answer = Answer(
        session_id=session_id,
        question_id=question_id,
        user_answer=user_answer,
        nlp_score=final_score,
        voice_score=0.0,
        face_score=0.0,
        total_score=final_score
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)

    response["answer_id"] = answer.id

    # --- Save to conversation memory ---
    save_memory(
        db=db,
        session_id=session_id,
        question_id=question_id,
        question_text=question.question_text,
        user_answer=user_answer,
        score=final_score,
        topic=question.topic.name if question.topic else "",
        subtopic=question.subtopic.name if question.subtopic else "",
        difficulty=question.difficulty,
    )

    return response