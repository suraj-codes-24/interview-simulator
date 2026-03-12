"""
Centralized Ollama HTTP helper.
All services should call generate() instead of requests.post() directly.
"""
import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"


def generate(prompt: str, temperature: float = 0.3, max_tokens: int = 300) -> str:
    """
    Send a prompt to Ollama and return the raw response string.

    Returns:
        The model response text, or "" on any failure.

    Raises:
        OllamaUnavailable if Ollama is not running (caller can catch to show
        a friendly message; other exceptions are swallowed and return "").
    """
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model":  MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            },
            timeout=90,
        )
        if resp.status_code != 200:
            return ""
        return resp.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        raise OllamaUnavailable("Ollama is not running. Start it with: ollama serve")
    except requests.exceptions.Timeout:
        return ""
    except Exception:
        return ""


def extract_json_object(text: str) -> dict | None:
    """Extract the first JSON object from a string. Returns None if not found."""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except (json.JSONDecodeError, AttributeError):
        pass
    return None


def extract_json_array(text: str) -> list | None:
    """Extract the first JSON array from a string. Returns None if not found."""
    try:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except (json.JSONDecodeError, AttributeError):
        pass
    return None


class OllamaUnavailable(Exception):
    """Raised when Ollama cannot be reached."""
    pass
