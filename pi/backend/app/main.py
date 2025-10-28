import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.jobs import router as jobs_router
from .api.v1.candidates import router as candidates_router
from .api.v1.scoring import router as scoring_router
from .api.v1.interviews import router as interviews_router
from .api.v1.ai_detect import router as ai_detect_router
from .api.v1.fairness import router as fairness_router
from .api.v1.utils import router as utils_router

app = FastAPI(title="Unified Hiring Platform API", version="1.0.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router, prefix="/api/v1")
app.include_router(candidates_router, prefix="/api/v1")
app.include_router(scoring_router, prefix="/api/v1")
app.include_router(interviews_router, prefix="/api/v1")
app.include_router(ai_detect_router, prefix="/api/v1")
app.include_router(fairness_router, prefix="/api/v1")
app.include_router(utils_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
