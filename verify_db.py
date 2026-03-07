from database import SessionLocal
from models.subject import Subject
from models.topic import Topic
from models.subtopic import Subtopic
from models.question import Question

db = SessionLocal()
try:
    s_c = db.query(Subject).count()
    t_c = db.query(Topic).count()
    st_c = db.query(Subtopic).count()
    q_c = db.query(Question).count()
    
    print(f"Subjects: {s_c}")
    print(f"Topics: {t_c}")
    print(f"Subtopics: {st_c}")
    print(f"Questions: {q_c}")
finally:
    db.close()
