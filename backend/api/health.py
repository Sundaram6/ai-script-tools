from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database.db import get_db
from backend.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    
    gemini_status = "ok" if settings.GEMINI_API_KEY else "missing_key"
    
    return {
        "status": "ok" if db_status == "ok" and gemini_status == "ok" else "degraded",
        "database": db_status,
        "gemini": gemini_status,
        "backend": "ok"
    }
