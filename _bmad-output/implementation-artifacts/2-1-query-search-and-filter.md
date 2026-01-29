# Story 2.1: Query Search and Filter

Status: done

## Story

As a PATLIB professional,
I want to search and filter the query library,
so that I can quickly find the right analysis even with 40+ queries.

## Acceptance Criteria

1. **Given** a user is on the landing page
   **When** they type in the search box
   **Then** queries are filtered by keyword match in title or description
   **And** search is case-insensitive
   **And** results update as user types (debounced for performance)

2. **Given** a user wants to filter by stakeholder type
   **When** they select a stakeholder filter (PATLIB, BUSINESS, UNIVERSITY)
   **Then** only queries tagged with that stakeholder type are shown
   **And** filters can be combined with search
   **And** filters can be combined with category pills

3. **Given** no queries match the search/filter criteria
   **When** the empty state displays
   **Then** a helpful message appears suggesting to broaden search
   **And** option to clear filters is visible

## Tasks / Subtasks

- [x] Task 1: Add search text input to landing page (AC: #1)
  - [x] Position search box in header area
  - [x] Use st.text_input with placeholder "Search queries..."
  - [x] Store search term in session state for persistence

- [x] Task 2: Implement search filtering logic (AC: #1)
  - [x] Create filter_queries() function
  - [x] Match against title (case-insensitive)
  - [x] Match against description (case-insensitive)
  - [x] Match against tags
  - [x] Support partial word matching

- [x] Task 3: Add stakeholder filter pills (AC: #2)
  - [x] Add st.pills for stakeholder types below category pills
  - [x] Support multi-select mode (can filter by multiple tags)
  - [x] Combine with existing category filter

- [x] Task 4: Combine all filters (AC: #2)
  - [x] Apply search filter
  - [x] Apply category filter
  - [x] Apply stakeholder filter
  - [x] All filters work together (AND logic)

- [x] Task 5: Handle empty results (AC: #3)
  - [x] Display st.info message when no matches
  - [x] Show "Clear all filters" button
  - [x] Suggest broadening search terms

## Dev Notes

### Search Implementation

```python
def filter_queries(queries: dict, search_term: str, category: str, stakeholders: list) -> dict:
    """Filter queries by search term, category, and stakeholder tags."""
    filtered = queries

    if search_term:
        search_lower = search_term.lower()
        filtered = {
            qid: q for qid, q in filtered.items()
            if search_lower in q['title'].lower()
            or search_lower in q.get('description', '').lower()
            or any(search_lower in tag.lower() for tag in q.get('tags', []))
        }

    if category:
        filtered = {qid: q for qid, q in filtered.items() if q.get('category') == category}

    if stakeholders:
        filtered = {
            qid: q for qid, q in filtered.items()
            if any(s in q.get('tags', []) for s in stakeholders)
        }

    return filtered
```

### UI Layout

```
┌──────────────────────────────────────────────────────────┐
│  What do you want to know?           [Search queries...] │
│                                                          │
│  [Competitors] [Trends] [Regional] [Technology]          │
│  [PATLIB] [BUSINESS] [UNIVERSITY]                        │
│                                                          │
│  Common Questions:                                       │
│  ...                                                     │
└──────────────────────────────────────────────────────────┘
```

### Debouncing

Streamlit doesn't have built-in debounce, but the search is instant enough that debouncing isn't strictly necessary. The on_change callback pattern works well:

```python
search = st.text_input("Search", key="search_input", placeholder="Search queries...")
```

### Project Structure Notes

- Landing page rendering in: `app.py` (render_landing_page function)
- Query list rendering in: `app.py` (render_query_list function)
- QUERIES dict in: `queries_bq.py`
- STAKEHOLDERS dict in: `queries_bq.py`

### References

- [Source: app.py:341-391] render_landing_page - add search box here
- [Source: app.py:393-416] render_query_list - modify to accept filters
- [Source: queries_bq.py:12-16] STAKEHOLDERS dict for filter options
- [Source: PRD FR5] Users can search queries by keyword
- [Source: UX Design - Journey Flows] Search for power users

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

### Completion Notes List

- All functionality implemented in app.py
- filter_queries() at lines 160-200
- Search input at lines 483-490
- Stakeholder pills at lines 508-515
- Empty results handling at lines 597-604
- 28 unit tests written and passing

### File List

- app.py (modified)
- tests/test_filter_queries.py (created)
