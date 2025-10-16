# =================================================================
# SECTION 1: IMPORTS
# =================================================================
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  # << -------------------- ADD THIS LINE
from sqlalchemy.orm import Session
from typing import List

# These are your application's internal imports
from . import models, schemas
from .database import engine, get_db
from .ai_modules.resume_parser import parse_resume
from .ai_modules.matching_engine import calculate_match_score


# =================================================================
# SECTION 2: APPLICATION SETUP
# =================================================================

# This command tells SQLAlchemy to create all tables defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Hiring Management App API",
    description="The backend API for the AI-powered hiring application.",
    version="0.1.0",
)

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# START OF NEW CODE BLOCK TO ADD
# This is the CORS configuration. It must be added after `app` is defined.
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

origins = [
    "http://localhost:3000",  # The default address for a React development server
    "http://localhost:3001",  # A common alternative port
    # You can add the addresses of your deployed frontend here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# END OF NEW CODE BLOCK
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =================================================================
# SECTION 3: API ENDPOINTS (No changes below this line)
# =================================================================

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Hiring API"}

@app.post("/jobs/", response_model=schemas.Job, status_code=201)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new job posting and save it to the database.
    """
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=List[schemas.Job])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all job postings from the database.
    """
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

@app.post("/upload/resume/", response_model=schemas.CandidateProfile)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to upload a resume, parse it, and save the candidate to the database.
    """
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF or DOCX.")
        
    file_bytes = await file.read()
    
    try:
        parsed_data = parse_resume(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

    if "error" in parsed_data or not parsed_data.get("email"):
        raise HTTPException(status_code=400, detail="Could not parse resume or find an email.")
    
    existing_candidate = db.query(models.Candidate).filter(models.Candidate.email == parsed_data["email"]).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail=f"Candidate with email {parsed_data['email']} already exists.")

    db_candidate = models.Candidate(**parsed_data)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return schemas.CandidateProfile.model_validate(db_candidate)

@app.get("/jobs/{job_id}/candidates/rank", response_model=List[schemas.CandidateProfile])
def get_ranked_candidates_for_job(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all candidates, calculates their match score for a specific job,
    and returns them ranked from highest score to lowest.
    """
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_skills = db_job.required_skills
    all_candidates = db.query(models.Candidate).all()
    if not all_candidates:
        return []

    for candidate in all_candidates:
        candidate.match_score = calculate_match_score(candidate.skills, job_skills)
    
    all_candidates.sort(key=lambda x: x.match_score, reverse=True)

    return all_candidates