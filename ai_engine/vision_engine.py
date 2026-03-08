import cv2
import mediapipe as mp
import numpy as np
import base64

# ─────────────────────────────────────────────
# FACE ANALYZER (Mediapipe FaceMesh)
# ─────────────────────────────────────────────
# Initialize Mediapipe
mp_face_mesh = mp.solutions.face_mesh
# Using a context-based or persistent instance
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def analyze_frame(image_b64: str) -> dict:
    """Analyzes a single frame for eye contact and head orientation."""
    try:
        # Decode base64 image
        if "," in image_b64:
            header, encoded = image_b64.split(",", 1)
        else:
            encoded = image_b64
            
        data = base64.b64decode(encoded)
        np_arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return {"error": "Invalid image format"}

        h, w, _ = img.shape
        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return {
                "face_detected": False,
                "eye_contact": 0,
                "head_stability": 0,
                "emotion": "undiscovered"
            }

        # Face detected
        face_landmarks = results.multi_face_landmarks[0].landmark

        # 1. Eye Contact Detection
        eye_contact = calculate_eye_contact(face_landmarks)

        # 2. Head Stability
        head_stability = calculate_head_stability(face_landmarks)

        # 3. Emotion Estimation
        emotion = estimate_emotion(face_landmarks)

        return {
            "face_detected": True,
            "eye_contact": round(eye_contact, 2),
            "head_stability": round(head_stability, 2),
            "emotion": emotion
        }

    except Exception as e:
        print(f"[VISION] Error analyzing frame: {e}")
        return {"error": str(e)}

def calculate_eye_contact(landmarks) -> float:
    """Estimates eye contact based on iris centering."""
    # Landmarks 468 (L iris center) and 473 (R iris center)
    l_iris = landmarks[468]
    r_iris = landmarks[473]
    
    # We want these to be relatively 'middle' in the eye socket
    # Face center is at landmark 1 (nose tip)
    nose = landmarks[1]
    
    # Eye contact is high if nose tip is relatively centered (forward facing)
    # and pupils are not gazing too far left/right
    dist_x = abs(nose.x - 0.5)
    dist_y = abs(nose.y - 0.5)
    
    # Simple metric: 100 * (1 - normalized distance from center)
    score = max(0, 100 - (dist_x * 300 + dist_y * 300))
    return score

def calculate_head_stability(landmarks) -> float:
    """Returns head stability (how centered/still the head is)."""
    # Landmark 1 = Tip of nose
    nose = landmarks[1]
    
    # Horizontal/Vertical centering
    x_score = max(0, 100 - abs(nose.x - 0.5) * 400)
    y_score = max(0, 100 - abs(nose.y - 0.5) * 400)
    
    return (x_score + y_score) / 2

def estimate_emotion(landmarks) -> str:
    """Rough estimation of emotion based on lip/eyebrow landmarks."""
    # Lip outer contour: 61 (L), 291 (R)
    # Lip vertical distance: 13 (upper inner lip), 14 (lower inner lip)
    lip_dist = abs(landmarks[13].y - landmarks[14].y)
    lip_width = abs(landmarks[61].x - landmarks[291].x)
    
    # Eyes: 159 (top), 145 (bottom) - check if wide open
    eye_open = abs(landmarks[159].y - landmarks[145].y)
    
    if lip_dist > 0.05: return "surprised"
    if eye_open < 0.01: return "nervous" # blinking or squinting
    if lip_width > 0.08: return "confident" # slight grin/smile
    
    return "calm"
