from fastapi import APIRouter
from ...services.ai_use_detection import detect_ai_usage_on_resume, detect_ai_usage_on_answer

router = APIRouter(prefix="/ai-detect", tags=["ai-detect"]) 

@router.post("/resume")
def detect_resume(text: str):
    return detect_ai_usage_on_resume(text)

@router.post("/answer")
def detect_answer(text: str):
    return detect_ai_usage_on_answer(text)
