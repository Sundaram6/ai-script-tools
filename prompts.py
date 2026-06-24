"""Prompt builder for monologue generation with Gemini."""


def build_monologue_prompt(
    archetype: str,
    emotion: str,
    age_range: str,
    medium: str,
    intensity: int,
    situation: str,
    spoken_to: str,
    language: str,
    word_count: int,
    extra_instructions: str = "",
) -> str:
    """Build a structured prompt for monologue generation.

    Args:
        archetype: Character archetype description.
        emotion: Dominant emotion for the monologue.
        age_range: Actor age range (e.g. "18-25", "25-35").
        medium: Performance medium (Film, OTT, Theatre).
        intensity: Emotional intensity from 1-10.
        situation: What just happened before the monologue begins.
        spoken_to: Who the character is speaking to.
        language: Language/style (Hindi Film, English Theatre, Hinglish).
        word_count: Target word count for the monologue.
        extra_instructions: Optional additional notes or requirements.

    Returns:
        A structured prompt string for Gemini.
    """
    extra_section = f"\nExtra instructions: {extra_instructions}" if extra_instructions else ""

    return f"""Write an audition-ready monologue with these exact parameters:

Character archetype: {archetype}
Character Age Range: {age_range}
Performance medium: {medium}
Emotional intensity: {intensity}/10
Dominant emotion: {emotion}
Situation (what just happened): {situation}
Speaking to: {spoken_to}
Target length: approximately {word_count} words
Language style: {language}{extra_section}

The monologue must have a clear arc — the character must be in a different emotional place at the end than at the start.
Include one unexpected moment — a beat where the emotion shifts or the character surprises themselves.

Return ONLY valid JSON in this exact structure:
{{
  "character_profile": {{
    "name": "A fitting name for this character",
    "age": "Age as a number",
    "background": "Two to three sentences — who this person is, where they come from, and what they carry",
    "core_desire": "What this character wants more than anything",
    "biggest_fear": "What they are most afraid of losing or facing"
  }},
  "character_breakdown": {{
    "objective": "What does this character want more than anything in this moment?",
    "obstacle": "What is stopping them from getting it — internal or external?",
    "stakes": "What happens if they fail? What do they lose?",
    "secret": "Something the character is hiding or hasn't admitted to themselves",
    "animal_reference": "An animal that captures this character's essence and why",
    "five_defining_traits": ["Trait 1", "Trait 2", "Trait 3", "Trait 4", "Trait 5"]
  }},
  "monologue": {{
    "text": "The full monologue text here — natural, emotionally layered, no clichés, no copyrighted content",
    "is_audition_ready": true,
    "has_natural_dialogue": true,
    "is_emotionally_layered": true,
    "no_cliches": true,
    "no_copyrighted_content": true,
    "suitable_for_medium": "{medium}"
  }},
  "emotional_beats": {{
    "beat_1": "Opening emotion and what triggers it",
    "beat_2": "First shift or escalation",
    "beat_3": "The turning point — where everything changes",
    "beat_4": "The aftermath or realization",
    "beat_5": "Final emotional state — where the character lands"
  }},
  "performance_notes": {{
    "voice": "Tone, pitch, volume changes throughout the monologue",
    "pacing": "Speed variations — where to rush, where to slow down, where to pause",
    "body_language": "Physical choices — posture, gestures, movement",
    "eye_focus": "Where the character looks — at whom, at what, into space",
    "breathing_notes": "How breath supports the emotion — shallow, deep, held, shaky"
  }}
}}"""


def build_smart_monologue_prompt(
    gender: str,
    age: str,
    language: str,
) -> str:
    """Build a smart generation prompt when user only provides gender, age, and language.
    
    The AI automatically chooses character details, situation, conflict, emotion, and archetype.
    
    Args:
        gender: Character gender (Male/Female).
        age: Age range label (Child/Teen/Young Adult/Adult/Senior).
        language: Language style (Hindi/English/Hinglish).
    
    Returns:
        A structured prompt string for Gemini.
    """
    return f"""Generate the most emotionally powerful, audition-worthy monologue for:

Gender: {gender}
Age: {age}
Language: {language}

Choose the most compelling character, situation and emotional journey yourself.

The monologue should be original, audition-ready, and emotionally layered.

Return ONLY valid JSON in this exact structure:
{{
  "character_profile": {{
    "name": "A fitting name for this character",
    "age": "Age as a number",
    "background": "Two to three sentences — who this person is, where they come from, and what they carry",
    "core_desire": "What this character wants more than anything",
    "biggest_fear": "What they are most afraid of losing or facing"
  }},
  "character_breakdown": {{
    "objective": "What does this character want more than anything in this moment?",
    "obstacle": "What is stopping them from getting it — internal or external?",
    "stakes": "What happens if they fail? What do they lose?",
    "secret": "Something the character is hiding or hasn't admitted to themselves",
    "animal_reference": "An animal that captures this character's essence and why",
    "five_defining_traits": ["Trait 1", "Trait 2", "Trait 3", "Trait 4", "Trait 5"]
  }},
  "monologue": {{
    "text": "The full monologue text here — natural, emotionally layered, no clichés, no copyrighted content",
    "is_audition_ready": true,
    "has_natural_dialogue": true,
    "is_emotionally_layered": true,
    "no_cliches": true,
    "no_copyrighted_content": true,
    "suitable_for_medium": "Choose the most appropriate medium for this character"
  }},
  "emotional_beats": {{
    "beat_1": "Opening emotion and what triggers it",
    "beat_2": "First shift or escalation",
    "beat_3": "The turning point — where everything changes",
    "beat_4": "The aftermath or realization",
    "beat_5": "Final emotional state — where the character lands"
  }},
  "performance_notes": {{
    "voice": "Tone, pitch, volume changes throughout the monologue",
    "pacing": "Speed variations — where to rush, where to slow down, where to pause",
    "body_language": "Physical choices — posture, gestures, movement",
    "eye_focus": "Where the character looks — at whom, at what, into space",
    "breathing_notes": "How breath supports the emotion — shallow, deep, held, shaky"
  }}
}}"""
