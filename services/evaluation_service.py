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
    user_id: int,
    voice_score: float = 0.0,
    face_score: float = 0.0
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
        nlp_score = result["hr_score"]
        # HR Score = 40% LLM + 30% Voice + 20% Face + 10% NLP (here nlp is simple semantic check)
        # For our system, the LLM result is already behavioral-focused
        total_score = (nlp_score * 0.5) + (voice_score * 0.3) + (face_score * 0.2)
        response = {
            "answer_id":      None,
            "session_id":     session_id,
            "question_id":    question_id,
            "user_answer":    user_answer,
            "semantic_score": result["clarity"],
            "keyword_score":  result["structure"],
            "structure_score":result["communication"],
            "nlp_score":      nlp_score,
            "voice_score":    voice_score,
            "face_score":     face_score,
            "total_score":    round(total_score, 1),
            "feedback":       result["feedback"],
            "engine":         "hr"
        }
    else:
        result = evaluate_answer(user_answer, question.ideal_answer, question.question_text)
        nlp_score = result["nlp_score"]
        # Technical: 70% NLP + 20% Voice + 10% Face
        total_score = (nlp_score * 0.7) + (voice_score * 0.2) + (face_score * 0.1)
        response = {
            "answer_id":      None,
            "session_id":     session_id,
            "question_id":    question_id,
            "user_answer":    user_answer,
            "semantic_score": result["semantic_score"],
            "keyword_score":  result["keyword_score"],
            "structure_score":result["structure_score"],
            "nlp_score":      nlp_score,
            "voice_score":    voice_score,
            "face_score":     face_score,
            "total_score":    round(total_score, 1),
            "feedback":       result["feedback"],
            "engine":         "nlp"
        }

    # --- Save answer to DB ---
    answer = Answer(
        session_id=session_id,
        question_id=question_id,
        user_answer=user_answer,
        nlp_score=nlp_score,
        voice_score=voice_score,
        face_score=face_score,
        total_score=total_score
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
        score=total_score,  # save the aggregated score for tracking
        topic=question.topic.name if question.topic else "",
        subtopic=question.subtopic.name if question.subtopic else "",
        difficulty=question.difficulty,
    )

    return response