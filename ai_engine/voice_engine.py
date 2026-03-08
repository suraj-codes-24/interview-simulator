import librosa
import numpy as np
import whisper
import parselmouth
from parselmouth.praat import call
import tempfile
import os
import re
import soundfile as sf
import scipy.signal as scipy_signal
from concurrent.futures import ThreadPoolExecutor

# ─────────────────────────────────────────────
# NORMALIZE audio → standard 16kHz mono WAV
# Fixes browser-converted WAV format issues
# ─────────────────────────────────────────────
def normalize_audio(audio_path: str) -> str:
    """Convert any WAV to standard 16kHz mono PCM WAV that all libraries can read."""
    try:
        y, sr_rate = librosa.load(audio_path, sr=16000, mono=True)
        
        # 1. ROBUST NORMALIZATION: Handle pops/clicks and low volume
        if len(y) > 0:
            # Use 99.5th percentile to find the 'real' peak, ignoring sudden pops/clicks (outliers)
            p99 = np.percentile(np.abs(y), 99.5)
            abs_max = np.abs(y).max()
            print(f"[DEBUG] Audio Peak (99.5th%): {p99:.4f} | Absolute Max: {abs_max:.4f}")
            
            if p99 > 0.00005:  # Not pure silence
                # Scale based on p99 to ensure the actual speech reaches a good volume
                # If there are pops (> p99), they will be clipped later
                scale_factor = 0.8 / p99 
                y = y * scale_factor
                
                # Clip any amplified pops to avoid digital distortion/overflow
                y = np.clip(y, -1.0, 1.0)
                
                db_boost = 20 * np.log10(scale_factor)
                print(f"[DEBUG] Applied Robust Boost: +{db_boost:.1f}dB")
            else:
                print(f"[DEBUG] Audio is too quiet/silent for normalization")

        normalized_path = audio_path.replace(".wav", "_norm.wav").replace(".webm", "_norm.wav")
        if normalized_path == audio_path:
            normalized_path = audio_path + "_norm.wav"

        sf.write(normalized_path, y, 16000, subtype="PCM_16")
        return normalized_path
    except Exception as e:
        print(f"Audio normalization failed: {e}")
        return audio_path

# ─────────────────────────────────────────────
# FILLER WORDS to detect
# ─────────────────────────────────────────────
FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically", "literally",
    "actually", "so", "right", "okay", "hmm", "er", "ah",
    "kind of", "sort of", "i mean", "you see"
]

# ─────────────────────────────────────────────
# TRANSCRIBE audio to text using SpeechRecognition
# ─────────────────────────────────────────────
# Load once at startup — use 'base' for speed, 'small' for accuracy
_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")  # loads on GPU automatically
    return _whisper_model

def transcribe_audio(audio_path: str) -> str:
    try:
        model = get_whisper_model()
        # Load audio using librosa (soundfile backend) to avoid ffmpeg dependency
        # Whisper expects 16kHz mono audio
        y, sr = librosa.load(audio_path, sr=16000)
        result = model.transcribe(y, language="en", fp16=False)
        transcript = result["text"].strip().lower()
        print(f"[DEBUG] Whisper transcript: '{transcript}'")
        return transcript
    except Exception as e:
        print(f"[DEBUG] Whisper error: {e}")
        return ""


# ─────────────────────────────────────────────
# SPEAKING PACE — words per minute
# ─────────────────────────────────────────────
def calculate_pace(transcript: str, duration_seconds: float) -> dict:
    if duration_seconds <= 0:
        return {"wpm": 0, "label": "unknown", "score": 0}

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
        return {"count": 0, "fillers_found": [], "score": 100}

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
# PITCH & CONFIDENCE via parselmouth (Praat)
# ─────────────────────────────────────────────
def analyze_pitch(audio_path: str) -> dict:
    try:
        sound = parselmouth.Sound(audio_path)
        pitch = call(sound, "To Pitch", 0.0, 40, 600)  # even lower floor for quiet mic
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values > 0]  # remove unvoiced frames

        if len(pitch_values) == 0:
            return {"mean_pitch": 0, "pitch_variation": 0, "confidence_score": 50}

        mean_pitch = float(np.mean(pitch_values))
        pitch_std = float(np.std(pitch_values))

        # Good variation = expressive speaker, too flat = monotone
        if pitch_std < 20:
            confidence_score = 55  # monotone
        elif pitch_std < 50:
            confidence_score = 80  # natural variation
        elif pitch_std < 100:
            confidence_score = 95  # great expressiveness
        else:
            confidence_score = 70  # too variable / nervous

        return {
            "mean_pitch": round(mean_pitch, 1),
            "pitch_variation": round(pitch_std, 1),
            "confidence_score": confidence_score
        }
    except Exception:
        return {"mean_pitch": 0, "pitch_variation": 0, "confidence_score": 50}


# ─────────────────────────────────────────────
# SILENCE RATIO via librosa
# Too much silence = hesitant, too little = rushed
# ─────────────────────────────────────────────
def analyze_silence(audio_path: str) -> dict:
    try:
        y, sr_rate = librosa.load(audio_path, sr=None)
        # Balanced threshold - 40dB below peak. 
        # 60 was too lenient (kept noise), 15 was too strict (cut speech).
        intervals = librosa.effects.split(y, top_db=40)

        total_frames = len(y)
        voiced_frames = sum(end - start for start, end in intervals)
        
        # Filter out tiny intervals (pops/clicks < 50ms)
        min_samples = int(sr_rate * 0.05)
        filtered_voiced_frames = sum(end - start for start, end in intervals if (end - start) > min_samples)
        
        silence_ratio = 1 - (filtered_voiced_frames / total_frames) if total_frames > 0 else 0
        
        print(f"[DEBUG] Voice Segments: {len(intervals)} | Robust Silence Ratio: {silence_ratio*100:.1f}%")

        if silence_ratio < 0.25:
            label = "minimal pauses"
            score = 85
        elif silence_ratio < 0.40:
            label = "good pausing"
            score = 100
        elif silence_ratio < 0.55:
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
    except Exception:
        return {"silence_ratio": 0, "label": "unknown", "score": 70}


# ─────────────────────────────────────────────
# ENERGY / LOUDNESS — detect low energy = nervous
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
    except Exception:
        return {"mean_energy": 0, "energy_variation": 0, "label": "unknown", "score": 70}


# ─────────────────────────────────────────────
# GENERATE VOICE FEEDBACK
# ─────────────────────────────────────────────
def generate_voice_feedback(
    pace: dict,
    filler: dict,
    pitch: dict,
    silence: dict,
    energy: dict,
    overall_score: float
) -> str:
    parts = []

    if overall_score >= 80:
        parts.append("Great delivery!")
    elif overall_score >= 60:
        parts.append("Decent delivery with some areas to work on.")
    else:
        parts.append("Your delivery needs improvement.")

    # Pace feedback
    if pace["label"] == "too fast":
        parts.append(f"You spoke at {pace['wpm']} WPM — slow down a bit.")
    elif pace["label"] == "too slow":
        parts.append(f"You spoke at {pace['wpm']} WPM — try to be more confident and fluent.")
    elif pace["label"] == "good pace":
        parts.append(f"Good speaking pace ({pace['wpm']} WPM).")

    # Filler feedback
    if filler["count"] > 5:
        top_fillers = [f["word"] for f in filler["fillers_found"][:3]]
        parts.append(f"Reduce filler words like: {', '.join(top_fillers)}.")
    elif filler["count"] > 0:
        parts.append(f"Minor filler words detected ({filler['count']} total) — keep reducing them.")

    # Confidence from pitch
    if pitch["confidence_score"] < 65:
        parts.append("Try to vary your tone more — monotone speech sounds less confident.")

    # Silence feedback
    if silence["label"] == "too many pauses":
        parts.append("Too many long pauses — practice speaking more fluently.")

    # Energy feedback
    if energy["label"] == "very quiet":
        parts.append("Speak louder and with more energy.")

    return " ".join(parts)


# ─────────────────────────────────────────────
# MAIN FUNCTION — full voice analysis
# ─────────────────────────────────────────────
def analyze_voice(audio_path: str) -> dict:
    # Normalize to 16kHz for librosa/parselmouth
    normalized_path = normalize_audio(audio_path)

    print(f"[DEBUG] Audio path: {audio_path}")
    print(f"[DEBUG] Normalized path: {normalized_path}")

    # Get duration
    try:
        y, sr_rate = librosa.load(normalized_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr_rate)
    except Exception:
        duration = 0

    print(f"[DEBUG] Duration: {duration}")

    # Run transcript + audio analyses IN PARALLEL
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Whisper works better on normalized WAV to avoid WinError 2 (ffmpeg missing)
        # We use normalized as it's pre-cleansed and amplified
        transcript_future = executor.submit(transcribe_audio, normalized_path)
        pitch_future = executor.submit(analyze_pitch, normalized_path)
        silence_future = executor.submit(analyze_silence, normalized_path)
        energy_future = executor.submit(analyze_energy, normalized_path)

        transcript = transcript_future.result()
        pitch = pitch_future.result()
        silence = silence_future.result()
        energy = energy_future.result()

    pace = calculate_pace(transcript, duration)
    filler = detect_filler_words(transcript)

    # Cleanup normalized file if different from original
    if normalized_path != audio_path and os.path.exists(normalized_path):
        os.remove(normalized_path)

    # Overall voice score (weighted)
    overall_score = round(
        (pace["score"] * 0.25) +
        (filler["score"] * 0.25) +
        (pitch["confidence_score"] * 0.20) +
        (silence["score"] * 0.15) +
        (energy["score"] * 0.15),
        2
    )

    feedback = generate_voice_feedback(pace, filler, pitch, silence, energy, overall_score)

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
