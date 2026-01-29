# Story 4.4: Save AI Query to Favorites

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to save successful AI-generated queries,
so that I can reuse them without regenerating.

## Acceptance Criteria

1. **Given** an AI-generated query produces good results
   **When** user clicks "Save to Favorites"
   **Then** the query is saved with a user-provided name
   **And** saved queries appear in a "My Queries" section
   **And** saved queries can be run like any library query

2. **Given** a user has saved queries
   **When** browsing the library
   **Then** "My Queries" section appears on landing page
   **And** saved queries show with "★" or similar indicator
   **And** user can delete saved queries

3. **Given** session-based storage in MVP
   **When** user saves a query
   **Then** query persists in browser local storage
   **And** queries survive page refresh (within same browser)
   **And** user is informed about storage limitations

## Tasks / Subtasks

- [ ] Task 1: Add "Save to Favorites" button (AC: #1)
  - [ ] Position button in AI query results area
  - [ ] Only show when results are satisfactory
  - [ ] Disable if query hasn't been previewed

- [ ] Task 2: Create save dialog (AC: #1)
  - [ ] Prompt for query name
  - [ ] Auto-suggest name from request
  - [ ] Optional: add tags/category
  - [ ] Confirm save action

- [ ] Task 3: Implement local storage persistence (AC: #3)
  - [ ] Use browser localStorage via streamlit-js-eval or similar
  - [ ] Serialize query data as JSON
  - [ ] Load saved queries on app start
  - [ ] Handle storage quota limits

- [ ] Task 4: Create "My Queries" section (AC: #2)
  - [ ] Add section on landing page
  - [ ] Show saved queries with star indicator
  - [ ] Include delete button for each
  - [ ] Show when queries are empty: "No saved queries yet"

- [ ] Task 5: Enable running saved queries (AC: #1, #2)
  - [ ] Clicking saved query opens detail view
  - [ ] Display like regular query with parameters
  - [ ] Allow re-running with modifications

- [ ] Task 6: Add storage limitation notice (AC: #3)
  - [ ] Info message about browser storage
  - [ ] Note that queries don't sync across devices
  - [ ] Offer export option for backup

## Dev Notes

### Save Dialog UI

```
┌──────────────────────────────────────────────────────────┐
│  ⭐ Save to Favorites                                    │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  Name your query:                                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Top wind energy filers in Germany                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Category: [Technology ▼]                                │
│  Tags: [PATLIB] [BUSINESS]                               │
│                                                          │
│  [Cancel]  [Save Query]                                  │
└──────────────────────────────────────────────────────────┘
```

### My Queries Section (Landing Page)

```
┌──────────────────────────────────────────────────────────┐
│  ⭐ My Queries                                           │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  ┌────────────────────────────────────────────┐  [🗑️]   │
│  │ ⭐ Top wind energy filers in Germany      │          │
│  │ AI-generated query saved Jan 28            │          │
│  └────────────────────────────────────────────┘          │
│                                                          │
│  ┌────────────────────────────────────────────┐  [🗑️]   │
│  │ ⭐ Medical device trends by country        │          │
│  │ AI-generated query saved Jan 27            │          │
│  └────────────────────────────────────────────┘          │
│                                                          │
│  ℹ️ Saved locally in your browser                        │
└──────────────────────────────────────────────────────────┘
```

### Local Storage Implementation

```python
# Using streamlit-javascript or similar approach
from streamlit_js_eval import streamlit_js_eval

def save_to_local_storage(key: str, data: dict):
    """Save data to browser localStorage."""
    json_data = json.dumps(data)
    streamlit_js_eval(js_expressions=f"localStorage.setItem('{key}', '{json_data}')")

def load_from_local_storage(key: str) -> dict:
    """Load data from browser localStorage."""
    result = streamlit_js_eval(js_expressions=f"localStorage.getItem('{key}')")
    if result:
        return json.loads(result)
    return None

def get_saved_queries() -> list:
    """Get all saved queries from localStorage."""
    data = load_from_local_storage('patstat_favorites')
    return data.get('queries', []) if data else []

def add_saved_query(query: dict):
    """Add a query to favorites."""
    queries = get_saved_queries()
    queries.append({
        **query,
        'id': f"FAV_{len(queries) + 1:03d}",
        'saved_at': datetime.now().isoformat(),
        'is_favorite': True
    })
    save_to_local_storage('patstat_favorites', {'queries': queries})

def remove_saved_query(query_id: str):
    """Remove a query from favorites."""
    queries = get_saved_queries()
    queries = [q for q in queries if q.get('id') != query_id]
    save_to_local_storage('patstat_favorites', {'queries': queries})
```

### Saved Query Structure

```python
saved_query = {
    'id': 'FAV_001',
    'name': 'Top wind energy filers in Germany',
    'original_request': 'Show me top wind energy filers...',
    'sql': 'SELECT ...',
    'explanation': 'This query finds...',
    'category': 'Technology',
    'tags': ['PATLIB', 'BUSINESS'],
    'saved_at': '2024-01-28T10:30:00',
    'is_favorite': True,
    'source': 'ai_generated'
}
```

### Alternative: Session State Only (Simpler MVP)

If localStorage proves complex, fall back to session state with warning:

```python
def save_query_session(query: dict):
    """Save to session state (lost on refresh)."""
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []
    st.session_state['favorites'].append(query)

# With clear warning:
st.warning("Note: Saved queries are stored in your browser session and will be lost when you close this tab.")
```

### Project Structure Notes

- Favorites in localStorage for persistence
- Display alongside library queries
- Export option for backup
- Consider adding to requirements.txt: streamlit-javascript

### References

- [Source: PRD FR35] Save AI queries to favorites
- [Source: UX Design - Journey 4] Save to favorites step
- [Source: app.py:341-391] Landing page structure for My Queries section
- [Source: PRD - Out of Scope] No user accounts, session-based

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
