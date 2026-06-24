"""Validation and response cleaning utilities for monologue generation."""

import re

SUPPORTED_LANGUAGES = ["Hindi Film", "English Theatre", "Hinglish (Mixed)"]


def validate_inputs(
    language: str,
    archetype: str,
    emotion: str,
    age_range: str,
    medium: str,
    emotional_intensity: int,
    situation: str,
    spoken_to: str,
    extra: str,
    target_words: int,
) -> bool:
    """Validate all monologue generation inputs.

    Args:
        language: Language/style for the monologue.
        archetype: Character archetype description.
        emotion: Dominant emotion.
        age_range: Actor age range.
        medium: Performance medium.
        emotional_intensity: Emotional intensity from 1-10.
        situation: What just happened before the monologue.
        spoken_to: Who the character is speaking to.
        extra: Optional extra notes.
        target_words: Target word count.

    Returns:
        True if all inputs are valid, False otherwise.
    """
    if not situation or not situation.strip():
        return False

    if not spoken_to or not spoken_to.strip():
        return False

    if not isinstance(target_words, int) or target_words <= 0:
        return False

    if language not in SUPPORTED_LANGUAGES:
        return False

    return True


def clean_response(raw_text: str) -> str:
    """Clean raw API response text.

    Removes markdown artifacts, duplicate headings, and normalizes spacing.

    Args:
        raw_text: Raw text from API response.

    Returns:
        Cleaned text string.
    """
    if not raw_text:
        return ""

    clean = raw_text.strip()

    clean = re.sub(r"```(?:json|text)?\s*", "", clean)
    clean = re.sub(r"```", "", clean)

    lines = clean.split("\n")
    seen_headings = set()
    filtered_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading_text = stripped.lower()
            if heading_text in seen_headings:
                continue
            seen_headings.add(heading_text)
        filtered_lines.append(line)

    clean = "\n".join(filtered_lines)

    clean = re.sub(r"[ \t]+", " ", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean)

    return clean.strip()
