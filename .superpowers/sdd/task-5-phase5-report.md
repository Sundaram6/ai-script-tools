# Task 5: Smart Generation Engine — Phase 5 Report

## What Changed

1. **prompts.py** — Added new function `build_smart_monologue_prompt(gender, age, language)` that generates a prompt for AI to auto‑choose character details, situation, conflict, emotion, and archetype.

2. **app.py** — Updated import to include `build_smart_monologue_prompt`. Modified the generate‑button logic to check if the `situation` field is empty (after stripping whitespace).  
   - If empty → use smart generation (user provided only gender, age, language).  
   - If non‑empty → validate all inputs and use the full `build_monologue_prompt`.

## Prompt Logic

- **Detection**: `situation_filled = inputs["situation"].strip()`. Empty string triggers smart mode.
- **Smart prompt**: Instructs the AI to choose the most compelling character, situation, and emotional journey. Returns the same JSON structure as the full prompt, ensuring compatibility with existing parser.
- **Full prompt**: Unchanged; requires all advanced fields (including situation and spoken_to).

## Concerns

1. **Medium selection**: The smart prompt asks the AI to “choose the most appropriate medium,” while the full prompt hard‑codes the medium. This is intentional — smart mode lets the AI decide, which may produce more varied results.

2. **Validation bypass**: When situation is empty, validation is skipped entirely. This is correct because smart mode does not require the user to fill advanced fields.

3. **Backward compatibility**: The JSON response structure is identical, so existing parsing and rendering components work without changes.

4. **User expectation**: Users who fill some advanced fields but leave situation empty will still get smart generation. This matches the requirement “user only provides Gender + Age.” If they want to use advanced fields, they must also provide a situation.

## Verification

- Both `prompts.py` and `app.py` pass `python -m py_compile` without errors.
- No other files were modified.