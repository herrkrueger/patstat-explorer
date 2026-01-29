# Story 1.7: Convert All Static Queries to Dynamic

Status: done

## Story

As a PATLIB professional,
I want all 18 existing queries to work with the new parameter system,
so that I have consistent experience across the entire query library.

## Acceptance Criteria

1. **Given** the existing 18 static queries in queries_bq.py (Q01-Q18)
   **When** conversion is complete
   **Then** all 18 queries use the new parameter pattern (jurisdictions, year_start, year_end, tech_field)
   **And** each query has appropriate default values based on query type
   **And** each query has a question-based title and description
   **And** each query is assigned to a category (Competitors, Trends, Regional, Technology)

2. **Given** any converted query is executed
   **When** run with various parameter combinations
   **Then** query executes successfully within 15 seconds
   **And** results display correctly with insight headline and chart
   **And** export functions work correctly (CSV and chart HTML)

3. **Given** the Interactive Analysis tab (DQ01)
   **When** reviewed after conversion
   **Then** it continues to work with the new UI patterns
   **And** multi-jurisdiction comparison is preserved

## Tasks / Subtasks

- [x] Task 1: Create parameterized SQL template system (AC: #1)
  - [x] Define SQL parameter placeholder syntax (@param for BigQuery)
  - [x] Create template substitution function in app.py
  - [x] Handle optional parameters (tech_field can be None)
  - [x] Handle array parameters (jurisdictions as list)

- [x] Task 2: Convert Overview queries Q01-Q05 to dynamic (AC: #1)
  - [x] Q01: Database Statistics - add year_range filter
  - [x] Q02: Filing Authorities - add year_range and jurisdiction filters
  - [x] Q03: Applications by Year - add jurisdiction filter
  - [x] Q04: Top IPC Classes - add year_range and jurisdiction filters
  - [x] Q05: Sample Patents - add year_range filter

- [x] Task 3: Convert Strategic queries Q06-Q07 to dynamic (AC: #1)
  - [x] Q06: Country Patent Activity - already has year filter, add tech_field
  - [x] Q07: Green Technology Trends - make jurisdictions dynamic

- [x] Task 4: Convert Technology queries Q08-Q10 to dynamic (AC: #1)
  - [x] Q08: Most Active Technology Fields - add jurisdiction filter
  - [x] Q09: AI-based ERP Patent Landscape - add year_range filter
  - [x] Q10: AI-Assisted Diagnostics Companies - add year_range filter

- [x] Task 5: Convert Competitive Intelligence Q11-Q12 to dynamic (AC: #1)
  - [x] Q11: Top Patent Applicants - add tech_field filter
  - [x] Q12: Competitor Filing Strategy - make competitors list configurable

- [x] Task 6: Convert Citation/Prosecution Q13-Q14 to dynamic (AC: #1)
  - [x] Q13: Most Cited Patents - make citation year dynamic
  - [x] Q14: Diagnostic Imaging Grant Rates - add year_range filter

- [x] Task 7: Convert Regional Analysis Q15-Q17 to dynamic (AC: #1)
  - [x] Q15: German States Medical Tech - add year_range filter
  - [x] Q16: German States Per Capita - add tech_field option
  - [x] Q17: Regional Tech Sector Comparison - make regions configurable

- [x] Task 8: Convert Technology Transfer Q18 to dynamic (AC: #1)
  - [x] Q18: Fastest-Growing G06Q Subclasses - add year_range filter

- [x] Task 9: Update run_query to use parameters (AC: #2)
  - [x] Modify run_query() to accept parameter dict
  - [x] Implement BigQuery parameterized query execution
  - [x] Add parameter validation before execution

- [x] Task 10: Verify all queries execute correctly (AC: #2, #3)
  - [x] Test each query with default parameters
  - [x] Test with modified parameter combinations
  - [x] Verify DQ01 still works with multi-jurisdiction comparison
  - [x] Confirm <15 second execution time

## Dev Notes

### SQL Template Pattern

Use BigQuery parameterized queries with @param syntax:

```python
sql_template = """
SELECT ...
FROM tls201_appln a
WHERE a.appln_filing_year BETWEEN @year_start AND @year_end
  AND a.appln_auth IN UNNEST(@jurisdictions)
  {tech_field_clause}
"""
```

### Parameter Types

- `@year_start`, `@year_end`: INT64
- `@jurisdictions`: ARRAY<STRING>
- `@tech_field`: INT64 (optional, can be NULL)

### Handling Optional Parameters

For tech_field which is optional:
```python
tech_field_clause = ""
if tech_field is not None:
    tech_field_clause = "AND tf.techn_field_nr = @tech_field"
```

### Query-Specific Parameters

Some queries need query-specific parameters beyond the standard set:
- Q12: competitor_names list
- Q13: citation_year
- Q17: region_codes list

### Testing Strategy

Test with edge cases:
- Empty jurisdiction list (should warn user)
- Single year (year_start == year_end)
- All fields selected (tech_field = None)
- Maximum date range

### Project Structure Notes

- Queries defined in: `queries_bq.py`
- Query execution in: `app.py` (run_query function)
- Parameter UI in: `app.py` (render_parameter_block function)
- Current parameters already work for display, need to pass to queries

### References

- [Source: queries_bq.py] QUERIES dict contains all 18 static queries
- [Source: queries_bq.py] DYNAMIC_QUERIES dict has DQ01 as reference pattern
- [Source: app.py:627-640] run_query function needs modification
- [Source: app.py:150-209] render_parameter_block already captures params
- [Source: PRD FR11-FR15] Dynamic parameter requirements
- [Source: UX Design - Parameter Patterns] Order: Time → Geography → Technology → Action

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

None - implementation was already complete from previous sessions.

### Completion Notes List

- All 18 queries (Q01-Q18) now have `sql_template` with @param placeholders
- `run_parameterized_query()` function in app.py handles BigQuery parameterized execution
- Parameters supported: @year_start, @year_end, @jurisdictions (array), @tech_field (optional)
- Detail page automatically uses sql_template when available, falls back to static sql
- DQ01 continues to work with multi-jurisdiction comparison

### File List

- queries_bq.py (modified - added sql_template to all 18 queries)
- app.py (modified - added run_parameterized_query function, updated detail page to use templates)
