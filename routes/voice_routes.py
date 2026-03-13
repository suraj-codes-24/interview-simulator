from fastapi import APIRouter, UploadFile, File, HTTPException
from ai_engine.voice_engine import analyze_voice
from core.logger import logger
import tempfile
import os

router = APIRouter()

@router.post("/voice/analyze")
async def analyze_voice_answer(audio: UploadFile = File(...)):
    tmp_path = None
    try:
        contents = await audio.read()
        logger.info("Voice upload: %d bytes | type: %s", len(contents), audio.content_type)

        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file received")

        if len(contents) > 50 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Audio file too large. Max 50 MB.")

        suffix = ".wav"
        if audio.filename and "." in audio.filename:
            suffix = "." + audio.filename.rsplit(".", 1)[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        result = analyze_voice(tmp_path)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Voice analysis failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Voice analysis failed: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)