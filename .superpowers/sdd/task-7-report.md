# Task 7: Add Input Validation — Report

## What Changed

Added a `validate_input()` helper function to both apps that validates required, min_length, and max_length constraints. Applied validation to the generate button handlers with appropriate minimum lengths.

## Files Modified

- `monologue_generator.py` — Added `validate_input()` helper; replaced bare `not situation` / `not spoken_to` checks with `validate_input(situation)` (min 10 chars) and `validate_input(spoken_to, min_length=3)`.
- `script generator.py` — Added `validate_input()` helper; replaced `not user_request` check with `validate_input(user_request)` (min 10 chars).

## Validation Rules

| App | Field | Min Length | Max Length |
|-----|-------|-----------|-----------|
| Monologue Generator | `situation` | 10 | 500 |
| Monologue Generator | `spoken_to` | 3 | 500 |
| Script Generator | `user_request` | 10 | 500 |

## Concerns

None. Both apps already had basic empty-field checks; this replaces them with structured validation that returns user-friendly error messages.
