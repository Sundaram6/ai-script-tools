# Changelog

## v0.4.0 - 24 June 2026

### Added
- New monologue generator app (`app.py`) with 5-section output (Character Profile, Character Breakdown, Monologue, Emotional Beats, Performance Notes)
- Prompt builder module (`prompts.py`) for structured Gemini prompts
- Generator layer (`generator.py`) wrapping Gemini API calls
- Safety utilities (`utils.py`) for input validation and response cleaning
- Tabbed output display (Monologue, Character Breakdown, Performance Notes)
- `.env` file support via python-dotenv

---

## v0.3.0 - 24 June 2026

### Added
- Shared Gemini client module (`gemini_client.py`) with retry logic and JSON parsing
- Unit tests for Gemini client (`gemini_client_test.py`)
- Session history — revisit generated monologues and scenes
- Copy to clipboard button for monologues and scenes
- Download all history as text file
- Input validation for required fields

### Changed
- Refactored both generators to use shared Gemini client
- Removed duplicated API call/retry/parse logic from both apps
- Pinned dependency versions in requirements.txt

### Fixed
- Improved error handling on API failures

---

## v0.2.0 - 20 June 2026

### Added
- Character profile card
- Emotional arc analysis
- Objective breakdown
- Obstacle breakdown
- Subtext analysis
- Given circumstances analysis
- Director notes
- Practice tips
- Improved JSON structure
- Improved UI layout using Streamlit containers

### Changed
- Removed broken HTML character card implementation
- Improved Gemini model selection
- Improved monologue output formatting

---

## v1.0.0 - June 2026

### Added
- Monologue Generator
- Script Generator
- GitHub Repository
- README Documentation
- requirements.txt
- MIT License
