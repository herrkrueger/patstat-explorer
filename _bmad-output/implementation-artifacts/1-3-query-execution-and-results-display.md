# Story 1.3: Query Execution & Results Display

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to run queries and see results clearly,
so that I can answer my client's question quickly.

## Acceptance Criteria

1. **Given** user clicks "Run Analysis"
   **Then** spinner shows contextual message (e.g., "Finding top filers...")
   **And** execution completes within 15 seconds for uncached queries

2. **Given** query returns results
   **Then** results appear in wide layout below parameters
   **And** data table available in expander ("View Data Table")
   **And** results cached for faster repeat access (<3 seconds)

3. **Given** query returns no data
   **Then** warning message with helpful suggestions appears

## Tasks

- [ ] Task 1: Contextual spinner messages based on query type
- [ ] Task 2: Results caching with @st.cache_data
- [ ] Task 3: Data table in expander with "View Data Table" label
- [ ] Task 4: Empty results handling with suggestions
- [ ] Task 5: Execution timing display

## Dev Notes

- Modify `render_detail_page()` execution block
- Use query title/category for contextual spinner text
- Cache key should include query_id + parameters
