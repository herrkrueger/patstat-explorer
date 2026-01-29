# Story 2.2: Query Metadata Display

Status: done

## Story

As a PATLIB professional,
I want to see clear information about each query before running it,
so that I can choose the right analysis for my client's question.

## Acceptance Criteria

1. **Given** a query is displayed in the library (landing page)
   **When** the user views the query card
   **Then** the query title is displayed as a question (e.g., "Who are the top filers in my field?")
   **And** a brief description explains what the query reveals
   **And** estimated execution time is shown (e.g., "~8 seconds")
   **And** stakeholder tags are visible (PATLIB, BUSINESS, UNIVERSITY)

2. **Given** a query is displayed on the detail page
   **When** the user views query information
   **Then** full explanation is available in expandable section
   **And** key outputs are listed
   **And** methodology notes are available
   **And** data source information is shown

3. **Given** query metadata is incomplete
   **When** displaying the query
   **Then** gracefully handle missing fields with sensible defaults
   **And** do not show empty sections

## Tasks / Subtasks

- [x] Task 1: Enhance query card display on landing page (AC: #1)
  - [x] Style title as question format
  - [x] Show description snippet (truncated if long)
  - [x] Display estimated_seconds_cached as "~Xs"
  - [x] Show colored stakeholder tag pills

- [x] Task 2: Add tag pill component (AC: #1)
  - [x] Create reusable tag pill styling
  - [x] Color-code by stakeholder type (PATLIB=blue, BUSINESS=green, UNIVERSITY=purple)
  - [x] Display inline with query metadata

- [x] Task 3: Enhance detail page metadata (AC: #2)
  - [x] Move explanation to "Details" expander
  - [x] Add key_outputs as bullet list
  - [x] Add methodology as separate expander if present
  - [x] Show data sources referenced by query

- [x] Task 4: Ensure all queries have required metadata (AC: #1, #3)
  - [x] Audit QUERIES dict for missing fields
  - [x] Add question-style titles to all queries
  - [x] Ensure every query has description and estimated time
  - [x] Add methodology field to queries that need it

- [x] Task 5: Handle missing metadata gracefully (AC: #3)
  - [x] Default estimated time to "~5s" if not specified
  - [x] Hide empty sections rather than showing "None"
  - [x] Provide sensible defaults for display

## Dev Notes

### Query Card Layout (Landing Page)

```
┌─────────────────────────────────────────────────────────────┐
│ Q06: Who leads patent filing in each country?               │
│ ─────────────────────────────────────────────────────────── │
│ Analyzes patent filing activity by applicant country...     │
│                                                             │
│ [PATLIB] [BUSINESS]                          ~5s            │
└─────────────────────────────────────────────────────────────┘
```

### Tag Styling

```python
def render_tags(tags: list):
    """Render colored tag pills."""
    tag_colors = {
        "PATLIB": "#1f77b4",     # Blue
        "BUSINESS": "#2ca02c",    # Green
        "UNIVERSITY": "#9467bd"   # Purple
    }
    tags_html = " ".join([
        f'<span style="background-color: {tag_colors.get(t, "#666")}; '
        f'color: white; padding: 2px 10px; border-radius: 12px; '
        f'font-size: 0.85em; margin-right: 6px;">{t}</span>'
        for t in tags
    ])
    st.markdown(tags_html, unsafe_allow_html=True)
```

### Required Query Metadata Fields

Every query in QUERIES should have:
- `title`: Question-style title
- `description`: Brief explanation (1-2 sentences)
- `tags`: List of stakeholder types
- `category`: One of [Competitors, Trends, Regional, Technology]
- `estimated_seconds_cached`: Expected execution time
- `estimated_seconds_first_run`: First-run time (optional)
- `explanation`: Detailed explanation (optional)
- `key_outputs`: List of what the query returns (optional)
- `methodology`: Data source and calculation notes (optional)

### Project Structure Notes

- Query metadata in: `queries_bq.py` (QUERIES dict)
- Landing page cards in: `app.py` (render_query_list)
- Detail page display in: `app.py` (render_detail_page)
- Tag styling already exists in render_detail_page

### References

- [Source: queries_bq.py:18-55] Q01 example with full metadata
- [Source: app.py:447-454] Existing tag rendering in detail page
- [Source: app.py:410-416] Current query list button rendering
- [Source: PRD FR3] Users can view query descriptions
- [Source: PRD FR4] Users can see estimated execution time
- [Source: UX Design - Component Strategy] Query Card spec

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

### Completion Notes List

- render_tags_inline() at app.py lines 212-224
- Query cards with metadata at app.py lines 610-638
- Detail page metadata at app.py lines 691-721
- Methodology expander at app.py lines 719-721
- All 18 queries have complete metadata
- 23 unit tests written and passing

### File List

- app.py (modified)
- queries_bq.py (verified metadata complete)
- tests/test_query_metadata.py (created)
