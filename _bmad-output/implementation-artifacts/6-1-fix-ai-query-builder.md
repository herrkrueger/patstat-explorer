---
status: done
epic: 6
story: 1
name: fix-ai-query-builder
---

# Story 6.1: Fix AI Query Builder & Dependencies

**As a** developer,
**I want** the AI Query Builder to work reliably in both local and cloud environments,
**So that** the core "AI" feature of the MVP is actually functional.

## Acceptance Criteria

### 1. Dependency Management
- **Given** `requirements.txt`
- **When** checked
- **Then** the `anthropic` library is explicitly listed with a version number

### 2. Environment Configuration
- **Given** the application startup
- **When** loading the `anthropic` API key
- **Then** the app checks `st.secrets` first (Cloud)
- **And** checks `os.environ` / `.env` second (Local)
- **And** if the key is missing from both, the app does NOT crash but shows a helpful warning in the UI

### 3. Functional Verification
- **Given** a valid API key
- **When** the user sends a natural language prompt
- **Then** the app successfully imports `anthropic` and calls the API
- **And** returns a valid SQL response

## Tasks/Subtasks

- [x] Fix Dependency: Add `anthropic` to `requirements.txt`
- [x] Fix Configuration: Update `app.py` to robustly load API key
- [x] Fix Implementation: Ensure `anthropic` client initialization handles missing keys gracefully
- [x] Verify: Test locally with `.env` (Manual check)

## Dev Notes

- `app.py` currently attempts to import `anthropic` at top level, which crashes if lib is missing.
- Need to use `python-dotenv` for local env loading (already in requirements).
- `st.secrets` is the Streamlit Cloud way.

## Dev Agent Record
### Implementation Plan
- [x] Verified `anthropic>=0.7.0` in requirements.txt
- [x] Verified `get_claude_client()` in modules/logic.py:116-144
- [x] Ran 14 tests in test_ai_config.py + test_ai_builder.py

### Completion Notes
- Implementation was already complete from Epic 4 work
- `get_claude_client()` correctly checks st.secrets first, os.getenv second
- Graceful None return on ImportError or missing key
- All 14 tests passed (2026-01-30)

## File List
- requirements.txt
- app.py

## Change Log
- 2026-01-30: Story created
- 2026-01-30: Story verified complete - all 14 tests passed, implementation was already in place from Epic 4

