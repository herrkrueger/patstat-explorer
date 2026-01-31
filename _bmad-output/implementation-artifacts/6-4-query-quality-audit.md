---
status: ready-for-dev
epic: 6
story: 4
name: query-quality-audit
---

# Story 6.4: Query Quality Audit (Content Polish)

**As a** Product Owner,
**I want** to review and polish every query in the library before release,
**So that** PATLIB staff get useful, well-presented insights from day one.

## What This Story Is

An **AI-assisted manual review** of all 42 queries. For each query:
1. Run it with default parameters
2. Check if results make sense
3. Check if the chart renders well
4. Polish parameters, defaults, column names, visualization config as needed
5. Move to the next query

This is a **content quality pass**, not a test automation story.

## What This Story Is NOT

- Building automated test infrastructure
- Adding "Under Maintenance" badges
- Creating validation frameworks
- Comprehensive edge-case testing

## Acceptance Criteria

### 1. Every Query Reviewed
- **Given** the 42 queries in `queries_bq.py`
- **When** the audit is complete
- **Then** each query has been executed at least once
- **And** any issues found have been fixed or documented

### 2. Quality Checklist Per Query
For each query, verify:
- [ ] Query executes without error
- [ ] Results are non-empty (with sensible parameters)
- [ ] Column names are user-friendly (no `f0_`, `_1`, etc.)
- [ ] Chart renders appropriately (right type, readable labels)
- [ ] Parameter defaults make sense for the use case
- [ ] Description matches what the query actually does

### 3. Fixes Applied
- **Given** issues found during review
- **When** they are fixable within scope
- **Then** fix them directly in `queries_bq.py`
- **And** document what was changed in the audit log

## Audit Process

### Setup
1. Open the app: `streamlit run app.py`
2. Have `queries_bq.py` open in editor
3. Work through queries in order: Q01, Q02, ... Q42

### Per Query Checklist

```markdown
## Q01: [Title]
- [ ] Executed successfully
- [ ] Row count: ___ (sensible?)
- [ ] Column names clear
- [ ] Chart type appropriate
- [ ] Chart readable (labels, colors)
- [ ] Parameters: defaults make sense
- [ ] Description accurate

**Issues found:**
- (none / list issues)

**Fixes applied:**
- (none / list fixes)
```

### Common Fixes Expected
- Rename columns: `COUNT(*)` → `patent_count`
- Adjust visualization config: add `"type": "bar"` or `"type": "line"`
- Fix parameter defaults: year range, jurisdictions
- Update descriptions to match actual output
- Add missing `explanation` text

## Queries to Review

| ID | Title | Category |
|----|-------|----------|
| Q01 | Overall PATSTAT database statistics | Trends |
| Q02 | Patent applications by filing year | Trends |
| Q03 | Top applicants by patent count | Competitors |
| Q04 | Technology distribution (IPC sections) | Technology |
| Q05 | Sample patent records | Technology |
| Q06 | Country patent activity | Competitors |
| Q07 | Green technology trends | Trends |
| Q08 | Most active technology fields | Technology |
| Q09 | Patent family sizes | Trends |
| Q10 | Citation analysis | Technology |
| Q11 | Top patent applicants | Competitors |
| Q12 | MedTech competitor analysis | Competitors |
| Q13 | University patent activity | Competitors |
| Q14 | IPC class deep dive | Technology |
| Q15 | German states medical tech | Regional |
| Q16 | Regional patent activity | Regional |
| Q17-Q42 | (EPO training queries) | Various |

## Output Artifacts

1. **Updated `queries_bq.py`** - with all fixes applied
2. **Audit Log** - document in this story file what was reviewed and changed

## Audit Log

### Session 1: 2026-01-31 (Q01-Q13)

#### Q01: Overall PATSTAT database statistics
- [x] Reviewed
- Changes: Added metrics_grid display mode, extended query with Publications/Families/CPC/Citations/Legal Events, year range defaults to 1782-2024
- Note: Significant enhancement, may be over-engineered

#### Q02: Which patent offices are most active?
- [x] Reviewed - Works fine, no changes needed

#### Q03: How have patent applications changed over time?
- [x] Reviewed
- Changes: Added stacked bar chart (granted vs not_granted), fixed SQL display to show sql_template
- Todo: avg_days_to_grant calculation removed (buggy), fix later

#### Q04: What are the most common technology classes?
- [x] Reviewed - Works fine
- Todo: Add IPC text description, not only the symbol

#### Q05: What do sample patent records look like?
- [x] Reviewed
- Changes: Chart disabled (made no sense for sample data)
- Todo: Extend table with more data (applicant count, inventor count, title)

#### Q06: Which countries lead in patent filing activity?
- [x] Reviewed - Works but has conceptual issue
- Todo: Fix query mixing person_ctry_code (applicant origin) with appln_auth filter (patent office)

#### Q07: What are the green technology trends by country?
- [x] Reviewed - Works fine, no changes needed

#### Q08: Which technology fields are most active?
- [x] Reviewed - Works great, no changes needed

#### Q09: How are patent families distributed?
- [x] Reviewed - Works fine, no changes needed

#### Q10: Who is building AI-assisted diagnostics portfolios?
- [x] Reviewed
- Changes: Fixed timing estimates (25s first run, 9s cached)

#### Q11: Who are the top patent filers?
- [x] Reviewed - Works fine, no changes needed

#### Q12: Where do MedTech competitors file their patents?
- [x] Reviewed
- Changes: Chart disabled (table data not suitable for chart)

#### Q13: Which patents are most frequently cited?
- [x] Reviewed
- Changes: Fixed timing estimates (22s first run, 3s cached)

#### Q14-Q42: Not yet reviewed
- [ ] To be continued in next session

### Infrastructure Improvements Made
- Added `metrics_grid` display mode for statistics overview
- Added `stacked_bar` chart type with column transformation
- Added `visualization: None` option to disable charts
- Added `todo` field to queries for future improvements
- Fixed View SQL Query to show sql_template instead of static sql
- Updated YEAR_MIN to 1782 (actual PATSTAT earliest year)

## Dev Notes

### How to Run This Story
1. This is an interactive session - dev + AI work through queries together
2. Use the running app to see actual results and charts
3. Edit `queries_bq.py` directly when fixes are needed
4. Check changes in browser (Streamlit hot-reloads)
5. Document findings in the Audit Log section above

### Typical Session Flow
```
Dev: "Let's review Q01"
AI: [Runs query mentally or dev runs in app]
Dev: "Chart looks wrong - it's showing a bar chart but should be a line chart"
AI: "I'll update the visualization config in queries_bq.py"
[Makes edit]
Dev: "Looks good now, next query"
```

### Time Expectation
- ~5 min per query average
- 42 queries × 5 min = ~3.5 hours total
- Can be split across multiple sessions

## File List
- queries_bq.py (primary - all query definitions)
- modules/ui.py (display mode and chart enhancements)
- modules/config.py (YEAR_MIN updated)
- This story file (audit log)

## Dependencies
- None (can run before or after 6.2, 6.3)
- Requires BigQuery access to run queries

## Change Log
- 2026-01-30: Story created
- 2026-01-31: Story rewritten - clarified as AI-assisted manual content review, not test automation
- 2026-01-31: Session 1 - Reviewed Q01-Q13, added infrastructure improvements (metrics_grid, stacked_bar, todo field)
