import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"


def evaluate_hr_answer(question_text: str, user_answer: str) -> dict:
    """
    Evaluate a behavioral/HR answer using Ollama (qwen2.5-coder).
    Returns scores for clarity, structure, communication, relevance + feedback.
    """

    if not user_answer or not user_answer.strip():
        return {
            "clarity":       0.0,
            "structure":     0.0,
            "communication": 0.0,
            "relevance":     0.0,
            "hr_score":      0.0,
            "feedback":      "No answer was provided."
        }

    prompt = f"""You are an expert HR interviewer evaluating a candidate's answer.

Question: {question_text}

Candidate Answer: {user_answer}

Evaluate the answer on these 4 criteria (score each from 0 to 10):
1. clarity - Is the answer clear and easy to understand?
2. structure - Is it well structured? (STAR method: Situation, Task, Action, Result)
3. communication - Does it show good communication skills?
4. relevance - Is it relevant and directly answers the question?

Also write one sentence of feedback.

Reply ONLY with this JSON format, nothing else:
{{
  "clarity": <number>,
  "structure": <number>,
  "communication": <number>,
  "relevance": <number>,
  "feedback": "<one sentence>"
}}"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 200,
                }
            },
            timeout=60
        )

        if response.status_code != 200:
            return _fallback_score(user_answer)

        raw = response.json().get("response", "")
        scores = _parse_response(raw)
        return scores

    except requests.exceptions.ConnectionError:
        return {
            "clarity":       0.0,
            "structure":     0.0,
            "communication": 0.0,
            "relevance":     0.0,
            "hr_score":      0.0,
            "feedback":      "Ollama is not running. Start it with: ollama serve"
        }
    except Exception as e:
        return _fallback_score(user_answer)


def _parse_response(raw: str) -> dict:
    """Extract JSON from Ollama response."""
    try:
        # Find JSON block in response
        match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if not match:
            return _fallback_score("")

        data = json.loads(match.group())

        clarity       = float(data.get("clarity", 5))
        structure     = float(data.get("structure", 5))
        communication = float(data.get("communication", 5))
        relevance     = float(data.get("relevance", 5))
        feedback      = str(data.get("feedback", "Good effort."))

        # HR score formula
        hr_score = round(
            (clarity * 0.25 +
             structure * 0.30 +
             communication * 0.25 +
             relevance * 0.20) * 10,
            2
        )

        return {
            "clarity":       round(clarity * 10, 2),
            "structure":     round(structure * 10, 2),
            "communication": round(communication * 10, 2),
            "relevance":     round(relevance * 10, 2),
            "hr_score":      hr_score,
            "feedback":      feedback
        }

    except Exception:
        return _fallback_score("")


def _fallback_score(user_answer: str) -> dict:
    """Simple rule-based fallback if Ollama fails."""
    word_count = len(user_answer.split()) if user_answer else 0

    if word_count >= 50:
        score = 60.0
        feedback = "Good length answer. Start Ollama for AI-powered evaluation."
    elif word_count >= 20:
        score = 40.0
        feedback = "Decent answer but try to elaborate more."
    else:
        score = 20.0
        feedback = "Answer is too short. Use the STAR method for HR questions."

    return {
        "clarity":       score,
        "structure":     score,
        "communication": score,
        "relevance":     score,
        "hr_score":      score,
        "feedback":      feedback
    }