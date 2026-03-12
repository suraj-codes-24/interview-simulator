import requests

OLLAMA_URL  = "http://localhost:11434/api/generate"
MODEL_NAME  = "qwen2.5-coder:7b"


def generate_followup(question_text: str, user_answer: str) -> str:
    """
    Ask Ollama to produce ONE short follow-up question (≤25 words).
    Returns the question string. Falls back to a generic probe on error.
    """
    prompt = f"""You are a senior technical interviewer.

Original question:
{question_text}

Candidate answer:
{user_answer}

Generate ONE follow-up question that probes deeper understanding.

Rules:
- Only one question
- Maximum 25 words
- No explanations
- Output only the question"""

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model":  MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.4,
                    "num_predict": 60,
                },
            },
            timeout=60,
        )

        if resp.status_code != 200:
            return _fallback(question_text)

        raw = resp.json().get("response", "").strip()

        # Strip any accidental numbering / bullets / quotes
        for prefix in ("1.", "-", "*", '"', "'"):
            if raw.startswith(prefix):
                raw = raw[len(prefix):].strip()

        # Take only the first sentence if the model returned more
        first_sentence = raw.split("?")[0].strip()
        if first_sentence:
            return first_sentence + "?"

        return _fallback(question_text)

    except requests.exceptions.ConnectionError:
        return "Ollama is not running — please start it with: ollama serve"
    except Exception:
        return _fallback(question_text)


def _fallback(question_text: str) -> str:
    q = question_text.lower()
    if any(k in q for k in ["time complexity", "complexity", "big o", "o(n"]):
        return "Can you explain the time and space complexity of your approach?"
    if any(k in q for k in ["edge case", "handle", "null", "empty"]):
        return "How would your solution handle edge cases like empty input or duplicates?"
    if any(k in q for k in ["algorithm", "sort", "search", "binary"]):
        return "Can you think of a more optimal approach or data structure for this?"
    if any(k in q for k in ["design", "system", "scale", "distributed"]):
        return "How would you scale this system to handle millions of requests per second?"
    return "Can you elaborate on why you chose this approach over alternatives?"
