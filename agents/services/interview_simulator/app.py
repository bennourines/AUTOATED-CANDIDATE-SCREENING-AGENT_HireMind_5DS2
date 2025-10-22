"""
Interview Simulator FastAPI Application.

Endpoints:
- POST /start_session: Start new interview session
- POST /submit_answer: Upload audio/video answer
- GET /session/{session_id}: Get session status
- GET /health: Health check
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import logging
import uuid
from pathlib import Path
import time
from datetime import datetime
import shutil
from typing import Optional

# Import our custom modules
from .models import (
    SessionStartRequest,
    SessionStartResponse,
    QuestionResponse,
    AnswerEvaluation,
    ProsodyMetrics,
    StressMetrics,
    EmotionResult,
    SessionSummary,
    ErrorResponse
)
from .qa_bank import question_bank
from .stt_handler import stt_handler
from .prosody_analyzer import prosody_analyzer
from .stress_analyzer import stress_analyzer
from .emotion_detector import emotion_detector
from .evaluator import answer_evaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Interview Simulator API",
    description="AI-powered interview practice with emotion and stress analysis",
    version="1.0.0"
)

# In-memory session storage (in production, use Redis or database)
sessions = {}

# Upload directory
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {"status": "healthy", "service": "interview_simulator"}

@app.post("/start_session", response_model=SessionStartResponse)
async def start_session(request: SessionStartRequest):
    """
    Start a new interview session.
    
    Args:
        request: Session configuration (categories, difficulty, num_questions)
        
    Returns:
        Session ID and first question
    """
    logger.info(f"Starting new session: {request.dict()}")
    
    # Generate unique session ID
    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    
    # Get random questions based on filters
    questions = question_bank.get_random_questions(
        num_questions=request.num_questions,
        categories=request.categories,
        difficulty=request.difficulty
    )
    
    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found matching the criteria"
        )
    
    # Store session
    sessions[session_id] = {
        "session_id": session_id,
        "questions": questions,
        "current_index": 0,
        "answers": [],
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    
    # Return first question
    first_question = questions[0]
    
    return SessionStartResponse(
        session_id=session_id,
        total_questions=len(questions),
        current_question=QuestionResponse(**first_question)
    )

@app.post("/submit_answer", response_model=AnswerEvaluation)
async def submit_answer(
    session_id: str = Form(...),
    question_id: int = Form(...),
    response_time: Optional[float] = Form(None),
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None)
):
    """
    Submit an answer (audio or video).
    
    Args:
        session_id: Active session ID
        question_id: Question being answered
        response_time: Time taken to answer (seconds)
        audio: Audio file upload (optional if video provided)
        video: Video file upload (optional if audio provided)
        
    Returns:
        Complete answer evaluation with scores and feedback
    """
    start_time = time.time()
    
    logger.info(f"Processing answer: session={session_id}, question={question_id}")
    
    # Validate session
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    # Validate at least one file is provided
    if not audio and not video:
        raise HTTPException(
            status_code=400,
            detail="Either audio or video file must be provided"
        )
    
    # Get question from Q&A bank
    question = question_bank.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Save uploaded file
    if video:
        file_path = UPLOAD_DIR / f"{session_id}_{question_id}_{video.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(video.file, f)
        logger.info(f"Video saved: {file_path}")
        is_video = True
    else:
        file_path = UPLOAD_DIR / f"{session_id}_{question_id}_{audio.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)
        logger.info(f"Audio saved: {file_path}")
        is_video = False
    
    try:
        # =====================================================================
        # STEP 1: Extract audio from video if needed
        # =====================================================================
        if is_video:
            logger.info("Extracting audio from video...")
            audio_path = stt_handler.extract_audio_from_video(str(file_path))
        else:
            audio_path = str(file_path)
        
        # =====================================================================
        # STEP 2: Speech-to-text
        # =====================================================================
        logger.info("Running speech-to-text...")
        transcript = stt_handler.transcribe_audio(audio_path)
        
        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="No speech detected in audio"
            )
        
        logger.info(f"Transcript: {transcript[:100]}...")
        
        # =====================================================================
        # STEP 3: Prosody analysis
        # =====================================================================
        logger.info("Analyzing prosody...")
        prosody_metrics_dict = prosody_analyzer.analyze(audio_path, transcript)
        prosody_metrics = ProsodyMetrics(**prosody_metrics_dict)
        
        # =====================================================================
        # STEP 4: Voice stress analysis
        # =====================================================================
        logger.info("Analyzing voice stress...")
        stress_metrics_dict = stress_analyzer.analyze(audio_path)
        stress_metrics = StressMetrics(**stress_metrics_dict)
        
        # =====================================================================
        # STEP 5: Emotion detection (video only)
        # =====================================================================
        emotion_timeline = None
        if is_video:
            logger.info("Detecting emotions from video...")
            emotion_results = emotion_detector.analyze_video(str(file_path))
            emotion_timeline = [EmotionResult(**e) for e in emotion_results]
        
        # =====================================================================
        # STEP 6: Evaluate answer
        # =====================================================================
        logger.info("Evaluating answer...")
        evaluation = answer_evaluator.evaluate_answer(
            question=question,
            transcript=transcript,
            prosody_metrics=prosody_metrics_dict,
            stress_metrics=stress_metrics_dict,
            emotion_timeline=emotion_results if is_video else None
        )
        
        # =====================================================================
        # STEP 7: Store answer in session
        # =====================================================================
        session['answers'].append({
            "question_id": question_id,
            "transcript": transcript,
            "scores": evaluation,
            "timestamp": datetime.now().isoformat()
        })
        
        # Move to next question
        session['current_index'] += 1
        if session['current_index'] >= len(session['questions']):
            session['completed'] = True
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Build response
        return AnswerEvaluation(
            session_id=session_id,
            question_id=question_id,
            question_text=question['question'],
            transcript=transcript,
            relevance_score=evaluation['relevance_score'],
            clarity_score=evaluation['clarity_score'],
            overall_score=evaluation['overall_score'],
            prosody_metrics=prosody_metrics,
            stress_metrics=stress_metrics,
            emotion_timeline=emotion_timeline,
            feedback=evaluation['feedback'],
            processing_time=round(processing_time, 2)
        )
    
    except Exception as e:
        logger.error(f"Error processing answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temporary files (optional - comment out for debugging)
        # file_path.unlink(missing_ok=True)
        # if is_video and Path(audio_path).exists():
        #     Path(audio_path).unlink(missing_ok=True)
        pass

@app.get("/session/{session_id}", response_model=SessionSummary)
async def get_session(session_id: str):
    """
    Get session status and summary.
    
    Args:
        session_id: Session ID to retrieve
        
    Returns:
        Session summary with statistics
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    # Calculate average score
    scores = [ans['scores']['overall_score'] for ans in session['answers']]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    # Calculate total duration
    if session['answers']:
        start_time = datetime.fromisoformat(session['created_at'])
        end_time = datetime.fromisoformat(session['answers'][-1]['timestamp'])
        duration = (end_time - start_time).total_seconds()
    else:
        duration = 0.0
    
    return SessionSummary(
        session_id=session_id,
        total_questions=len(session['questions']),
        questions_answered=len(session['answers']),
        average_score=round(avg_score, 1),
        total_duration=round(duration, 1),
        completed=session['completed']
    )

@app.get("/next_question/{session_id}", response_model=QuestionResponse)
async def get_next_question(session_id: str):
    """
    Get next question in the session.
    
    Args:
        session_id: Active session ID
        
    Returns:
        Next question or error if session completed
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if session['completed']:
        raise HTTPException(
            status_code=400,
            detail="Session already completed"
        )
    
    current_idx = session['current_index']
    if current_idx >= len(session['questions']):
        raise HTTPException(status_code=400, detail="No more questions")
    
    question = session['questions'][current_idx]
    return QuestionResponse(**question)

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc)
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )

# =============================================================================
# STARTUP/SHUTDOWN
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("🚀 Interview Simulator starting up...")
    logger.info(f"Loaded {question_bank.get_total_questions()} questions")
    logger.info("✅ Ready to accept requests")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("👋 Interview Simulator shutting down...")
    # Clean up temporary files
    for file in UPLOAD_DIR.glob("*"):
        file.unlink()
    logger.info("✅ Cleanup complete")