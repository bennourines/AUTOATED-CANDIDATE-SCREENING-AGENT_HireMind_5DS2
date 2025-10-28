from fastapi import APIRouter
from ...services.fairness import compute_fairness_metrics, explain_fit_score

router = APIRouter(tags=["fairness"])

@router.get("/jobs/{job_id}/fairness-metrics")
def fairness_metrics(job_id: int):
    return compute_fairness_metrics(job_id)

@router.get("/explain/fit-score/{candidate_id}/{job_id}")
def explain(candidate_id: int, job_id: int):
    return explain_fit_score(candidate_id, job_id)
