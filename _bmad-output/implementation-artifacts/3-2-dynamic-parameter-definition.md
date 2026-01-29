# Story 3.2: Dynamic Parameter Definition

Status: ready-for-dev

## Story

As a data-savvy PATLIB professional (Klaus),
I want to define which parts of my query should be dynamic parameters,
so that other users can customize the query for their context.

## Acceptance Criteria

1. **Given** a user is submitting a query
   **When** they define parameters
   **Then** they can specify parameter name, type (text, number, select, multiselect, range)
   **And** they can provide default values
   **And** they can mark parameters as required or optional
   **And** parameter placeholders in SQL use @parameter_name syntax

2. **Given** a parameter is defined
   **When** the user provides options for select/multiselect types
   **Then** they can enter comma-separated values
   **Or** they can reference predefined option sets (JURISDICTIONS, TECH_FIELDS)

3. **Given** a user has defined parameters
   **When** viewing the SQL
   **Then** placeholders are highlighted in the SQL preview
   **And** user can verify parameters match their SQL

## Tasks / Subtasks

- [ ] Task 1: Create parameter definition UI (AC: #1)
  - [ ] Add "Define Parameters" section
  - [ ] Button to "Add Parameter"
  - [ ] List of defined parameters with edit/delete
  - [ ] Dynamic form for each parameter

- [ ] Task 2: Implement parameter type selection (AC: #1)
  - [ ] Text input type
  - [ ] Number input type (with min/max)
  - [ ] Select dropdown type
  - [ ] Multiselect type
  - [ ] Range slider type (for years)

- [ ] Task 3: Handle default values per type (AC: #1)
  - [ ] Text: string default
  - [ ] Number: numeric default with validation
  - [ ] Select: one of the options
  - [ ] Multiselect: subset of options
  - [ ] Range: tuple of (min, max) defaults

- [ ] Task 4: Handle select/multiselect options (AC: #2)
  - [ ] Text area for comma-separated values
  - [ ] Option to use predefined sets
  - [ ] JURISDICTIONS reference
  - [ ] TECH_FIELDS reference

- [ ] Task 5: SQL placeholder highlighting (AC: #3)
  - [ ] Parse SQL for @parameter patterns
  - [ ] Show list of detected placeholders
  - [ ] Warn if SQL placeholder doesn't match defined parameter
  - [ ] Warn if defined parameter not found in SQL

## Dev Notes

### Parameter Definition Schema

```python
parameter = {
    'name': 'year_start',           # Must match @year_start in SQL
    'label': 'Start Year',          # Display label
    'type': 'number',               # text, number, select, multiselect, range
    'required': True,
    'default': 2015,
    'options': None,                # For select/multiselect
    'options_ref': None,            # 'JURISDICTIONS' or 'TECH_FIELDS'
    'min': 1990,                    # For number/range
    'max': 2024,                    # For number/range
    'help': 'Select the starting year'
}
```

### Parameter UI Layout

```
┌──────────────────────────────────────────────────────────┐
│  Define Parameters                                       │
│                                                          │
│  Your SQL can include @parameter placeholders that       │
│  users can customize when running the query.             │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Parameter 1: year_start                        [🗑️] │ │
│  │ ─────────────────────────────────────────────────── │ │
│  │ Name: [year_start    ]  Label: [Start Year   ]     │ │
│  │ Type: [Number ▼]        Required: [✓]              │ │
│  │ Default: [2015]  Min: [1990]  Max: [2024]          │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  [+ Add Parameter]                                       │
│                                                          │
│  Detected in SQL: @year_start, @year_end, @jurisdictions │
│  ⚠️ @jurisdictions not defined - add parameter?         │
└──────────────────────────────────────────────────────────┘
```

### SQL Placeholder Detection

```python
import re

def detect_sql_parameters(sql: str) -> list:
    """Extract @parameter names from SQL."""
    pattern = r'@(\w+)'
    return list(set(re.findall(pattern, sql)))

def validate_parameters(sql: str, defined_params: list) -> dict:
    """Check SQL placeholders match defined parameters."""
    sql_params = set(detect_sql_parameters(sql))
    defined_names = set(p['name'] for p in defined_params)

    return {
        'undefined': sql_params - defined_names,  # In SQL but not defined
        'unused': defined_names - sql_params,      # Defined but not in SQL
        'valid': sql_params & defined_names        # Matched
    }
```

### Predefined Option References

```python
PREDEFINED_OPTIONS = {
    'JURISDICTIONS': ['EP', 'US', 'CN', 'JP', 'KR', 'DE', 'FR', 'GB', 'WO'],
    'TECH_FIELDS': list(TECH_FIELDS.keys()),  # From app.py
}
```

### Project Structure Notes

- Parameter definition UI in contribution flow
- Store parameters in session state with contribution data
- Reference JURISDICTIONS from app.py
- Reference TECH_FIELDS from app.py

### References

- [Source: PRD FR27] Users can define dynamic parameters
- [Source: app.py:107-147] TECH_FIELDS reference data
- [Source: app.py:107] JURISDICTIONS list
- [Source: queries_bq.py:975-1013] DQ01 parameters as example

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
