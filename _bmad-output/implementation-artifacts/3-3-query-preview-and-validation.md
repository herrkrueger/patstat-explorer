# Story 3.3: Query Preview and Validation

Status: ready-for-dev

## Story

As a data-savvy PATLIB professional (Klaus),
I want to preview how my query will appear before submitting,
so that I can verify it looks correct for other users.

## Acceptance Criteria

1. **Given** a user has entered query and metadata
   **When** they click "Preview"
   **Then** they see exactly how the query will appear in the library
   **And** they see how parameters will render as controls
   **And** they can test the query with sample parameters

2. **Given** a user submits a query for preview
   **When** validation runs
   **Then** SQL syntax is validated against BigQuery
   **And** required fields are checked for completeness
   **And** clear error messages explain any issues

3. **Given** validation passes
   **When** user tests the query
   **Then** query executes with sample/default parameters
   **And** results display using standard patterns
   **And** execution time is measured and displayed

## Tasks / Subtasks

- [ ] Task 1: Create preview mode UI (AC: #1)
  - [ ] Show query card as it would appear on landing
  - [ ] Show parameter block as it would appear on detail page
  - [ ] Display estimated execution time
  - [ ] Show tags and category assignment

- [ ] Task 2: Render parameter controls in preview (AC: #1)
  - [ ] Generate st widgets from parameter definitions
  - [ ] Show with default values pre-filled
  - [ ] Demonstrate the user experience

- [ ] Task 3: Add "Test Query" functionality (AC: #1, #3)
  - [ ] Execute query with current parameter values
  - [ ] Show results in preview mode
  - [ ] Display execution time
  - [ ] Show insight headline generation

- [ ] Task 4: Implement SQL validation (AC: #2)
  - [ ] Use BigQuery dry-run to validate syntax
  - [ ] Check for common SQL errors
  - [ ] Validate table names exist
  - [ ] Check parameter placeholders are valid

- [ ] Task 5: Implement metadata validation (AC: #2)
  - [ ] Verify all required fields present
  - [ ] Check title format (question style recommended)
  - [ ] Validate tags and category
  - [ ] Check parameter definitions complete

- [ ] Task 6: Display validation results (AC: #2)
  - [ ] Show success/error status clearly
  - [ ] List specific issues found
  - [ ] Provide guidance on fixing issues
  - [ ] Block submission until validation passes

## Dev Notes

### Preview Layout

```
┌──────────────────────────────────────────────────────────┐
│  Preview Your Query                                      │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  📋 Query Card Preview (Landing Page)                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Q??: Your Query Title Here?                        │  │
│  │ Your description text...                           │  │
│  │ [PATLIB] [BUSINESS]                       ~5s      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  📊 Detail Page Preview                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Parameters                                         │  │
│  │ [2015────2024] [EP, US, CN ▼] [Run Test Query]    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Validation Status: ✅ All checks passed                 │
│                                                          │
│  [← Edit Query]  [Test Query]  [Submit Query →]          │
└──────────────────────────────────────────────────────────┘
```

### SQL Validation via Dry Run

```python
from google.cloud import bigquery

def validate_sql_syntax(sql: str, client: bigquery.Client) -> dict:
    """Validate SQL using BigQuery dry run."""
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    try:
        query_job = client.query(sql, job_config=job_config)
        return {
            'valid': True,
            'bytes_processed': query_job.total_bytes_processed,
            'error': None
        }
    except Exception as e:
        return {
            'valid': False,
            'bytes_processed': 0,
            'error': str(e)
        }
```

### Dynamic Widget Generation

```python
def render_parameter_widget(param: dict):
    """Generate Streamlit widget from parameter definition."""
    if param['type'] == 'text':
        return st.text_input(param['label'], value=param['default'])
    elif param['type'] == 'number':
        return st.number_input(
            param['label'],
            min_value=param.get('min'),
            max_value=param.get('max'),
            value=param['default']
        )
    elif param['type'] == 'select':
        return st.selectbox(param['label'], options=param['options'])
    elif param['type'] == 'multiselect':
        return st.multiselect(
            param['label'],
            options=param['options'],
            default=param['default']
        )
    elif param['type'] == 'range':
        return st.slider(
            param['label'],
            min_value=param.get('min', 1990),
            max_value=param.get('max', 2024),
            value=param['default']
        )
```

### Validation Checklist

```python
def validate_contribution(contribution: dict) -> list:
    """Return list of validation issues."""
    issues = []

    # Required fields
    if not contribution.get('title'):
        issues.append("❌ Title is required")
    if not contribution.get('description'):
        issues.append("❌ Description is required")
    if not contribution.get('sql'):
        issues.append("❌ SQL query is required")
    if not contribution.get('tags'):
        issues.append("❌ Select at least one stakeholder tag")
    if not contribution.get('category'):
        issues.append("❌ Select a category")

    # SQL parameter matching
    sql_params = detect_sql_parameters(contribution.get('sql', ''))
    defined_params = [p['name'] for p in contribution.get('parameters', [])]
    undefined = set(sql_params) - set(defined_params)
    if undefined:
        issues.append(f"⚠️ SQL parameters not defined: {', '.join(undefined)}")

    return issues
```

### Project Structure Notes

- Preview rendering uses same patterns as main app
- SQL validation requires BigQuery client
- Test execution uses same run_query function
- Validation happens before preview display

### References

- [Source: PRD FR28] Users can preview contributed query
- [Source: PRD FR29] System validates SQL syntax
- [Source: app.py:419-587] Detail page rendering patterns
- [Source: app.py:627-640] Query execution function

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
