from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from backend.database.db import Base

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Inputs
    gender = Column(String(50))
    age = Column(String(50))
    language = Column(String(50))
    prompt = Column(Text)
    
    # Outputs
    character_name = Column(String(255))
    monologue = Column(Text)
    acting_notes = Column(Text)
    similar_characters = Column(Text)
    
    # Analytics
    generation_time = Column(Integer)  # in milliseconds
