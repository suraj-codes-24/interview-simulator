from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import Base

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    avg_technical_score = Column(Float, nullable=True)
    avg_hr_score = Column(Float, nullable=True)
    weakest_topic = Column(String, nullable=True)
    strongest_topic = Column(String, nullable=True)