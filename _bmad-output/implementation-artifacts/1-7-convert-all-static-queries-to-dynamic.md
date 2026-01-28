# Story 1.7: Convert All Static Queries to Dynamic

Status: ready-for-dev

## Story

As a PATLIB professional,
I want all 18 existing queries to work with the new parameter system,
so that I have consistent experience across the entire query library.

## Acceptance Criteria

1. **Given** existing 18 static queries
   **When** conversion complete
   **Then** all use parameter pattern (jurisdictions, year_start, year_end, tech_field)
   **And** each has appropriate defaults
   **And** each has question-based title/description
   **And** each assigned to category

2. **Given** any converted query executed
   **Then** executes within 15 seconds
   **And** results display with insight headline and chart
   **And** export functions work

## Tasks

- [ ] Task 1: Create parameterized SQL template system
- [ ] Task 2: Convert Q01-Q06 to dynamic
- [ ] Task 3: Convert Q07-Q12 to dynamic
- [ ] Task 4: Convert Q13-Q18 to dynamic
- [ ] Task 5: Update run_query to use parameters
- [ ] Task 6: Verify all queries execute correctly

## Dev Notes

- SQL templates use @param syntax for BigQuery
- Not all queries need all parameters - make optional
- Some queries may need query-specific parameters
- Test each query after conversion
