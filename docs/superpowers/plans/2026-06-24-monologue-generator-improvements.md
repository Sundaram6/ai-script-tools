# Monologue Generator Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor and improve the monologue generator and script generator apps by extracting shared logic, adding session history, pinning dependencies, and adding tests.

**Architecture:** Extract a shared Gemini client module to eliminate duplicated API call/retry/parse logic across both generators. Add session history via Streamlit session state. Pin dependencies and add pytest-based tests.

**Tech Stack:** Python 3.10+, Streamlit, google-genai, pytest

## Global Constraints

- Python 3.10+ required
- Streamlit for UI
- Google Gemini API (google-genai package)
- All new modules must have docstrings
- TDD: write failing test first, then implement, then verify

---

## File Structure

| File | Purpose |
|------|---------|
| `gemini_client.py` | Shared Gemini API client with retry, error handling, JSON parsing |
| `gemini_client_test.py` | Tests for the shared client |
| `monologue_generator.py` | Refactored to use shared client + session history |
| `script_generator.py` | Refactored to use shared client + session history |
| `requirements.txt` | Pinned dependency versions |

---

### Task 1: Pin Dependencies

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Check current installed versions**

Run: `pip show streamlit google-genai`
Expected: Version numbers for both packages

- [ ] **Step 2: Update requirements.txt with pinned versions**

```txt
streamlit==1.45.1
google-genai==1.21.1
```

- [ ] **Step 3: Verify requirements.txt**

Run: `pip install -r requirements.txt`
Expected: Success, no version conflicts

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "chore: pin dependency versions"
```

---

### Task 2: Create Shared Gemini Client Module

**Files:**
- Create: `gemini_client.py`
- Create: `gemini_client_test.py`

- [ ] **Step 1: Write failing test for generate_json**

Create `gemini_client_test.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
import gemini_client


def test_generate_json_returns_parsed_dict():
    mock_response = MagicMock()
    mock_response.text = '{"key": "value"}'
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result == {"key": "value"}


def test_generate_json_strips_markdown_fences():
    mock_response = MagicMock()
    mock_response.text = '```json\n{"key": "value"}\n```'
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result == {"key": "value"}


def test_generate_json_returns_none_on_parse_error():
    mock_response = MagicMock()
    mock_response.text = "not valid json"
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result is None


def test_generate_json_returns_none_on_non_429_error():
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.side_effect = Exception("auth error")
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result is None


def test_generate_json_retries_on_429():
    with patch("gemini_client.genai.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.models.generate_content.side_effect = [
            Exception("429 quota exceeded"),
            MagicMock(text='{"ok": true}')
        ]
        with patch("gemini_client.time.sleep"):
            result = gemini_client.generate_json(
                api_key="fake-key",
                model="gemini-2.5-flash",
                temperature=1.0,
                system_instruction="You are a writer.",
                prompt="Write something",
                max_retries=3
            )
    assert result == {"ok": True}
    assert mock_client.models.generate_content.call_count == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest gemini_client_test.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gemini_client'`

- [ ] **Step 3: Implement gemini_client.py**

Create `gemini_client.py`:

```python
"""Shared Gemini API client with retry logic and JSON parsing."""

import json
import time
from google import genai
from google.genai import types


def generate_json(
    api_key: str,
    model: str,
    temperature: float,
    system_instruction: str,
    prompt: str,
    max_retries: int = 3,
    on_retry=None,
) -> dict | None:
    """Call Gemini API and return parsed JSON response.

    Args:
        api_key: Gemini API key.
        model: Model identifier (e.g. 'gemini-2.5-flash').
        temperature: Sampling temperature (0.0-2.0).
        system_instruction: System prompt for the model.
        prompt: User prompt.
        max_retries: Maximum retry attempts on 429 errors.
        on_retry: Optional callback(attempt, wait_seconds) for UI feedback.

    Returns:
        Parsed dict from JSON response, or None on error.
    """
    client = genai.Client(api_key=api_key)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                ),
                contents=prompt,
            )
            return _parse_json(response.text)

        except Exception as e:
            if "429" in str(e):
                wait = 30 * (attempt + 1)
                if on_retry:
                    on_retry(attempt, wait)
                time.sleep(wait)
            else:
                return None

    return None


def _parse_json(raw_text: str) -> dict | None:
    """Parse JSON from model response, stripping markdown fences."""
    if not raw_text:
        return None

    clean = raw_text.strip()
    if clean.startswith("```"):
        parts = clean.split("```")
        if len(parts) >= 2:
            clean = parts[1]
            if clean.startswith("json"):
                clean = clean[4:]

    try:
        return json.loads(clean.strip())
    except json.JSONDecodeError:
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest gemini_client_test.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add gemini_client.py gemini_client_test.py
git commit -m "feat: add shared gemini client module with tests"
```

---

### Task 3: Refactor Monologue Generator to Use Shared Client

**Files:**
- Modify: `monologue_generator.py`

- [ ] **Step 1: Replace generate_monologue function**

Remove the existing `generate_monologue` function (lines 214-239) and replace with:

```python
from gemini_client import generate_json


def generate_monologue(api_key, model, temperature, system_instruction, prompt):
    """Generate a monologue using the shared Gemini client."""
    def on_retry(attempt, wait):
        st.warning(f"Quota hit. Retrying in {wait}s... ({attempt + 1}/3)")

    return generate_json(
        api_key=api_key,
        model=model,
        temperature=temperature,
        system_instruction=system_instruction,
        prompt=prompt,
        max_retries=3,
        on_retry=on_retry,
    )
```

- [ ] **Step 2: Remove the raw JSON cleaning block**

In the output section (around lines 305-310), remove the manual JSON cleaning:

```python
# DELETE this block:
clean_text = raw_text.strip()
if clean_text.startswith("```"):
    clean_text = clean_text.split("```")[1]
    if clean_text.startswith("json"):
        clean_text = clean_text[4:]
```

Replace with:

```python
data = raw_text  # Already parsed by generate_json
```

- [ ] **Step 3: Update the output section to use parsed data directly**

Change the output block (around line 311) from:

```python
try:
    data = json.loads(clean_text.strip())
```

To:

```python
if data:
```

And change the except block (line 406) from:

```python
except json.JSONDecodeError:
    st.error("Couldn't parse response. Raw output:")
    st.code(raw_text)
```

To:

```python
else:
    st.error("Couldn't parse response. Try again.")
```

- [ ] **Step 4: Update the generate_btn handler**

Change line 299-303 from:

```python
with st.spinner("Writing your monologue..."):
    raw_text = generate_monologue(
        api_key, model_choice, temperature,
        system_instruction, prompt
    )
```

To:

```python
with st.spinner("Writing your monologue..."):
    data = generate_monologue(
        api_key, model_choice, temperature,
        system_instruction, prompt
    )
```

And change line 304 from `if raw_text:` to `if data:`.

- [ ] **Step 5: Remove unused import**

Remove `import json` from the top of the file since it's no longer needed here.

- [ ] **Step 6: Run the app to verify it works**

Run: `streamlit run monologue_generator.py`
Expected: App loads, generate button works, output displays correctly

- [ ] **Step 7: Commit**

```bash
git add monologue_generator.py
git commit -m "refactor: use shared gemini client in monologue generator"
```

---

### Task 4: Refactor Script Generator to Use Shared Client

**Files:**
- Modify: `script_generator.py`

- [ ] **Step 1: Replace generate_scene function**

Remove the existing `generate_scene` function (lines 148-187) and replace with:

```python
from gemini_client import generate_json


def generate_scene(api_key, model, temperature, system_instruction, user_request, extra_notes):
    """Generate a scene using the shared Gemini client."""
    prompt = f"""
Write a short scene based on: {user_request}
{f"Additional notes: {extra_notes}" if extra_notes else ""}

Return ONLY valid JSON, no extra text:
{{
  "scene_heading": "INT./EXT. LOCATION - TIME OF DAY",
  "character_name": "NAME IN CAPS",
  "character_description": "Age, one striking detail",
  "logline": "One sentence about what the scene is really about",
  "scene_text": "Full formatted scene here"
}}
"""

    def on_retry(attempt, wait):
        st.warning(f"Quota hit. Retrying in {wait}s... ({attempt + 1}/3)")

    return generate_json(
        api_key=api_key,
        model=model,
        temperature=temperature,
        system_instruction=system_instruction,
        prompt=prompt,
        max_retries=3,
        on_retry=on_retry,
    )
```

- [ ] **Step 2: Remove the raw JSON cleaning block**

In the output section (around lines 207-211), remove:

```python
# DELETE this block:
clean_text = raw_text.strip()
if clean_text.startswith("```"):
    clean_text = clean_text.split("```")[1]
    if clean_text.startswith("json"):
        clean_text = clean_text[4:]
```

- [ ] **Step 3: Update the output section**

Change line 214 from:

```python
data = json.loads(clean_text.strip())
```

To:

```python
data = raw_text  # Already parsed by generate_json
```

Change line 199 from:

```python
with st.spinner("Generating your scene..."):
    raw_text = generate_scene(
```

To:

```python
with st.spinner("Generating your scene..."):
    data = generate_scene(
```

Change line 205 from `if raw_text:` to `if data:`.

- [ ] **Step 4: Replace the except block**

Change lines 251-253 from:

```python
except json.JSONDecodeError:
    st.error("Couldn't parse the response. Raw output below:")
    st.code(raw_text)
```

To:

```python
else:
    st.error("Couldn't parse response. Try again.")
```

- [ ] **Step 5: Remove unused import**

Remove `import json` from the top of the file.

- [ ] **Step 6: Run the app to verify it works**

Run: `streamlit run "script generator.py"`
Expected: App loads, generate button works, output displays correctly

- [ ] **Step 7: Commit**

```bash
git add "script generator.py"
git commit -m "refactor: use shared gemini client in script generator"
```

---

### Task 5: Add Session History

**Files:**
- Modify: `monologue_generator.py`
- Modify: `script generator.py`

- [ ] **Step 1: Add session state initialization to monologue_generator.py**

After the `st.divider()` on line 54, add:

```python
# ── SESSION HISTORY ──────────────────────────────────
if "monologue_history" not in st.session_state:
    st.session_state.monologue_history = []
```

- [ ] **Step 2: Save generated monologue to history**

After the download button (around line 404), add:

```python
# Save to history
st.session_state.monologue_history.append({
    "character_name": data["character_name"],
    "character_age": data["character_age"],
    "monologue": data["monologue"],
    "emotional_arc": data["emotional_arc"],
    "timestamp": time.strftime("%Y-%m-%d %H:%M"),
})
```

- [ ] **Step 3: Add history display section**

Before the main form section (before line 137), add:

```python
# ── HISTORY ──────────────────────────────────────────
if st.session_state.monologue_history:
    with st.expander(f"📜 History ({len(st.session_state.monologue_history)} monologues)", expanded=False):
        for i, entry in enumerate(reversed(st.session_state.monologue_history)):
            st.markdown(f"**{entry['character_name']}**, {entry['character_age']} — {entry['timestamp']}")
            st.markdown(f"*{entry['emotional_arc']}*")
            st.code(entry['monologue'][:200] + "..." if len(entry['monologue']) > 200 else entry['monologue'])
            if i < len(st.session_state.monologue_history) - 1:
                st.divider()
```

- [ ] **Step 4: Add history to script generator**

Repeat steps 1-3 for `script generator.py`, using `"script_history"` as the key and storing `scene_heading`, `character_name`, `scene_text`, and `timestamp`.

- [ ] **Step 5: Run both apps to verify history works**

Run: `streamlit run monologue_generator.py`
Generate a monologue, verify it appears in history. Reload page, verify history persists.

- [ ] **Step 6: Commit**

```bash
git add monologue_generator.py "script generator.py"
git commit -m "feat: add session history to both generators"
```

---

### Task 6: Add Copy Button and Download History

**Files:**
- Modify: `monologue_generator.py`
- Modify: `script generator.py`

- [ ] **Step 1: Add clipboard copy to monologue output**

After the monologue box display (around line 342), add:

```python
st.markdown(
    f'<button onclick="navigator.clipboard.writeText(document.querySelector(\'.monologue-box\').innerText)" '
    f'style="background:#333;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;margin-top:8px;">'
    f'📋 Copy Monologue</button>',
    unsafe_allow_html=True
)
```

- [ ] **Step 2: Add "Download All History" button**

After the history expander, add:

```python
if st.session_state.monologue_history:
    all_text = "\n\n".join([
        f"MONOLOGUE — {h['character_name']}, {h['character_age']} ({h['timestamp']})\n{'='*60}\n{h['monologue']}"
        for h in st.session_state.monologue_history
    ])
    st.download_button(
        label="⬇️ Download All History",
        data=all_text,
        file_name="monologue_history.txt",
        mime="text/plain",
        use_container_width=True,
    )
```

- [ ] **Step 3: Repeat for script generator**

- [ ] **Step 4: Commit**

```bash
git add monologue_generator.py "script generator.py"
git commit -m "feat: add copy button and download history"
```

---

### Task 7: Add Input Validation

**Files:**
- Modify: `monologue_generator.py`
- Modify: `script generator.py`

- [ ] **Step 1: Add validation helper to monologue_generator.py**

Before the main form section, add:

```python
def validate_input(text: str, min_length: int = 10, max_length: int = 500) -> str | None:
    """Validate text input. Returns error message or None."""
    if not text or not text.strip():
        return "This field is required."
    if len(text.strip()) < min_length:
        return f"Please write at least {min_length} characters."
    if len(text.strip()) > max_length:
        return f"Please keep it under {max_length} characters."
    return None
```

- [ ] **Step 2: Add validation to the generate button handler**

Replace the existing validation block (lines 283-288) with:

```python
if not api_key:
    st.error("Enter your Gemini API key in the sidebar.")
elif validate_input(situation):
    st.error(validate_input(situation))
elif validate_input(spoken_to, min_length=3):
    st.error(validate_input(spoken_to, min_length=3))
else:
    # ... generation code
```

- [ ] **Step 3: Repeat for script generator**

- [ ] **Step 4: Commit**

```bash
git add monologue_generator.py "script generator.py"
git commit -m "feat: add input validation"
```

---

### Task 8: Run All Tests and Verify

**Files:**
- Test: `gemini_client_test.py`

- [ ] **Step 1: Run all tests**

Run: `pytest gemini_client_test.py -v`
Expected: All tests PASS

- [ ] **Step 2: Run both apps manually**

Run: `streamlit run monologue_generator.py`
Run: `streamlit run "script generator.py"`
Test: Generate monologues and scenes, verify history, copy, download all work.

- [ ] **Step 3: Final commit if any fixes needed**

```bash
git add -A
git commit -m "chore: final fixes after verification"
```

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-06-24-monologue-generator-improvements.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
