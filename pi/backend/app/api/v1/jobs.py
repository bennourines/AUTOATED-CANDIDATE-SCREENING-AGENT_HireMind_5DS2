from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import Base, engine, get_db
from ... import models
from ... import schemas

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@router.post("", response_model=schemas.JobRead)
def create_job(payload: schemas.JobCreate, db: Session = Depends(get_db)):
    job = models.Job(title=payload.title, description=payload.description)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("", response_model=list[schemas.JobRead])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@router.get("/{job_id}", response_model=schemas.JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
