# Story 4.3: Query Preview and Refinement

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to preview AI-generated query results and refine if needed,
so that I can ensure the query answers my actual question.

## Acceptance Criteria

1. **Given** an AI-generated SQL query is displayed
   **When** user clicks "Preview Results"
   **Then** the query executes with a sample/limited result set
   **And** results display using the same patterns as regular queries
   **And** user can verify the output matches their intent

2. **Given** the results don't match expectations
   **When** user wants to refine
   **Then** they can modify their natural language input
   **And** click "Regenerate Query" to get an updated SQL
   **And** previous versions are not lost (can toggle back)

3. **Given** multiple refinement attempts
   **When** user wants to compare versions
   **Then** version history shows previous attempts
   **And** user can select any previous version to view/use

## Tasks / Subtasks

- [ ] Task 1: Implement "Preview Results" functionality (AC: #1)
  - [ ] Add preview button below generated SQL
  - [ ] Execute query with LIMIT if not present
  - [ ] Show results using standard display patterns
  - [ ] Show execution time and row count

- [ ] Task 2: Display preview results (AC: #1)
  - [ ] Generate insight headline from results
  - [ ] Render chart if appropriate
  - [ ] Show data table in expander
  - [ ] Reuse existing render_chart and generate_insight_headline

- [ ] Task 3: Enable request refinement (AC: #2)
  - [ ] Keep original request in editable text area
  - [ ] Add "Refine & Regenerate" button
  - [ ] Preserve generated SQL while editing request
  - [ ] Clear results on new generation

- [ ] Task 4: Implement version history (AC: #2, #3)
  - [ ] Store each generation attempt in session state
  - [ ] Include: request, SQL, explanation, timestamp
  - [ ] Maximum 5 versions stored

- [ ] Task 5: Create version selector UI (AC: #3)
  - [ ] Show version history in sidebar/expander
  - [ ] Allow switching between versions
  - [ ] Show diff or summary of changes

## Dev Notes

### Preview Flow Layout

```
┌──────────────────────────────────────────────────────────┐
│  Generated Query                                         │
│  ─────────────────────────────────────────────────────── │
│  [SQL and explanation as shown in Story 4.2]             │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  📊 Preview Results                                      │
│                                                          │
│  **Siemens leads with 847 wind energy patents**          │
│                                                          │
│  [Chart visualization]                                   │
│                                                          │
│  Completed in 3.2s | 10 rows returned                    │
│                                                          │
│  [▸ View Data Table]                                     │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  Not quite right?                                        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ [Original request, now editable...]               │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  [Refine & Regenerate]  [View Previous Versions (3)]     │
└──────────────────────────────────────────────────────────┘
```

### Version History Structure

```python
# Store in session state
st.session_state['ai_query_versions'] = [
    {
        'version': 1,
        'timestamp': '2024-01-28 10:30',
        'request': "Show me top wind energy filers...",
        'sql': "SELECT ...",
        'explanation': "This query...",
        'notes': "None",
        'preview_results': None  # DataFrame if previewed
    },
    # ... more versions
]
```

### Preview with Safety LIMIT

```python
def execute_preview(sql: str, client) -> tuple:
    """Execute query with safety LIMIT for preview."""
    # Ensure LIMIT exists
    if 'LIMIT' not in sql.upper():
        # Find end of query and add LIMIT
        sql = sql.rstrip().rstrip(';') + ' LIMIT 100'

    return run_query(client, sql)
```

### Version Selector UI

```python
def render_version_selector():
    """Show version history for AI queries."""
    versions = st.session_state.get('ai_query_versions', [])

    if len(versions) > 1:
        with st.expander(f"Previous Versions ({len(versions) - 1})"):
            for i, version in enumerate(reversed(versions[:-1])):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"v{version['version']} - {version['timestamp']}")
                    st.text(version['request'][:50] + "..." if len(version['request']) > 50 else version['request'])
                with col2:
                    if st.button("Use", key=f"use_v{version['version']}"):
                        restore_version(version)
```

### Refinement Flow

```python
def handle_refinement():
    """Handle query refinement process."""
    # Get current request (may be edited)
    refined_request = st.session_state.get('current_request', '')

    if st.button("Refine & Regenerate"):
        # Save current version to history
        save_current_to_history()

        # Generate new query
        new_result = generate_sql_query(refined_request, get_claude_client())

        # Update current state
        st.session_state['current_generation'] = new_result
        st.session_state['preview_results'] = None  # Clear old results

        st.rerun()
```

### Integration with Standard Display

Reuse existing functions from app.py:
- `generate_insight_headline(df, query_info)` for headlines
- `render_chart(df, query_info)` for visualization
- `render_metrics(df, query_info)` for metric cards

Create query_info structure from AI-generated content:
```python
def create_query_info_from_ai(generation: dict) -> dict:
    """Create query_info dict from AI generation for display functions."""
    return {
        'title': 'AI-Generated Query',
        'category': 'Technology',  # Could try to detect from request
        'description': generation.get('explanation', ''),
        'sql': generation.get('sql', '')
    }
```

### Project Structure Notes

- Version history in session state
- Preview uses standard display patterns
- Refinement preserves context
- Limited to 5 versions to avoid memory bloat

### References

- [Source: PRD FR33] Preview AI query results
- [Source: PRD FR34] Refine and regenerate
- [Source: app.py:215-250] Insight headline generation
- [Source: app.py:253-296] Chart rendering
- [Source: UX Design - Experience Mechanics] Understand phase patterns

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
