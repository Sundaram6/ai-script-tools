from pydantic import BaseModel
from typing import Optional, Dict, Any

class GenerationResponse(BaseModel):
    success: bool
    character_name: Optional[str] = None
    monologue: Optional[str] = None
    acting_notes: Optional[str] = None
    similar_characters: Optional[str] = None
    generation_id: Optional[int] = None
    content: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
