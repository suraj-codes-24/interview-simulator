from sentence_transformers import SentenceTransformer, util
import re

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── Technical Synonym Map ─────────────────────────────────────────────────────
# If user says any of these words, they get credit for the concept
SYNONYM_MAP = {
    "time complexity": ["big o", "o(n)", "o(log n)", "o(1)", "runtime", "time taken", "efficiency"],
    "space complexity": ["memory", "extra space", "auxiliary space", "o(1) space"],
    "array": ["list", "contiguous", "sequential", "indexed", "fixed size"],
    "pointer": ["reference", "address", "memory location"],
    "recursion": ["recursive", "base case", "call stack", "self-calling"],
    "iteration": ["loop", "iterate", "for loop", "while loop"],
    "sorting": ["arrange", "order", "ascending", "descending"],
    "searching": ["find", "lookup", "binary search", "linear search"],
    "tree": ["node", "root", "leaf", "child", "parent", "binary"],
    "graph": ["vertex", "edge", "node", "connected", "path"],
    "stack": ["lifo", "push", "pop", "last in first out"],
    "queue": ["fifo", "enqueue", "dequeue", "first in first out"],
    "hash": ["hashmap", "dictionary", "key value", "hashing", "collision"],
    "dynamic programming": ["memoization", "tabulation", "overlapping", "subproblem", "optimal substructure"],
    "greedy": ["local optimal", "greedy choice", "greedy algorithm"],
    "divide and conquer": ["merge sort", "quick sort", "divide", "conquer", "split"],
    "oop": ["object oriented", "class", "object", "encapsulation", "inheritance", "polymorphism", "abstraction"],
    "inheritance": ["extends", "parent class", "child class", "base class", "derived"],
    "polymorphism": ["overloading", "overriding", "method overriding", "runtime"],
    "encapsulation": ["private", "public", "getter", "setter", "data hiding"],
    "linked list": ["node", "next pointer", "head", "tail", "singly", "doubly"],
    "binary search": ["mid", "left", "right", "sorted", "halving", "log n"],
    "two pointer": ["left pointer", "right pointer", "both ends", "inward"],
    "sliding window": ["window", "subarray", "fixed size", "variable size"],
    "bfs": ["breadth first", "level order", "queue", "shortest path"],
    "dfs": ["depth first", "stack", "backtracking", "preorder", "inorder"],
}


# ─── Semantic Similarity ───────────────────────────────────────────────────────

def calculate_semantic_similarity(user_answer: str, ideal_answer: str) -> float:
    """
    Smart semantic comparison.
    - Compares user answer against ideal answer
    - Calibrates score since MiniLM tends to score conservatively
    """
    embeddings = model.encode([user_answer, ideal_answer], convert_to_tensor=True)
    raw_score = float(util.cos_sim(embeddings[0], embeddings[1]).item())
    calibrated = calibrate_score(raw_score)
    return round(max(0.0, min(1.0, calibrated)), 4)


def calibrate_score(raw: float) -> float:
    """
    Rescale raw cosine similarity.
    MiniLM raw scores:
      ~0.9+ = near identical meaning
      ~0.7  = same topic, good overlap
      ~0.5  = related but vague
      ~0.3  = off topic
    We want to spread these out so scoring feels fair.
    """
    if raw >= 0.88:
        return 0.90 + (raw - 0.88) * 0.8    # 0.88 → 90%, 0.98 → 98%
    elif raw >= 0.75:
        return 0.72 + (raw - 0.75) * 1.4    # 0.75 → 72%, 0.88 → 90%
    elif raw >= 0.60:
        return 0.52 + (raw - 0.60) * 1.3    # 0.60 → 52%, 0.75 → 72%
    elif raw >= 0.45:
        return 0.35 + (raw - 0.45) * 1.1    # 0.45 → 35%, 0.60 → 52%
    elif raw >= 0.30:
        return 0.18 + (raw - 0.30) * 1.1    # 0.30 → 18%, 0.45 → 35%
    else:
        return raw * 0.6                     # very low raw → very low score


# ─── Keyword Coverage ─────────────────────────────────────────────────────────

def calculate_keyword_coverage(user_answer: str, ideal_answer: str) -> float:
    """
    Smart keyword coverage:
    - Extracts technical keywords from ideal answer
    - Checks if user used those words OR their synonyms/related terms
    - Gives partial credit for related concepts
    """
    stop_words = {
        "this", "that", "with", "from", "they", "them", "then", "than",
        "when", "where", "which", "have", "been", "will", "also", "more",
        "some", "into", "each", "used", "using", "very", "just", "about",
        "would", "could", "should", "there", "their", "these", "those",
        "what", "while", "after", "before", "other", "first", "last"
    }

    def extract_keywords(text: str) -> set:
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return {w for w in words if len(w) > 3 and w not in stop_words}

    ideal_keywords = extract_keywords(ideal_answer)
    user_text_lower = user_answer.lower()
    user_keywords = extract_keywords(user_answer)

    if not ideal_keywords:
        return 1.0

    matched = 0
    total = len(ideal_keywords)

    for kw in ideal_keywords:
        # Direct match
        if kw in user_keywords:
            matched += 1
            continue

        # Synonym/related term match
        synonym_matched = False
        for concept, synonyms in SYNONYM_MAP.items():
            all_terms = [concept] + synonyms
            if any(kw in term or term in kw for term in all_terms):
                if any(syn in user_text_lower for syn in all_terms):
                    matched += 0.8
                    synonym_matched = True
                    break

        if not synonym_matched:
            # Partial match
            if any(kw in uk or uk in kw for uk in user_keywords if len(uk) > 3):
                matched += 0.5

    score = matched / total
    return round(min(1.0, score), 4)


# ─── Structure Quality ─────────────────────────────────────────────────────────

def calculate_structure_quality(user_answer: str) -> float:
    """
    Smarter structure analysis — rewards thorough, well-explained answers.
    """
    score = 0.0
    text = user_answer.lower()
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]', user_answer)
    sentence_count = len([s for s in sentences if s.strip()])

    # Length scoring
    if word_count >= 10:
        score += 0.2
    if word_count >= 25:
        score += 0.15
    if word_count >= 50:
        score += 0.1

    # Multiple sentences
    if sentence_count >= 2:
        score += 0.1
    if sentence_count >= 3:
        score += 0.05

    # Uses an example
    if re.search(r'\bexample\b|\bfor instance\b|\bsuch as\b|\be\.g\b|\blike\b', text):
        score += 0.1

    # Mentions complexity
    if re.search(r'o\(|time complexity|space complexity|efficient|faster|slower', text):
        score += 0.1

    # Comparison language
    if re.search(r'instead of|better than|compared to|difference|whereas|however|unlike', text):
        score += 0.1

    # Explanation markers
    if re.search(r'because|therefore|this means|which means|so that|in order to', text):
        score += 0.1

    return round(min(1.0, score), 4)


# ─── Main Evaluator ────────────────────────────────────────────────────────────

def evaluate_answer(user_answer: str, ideal_answer: str) -> dict:
    """
    Evaluate user answer with smart scoring.
    Formula: 55% Semantic + 25% Keyword + 20% Structure
    Semantic is weighted highest — we reward understanding over memorization.
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

    nlp_score = round((semantic * 0.55 + keyword * 0.25 + structure * 0.20) * 100, 2)
    feedback = generate_feedback(semantic, keyword, structure, user_answer)

    return {
        "semantic_score": round(semantic * 100, 2),
        "keyword_score": round(keyword * 100, 2),
        "structure_score": round(structure * 100, 2),
        "nlp_score": nlp_score,
        "feedback": feedback
    }


# ─── Smart Feedback ────────────────────────────────────────────────────────────

def generate_feedback(semantic: float, keyword: float, structure: float, user_answer: str) -> str:
    """Generate specific, actionable feedback."""
    parts = []
    word_count = len(user_answer.split())

    # Semantic feedback
    if semantic >= 0.80:
        parts.append("Excellent understanding of the concept.")
    elif semantic >= 0.60:
        parts.append("Good understanding — you got the core idea.")
    elif semantic >= 0.40:
        parts.append("Partial understanding — you are on the right track but missed some key ideas.")
    else:
        parts.append("Your answer needs more depth — try to explain the core concept more clearly.")

    # Keyword feedback
    if keyword < 0.35:
        parts.append("Use more technical terms in your answer — keywords matter in interviews.")
    elif keyword < 0.55:
        parts.append("Include a few more specific technical terms to strengthen your answer.")

    # Structure feedback
    if word_count < 15:
        parts.append("Your answer is too short — interviewers expect at least 2-3 sentences.")
    elif structure < 0.40:
        parts.append("Try adding an example or mentioning time/space complexity to show deeper understanding.")
    elif structure >= 0.75:
        parts.append("Great structure — clear and well-explained.")

    return " ".join(parts)
