from fastapi import APIRouter
from ...services.utils import parse_resume, parse_job_description

router = APIRouter(prefix="/utils", tags=["utils"])

@router.post("/parse-resume-for-profile")
def parse_resume_for_profile(text: str):
    return parse_resume(text)

@router.post("/parse-job-description")
def parse_job_description_endpoint(text: str):
    return parse_job_description(text)
