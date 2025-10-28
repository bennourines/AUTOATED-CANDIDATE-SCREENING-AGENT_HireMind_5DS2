from typing import Optional, List
from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    description: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobRead(JobBase):
    id: int
    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class CandidateCreate(CandidateBase):
    resume_text: Optional[str] = None

class CandidateRead(CandidateBase):
    id: int
    job_id: int
    resume_text: Optional[str] = None
    shortlisted: bool
    decision: Optional[str] = None
    class Config:
        from_attributes = True

class ScoreRead(BaseModel):
    candidate_id: int
    job_id: int
    score: float

class Recommendation(BaseModel):
    candidate_id: int
    job_id: int
    reason: str
