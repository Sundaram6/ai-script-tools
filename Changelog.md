# Changelog

## v0.6.0 - 24 June 2026

### Added
- One-click generation: Select Age + Gender → Generate
- Smart AI engine that auto-chooses character details
- Character card selectors (Gender, Age, Language)
- Quick preset chips (Broken Heart, Betrayal, Dreamer, etc.)
- Demo mode with sample monologues (no API key required)
- API key persistence in session state
- Collapsible advanced options for power users
- Category tabs (Random, Film, Theatre, OTT)
- AI Character Creator with Name, Age, Occupation, Core Wound, Goal
- Premium output tabs (Monologue, Character, Acting Notes, Full Package)
- History system storing last 10 generations
- PDF download support
- "Generate Another Version" button
- Improved mobile-responsive layout

### Changed
- Simplified UX from 10 fields to 3 essentials (Age, Gender, Language)
- Moved advanced options to collapsible section
- Removed old monolith files (monologue_generator.py, script generator.py)
- Reorganized into components/, services/, utils/ packages

### Removed
- Old monologue_generator.py and script generator.py

---

## v0.5.0 - 24 June 2026

### Added
- Premium component architecture (`components/` directory)
- Hero section with branded header
- Sidebar with grouped inputs (Character, Emotional, Performance sections)
- 5-tab output workspace (Monologue, Character Breakdown, Emotional Beats, Performance Notes, Full Output)
- Smart response parser with section detection
- Character summary card above output
- Monologue reading pane with optimized typography
- Vertical emotional beat visualization with color-coded progression
- Performance notes cards with styled headers
- Copy monologue and copy full output buttons
- TXT download functionality
- Rotating loading messages during generation
- Empty state placeholder before first generation
- Friendly error messages (no raw exceptions)
- Mobile-responsive CSS
- Session memory for last generated result
- Branding footer

### Changed
- Restructured into component-based architecture
- Moved all inputs to sidebar
- Improved output display with tabbed interface

---

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
