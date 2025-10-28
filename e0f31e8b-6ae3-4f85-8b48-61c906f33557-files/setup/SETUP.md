Unified App Setup (Windows 10 friendly)

Prerequisites
- Python 3.10.x
- Node.js 18+ (Node 20 recommended)
- Git (optional)

Environment variables
Backend
- DATABASE_URL (default: sqlite:///./app.db)
- HUGGINGFACE_API_KEY (optional)
- CORS_ORIGINS (default: http://localhost:3000)

Frontend
- REACT_APP_API_BASE (default: http://localhost:8000/api/v1)

Backend setup
1) Open Windows Terminal (PowerShell)
2) Create and activate venv
   python -m venv .venv
   .\.venv\Scripts\activate
3) Install deps
   pip install -r requirements.txt
4) Run API
   uvicorn backend.app.main:app --reload --port 8000
5) Test
   curl http://localhost:8000/health

Frontend setup
1) Open a new terminal in frontend/
2) Install deps
   npm install
3) Start dev server
   npm start

Directory structure
backend/
  app/
    main.py
    database.py, models.py, schemas.py
    services/
      utils.py, matching_engine.py, interview_analytics.py, hr_question_recommender.py,
      ai_use_detection.py, fairness.py, feedback.py, dedup_shortlist.py, data_loader.py
    api/
      v1/
        jobs.py, candidates.py, scoring.py, interviews.py, ai_detect.py, fairness.py, utils.py
frontend/
  src/ (App.js, components/, pages/, layouts/)
  public/index.html
requirements.txt
setup/
  env/, scripts/, postman/

Migration notes
- Single FastAPI entrypoint at backend/app/main.py
- All endpoints consolidated under /api/v1 routers
- Matching and resume parsing centralized in services/
- React frontend standardized under frontend/ with one App.js and central API base (src/api.js)
- If you had older multiple main.py files, point any external launch scripts to backend.app.main:app

Windows tips
- If uvicorn fails on port in use, change --port 8001 and update REACT_APP_API_BASE accordingly
- For PowerShell: set env vars per-session like $env:REACT_APP_API_BASE = "http://localhost:8000/api/v1"
