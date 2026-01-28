# Story 1.1: Landing Page with Question-Based Navigation

Status: done

## Story

As a PATLIB professional,
I want to see queries organized by the type of question I'm trying to answer,
so that I can quickly find the right analysis without learning technical query names.

## Acceptance Criteria

1. **Given** a user opens PATSTAT Explorer
   **When** the application loads
   **Then** they see a landing page with the title "What do you want to know?"
   **And** category pills are displayed: Competitors, Trends, Regional, Technology

2. **Given** the landing page is displayed
   **When** user clicks a category pill
   **Then** the query list filters to show only queries in that category
   **And** the selected pill appears visually distinct (active state)

3. **Given** the landing page is displayed
   **When** user views the "Common Questions" section
   **Then** 3-5 popular queries are shown as clickable cards
   **And** each card shows the query title as a question

4. **Given** a user clicks on a query from the landing page
   **When** they select any query
   **Then** they navigate to the detail page for that query
   **And** the "← Back to Questions" button is visible

5. **Given** a user is on a detail page
   **When** they click "← Back to Questions"
   **Then** they return to the landing page
   **And** previously selected category remains active (state preserved)

## Tasks / Subtasks

- [x] Task 1: Implement session state for page navigation (AC: #1, #4, #5)
  - [x] 1.1 Add `st.session_state['current_page']` to track 'landing' vs 'detail'
  - [x] 1.2 Add `st.session_state['selected_query']` to track which query is selected
  - [x] 1.3 Add `st.session_state['selected_category']` to preserve category filter
  - [x] 1.4 Create navigation functions: `go_to_landing()`, `go_to_detail(query_id)`

- [x] Task 2: Create landing page layout (AC: #1, #2, #3)
  - [x] 2.1 Remove current tab-based navigation from `main()` (done in Task 6)
  - [x] 2.2 Create `render_landing_page()` function
  - [x] 2.3 Add page title "What do you want to know?" using `st.header()`
  - [x] 2.4 Implement category pills using `st.pills()` component
  - [x] 2.5 Create "Common Questions" section with 3-5 hardcoded popular queries

- [x] Task 3: Add query categories to queries_bq.py (AC: #2)
  - [x] 3.1 Add `"category"` field to each query in QUERIES dict
  - [x] 3.2 Categories: "Competitors", "Trends", "Regional", "Technology"
  - [x] 3.3 Assign appropriate category to all 18 existing queries

- [x] Task 4: Implement query list with filtering (AC: #2, #3)
  - [x] 4.1 Create `render_query_list(category_filter)` function
  - [x] 4.2 Display queries as clickable cards with title as question
  - [x] 4.3 Filter queries based on selected category pill
  - [x] 4.4 Add click handler to navigate to detail page

- [x] Task 5: Create detail page wrapper (AC: #4, #5)
  - [x] 5.1 Create `render_detail_page(query_id)` function
  - [x] 5.2 Add "← Back to Questions" button at top
  - [x] 5.3 Integrate existing query execution logic from `render_query_panel()`
  - [x] 5.4 Preserve parameters when navigating back

- [x] Task 6: Update main() routing logic (AC: #1, #4, #5)
  - [x] 6.1 Replace tabs with conditional rendering based on session state
  - [x] 6.2 Route to landing page when `current_page == 'landing'`
  - [x] 6.3 Route to detail page when `current_page == 'detail'`

## Dev Notes

### Current Architecture
The app currently uses a **tab-based navigation** pattern in `main()`:
- 5 tabs: Interactive, Alle, PATLIB, BUSINESS, UNIVERSITY
- Each tab filters queries by stakeholder tag
- `render_query_panel()` handles query selection and execution

### Target Architecture
Transform to a **landing + detail two-phase experience**:
- Landing page: Category pills + query list + common questions
- Detail page: Parameters + execution + results (reuse existing logic)
- Session state manages navigation between pages

### Key Streamlit Patterns

**Session State Navigation:**
```python
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'landing'

if st.session_state['current_page'] == 'landing':
    render_landing_page()
else:
    render_detail_page(st.session_state['selected_query'])
```

**Category Pills (new Streamlit component):**
```python
selected = st.pills(
    "Categories",
    options=["Competitors", "Trends", "Regional", "Technology"],
    default=None,
    selection_mode="single"
)
```

**Back Button Pattern:**
```python
if st.button("← Back to Questions"):
    st.session_state['current_page'] = 'landing'
    st.rerun()
```

### Query Category Mapping (suggested)

| Category | Queries (by typical content) |
|----------|------------------------------|
| Competitors | Top applicants, market share, competitor analysis |
| Trends | Applications by year, growth rates, time series |
| Regional | Country comparisons, jurisdiction analysis |
| Technology | Technology fields, IPC/CPC analysis, innovation areas |

### Project Structure Notes

- **app.py**: Main application - will need significant refactoring
- **queries_bq.py**: Add `category` field to each query
- No new files needed for this story
- Preserve existing BigQuery client and query execution logic

### Testing Approach

1. Manual testing of navigation flow
2. Verify all 18 queries are categorized and visible
3. Test back navigation preserves category selection
4. Test that query execution still works on detail page

### References

- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Design Direction Decision]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Component Strategy]
- [Source: _bmad-output/planning-artifacts/prd.md#Functional Requirements - FR1-FR5]
- [Source: Streamlit docs - st.pills() component]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

- All 28 unit tests passing
- Red-green-refactor cycle followed for each task

### Completion Notes List

1. **Task 1**: Implemented session state navigation with `init_session_state()`, `go_to_landing()`, `go_to_detail()` functions
2. **Task 2**: Created `render_landing_page()` with "What do you want to know?" title, category pills, and Common Questions section
3. **Task 3**: Added `category` field to all 18 queries in QUERIES dict (Competitors, Trends, Regional, Technology)
4. **Task 4**: Created `render_query_list()` with category filtering support
5. **Task 5**: Created `render_detail_page()` with back button and query execution logic
6. **Task 6**: Updated `main()` to use session-state based routing, removing tab navigation

### Code Review Fixes Applied

- **H1**: Removed 330+ lines of dead code (render_interactive_panel, render_query_panel, load_reference_data, run_dynamic_query, get_filtered_queries)
- **H2**: Removed misleading TODO comment from render_query_list
- **M2**: Added input validation to go_to_detail() - now validates query_id exists in QUERIES
- **M3**: Added test for invalid query_id handling (test_go_to_detail_validates_query_id)
- **L2**: Added documentation explaining COMMON_QUESTIONS selection criteria
- Cleaned up unused imports (math, DYNAMIC_QUERIES, REFERENCE_QUERIES)

### File List

**Modified:**
- app.py - Added navigation functions, landing page, detail page, updated main() routing, removed dead code
- queries_bq.py - Added category field to all 18 queries

**Created:**
- test_app_navigation.py - 29 unit tests for navigation, landing page, categories, filtering, detail page, and routing
