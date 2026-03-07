from sqlalchemy import Column, Integer, Float, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class ConversationMemory(Base):
    __tablename__ = "conversation_memory"

    id            = Column(Integer, primary_key=True, index=True)
    session_id    = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_id   = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    user_answer   = Column(Text, nullable=False)
    score         = Column(Float, nullable=True)
    topic         = Column(String, nullable=True)
    subtopic      = Column(String, nullable=True)
    difficulty    = Column(String, nullable=True)
    timestamp     = Column(DateTime, default=datetime.utcnow)

    session  = relationship("InterviewSession", backref="memory")
    question = relationship("Question")