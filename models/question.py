from sqlalchemy import Column, Integer, String, Text
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    type = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    ideal_answer = Column(Text, nullable=False)
