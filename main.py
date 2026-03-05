from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.interview_routes import router as interview_router
from routes.answer_routes import router as answer_router
from routes.analytics_routes import router as analytics_router

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