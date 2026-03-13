import os
import logging
import imageio_ffmpeg
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# ── Structured logging ───────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("interview_api")
from routes.auth_routes import router as auth_router
from routes.interview_routes import router as interview_router
from routes.answer_routes import router as answer_router
from routes.analytics_routes import router as analytics_router
from routes.voice_routes import router as voice_router
from routes.vision_routes import router as vision_router
from routes.code_routes import router as code_router
from routes.ai_routes import router as ai_router
from routes.resume_routes import router as resume_router
from routes.jd_routes import router as jd_router
from routes.report_routes import router as report_router

from database import engine, Base

# Import all models so SQLAlchemy creates all tables
import models.user
import models.subject
import models.topic
import models.subtopic
import models.question
import models.interview_session
import models.answer

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Simulator API", version="1.0.0")

logger.info("Interview Simulator API starting up")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(interview_router)
app.include_router(answer_router)
app.include_router(analytics_router)
app.include_router(voice_router, prefix="/api", tags=["Voice"])
app.include_router(vision_router)
app.include_router(code_router)
app.include_router(ai_router, prefix="/ai")
app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(report_router)

# ── Global error handlers ────────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("HTTP %d | %s %s | %s", exc.status_code, request.method, request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "path": str(request.url.path),
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation 422 | %s %s | %s", request.method, request.url.path, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "message": "Invalid request parameters",
                "details": exc.errors(),
                "path": str(request.url.path),
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled 500 | %s %s | %s: %s", request.method, request.url.path, type(exc).__name__, exc)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "InternalError",
                "message": "An unexpected error occurred.",
                "path": str(request.url.path),
            },
        },
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"success": True, "message": "Interview Simulator API is running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "AI Interview Simulator", "version": "1.0"}