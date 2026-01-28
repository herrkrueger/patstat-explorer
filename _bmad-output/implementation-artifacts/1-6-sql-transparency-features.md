# Story 1.6: SQL Transparency Features

Status: ready-for-dev

## Story

As a data-savvy PATLIB professional,
I want to see the SQL query behind the analysis,
so that I can learn, verify, or adapt the query for my own use.

## Acceptance Criteria

1. **Given** detail page displayed
   **When** user expands "View SQL"
   **Then** SQL shown with parameter values substituted
   **And** SQL formatted for readability

2. **Given** SQL displayed
   **When** user clicks "Copy to Clipboard"
   **Then** SQL copied with success message

3. **Given** any query selected
   **Then** methodology explanation shown (data sources, limitations)

## Tasks

- [ ] Task 1: SQL parameter substitution display
- [ ] Task 2: Copy to clipboard button with pyperclip or st.code copy
- [ ] Task 3: Methodology section in query metadata
- [ ] Task 4: SQL formatting/pretty-print

## Dev Notes

- st.code has built-in copy button
- Parameter substitution: replace placeholders with actual values
- Methodology can be added to QUERIES dict as "methodology" field
