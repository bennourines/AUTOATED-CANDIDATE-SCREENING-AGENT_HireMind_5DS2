from pydantic import BaseModel, Field, ConfigDict 
from typing import List, Optional

class JobCreate(BaseModel):
    title: str = Field(..., example="Senior Python Developer")
    description: str = Field(..., example="We are looking for a developer with experience in FastAPI and AWS.")
    required_skills: List[str] = Field(..., example=["Python", "FastAPI", "AWS", "SQL"])

    
class Job(JobCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

  

class CandidateProfile(BaseModel):
    name: Optional[str] = Field(None, example="Jane Doe")
    email: Optional[str] = Field(None, example="jane.doe@example.com")
    skills: List[str] = Field([], example=["Python", "Machine Learning"])
    raw_text: Optional[str] = Field(None, example="Experienced Python developer...")
    match_score: Optional[int] = Field(None, example=95) # <-- ADD THIS LINE
    model_config = ConfigDict(from_attributes=True)