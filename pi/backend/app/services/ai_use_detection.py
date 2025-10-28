def detect_ai_usage_on_resume(text: str) -> dict:
    score = min(0.99, max(0.0, len([c for c in text if c.isupper()]) / (len(text) + 1)))
    return {"ai_likelihood": round(score, 2)}

def detect_ai_usage_on_answer(text: str) -> dict:
    return detect_ai_usage_on_resume(text)
