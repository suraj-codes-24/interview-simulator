from fastapi import APIRouter, UploadFile, File, HTTPException
from ai_engine.voice_engine import analyze_voice
import tempfile
import os

router = APIRouter()

@router.post("/voice/analyze")
async def analyze_voice_answer(audio: UploadFile = File(...)):
    tmp_path = None
    try:
        # Read all bytes async — fixes the shutil issue
        contents = await audio.read()
        print(f"[DEBUG] Received: {len(contents)} bytes | type: {audio.content_type} | file: {audio.filename}")

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

        print(f"[DEBUG] Saved to: {tmp_path} | size: {os.path.getsize(tmp_path)} bytes")

        result = analyze_voice(tmp_path)
        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Voice analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice analysis failed: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)