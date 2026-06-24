from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.services.analytics_service import get_analytics_summary

router = APIRouter()

@router.get("/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    return get_analytics_summary(db)
