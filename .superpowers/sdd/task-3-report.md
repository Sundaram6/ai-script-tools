# Task 3: Refactor Monologue Generator to Use Shared Client

**Status:** DONE

## Changes Made

1. **Replaced `generate_monologue` function** (lines 212-225) - Now delegates to `generate_json` from `gemini_client.py` with a retry callback for Streamlit UI feedback.

2. **Removed manual JSON cleaning** - Deleted the markdown fence stripping block that was previously at lines 305-309. The shared client handles this internally.

3. **Updated output section** - Changed from using `json.loads()` on raw text to directly using the already-parsed dict returned by the shared client. Changed `raw_text` variable to `data`.

4. **Removed unused import** - Removed `import json` from line 1 since JSON parsing is now handled by the shared client.

5. **Updated error handling** - Replaced `except json.JSONDecodeError` block with a simple `else` clause since the shared client returns `None` on parse errors.

## Files Modified

- `monologue_generator.py`

## Concerns

- None. The shared client handles all JSON parsing, retry logic, and error handling. The monologue generator is now a thin wrapper.
