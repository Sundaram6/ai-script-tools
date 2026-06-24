# Task 1 Phase 3 Report: Create prompts.py - Prompt Builder

## What I Created

Created `prompts.py` containing the `build_monologue_prompt()` function for structured monologue generation.

## Function Signature

```python
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
```

## Output Structure

The prompt requests JSON output with 5 sections:

1. **character_profile** - Name, age, background, core_desire, biggest_fear
2. **character_breakdown** - objective, obstacle, stakes, secret, animal_reference, five_defining_traits
3. **monologue** - text, is_audition_ready, has_natural_dialogue, is_emotionally_layered, no_cliches, no_copyrighted_content, suitable_for_medium
4. **emotional_beats** - beat_1 through beat_5
5. **performance_notes** - voice, pacing, body_language, eye_focus, breathing_notes

## Concerns

1. **Integration**: The existing `monologue_generator.py` still uses the old `build_prompt()` function. A future task should update it to use the new `prompts.py` module.

2. **JSON Schema Validation**: No validation is currently performed on the returned JSON structure. Consider adding schema validation in a future task.

3. **Language-Specific Prompts**: The current implementation uses a generic prompt. The existing `SYSTEM_INSTRUCTIONS` dictionary in `monologue_generator.py` provides language-specific system prompts that work well. The new prompt builder could benefit from incorporating language-specific instructions directly.
