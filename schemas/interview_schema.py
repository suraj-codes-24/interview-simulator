from pydantic import BaseModel
from datetime import datetime


class StartInterviewRequest(BaseModel):
    interview_type: str
    topic: str
    difficulty: str


class StartInterviewResponse(BaseModel):
    session_id: int
    interview_type: str
    topic: str
    difficulty: str
    start_time: datetime
    message: str

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    type: str
    topic: str
    difficulty: str

    class Config:
        from_attributes = True