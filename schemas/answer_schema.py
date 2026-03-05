from pydantic import BaseModel


# --- Request: Submit an answer ---
class SubmitAnswerRequest(BaseModel):
    session_id: int
    question_id: int
    user_answer: str


# --- Response: Score breakdown ---
class SubmitAnswerResponse(BaseModel):
    answer_id: int
    session_id: int
    question_id: int
    user_answer: str
    semantic_score: float
    keyword_score: float
    structure_score: float
    nlp_score: float
    feedback: str

    class Config:
        from_attributes = True
