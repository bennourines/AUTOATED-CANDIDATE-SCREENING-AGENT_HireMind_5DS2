import os
import requests
from typing import Dict

HF_API_URL = os.getenv("HF_INFERENCE_URL", "https://api-inference.huggingface.co/models/bert-base-uncased")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def parse_resume(resume_text: str) -> Dict:
    if not resume_text:
        return {"skills": [], "summary": "", "experience": []}
    headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
    try:
        _ = requests.post(HF_API_URL, headers=headers, json={"inputs": resume_text}, timeout=10)
    except Exception:
        pass
    skills = []
    for token in resume_text.split():
        if token.istitle() and token.lower() not in {"and", "or", "the", "a"}:
            skills.append(token)
    unique_skills = sorted(set(skills))[:20]
    return {"skills": unique_skills, "summary": resume_text[:200], "experience": []}

def parse_job_description(text: str) -> Dict:
    skills = []
    for token in text.split():
        if token.istitle() and token.lower() not in {"and", "or", "the", "a"}:
            skills.append(token)
    return {"skills": sorted(set(skills))[:20], "summary": text[:200]}
