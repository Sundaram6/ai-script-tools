from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database.models import Generation

def get_analytics_summary(db: Session) -> dict:
    total_generations = db.query(func.count(Generation.id)).scalar() or 0
    
    avg_time = db.query(func.avg(Generation.generation_time)).scalar()
    avg_time_ms = int(avg_time) if avg_time else 0
    
    most_common_age = db.query(Generation.age, func.count(Generation.id).label('qty')).group_by(Generation.age).order_by(func.count(Generation.id).desc()).first()
    most_common_language = db.query(Generation.language, func.count(Generation.id).label('qty')).group_by(Generation.language).order_by(func.count(Generation.id).desc()).first()
    
    return {
        "total_generations": total_generations,
        "average_response_time_ms": avg_time_ms,
        "most_common_age_group": most_common_age[0] if most_common_age else "N/A",
        "most_common_language": most_common_language[0] if most_common_language else "N/A",
        "most_common_theme": "N/A" # Complex to extract from prompt right now, keeping N/A
    }
