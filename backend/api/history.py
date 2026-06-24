from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Generation

router = APIRouter()

@router.get("/history")
async def get_history(limit: int = 10, db: Session = Depends(get_db)):
    gens = db.query(Generation).order_by(Generation.created_at.desc()).limit(limit).all()
    return [{
        "id": g.id,
        "created_at": g.created_at.isoformat() if g.created_at else None,
        "gender": g.gender,
        "age": g.age,
        "language": g.language,
        "character_name": g.character_name,
        "monologue": g.monologue,
        "acting_notes": g.acting_notes
    } for g in gens]
