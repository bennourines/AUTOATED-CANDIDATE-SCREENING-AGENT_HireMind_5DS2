"""
Interview Simulator with Ollama-powered CrewAI integration.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import logging
from pathlib import Path
import shutil
from typing import Optional
import sys
import uuid

# Add agents to path
sys.path.append('../../')

from agents.crews.interview_crew import InterviewCrew
from core.ollama_config import OllamaConfig
from .models import (
    SessionStartRequest,
    SessionStartResponse,
    QuestionResponse
)
from .qa_bank import question_bank

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Interview Crew AI (Ollama)",
    description="Multi-agent interview system powered by Ollama Phi4-Mini",
    version="2.0.0-ollama"
)

# Initialize crew
try:
    interview_crew = InterviewCrew()
    CREW_AVAILABLE = True
except Exception as e:
    logger.error(f"Failed to initialize crew: {e}")
    logger.error("💡 Make sure Ollama is running: ollama serve")
    logger.error("💡 And model is pulled: ollama pull phi4-mini")
    CREW_AVAILABLE = False

sessions = {}
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/health")
async def health_check():
    """Health check with Ollama status."""
    ollama_status = OllamaConfig.check_availability()
    
    return {
        "status": "healthy" if CREW_AVAILABLE else "degraded",
        "service": "interview_crew_ai_ollama",
        "ollama_available": ollama_status,
        "model": OllamaConfig.MODEL_NAME,
        "agents": ["interviewer", "stt", "prosody", "emotion", "evaluator", "summarizer"] if CREW_AVAILABLE else []
    }

@app.post("/start_session", response_model=SessionStartResponse)
async def start_session(request: SessionStartRequest):
    """Start interview session with Ollama-powered question selection."""
    
    if not CREW_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Crew not available. Check Ollama server."
        )
    
    logger.info(f"🚀 Starting Ollama-powered session: {request.dict()}")
    
    try:
        # Use traditional question bank for now
        questions = question_bank.get_random_questions(
            num_questions=request.num_questions,
            categories=request.categories,
            difficulty=request.difficulty
        )
        
        if not questions:
            raise HTTPException(status_code=404, detail="No questions found")
        
        session_id = f"ollama_{uuid.uuid4().hex[:12]}"
        
        sessions[session_id] = {
            "session_id": session_id,
            "questions": questions,
            "current_index": 0,
            "answers": []
        }
        
        return SessionStartResponse(
            session_id=session_id,
            total_questions=request.num_questions,
            current_question=QuestionResponse(**questions[0])
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit_answer")
async def submit_answer(
    session_id: str = Form(...),
    question_id: int = Form(...),
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None)
):
    """Process answer with Ollama crew."""
    
    if not CREW_AVAILABLE:
        raise HTTPException(status_code=503, detail="Crew not available")
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save file
    if video:
        file_path = UPLOAD_DIR / f"{session_id}_{question_id}_{video.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(video.file, f)
        video_path = str(file_path)
        audio_path = None
    elif audio:
        file_path = UPLOAD_DIR / f"{session_id}_{question_id}_{audio.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)
        audio_path = str(file_path)
        video_path = None
    else:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        session = sessions[session_id]
        question = next((q for q in session["questions"] if q["id"] == question_id), None)
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Process with crew
        logger.info("🤖 Processing with Ollama crew...")
        result = await interview_crew.process_answer(
            question=question,
            audio_path=audio_path or video_path,
            video_path=video_path
        )
        
        # Store result
        session["answers"].append({
            "question_id": question_id,
            "evaluation": result["evaluation"]
        })
        
        # Move to next question
        session["current_index"] += 1
        
        return JSONResponse(content={
            "status": "success",
            "result": result,
            "model": "phi4-mini",
            "message": "Processed by Ollama-powered crew"
        })
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session_summary/{session_id}")
async def get_session_summary(session_id: str):
    """Generate final session summary."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    # Generate summary through crew
    summary = await interview_crew.generate_session_summary(session)
    
    return JSONResponse(content=summary)

@app.on_event("startup")
async def startup():
    """Check Ollama on startup."""
    logger.info("🦙 Interview Crew with Ollama Phi4-Mini starting...")
    
    if OllamaConfig.check_availability():
        logger.info(f"✅ Using model: {OllamaConfig.MODEL_NAME}")
        logger.info("✅ All agents ready")
    else:
        logger.warning("⚠️ Ollama not available - some features disabled")
        logger.info("💡 Start Ollama: ollama serve")
        logger.info(f"💡 Pull model: ollama pull {OllamaConfig.MODEL_NAME}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)