import torch
import librosa
import numpy as np
import whisper
import parselmouth
from parselmouth.praat import call
import soundfile as sf
import tempfile
import os
import re
from concurrent.futures import ThreadPoolExecutor

# ─────────────────────────────────────────────
# LOAD WHISPER ONCE at startup (GPU auto-detected)
# ─────────────────────────────────────────────
print("[VOICE] Loading Whisper model...")
_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[VOICE] Loading Whisper on {device}...")
        _whisper_model = whisper.load_model("base", device=device)
        print(f"[VOICE] Whisper loaded on {device}!")
    return _whisper_model

# Pre-load on import
try:
    get_whisper_model()
except Exception as e:
    print(f"[VOICE] Whisper load failed: {e}")

# ─────────────────────────────────────────────
# FILLER WORDS
# ─────────────────────────────────────────────
FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically", "literally",
    "actually", "so", "right", "okay", "hmm", "er", "ah",
    "kind of", "sort of", "i mean", "you see"
]

# ─────────────────────────────────────────────
# NORMALIZE audio → standard 16kHz mono WAV
# ─────────────────────────────────────────────
def normalize_audio(audio_path: str) -> str:
    try:
        y, sr_rate = librosa.load(audio_path, sr=16000, mono=True)
        normalized_path = audio_path.rsplit(".", 1)[0] + "_norm.wav"
        sf.write(normalized_path, y, 16000, subtype="PCM_16")
        return normalized_path
    except Exception as e:
        print(f"[VOICE] Normalization failed: {e}")
        return audio_path

# ─────────────────────────────────────────────
# TRANSCRIBE using Whisper (local GPU)
# ─────────────────────────────────────────────
def transcribe_audio(audio_path: str) -> str:
    try:
        model = get_whisper_model()
        
        # Load audio manually with librosa → pass as numpy array
        # This bypasses ffmpeg completely
        y, sr_rate = librosa.load(audio_path, sr=16000, mono=True)
        audio_array = y.astype(np.float32)
        
        # Use GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[VOICE] Whisper running on: {device}")
        
        result = model.transcribe(
            audio_array,        # numpy array instead of file path
            language="en",
            fp16=torch.cuda.is_available(),
            verbose=False
        )
        transcript = result["text"].strip().lower()
        print(f"[VOICE] Transcript: '{transcript}'")
        return transcript
    except Exception as e:
        print(f"[VOICE] Whisper error: {e}")
        return ""

# ─────────────────────────────────────────────
# PACE — words per minute
# ─────────────────────────────────────────────
def calculate_pace(transcript: str, duration_seconds: float) -> dict:
    if duration_seconds <= 0:
        return {"wpm": 0, "label": "unknown", "score": 50}

    words = transcript.split()
    word_count = len(words)
    wpm = (word_count / duration_seconds) * 60

    if wpm < 80:
        label = "too slow"
        score = 50
    elif wpm < 120:
        label = "slightly slow"
        score = 75
    elif wpm <= 160:
        label = "good pace"
        score = 100
    elif wpm <= 200:
        label = "slightly fast"
        score = 75
    else:
        label = "too fast"
        score = 50

    return {"wpm": round(wpm, 1), "label": label, "score": score}

# ─────────────────────────────────────────────
# FILLER WORD COUNT
# ─────────────────────────────────────────────
def detect_filler_words(transcript: str) -> dict:
    if not transcript:
        return {"count": 0, "fillers_found": [], "score": 100, "filler_ratio_percent": 0}

    found = []
    text_lower = transcript.lower()
    for filler in FILLER_WORDS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            found.append({"word": filler, "count": len(matches)})

    total_count = sum(f["count"] for f in found)
    word_count = max(len(transcript.split()), 1)
    filler_ratio = total_count / word_count

    if filler_ratio < 0.03:
        score = 100
    elif filler_ratio < 0.06:
        score = 80
    elif filler_ratio < 0.10:
        score = 60
    elif filler_ratio < 0.15:
        score = 40
    else:
        score = 20

    return {
        "count": total_count,
        "fillers_found": found,
        "score": score,
        "filler_ratio_percent": round(filler_ratio * 100, 1)
    }

# ─────────────────────────────────────────────
# PITCH & CONFIDENCE via parselmouth
# ─────────────────────────────────────────────
def analyze_pitch(audio_path: str) -> dict:
    try:
        sound = parselmouth.Sound(audio_path)

        # Try multiple pitch floor values for better detection
        pitch_values = np.array([])
        for floor in [50, 60, 75]:
            pitch = call(sound, "To Pitch", 0.0, floor, 600)
            vals = pitch.selected_array['frequency']
            vals = vals[vals > 0]
            if len(vals) > len(pitch_values):
                pitch_values = vals

        if len(pitch_values) == 0:
            # Fallback: use librosa for pitch estimation
            y, sr_rate = librosa.load(audio_path, sr=None)
            f0 = librosa.yin(y, fmin=50, fmax=600)
            f0 = f0[f0 > 50]
            if len(f0) == 0:
                return {"mean_pitch": 0, "pitch_variation": 0, "confidence_score": 60}
            pitch_values = f0

        mean_pitch = float(np.mean(pitch_values))
        pitch_std = float(np.std(pitch_values))

        # More lenient confidence scoring
        # Normal speech: 10-80 Hz variation is completely fine
        if pitch_std < 8:
            confidence_score = 55   # very monotone
        elif pitch_std < 15:
            confidence_score = 70   # slightly flat
        elif pitch_std < 40:
            confidence_score = 85   # good natural variation
        elif pitch_std < 80:
            confidence_score = 95   # great expressiveness
        else:
            confidence_score = 75   # too variable / nervous

        print(f"[VOICE] Pitch: mean={mean_pitch:.1f}Hz std={pitch_std:.1f}Hz confidence={confidence_score}%")

        return {
            "mean_pitch": round(mean_pitch, 1),
            "pitch_variation": round(pitch_std, 1),
            "confidence_score": confidence_score
        }
    except Exception as e:
        print(f"[VOICE] Pitch analysis error: {e}")
        return {"mean_pitch": 0, "pitch_variation": 0, "confidence_score": 60}

# ─────────────────────────────────────────────
# SILENCE RATIO
# ─────────────────────────────────────────────
def analyze_silence(audio_path: str) -> dict:
    try:
        y, sr_rate = librosa.load(audio_path, sr=None)
        intervals = librosa.effects.split(y, top_db=30)

        total_frames = len(y)
        voiced_frames = sum(end - start for start, end in intervals)
        silence_ratio = 1 - (voiced_frames / total_frames) if total_frames > 0 else 0

        if silence_ratio < 0.10:
            label = "minimal pauses"
            score = 85
        elif silence_ratio < 0.25:
            label = "good pausing"
            score = 100
        elif silence_ratio < 0.40:
            label = "some hesitation"
            score = 70
        else:
            label = "too many pauses"
            score = 50

        return {
            "silence_ratio": round(silence_ratio * 100, 1),
            "label": label,
            "score": score
        }
    except Exception as e:
        print(f"[VOICE] Silence analysis error: {e}")
        return {"silence_ratio": 0, "label": "unknown", "score": 70}

# ─────────────────────────────────────────────
# ENERGY / LOUDNESS
# ─────────────────────────────────────────────
def analyze_energy(audio_path: str) -> dict:
    try:
        y, sr_rate = librosa.load(audio_path, sr=None)
        rms = librosa.feature.rms(y=y)[0]
        mean_energy = float(np.mean(rms))
        energy_std = float(np.std(rms))

        if mean_energy < 0.01:
            label = "very quiet"
            score = 50
        elif mean_energy < 0.05:
            label = "soft spoken"
            score = 75
        elif mean_energy < 0.15:
            label = "clear volume"
            score = 100
        else:
            label = "loud"
            score = 80

        return {
            "mean_energy": round(mean_energy, 4),
            "energy_variation": round(energy_std, 4),
            "label": label,
            "score": score
        }
    except Exception as e:
        print(f"[VOICE] Energy analysis error: {e}")
        return {"mean_energy": 0, "energy_variation": 0, "label": "unknown", "score": 70}

# ─────────────────────────────────────────────
# FEEDBACK GENERATOR
# ─────────────────────────────────────────────
def generate_voice_feedback(pace, filler, pitch, silence, energy, overall_score) -> str:
    parts = []

    if overall_score >= 80:
        parts.append("Great delivery!")
    elif overall_score >= 60:
        parts.append("Decent delivery with some areas to work on.")
    else:
        parts.append("Your delivery needs improvement.")

    if pace["label"] == "too fast":
        parts.append(f"You spoke at {pace['wpm']} WPM — slow down a bit.")
    elif pace["label"] in ["too slow", "slightly slow"] and pace["wpm"] > 0:
        parts.append(f"You spoke at {pace['wpm']} WPM — try to be more fluent.")
    elif pace["label"] == "good pace":
        parts.append(f"Good speaking pace ({pace['wpm']} WPM).")

    if filler["count"] > 5:
        top = [f["word"] for f in filler["fillers_found"][:3]]
        parts.append(f"Reduce filler words like: {', '.join(top)}.")
    elif filler["count"] > 0:
        parts.append(f"Minor filler words detected ({filler['count']}) — keep reducing them.")

    if pitch["confidence_score"] < 65:
        parts.append("Vary your tone more — monotone speech sounds less confident.")

    if silence["label"] == "too many pauses":
        parts.append("Too many long pauses — practice speaking more fluently.")

    if energy["label"] == "very quiet":
        parts.append("Speak louder and with more energy.")

    return " ".join(parts)

# ─────────────────────────────────────────────
# MAIN — full voice analysis with parallel processing
# ─────────────────────────────────────────────
def analyze_voice(audio_path: str) -> dict:
    print(f"[VOICE] Starting analysis: {audio_path}")

    # Normalize for librosa/parselmouth
    normalized_path = normalize_audio(audio_path)
    print(f"[VOICE] Normalized: {normalized_path}")

    # Get duration
    try:
        y, sr_rate = librosa.load(normalized_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr_rate)
    except Exception:
        duration = 0
    print(f"[VOICE] Duration: {duration:.2f}s")

    # Run Whisper + audio analyses IN PARALLEL
    with ThreadPoolExecutor(max_workers=4) as executor:
        transcript_future = executor.submit(transcribe_audio, audio_path)      # original for STT
        pitch_future      = executor.submit(analyze_pitch, normalized_path)
        silence_future    = executor.submit(analyze_silence, normalized_path)
        energy_future     = executor.submit(analyze_energy, normalized_path)

        transcript = transcript_future.result()
        pitch      = pitch_future.result()
        silence    = silence_future.result()
        energy     = energy_future.result()

    print(f"[VOICE] All analysis done. Transcript length: {len(transcript)}")

    pace   = calculate_pace(transcript, duration)
    filler = detect_filler_words(transcript)

    overall_score = round(
        (pace["score"]                  * 0.25) +
        (filler["score"]                * 0.25) +
        (pitch["confidence_score"]      * 0.20) +
        (silence["score"]               * 0.15) +
        (energy["score"]                * 0.15),
        2
    )

    feedback = generate_voice_feedback(pace, filler, pitch, silence, energy, overall_score)

    # Cleanup normalized file
    if normalized_path != audio_path and os.path.exists(normalized_path):
        os.remove(normalized_path)

    return {
        "transcript": transcript,
        "duration_seconds": round(duration, 1),
        "overall_voice_score": overall_score,
        "feedback": feedback,
        "details": {
            "pace": pace,
            "filler_words": filler,
            "confidence": pitch,
            "silence": silence,
            "energy": energy
        }
    }
