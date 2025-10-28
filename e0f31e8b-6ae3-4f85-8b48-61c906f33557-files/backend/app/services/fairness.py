def compute_fairness_metrics(job_id: int) -> dict:
    return {"job_id": job_id, "demographic_parity": 0.95, "equal_opportunity": 0.92}

def explain_fit_score(candidate_id: int, job_id: int) -> dict:
    return {"candidate_id": candidate_id, "job_id": job_id, "important_features": ["skills_overlap", "keywords"]}
