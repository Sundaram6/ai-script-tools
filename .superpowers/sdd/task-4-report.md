# Task 4 Report: Refactor Script Generator to Use Shared Client

**Status:** DONE

**Files modified:**
- `script generator.py` - Replaced `generate_scene` function with shared `generate_json` from gemini_client, removed manual JSON cleaning, removed unused `import json`.

**Changes made:**
1. Replaced `generate_scene` function to use `generate_json` from gemini_client with retry callback.
2. Removed the raw JSON cleaning block (stripping markdown fences).
3. Updated output section to use already-parsed dict directly.
4. Removed unused `import json` and `import time` and google imports.
5. Verified Python syntax.

**Commits created:**
- `f3f316c` - refactor: use shared gemini client in script generator

**Concerns:**
- None. The refactoring follows the same pattern as monologue_generator.py.
