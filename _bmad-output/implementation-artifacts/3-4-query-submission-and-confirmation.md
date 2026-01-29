# Story 3.4: Query Submission and Confirmation

Status: ready-for-dev

## Story

As a data-savvy PATLIB professional (Klaus),
I want confirmation when my query is successfully added,
so that I know my contribution is available for others.

## Acceptance Criteria

1. **Given** a user has a valid query ready to submit
   **When** they click "Submit Query"
   **Then** the query is added to the library (session-based in MVP)
   **And** a confirmation message appears: "Thank you for your contribution!"
   **And** the new query ID is shown (e.g., "Your query is now Q42")

2. **Given** a query has been submitted
   **When** confirmation displays
   **Then** a link to view the query is provided
   **And** option to share the link with colleagues is available
   **And** user can navigate back to contribute another query

3. **Given** MVP constraints (no database persistence)
   **When** a query is submitted
   **Then** it is added to QUERIES dict in memory
   **And** it appears in the library for current session
   **And** user is informed that persistence is coming in future version

## Tasks / Subtasks

- [ ] Task 1: Implement query submission logic (AC: #1)
  - [ ] Generate new query ID (Q + next number)
  - [ ] Format contribution as QUERIES dict entry
  - [ ] Add to runtime QUERIES dict
  - [ ] Store in session state for session persistence

- [ ] Task 2: Create confirmation UI (AC: #1, #2)
  - [ ] Display success message with green styling
  - [ ] Show assigned query ID
  - [ ] Provide link to view the new query
  - [ ] Add "Contribute Another" button

- [ ] Task 3: Add share functionality (AC: #2)
  - [ ] Generate shareable query reference
  - [ ] Copy to clipboard button for query ID
  - [ ] Note about session-based availability

- [ ] Task 4: Handle MVP persistence limitations (AC: #3)
  - [ ] Display info about session-only storage
  - [ ] Explain future persistence plans
  - [ ] Offer to export query as JSON for backup

- [ ] Task 5: Test complete contribution flow (AC: #1, #2, #3)
  - [ ] Submit test query
  - [ ] Verify appears in library
  - [ ] Verify navigation to new query works
  - [ ] Verify query executes correctly

## Dev Notes

### Submission Process

```python
def submit_contribution(contribution: dict) -> str:
    """Add contribution to QUERIES and return new query ID."""
    # Generate next available ID
    existing_ids = [int(qid[1:]) for qid in QUERIES.keys() if qid.startswith('Q') and qid[1:].isdigit()]
    next_num = max(existing_ids, default=0) + 1
    new_id = f"Q{next_num:02d}"

    # Format as QUERIES entry
    new_query = {
        'title': contribution['title'],
        'tags': contribution['tags'],
        'category': contribution['category'],
        'description': contribution['description'],
        'explanation': contribution.get('explanation', ''),
        'key_outputs': contribution.get('key_outputs', []),
        'estimated_seconds_first_run': contribution.get('estimated_time', 5),
        'estimated_seconds_cached': contribution.get('estimated_time', 2),
        'sql': contribution['sql'],
        'parameters': contribution.get('parameters', []),
        'contributed': True,  # Flag as user-contributed
        'contributor_session': st.session_state.get('session_id', 'unknown')
    }

    # Add to QUERIES
    QUERIES[new_id] = new_query

    # Also store in session for persistence within session
    if 'contributed_queries' not in st.session_state:
        st.session_state['contributed_queries'] = {}
    st.session_state['contributed_queries'][new_id] = new_query

    return new_id
```

### Confirmation UI Layout

```
┌──────────────────────────────────────────────────────────┐
│  🎉 Query Submitted Successfully!                        │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  Thank you for your contribution!                        │
│                                                          │
│  Your query has been added to the library:               │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Query ID: Q42                                      │  │
│  │ Title: "Which companies collaborate most?"         │  │
│  │ Category: Competitors                              │  │
│  │ Tags: PATLIB, BUSINESS                             │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  [View Your Query]  [Copy Query ID]  [Contribute Another]│
│                                                          │
│  ────────────────────────────────────────────────────────│
│  ℹ️ Note: Your query is available for this session.      │
│  Persistent storage coming in a future update.           │
│  [Export as JSON] for backup                             │
└──────────────────────────────────────────────────────────┘
```

### Export for Backup

```python
def export_contribution_json(query_id: str) -> str:
    """Export contributed query as JSON for user backup."""
    query = QUERIES.get(query_id, {})
    return json.dumps(query, indent=2)
```

### Session ID Generation

```python
import uuid

def get_session_id():
    """Get or create session ID for contribution tracking."""
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())[:8]
    return st.session_state['session_id']
```

### Post-MVP Considerations

For future persistence:
- Store in JSON file in repository (requires PR workflow)
- Use Streamlit Cloud secrets for database connection
- Implement moderation queue (optional)

### Project Structure Notes

- Submission modifies QUERIES dict in queries_bq.py (runtime)
- Session state stores contributions for session persistence
- Future: JSON file storage or database

### References

- [Source: PRD FR25-FR29] Query contribution requirements
- [Source: UX Design - Journey 2] Klaus contribution journey
- [Source: queries_bq.py:18] QUERIES dict structure
- [Source: PRD - Out of Scope] No moderation workflow in MVP

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
