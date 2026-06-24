import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Generation
from backend.schemas.request import GenerationRequest
from backend.schemas.response import GenerationResponse
from backend.services.prompt_service import build_monologue_prompt, build_smart_monologue_prompt
from backend.services.gemini_service import generate_monologue, regenerate_monologue
from backend.services.cache_service import get_cached_response, set_cached_response

router = APIRouter()

@router.post("/generate", response_model=GenerationResponse)
async def api_generate_monologue(req: GenerationRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    if req.archetype and req.emotion and req.situation and req.medium:
        prompt = build_monologue_prompt(
            archetype=req.archetype,
            emotion=req.emotion,
            age_range=req.age,
            medium=req.medium,
            intensity=8,
            situation=req.situation,
            spoken_to="Someone",
            language=req.language,
            word_count=int(req.word_count) if req.word_count else 150
        )
    else:
        prompt = build_smart_monologue_prompt(
            gender=req.gender,
            age=req.age,
            language=req.language
        )
        
    cached = get_cached_response(prompt)
    if cached:
        return GenerationResponse(**cached)
        
    result = generate_monologue(prompt)
    
    if not result["success"]:
        return GenerationResponse(success=False, error=result.get("error"))
        
    content = result["content"]
    generation_time_ms = int((time.time() - start_time) * 1000)
    
    db_gen = Generation(
        gender=req.gender,
        age=req.age,
        language=req.language,
        prompt=prompt,
        character_name=content.get("character_profile", {}).get("name", ""),
        monologue=content.get("monologue", {}).get("text", ""),
        acting_notes=str(content.get("performance_notes", {})),
        generation_time=generation_time_ms
    )
    db.add(db_gen)
    db.commit()
    db.refresh(db_gen)
    
    response_data = {
        "success": True,
        "character_name": db_gen.character_name,
        "monologue": db_gen.monologue,
        "acting_notes": db_gen.acting_notes,
        "generation_id": db_gen.id,
        "content": content
    }
    
    set_cached_response(prompt, response_data)
    
    return GenerationResponse(**response_data)

@router.post("/regenerate", response_model=GenerationResponse)
async def api_regenerate_monologue(req: GenerationRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    if req.archetype and req.emotion and req.situation and req.medium:
        prompt = build_monologue_prompt(
            archetype=req.archetype,
            emotion=req.emotion,
            age_range=req.age,
            medium=req.medium,
            intensity=8,
            situation=req.situation,
            spoken_to="Someone",
            language=req.language,
            word_count=int(req.word_count) if req.word_count else 150
        )
    else:
        prompt = build_smart_monologue_prompt(
            gender=req.gender,
            age=req.age,
            language=req.language
        )
    
    result = regenerate_monologue(prompt)
    
    if not result["success"]:
        return GenerationResponse(success=False, error=result.get("error"))
        
    content = result["content"]
    generation_time_ms = int((time.time() - start_time) * 1000)
    
    db_gen = Generation(
        gender=req.gender,
        age=req.age,
        language=req.language,
        prompt=prompt,
        character_name=content.get("character_profile", {}).get("name", ""),
        monologue=content.get("monologue", {}).get("text", ""),
        acting_notes=str(content.get("performance_notes", {})),
        generation_time=generation_time_ms
    )
    db.add(db_gen)
    db.commit()
    db.refresh(db_gen)
    
    response_data = {
        "success": True,
        "character_name": db_gen.character_name,
        "monologue": db_gen.monologue,
        "acting_notes": db_gen.acting_notes,
        "generation_id": db_gen.id,
        "content": content
    }
    
    return GenerationResponse(**response_data)
