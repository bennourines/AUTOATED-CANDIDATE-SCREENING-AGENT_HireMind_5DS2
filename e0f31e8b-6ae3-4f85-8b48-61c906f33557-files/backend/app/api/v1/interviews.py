from fastapi import APIRouter
from ...services.hr_question_recommender import next_question
from ...services.interview_analytics import analyze_answer

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.post("/start")
def start():
    return {"question": next_question()}

@router.post("/next")
def next():
    return {"question": next_question()}

@router.post("/analyze/answer")
def analyze(answer: str):
    return analyze_answer(answer)
