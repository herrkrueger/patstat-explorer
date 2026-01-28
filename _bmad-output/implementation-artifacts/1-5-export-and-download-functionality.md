# Story 1.5: Export & Download Functionality

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to export charts and data for my client,
so that I can deliver professional results without editing.

## Acceptance Criteria

1. **Given** query has chart
   **When** user clicks "Download Chart"
   **Then** chart exports as PNG, presentation-ready

2. **Given** query has data
   **When** user clicks "Download Data"
   **Then** CSV exports with all columns, proper formatting

## Tasks

- [ ] Task 1: Add chart PNG export via Altair save
- [ ] Task 2: Enhance CSV download with proper date/number formatting
- [ ] Task 3: Add download buttons below results
- [ ] Task 4: Generate meaningful filenames

## Dev Notes

- Altair charts can export to PNG via altair_saver or vl-convert
- CSV already exists, enhance formatting
- Filename pattern: {query_id}_{title}_{date}.{ext}
