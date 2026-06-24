"""Generator layer for monologue generation using Gemini API."""

from gemini_client import generate_json


def generate_monologue(
    prompt: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
    temperature: float = 1.2,
    system_instruction: str = "You are a professional monologue writer.",
) -> dict:
    """Generate a monologue using the Gemini API.

    Args:
        prompt: The user prompt for monologue generation.
        api_key: Gemini API key.
        model: Model identifier (default: 'gemini-2.5-flash').
        temperature: Sampling temperature 0.0-2.0 (default: 1.2).
        system_instruction: System prompt for the model.

    Returns:
        Dict with 'success' key. If success, includes 'content' with
        the generated text. If failure, includes 'error' message.
    """
    try:
        result = generate_json(
            api_key=api_key,
            model=model,
            temperature=temperature,
            system_instruction=system_instruction,
            prompt=prompt,
        )

        if result is None:
            return {
                "success": False,
                "error": "Failed to generate response. Please try again.",
            }

        return {
            "success": True,
            "content": result,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}",
        }
