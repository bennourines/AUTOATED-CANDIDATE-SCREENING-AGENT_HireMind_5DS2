from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models, schemas
from ...services.utils import parse_resume
from ...services.matching_engine import compute_fit_score
from ...services.utils import parse_job_description

router = APIRouter(tags=["candidates"])

@router.post("/jobs/{job_id}/upload_resume", response_model=schemas.CandidateRead)
def upload_resume(job_id: int, file: UploadFile = File(...), name: str = Form(None), email: str = Form(None), db: Session = Depends(get_db)):
    job = db.query(models.Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    content = file.file.read().decode("utf-8", errors="ignore")
    profile = parse_resume(content)
    candidate = models.Candidate(name=name, email=email, resume_text=content, job_id=job_id)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@router.get("/jobs/{job_id}/candidates/rank")
def rank_candidates(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_profile = parse_job_description(job.description or "")
    ranking = []
    for c in job.candidates:
        cand_profile = parse_resume(c.resume_text or "")
        score = compute_fit_score(cand_profile, job_profile)
        ranking.append({"candidate_id": c.id, "name": c.name, "email": c.email, "score": score})
    ranking.sort(key=lambda x: x["score"], reverse=True)
    return {"job_id": job_id, "ranking": ranking}

@router.post("/candidates/{candidate_id}/shortlist", response_model=schemas.CandidateRead)
def shortlist_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate.shortlisted = True
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@router.get("/jobs/{job_id}/shortlisted_candidates", response_model=list[schemas.CandidateRead])
def shortlisted_candidates(job_id: int, db: Session = Depends(get_db)):
    return db.query(models.Candidate).filter(models.Candidate.job_id==job_id, models.Candidate.shortlisted==True).all()

@router.post("/candidates/{candidate_id}/decision", response_model=schemas.CandidateRead)
def decision(candidate_id: int, decision: str = Form(...), db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate.decision = decision
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate
