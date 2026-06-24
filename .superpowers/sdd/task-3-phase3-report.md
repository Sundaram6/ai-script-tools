# Task 3: Create utils.py - Safety Layer

**Status:** DONE

## What Was Created

Created `utils.py` with two utility functions for input validation and response cleaning:

1. **validate_inputs()** - Validates all monologue generation input parameters
2. **clean_response()** - Cleans raw API response text by removing markdown artifacts and normalizing formatting

## Function Signatures

```python
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
```

```python
def clean_response(raw_text: str) -> str:
```

## Implementation Details

### validate_inputs()
- Checks that `situation` and `spoken_to` are not empty
- Validates `target_words` is a positive integer
- Ensures `language` is one of the supported values: "Hindi Film", "English Theatre", "Hinglish (Mixed)"
- Returns `True` if all validations pass, `False` otherwise

### clean_response()
- Removes markdown code fences (```json, ```, etc.)
- Removes duplicate headings (case-insensitive comparison)
- Normalizes whitespace (collapses multiple spaces/tabs, limits consecutive newlines)
- Returns cleaned text string

## Tests

Created `test_utils.py` with 9 test cases covering:
- Valid inputs validation
- Empty required fields validation
- Invalid word count validation
- Unsupported language validation
- Markdown artifact removal
- Duplicate heading removal
- Whitespace normalization
- Empty input handling

All tests pass successfully.

## Commit

```
1fef05e feat: add validation and response cleaning utils
```

## Concerns

None. The implementation is straightforward and follows existing project patterns.
