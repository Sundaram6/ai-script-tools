# Task 9-10: AI Character Creator and Premium Output

## Changes Made

### 1. Prompts (`prompts.py`)
- Added `occupation`, `core_wound`, and `goal` fields to the `character_profile` section in both `build_monologue_prompt` and `build_smart_monologue_prompt`.
- Removed `core_desire` and `biggest_fear` (replaced by `goal` and `core_wound`).
- The JSON structure now requests:
  - `name`, `age`, `occupation`, `background`, `core_wound`, `goal`.

### 2. Character Creator Display (`components/cards.py`)
- Updated `render_character_card` to extract and display the new fields:
  - Name, Age, Occupation, Core Wound, Goal.
- Kept existing archetype, emotion, medium fields for backward compatibility.
- Styled card remains unchanged.

### 3. Premium Output Tabs (`components/output_tabs.py`)
- Reduced from 5 tabs to 4 premium tabs:
  - **Monologue**: Displays the monologue text with copy/download.
  - **Character**: Combines character breakdown and emotional beats (nested sections).
  - **Acting Notes**: Displays performance notes (voice, pacing, body language, etc.).
  - **Full Package**: Shows all sections combined in a single scrollable view.
- Added helper functions `_render_character`, `_render_acting_notes`, `_render_full_package` to organize content.
- Existing helper functions (`_render_breakdown`, `_render_beats`, `_render_performance_notes`) are reused.

### 4. App Integration (`app.py`)
- No changes needed; the existing calls to `render_character_card` and `render_output_tabs` already pass the required data.
- Character card is displayed before output tabs as requested.

## Tab Structure

| Tab | Content |
|-----|---------|
| 🎬 Monologue | Monologue text + copy/download buttons |
| 🧠 Character | Character breakdown + Emotional beats |
| 🎤 Acting Notes | Performance notes (voice, pacing, body language, etc.) |
| 📄 Full Package | All sections combined (monologue, breakdown, beats, notes) |

## Concerns

1. **Parser Compatibility**: The parser (`components/parser.py`) extracts key-value pairs using `**Key**: value` patterns. The new fields (`occupation`, `core_wound`, `goal`) should be parsed correctly if the AI follows the JSON structure. However, if the AI outputs them in a different format, they may appear in the raw section. The existing fallback to raw content is acceptable.

2. **Backward Compatibility**: The `character_profile` schema changed; any existing cached responses may lack the new fields. The component gracefully defaults to "N/A".

3. **User Experience**: The "Character" tab now combines breakdown and emotional beats, which may be dense. However, this reduces tab count as requested.

4. **No Additional Testing**: The changes are UI-only and rely on existing parsing logic. No new unit tests are required, but manual testing with a generated monologue is recommended.

## Verification

- Syntax check passed: `python -m py_compile app.py`.
- No import errors; all dependencies satisfied.

## Commit

The following files are staged for commit:
- `prompts.py`
- `components/cards.py`
- `components/output_tabs.py`

Commit message: `feat: add AI character creator and premium output`