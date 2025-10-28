SCR-012 Migration Notes

- Single entrypoint: backend/app/main.py (use uvicorn backend.app.main:app)
- Endpoints moved under /api/v1 with modular routers:
  - jobs, candidates, scoring, interviews, ai-detect, fairness, utils
- Matching logic consolidated in backend/app/services/matching_engine.py
- Resume parsing centralized in backend/app/services/utils.py
- Database setup in backend/app/database.py with SQLAlchemy Base and get_db
- Frontend unified under frontend/ with a single App.js and central API base at src/api.js (uses REACT_APP_API_BASE)
- requirements.txt at repo root with Windows 10 friendly pins
- Deprecated duplicate mains/modules should be removed or updated to import from backend.app
