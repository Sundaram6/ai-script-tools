from pydantic import BaseModel
from typing import Optional

class GenerationRequest(BaseModel):
    gender: str
    age: str
    language: str
    archetype: Optional[str] = None
    emotion: Optional[str] = None
    situation: Optional[str] = None
    medium: Optional[str] = None
    word_count: Optional[str] = None
