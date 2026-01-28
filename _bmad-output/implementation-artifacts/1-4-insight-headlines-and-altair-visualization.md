# Story 1.4: Insight Headlines & Altair Visualization

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to see the key finding immediately with a beautiful chart,
so that I understand the answer at a glance and can impress my client.

## Acceptance Criteria

1. **Given** query returns results
   **Then** insight headline appears first, in bold
   **And** headline is complete sentence answering the query's question
   **And** headline appears above any chart or data

2. **Given** results include visualization
   **Then** Altair chart displays with color palette (#1E3A5F, #0A9396, #FFB703)
   **And** chart renders within 2 seconds
   **And** multi-series data uses distinct colors
   **And** chart includes axis labels, legend, tooltips

3. **Given** results include KPI metrics
   **Then** metric cards show values with delta indicators
   **And** positive=green, negative=red

## Tasks

- [ ] Task 1: Add `generate_insight_headline()` function
- [ ] Task 2: Create Altair chart renderer with consistent styling
- [ ] Task 3: Add metric cards with delta indicators
- [ ] Task 4: Define color palette constants
- [ ] Task 5: Integrate into results display flow

## Dev Notes

- Altair for charts (export-ready)
- Color palette: PRIMARY=#1E3A5F, SECONDARY=#0A9396, ACCENT=#FFB703
- Insight headline generation can be simple template-based for now
