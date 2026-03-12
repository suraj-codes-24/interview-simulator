from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database import get_db
from models.user import User
from services.resume_service import analyse_resume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/analyse")
async def analyse_resume_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a PDF resume and get ATS score, skills, suggestions, and interview questions."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    if len(pdf_bytes) > 5 * 1024 * 1024:   # 5 MB limit
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 5 MB.")

    result = analyse_resume(pdf_bytes)
    return result
