from sqlalchemy import Column, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=False)
    nlp_score = Column(Float, nullable=True)
    voice_score = Column(Float, nullable=True)
    face_score = Column(Float, nullable=True)
    total_score = Column(Float, nullable=True)

    session = relationship("InterviewSession", backref="answers")
    question = relationship("Question", backref="answers")
