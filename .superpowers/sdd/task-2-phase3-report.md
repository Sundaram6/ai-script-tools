# Task 2 Phase 3 Report: Create generator.py - Gemini API Layer

## What I Created

Created `generator.py` containing the `generate_monologue()` function that wraps the shared `gemini_client.generate_json()` function.

## Function Signature

```python
def generate_monologue(
    prompt: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
    temperature: float = 1.2,
    system_instruction: str = "You are a professional monologue writer.",
) -> dict:
```

## Return Format

Success:
```python
{"success": True, "content": parsed_json_dict}
```

Failure:
```python
{"success": False, "error": "error message"}
```

## Implementation Details

- Imports `generate_json` from `gemini_client.py`
- Wraps the API call with exception handling
- Returns structured success/error response format
- Default model: `gemini-2.5-flash`
- Default temperature: `1.2`
- Handles `None` responses from `generate_json` (parse failures, non-429 errors)

## Concerns

1. **Retry Logic**: The `gemini_client.generate_json()` handles 429 retries internally. The `generator.py` layer does not expose retry status to callers. A future enhancement could add an `on_retry` callback parameter.

2. **System Instruction Default**: The default system instruction is generic. Callers should provide language-specific instructions (e.g., from `SYSTEM_INSTRUCTIONS` in `monologue_generator.py`).

3. **Integration**: The existing `monologue_generator.py` has its own `generate_monologue` function that uses Streamlit's `st.warning` for retry feedback. This new module provides a Streamlit-agnostic alternative for cleaner separation of concerns.
