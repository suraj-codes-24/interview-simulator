from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ai_engine.vision_engine import analyze_frame as analyze_vision_frame
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/vision", tags=["Vision"])

class VisionFrameRequest(BaseModel):
    image: str # Base64 encoded frame
    session_id: int
    question_id: int

@router.post("/analyze")
async def analyze_frame_endpoint(
    request: VisionFrameRequest,
    current_user: User = Depends(get_current_user),
):
    """Analyze a single frame for facial metrics."""
    try:
        results = analyze_vision_frame(request.image)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
