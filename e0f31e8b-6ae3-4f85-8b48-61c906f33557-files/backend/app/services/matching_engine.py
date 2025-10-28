from typing import List, Dict


def compute_fit_score(candidate_profile: Dict, job_profile: Dict) -> float:
    c_skills = set(map(str.lower, candidate_profile.get("skills", [])))
    j_skills = set(map(str.lower, job_profile.get("skills", [])))
    if not j_skills:
        return 0.0
    overlap = c_skills & j_skills
    score = len(overlap) / len(j_skills)
    return round(float(score * 100), 2)


def calculate_match_score(resume_text: str, job_description: str) -> float:
    cand = {"skills": [w for w in resume_text.split() if w.istitle()]}
    job = {"skills": [w for w in job_description.split() if w.istitle()]}
    return compute_fit_score(cand, job)
