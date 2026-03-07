from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.interview_routes import router as interview_router
from routes.answer_routes import router as answer_router
from routes.analytics_routes import router as analytics_router

from database import engine, Base

# Import all models so SQLAlchemy creates all tables
import models.user
import models.subject
import models.topic
import models.subtopic
import models.question
import models.interview_session
import models.answer
import models.score
import models.conversation_memory
import models.analytics

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(interview_router)
app.include_router(answer_router)
app.include_router(analytics_router)

@app.get("/")
def root():
    return {"message": "Interview Simulator API is running"}