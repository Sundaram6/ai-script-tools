# Task 6: Add Copy Button and Download History — Report

## Status: DONE

## What Was Changed

Added clipboard copy buttons and download-all-history buttons to both Streamlit apps.

### monologue_generator.py
- Added a "Copy Monologue" button using JavaScript clipboard API after the monologue display box (line 346-351)
- Added a "Download All History" button after the history expander section (lines 149-159)
- Download formats all monologues with separators and metadata into a single `.txt` file

### script generator.py
- Added a "Copy Scene" button using JavaScript clipboard API after the scene display box (lines 236-241)
- Added a "Download All History" button after the history expander section (lines 138-148)
- Download formats all scenes with separators and metadata into a single `.txt` file

## Files Modified
- `monologue_generator.py` — 2 additions (copy button + download all button)
- `script generator.py` — 2 additions (copy button + download all button)

## Concerns
- None. All changes follow existing code conventions and use `st.markdown` with `unsafe_allow_html=True` for clipboard buttons as specified.
