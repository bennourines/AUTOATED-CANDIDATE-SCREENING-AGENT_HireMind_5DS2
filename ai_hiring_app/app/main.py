# In app/main.py
print("--- RUNNING LATEST main.py (WITH ADVANCED PARSER AND SIMPLE AUTH) ---")

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Hiring App - Simple Auth", version="1.1.0") # Version bump

origins = ["http://localhost:3000", "http://localhost:3001", "*"] # Added wildcard for safety
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =================================================================
# NEW SCHEMA - Required for the advanced parser endpoint
# =================================================================
class ParsedResumeData(schemas.BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    current_title: Optional[str] = None
    experience: Optional[str] = None
    skills: List[str] = []
    education: Optional[str] = None
    professional_summary: Optional[str] = None

# =================================================================
# ENDPOINTS
# =================================================================

@app.post("/utils/parse-resume-for-profile", response_model=ParsedResumeData, tags=["Utilities"])
async def parse_resume_for_profile(file: UploadFile = File(...)):
    """
    (ADVANCED PARSER) Parses a resume and returns the extracted data as JSON
    without saving it to the database.
    """
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF or DOCX.")
        
    file_bytes = await file.read()
    
    try:
        # This now correctly calls the advanced parser in utils.py
        parsed_data = utils.parse_resume(file_bytes, file.filename)
        if "error" in parsed_data:
            raise HTTPException(status_code=400, detail=parsed_data["error"])
        return parsed_data
    except Exception as e:
        print(f"Error parsing resume for profile: {e}")
        # Make sure to import traceback at the top of the file to see the full error
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to parse resume.")

# --- AUTHENTICATION (SIMPLE) ---
@app.post("/users/register", response_model=schemas.User, tags=["Authentication"])
def create_user_simple(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, password=user.password, role=user.role)
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user
    
@app.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_simple(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = f"simple-token-for-{user.email}-role-{user.role}"
    return {"access_token": access_token, "token_type": "bearer"}

# --- JOBS ---
@app.post("/jobs/", response_model=schemas.Job, tags=["Jobs"])
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(**job.model_dump())
    db.add(db_job); db.commit(); db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=List[schemas.Job], tags=["Jobs"])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@app.get("/jobs/{job_id}", response_model=schemas.Job, tags=["Jobs"])
def get_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

# --- CANDIDATES ---
@app.post("/jobs/{job_id}/upload_resume/", response_model=schemas.CandidateProfile, tags=["Candidates"])
async def upload_resume(job_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    file_bytes = await file.read()
    
    # NOTE: This endpoint still uses the advanced parser. 
    # This is good because it ensures consistency.
    parsed_data = utils.parse_resume(file_bytes, file.filename)
    
    if "error" in parsed_data or not parsed_data.get("email"):
        raise HTTPException(status_code=400, detail="Could not parse resume or find an email.")
    
    existing_candidate = db.query(models.Candidate).filter(models.Candidate.email == parsed_data["email"], models.Candidate.job_id == job_id).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="Candidate has already applied for this job.")
    
    db_candidate = models.Candidate(**parsed_data, job_id=job_id)
    db.add(db_candidate); db.commit(); db.refresh(db_candidate)
    return db_candidate

@app.get("/jobs/{job_id}/candidates/rank", response_model=List[schemas.CandidateProfile], tags=["Candidates"])
def get_ranked_candidates_for_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_candidates = db.query(models.Candidate).filter(models.Candidate.job_id == job_id).all()
    for candidate in job_candidates:
        candidate.match_score = utils.calculate_match_score(candidate.skills, db_job.required_skills)
    job_candidates.sort(key=lambda x: x.match_score, reverse=True)
    return job_candidates

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "AI Hiring Management App API is running!"}