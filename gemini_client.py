"""Shared Gemini API client with retry logic and JSON parsing."""

import json
import time
from google import genai
from google.genai import types


def generate_json(
    api_key: str,
    model: str,
    temperature: float,
    system_instruction: str,
    prompt: str,
    max_retries: int = 3,
    on_retry=None,
) -> dict | None:
    """Call Gemini API and return parsed JSON response.

    Args:
        api_key: Gemini API key.
        model: Model identifier (e.g. 'gemini-2.5-flash').
        temperature: Sampling temperature (0.0-2.0).
        system_instruction: System prompt for the model.
        prompt: User prompt.
        max_retries: Maximum retry attempts on 429 errors.
        on_retry: Optional callback(attempt, wait_seconds) for UI feedback.

    Returns:
        Parsed dict from JSON response, or None on error.
    """
    client = genai.Client(api_key=api_key)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                ),
                contents=prompt,
            )
            return _parse_json(response.text)

        except Exception as e:
            if "429" in str(e):
                wait = 30 * (attempt + 1)
                if on_retry:
                    on_retry(attempt, wait)
                time.sleep(wait)
            else:
                return None

    return None


def _parse_json(raw_text: str) -> dict | None:
    """Parse JSON from model response, stripping markdown fences."""
    if not raw_text:
        return None

    clean = raw_text.strip()
    if clean.startswith("```"):
        parts = clean.split("```")
        if len(parts) >= 2:
            clean = parts[1]
            if clean.startswith("json"):
                clean = clean[4:]

    try:
        return json.loads(clean.strip())
    except json.JSONDecodeError:
        return None
