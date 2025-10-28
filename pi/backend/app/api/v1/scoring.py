from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models, schemas
from ...services.utils import parse_resume, parse_job_description
from ...services.matching_engine import compute_fit_score

router = APIRouter(prefix="/candidates", tags=["scoring"])

@router.get("/{candidate_id}/fit-score/{job_id}", response_model=schemas.ScoreRead)
def fit_score(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).get(candidate_id)
    job = db.query(models.Job).get(job_id)
    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Not found")
    c_prof = parse_resume(candidate.resume_text or "")
    j_prof = parse_job_description(job.description or "")
    score = compute_fit_score(c_prof, j_prof)
    return {"candidate_id": candidate_id, "job_id": job_id, "score": score}

@router.get("/{candidate_id}/recommendations-24h")
def recommendations(candidate_id: int):
    return {"candidate_id": candidate_id, "recommendations": []}
