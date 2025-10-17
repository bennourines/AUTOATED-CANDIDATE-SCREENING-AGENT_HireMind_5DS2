# In app/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class JobBase(BaseModel): title: str; description: str; required_skills: List[str]
class JobCreate(JobBase): pass
class Job(JobBase): # REMOVING hiring_manager_id
    id: int; model_config = ConfigDict(from_attributes=True)

# ... (the rest of the schemas: Candidate, User, Token can remain the same as the 'simple auth' version)
class CandidateBase(BaseModel): name: Optional[str] = None; email: Optional[str] = None; skills: List[str] = []; raw_text: Optional[str] = None
class CandidateProfile(CandidateBase): id: int; job_id: int; status: str; match_score: Optional[int] = None; model_config = ConfigDict(from_attributes=True)
class UserBase(BaseModel): email: str; role: str
class UserCreate(UserBase): password: str
class User(UserBase): id: int; model_config = ConfigDict(from_attributes=True)
class Token(BaseModel): access_token: str; token_type: str
class TokenData(BaseModel): email: Optional[str] = None
class ProfileCompleteData(BaseModel):
    full_name: str
    email: str
    password: str
    skills: List[str]