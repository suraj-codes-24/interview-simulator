from sqlalchemy import Column, Integer, Float, ForeignKey
from database import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    nlp_score = Column(Float, nullable=True)
    voice_score = Column(Float, nullable=True)
    face_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)
