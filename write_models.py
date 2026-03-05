files = {
    'models/question.py': """from sqlalchemy import Column, Integer, String, Text
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    type = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    ideal_answer = Column(Text, nullable=False)
""",
    'models/answer.py': """from sqlalchemy import Column, Integer, Float, Text, ForeignKey
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
""",
    'models/score.py': """from sqlalchemy import Column, Integer, Float, ForeignKey
from database import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    nlp_score = Column(Float, nullable=True)
    voice_score = Column(Float, nullable=True)
    face_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)
""",
    'models/analytics.py': """from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import Base

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    avg_technical_score = Column(Float, nullable=True)
    avg_hr_score = Column(Float, nullable=True)
    weakest_topic = Column(String, nullable=True)
    strongest_topic = Column(String, nullable=True)
"""
}

for path, content in files.items():
    with open(path, 'w') as f:
        f.write(content)
    print(f'Written: {path}')
