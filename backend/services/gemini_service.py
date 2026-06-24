"""Generator layer for monologue generation using Gemini API."""

import time
from backend.services.gemini_client import generate_json
from backend.config import settings

def generate_monologue(
    prompt: str,
    model: str = "gemini-2.5-flash",
    temperature: float = 1.2,
    system_instruction: str = "You are a professional monologue writer.",
) -> dict:
    """Generate a monologue using the Gemini API.

    Args:
        prompt: The user prompt for monologue generation.
        model: Model identifier (default: 'gemini-2.5-flash').
        temperature: Sampling temperature 0.0-2.0 (default: 1.2).
        system_instruction: System prompt for the model.

    Returns:
        Dict with 'success' key. If success, includes 'content' with
        the generated text. If failure, includes 'error' message.
    """
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            result = generate_json(
                api_key=settings.GEMINI_API_KEY,
                model=model,
                temperature=temperature,
                system_instruction=system_instruction,
                prompt=prompt,
                max_retries=1  # We handle the retry loop here for broader coverage
            )

            if result is not None:
                return {
                    "success": True,
                    "content": result,
                }
            
            # If result is None, the client failed gracefully
            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            
            return {
                "success": False,
                "error": "Our AI writers are currently unavailable. Please try again later.",
            }

        except Exception:
            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt)
                continue
            return {
                "success": False,
                "error": "An unexpected error occurred while generating the monologue. Please try again later.",
            }
    
    return {
        "success": False,
        "error": "Failed to connect to the AI service after multiple attempts. Please check back later.",
    }

def regenerate_monologue(
    prompt: str,
    model: str = "gemini-2.5-flash",
) -> dict:
    # Slightly higher temperature for regeneration for more variation
    return generate_monologue(
        prompt=prompt,
        model=model,
        temperature=1.5
    )
