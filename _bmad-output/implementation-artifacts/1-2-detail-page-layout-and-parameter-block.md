# Story 1.2: Detail Page Layout & Parameter Block

Status: done

## Story

As a PATLIB professional,
I want consistent parameter controls on every query,
so that I can adjust jurisdiction, year range, and technology without learning new interfaces.

## Acceptance Criteria

1. **Given** a user is on a query detail page
   **When** the page loads
   **Then** a bordered parameter container is displayed at the top
   **And** parameters appear in order: Time → Geography → Technology → Action
   **And** year range uses a slider with sensible defaults (e.g., 2015-2024)
   **And** jurisdiction uses multiselect with defaults (e.g., EP, US, CN)
   **And** technology field uses selectbox grouped by sector
   **And** "Run Analysis" button is styled as primary (type="primary")

2. **Given** a user clicks "← Back to Questions"
   **When** navigation occurs
   **Then** they return to the landing page
   **And** any unsaved parameter changes are discarded

## Tasks / Subtasks

- [x] Task 1: Add parameter session state management (AC: #1, #2)
  - [x] 1.1 Add session state keys for year_start, year_end, jurisdictions, tech_field
  - [x] 1.2 Initialize with sensible defaults (2015-2024, ["EP", "US", "CN"], None)
  - [x] 1.3 Clear parameter state on `go_to_landing()` (AC #2 - discard unsaved changes)

- [x] Task 2: Create reference data loading (AC: #1)
  - [x] 2.1 Create JURISDICTIONS constant with valid jurisdiction codes
  - [x] 2.2 Create TECH_FIELDS dict with 35 WIPO tech fields and sector grouping
  - [x] 2.3 Data is static, no caching needed

- [x] Task 3: Implement parameter block component (AC: #1)
  - [x] 3.1 Create `render_parameter_block()` function
  - [x] 3.2 Wrap in `st.container(border=True)` for visual grouping
  - [x] 3.3 Add year range slider: `st.slider()` with min=1990, max=2024, default=(2015, 2024)
  - [x] 3.4 Add jurisdiction multiselect: `st.multiselect()` with default=["EP", "US", "CN"]
  - [x] 3.5 Add technology field selectbox: `st.selectbox()` with sector grouping via format_func
  - [x] 3.6 Add "Run Analysis" button with `type="primary"`
  - [x] 3.7 Ensure parameter order: Time → Geography → Technology → Action

- [x] Task 4: Integrate parameter block into detail page (AC: #1)
  - [x] 4.1 Call `render_parameter_block()` at top of `render_detail_page()`
  - [x] 4.2 Pass parameter values to query execution (run_clicked triggers execution)
  - [ ] 4.3 Update query SQL to use parameter placeholders where applicable (deferred to Story 1.7)

- [x] Task 5: Update tests for parameter functionality
  - [x] 5.1 Add tests for parameter session state initialization
  - [x] 5.2 Add tests for parameter clearing on back navigation
  - [x] 5.3 Add tests for render_parameter_block existence and structure

## Dev Notes

### Current State (from Story 1.1)
- `render_detail_page()` exists at app.py:147-261
- Currently shows query info, SQL expander, and "Run Query" button
- No parameter controls yet - queries run with hardcoded values
- Session state has: current_page, selected_query, selected_category
- Back navigation works via `go_to_landing()` at app.py:35-40

### Key Implementation Points

**Parameter Order (UX11):**
```
Time → Geography → Technology → Action
```

**Bordered Container Pattern:**
```python
with st.container(border=True):
    # Parameter controls here
```

**Year Range Slider:**
```python
year_start, year_end = st.slider(
    "Year Range",
    min_value=1990,
    max_value=2024,
    value=(2015, 2024),
    help="Select the filing year range for analysis"
)
```

**Jurisdiction Multiselect:**
```python
jurisdictions = st.multiselect(
    "Jurisdictions",
    options=["EP", "US", "CN", "JP", "KR", "DE", "FR", "GB"],
    default=["EP", "US", "CN"],
    help="Select patent offices to include"
)
```

**Technology Field Selectbox with Grouping:**
```python
# Tech fields from WIPO classification
TECH_FIELDS = {
    1: ("Electrical machinery", "Electrical engineering"),
    2: ("Audio-visual technology", "Electrical engineering"),
    # ... more fields
    13: ("Medical technology", "Instruments"),
    # ... etc
}

tech_field = st.selectbox(
    "Technology Field",
    options=list(TECH_FIELDS.keys()),
    index=12,  # Default to Medical technology (13)
    format_func=lambda x: f"{TECH_FIELDS[x][0]} ({TECH_FIELDS[x][1]})"
)
```

### Testing Approach
- Continue using module-level mocking pattern from Story 1.1
- Test session state initialization for parameters
- Test parameter clearing on back navigation
- Test render_parameter_block output structure

### Project Structure Notes

**Files to modify:**
- `app.py` - Add parameter block to render_detail_page()
- `test_app_navigation.py` - Add parameter tests

**No new files needed** - extend existing implementation

### References

- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UX11] Parameter order
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#UX5] Bordered containers
- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.2] Acceptance criteria
- [Source: app.py:147-261] Current render_detail_page implementation
- [Source: test_app_navigation.py] Testing patterns from Story 1.1

### Previous Story Intelligence (Story 1.1)

**Key Learnings:**
- Module-level mocking works well for Streamlit testing
- Session state requires explicit initialization checks
- Python 3.9 compatibility: avoid `str | None` type hints, use plain types
- Code review found and removed 350+ lines of dead code - keep this clean

**Established Patterns:**
- Navigation functions: `go_to_landing()`, `go_to_detail()`
- Session state keys: `current_page`, `selected_query`, `selected_category`
- Test structure: Classes for each feature area

**Files from Previous Story:**
- app.py: 361 lines (lean after cleanup)
- test_app_navigation.py: 377 lines, 29 tests

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

- 35 unit tests passing
- Red-green-refactor cycle followed for each task

### Completion Notes List

1. **Task 1**: Added parameter session state (year_start, year_end, jurisdictions, tech_field) with defaults and reset on back navigation
2. **Task 2**: Added JURISDICTIONS list (9 patent offices) and TECH_FIELDS dict (35 WIPO fields with sector grouping)
3. **Task 3**: Created `render_parameter_block()` with bordered container, 4-column layout (Time|Geography|Technology|Action)
4. **Task 4**: Integrated parameter block into `render_detail_page()`, Run Analysis button triggers query execution
5. **Task 5**: Added 6 new tests for parameter session state and parameter block

**Note**: Task 4.3 (parameterized SQL) deferred to Story 1.7 which converts all static queries to dynamic

### Code Review Fixes Applied

- **M1**: Extracted default parameter values to constants (DEFAULT_YEAR_START, etc.) - DRY principle
- **M2**: Added validation warning when no jurisdictions selected
- **M3**: Removed unused STAKEHOLDERS import
- **L1**: Removed Python 3.10+ type hint from run_query()

### File List

**Modified:**
- app.py - Added parameter state, JURISDICTIONS, TECH_FIELDS, render_parameter_block(), updated render_detail_page()
- test_app_navigation.py - Added TestParameterSessionState and TestParameterBlock test classes (6 new tests)
