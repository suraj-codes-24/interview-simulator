from sqlalchemy import Column, Integer, String, Text
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id               = Column(Integer, primary_key=True, index=True)
    topic            = Column(String, index=True)
    subtopic         = Column(String, default="general")
    difficulty       = Column(String, index=True)   # beginner | intermediate | advanced | expert
    type             = Column(String)                # technical | hr
    question_text    = Column(Text)
    ideal_answer     = Column(Text)
    tags             = Column(String, default="")
    companies        = Column(String, default="")
    time_complexity  = Column(String, default="N/A")
    space_complexity = Column(String, default="N/A")
