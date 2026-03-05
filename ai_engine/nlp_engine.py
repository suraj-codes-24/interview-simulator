from sentence_transformers import SentenceTransformer, util
import re

# Load model once when the module is imported
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(user_answer: str, ideal_answer: str) -> float:
    """
    Compare meaning of user answer vs ideal answer.
    Returns a score between 0.0 and 1.0
    """
    embeddings = model.encode([user_answer, ideal_answer], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    score = float(similarity.item())
    # Clamp between 0 and 1
    return max(0.0, min(1.0, score))


def calculate_keyword_coverage(user_answer: str, ideal_answer: str) -> float:
    """
    Check how many important keywords from ideal answer are in user answer.
    Returns a score between 0.0 and 1.0
    """
    # Extract keywords (words longer than 4 chars, ignore common words)
    stop_words = {
        "this", "that", "with", "from", "they", "them", "then",
        "than", "when", "where", "which", "have", "been", "will",
        "also", "more", "some", "into", "each", "used", "using",
        "very", "just", "about", "would", "could", "should"
    }

    def extract_keywords(text: str) -> set:
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return {w for w in words if len(w) > 4 and w not in stop_words}

    ideal_keywords = extract_keywords(ideal_answer)
    user_keywords = extract_keywords(user_answer)

    if not ideal_keywords:
        return 1.0

    matched = ideal_keywords.intersection(user_keywords)
    score = len(matched) / len(ideal_keywords)
    return round(min(1.0, score), 4)


def calculate_structure_quality(user_answer: str) -> float:
    """
    Check if the answer is well structured.
    Looks at: length, sentence count, use of technical terms.
    Returns a score between 0.0 and 1.0
    """
    score = 0.0
    word_count = len(user_answer.split())
    sentence_count = len(re.findall(r'[.!?]', user_answer))

    # Length check — good answers are usually 30-200 words
    if word_count >= 15:
        score += 0.4
    if word_count >= 40:
        score += 0.2

    # Sentence structure
    if sentence_count >= 2:
        score += 0.2

    # Uses numbers or technical terms (O(n), %, complexity, etc.)
    if re.search(r'O\(|%|time|space|complex|algorithm|example|because|therefore', user_answer, re.IGNORECASE):
        score += 0.2

    return round(min(1.0, score), 4)


def evaluate_answer(user_answer: str, ideal_answer: str) -> dict:
    """
    Main function — evaluates user answer and returns full breakdown.

    Formula:
        NLP Score = 50% Semantic + 30% Keyword + 20% Structure
    """
    if not user_answer or not user_answer.strip():
        return {
            "semantic_score": 0.0,
            "keyword_score": 0.0,
            "structure_score": 0.0,
            "nlp_score": 0.0,
            "feedback": "No answer was provided."
        }

    semantic = calculate_semantic_similarity(user_answer, ideal_answer)
    keyword = calculate_keyword_coverage(user_answer, ideal_answer)
    structure = calculate_structure_quality(user_answer)

    # Weighted final score (out of 100)
    nlp_score = round((semantic * 0.5 + keyword * 0.3 + structure * 0.2) * 100, 2)

    # Generate simple feedback
    feedback = generate_feedback(semantic, keyword, structure)

    return {
        "semantic_score": round(semantic * 100, 2),
        "keyword_score": round(keyword * 100, 2),
        "structure_score": round(structure * 100, 2),
        "nlp_score": nlp_score,
        "feedback": feedback
    }


def generate_feedback(semantic: float, keyword: float, structure: float) -> str:
    """Generate a simple feedback message based on scores."""
    feedback_parts = []

    if semantic >= 0.75:
        feedback_parts.append("Great understanding of the concept.")
    elif semantic >= 0.5:
        feedback_parts.append("You have a basic understanding but missed some key ideas.")
    else:
        feedback_parts.append("Your answer is off-topic or too vague.")

    if keyword < 0.4:
        feedback_parts.append("Try to include more technical keywords in your answer.")

    if structure < 0.6:
        feedback_parts.append("Work on structuring your answer better — add examples or explain your reasoning.")

    return " ".join(feedback_parts)
