# Story 3.1: Query Submission Interface

Status: ready-for-dev

## Story

As a data-savvy PATLIB professional (Klaus),
I want to submit my own SQL queries to the library,
so that I can share my expertise with 300 PATLIB centres.

## Acceptance Criteria

1. **Given** a user navigates to "Contribute Query" section
   **When** the contribution form loads
   **Then** a text area is available for SQL query input
   **And** fields are provided for: title, description, tags
   **And** the interface explains the contribution process

2. **Given** a user enters a SQL query
   **When** they fill in the metadata
   **Then** title field accepts question-style input
   **And** description field accepts detailed explanation
   **And** tags can be selected from existing categories (multi-select)
   **And** category selection is available (Competitors, Trends, Regional, Technology)

3. **Given** a user is filling out the form
   **When** required fields are empty
   **Then** validation feedback indicates what's missing
   **And** form cannot proceed until required fields are filled

## Tasks / Subtasks

- [ ] Task 1: Add "Contribute Query" navigation option (AC: #1)
  - [ ] Add new page/section to landing page
  - [ ] Create "Contribute" button or pill
  - [ ] Set up navigation to contribution form

- [ ] Task 2: Create SQL query input area (AC: #1)
  - [ ] Add st.text_area for SQL input
  - [ ] Set appropriate height for SQL editing
  - [ ] Add syntax highlighting guidance
  - [ ] Include placeholder with example query structure

- [ ] Task 3: Create metadata input fields (AC: #2)
  - [ ] Title field (text input, required)
  - [ ] Description field (text area, required)
  - [ ] Tags multiselect (PATLIB, BUSINESS, UNIVERSITY)
  - [ ] Category selectbox (Competitors, Trends, Regional, Technology)
  - [ ] Explanation field (optional, for detailed notes)

- [ ] Task 4: Add contribution process explanation (AC: #1)
  - [ ] Add expander with guidelines
  - [ ] Explain what makes a good query
  - [ ] Note that queries should work with PATSTAT BigQuery
  - [ ] Explain parameter syntax for dynamic queries

- [ ] Task 5: Implement form validation (AC: #3)
  - [ ] Validate SQL is not empty
  - [ ] Validate title is not empty
  - [ ] Validate description is not empty
  - [ ] Validate at least one tag selected
  - [ ] Show validation messages inline

## Dev Notes

### Page Layout

```
┌──────────────────────────────────────────────────────────┐
│  ← Back to Questions                                     │
│  ─────────────────────────────────────────────────────── │
│  Contribute a Query                                      │
│                                                          │
│  Share your SQL expertise with 300 PATLIB centres!       │
│                                                          │
│  [▸ Contribution Guidelines]                             │
│                                                          │
│  Query Details                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Title (question format): _________________________│  │
│  │                                                    │  │
│  │ Description: ____________________________________│  │
│  │                                                    │  │
│  │ Tags: [PATLIB] [BUSINESS] [UNIVERSITY]           │  │
│  │ Category: [Competitors ▼]                         │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  SQL Query                                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ SELECT ...                                        │  │
│  │ FROM tls201_appln a                               │  │
│  │ WHERE ...                                         │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  [Continue to Parameters →]                              │
└──────────────────────────────────────────────────────────┘
```

### Navigation Structure

Use session state to manage contribution flow:
```python
st.session_state['contribution_step'] = 1  # 1: Input, 2: Parameters, 3: Preview, 4: Submit
```

### Form State Management

Store contribution data in session state:
```python
st.session_state['contribution'] = {
    'title': '',
    'description': '',
    'tags': [],
    'category': '',
    'sql': '',
    'parameters': [],
    'explanation': ''
}
```

### Validation Function

```python
def validate_contribution_step1():
    """Validate basic query information."""
    contrib = st.session_state.get('contribution', {})
    errors = []
    if not contrib.get('title', '').strip():
        errors.append("Title is required")
    if not contrib.get('description', '').strip():
        errors.append("Description is required")
    if not contrib.get('sql', '').strip():
        errors.append("SQL query is required")
    if not contrib.get('tags', []):
        errors.append("Select at least one stakeholder tag")
    return errors
```

### Project Structure Notes

- Add new contribution page handling in: `app.py`
- Create new file if needed: `contribution.py` for form logic
- Store contributions in session state (no persistence in MVP)
- Contribution guidelines as static markdown

### References

- [Source: PRD FR25] Users can submit new queries to library
- [Source: PRD FR26] Users can provide metadata
- [Source: UX Design - Journey 2] Klaus's contribution journey
- [Source: queries_bq.py] QUERIES structure for reference

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
