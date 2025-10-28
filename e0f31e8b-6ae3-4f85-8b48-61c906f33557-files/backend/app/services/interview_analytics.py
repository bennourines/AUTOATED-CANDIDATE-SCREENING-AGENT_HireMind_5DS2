def analyze_answer(answer: str) -> dict:
    return {"sentiment": "neutral", "keywords": list({w.lower() for w in answer.split() if len(w) > 6})[:5]}
