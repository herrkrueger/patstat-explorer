# Story 4.2: AI-Generated SQL with Explanation

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to see the generated SQL with a plain-language explanation,
so that I understand what the query does even without SQL knowledge.

## Acceptance Criteria

1. **Given** the AI has generated a SQL query
   **When** the results display
   **Then** the generated SQL is shown in a code block
   **And** a plain-language explanation appears above the SQL
   **And** the explanation describes: what data is queried, how it's filtered, what the output means

2. **Given** the AI cannot generate a valid query
   **When** the error state displays
   **Then** a helpful message explains why (e.g., "I couldn't understand the technology field...")
   **And** suggestions are provided to refine the request
   **And** original request is preserved for editing

3. **Given** a generated query might have issues
   **When** reviewing the output
   **Then** warning indicators show if query might be slow or return many rows
   **And** suggestions for optimization are provided if relevant

## Tasks / Subtasks

- [ ] Task 1: Design AI response parsing (AC: #1)
  - [ ] Parse SQL from Claude response
  - [ ] Parse explanation from Claude response
  - [ ] Handle structured response format

- [ ] Task 2: Display generated SQL (AC: #1)
  - [ ] Show SQL in st.code block with SQL syntax
  - [ ] Add copy button functionality
  - [ ] Format SQL for readability

- [ ] Task 3: Display plain-language explanation (AC: #1)
  - [ ] Show explanation above SQL
  - [ ] Use clear, non-technical language
  - [ ] Structure: What it queries, How it filters, What output means

- [ ] Task 4: Handle generation failures (AC: #2)
  - [ ] Detect when AI couldn't generate valid SQL
  - [ ] Show helpful error message
  - [ ] Provide specific suggestions based on error type
  - [ ] Keep original request in input area

- [ ] Task 5: Add query quality warnings (AC: #3)
  - [ ] Detect potentially slow queries (many JOINs, no LIMIT)
  - [ ] Warn about queries that might return many rows
  - [ ] Suggest optimizations where applicable

## Dev Notes

### Response Display Layout

```
┌──────────────────────────────────────────────────────────┐
│  🤖 Generated Query                                      │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  📝 What this query does:                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │ This query finds the top 10 companies filing wind │  │
│  │ energy patents (IPC class F03D) in Germany since  │  │
│  │ 2018. It counts unique patent applications per    │  │
│  │ company and sorts by total filings.               │  │
│  │                                                    │  │
│  │ The output includes company name, country, and    │  │
│  │ patent count.                                      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  💻 SQL Query:                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │ SELECT                                            │  │
│  │   p.person_name AS company,                       │  │
│  │   COUNT(DISTINCT a.appln_id) AS patent_count      │  │
│  │ FROM tls201_appln a                               │  │
│  │ ...                                               │  │
│  └────────────────────────────────────────────────────┘  │
│  [Copy SQL]                                              │
│                                                          │
│  ⚠️ Note: Query uses multiple JOINs, may take ~10s      │
│                                                          │
│  [Preview Results]  [Refine Request]  [Save to Favorites]│
└──────────────────────────────────────────────────────────┘
```

### Claude Response Structure

Request Claude to return structured response:

```python
def generate_sql_query(user_request: str, client) -> dict:
    """Generate SQL from natural language using Claude."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=PATSTAT_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""Generate a BigQuery SQL query for this request:

{user_request}

Respond in this exact format:
EXPLANATION:
[2-3 sentences explaining what the query does in plain language]

SQL:
```sql
[Your SQL query here]
```

NOTES:
[Any warnings or suggestions, or "None" if the query is straightforward]"""
            }
        ]
    )

    return parse_ai_response(response.content[0].text)

def parse_ai_response(response_text: str) -> dict:
    """Parse structured response from Claude."""
    result = {
        'explanation': '',
        'sql': '',
        'notes': '',
        'success': True,
        'error': None
    }

    try:
        # Extract explanation
        if 'EXPLANATION:' in response_text:
            explanation_start = response_text.index('EXPLANATION:') + len('EXPLANATION:')
            explanation_end = response_text.index('SQL:')
            result['explanation'] = response_text[explanation_start:explanation_end].strip()

        # Extract SQL
        if '```sql' in response_text:
            sql_start = response_text.index('```sql') + 6
            sql_end = response_text.index('```', sql_start)
            result['sql'] = response_text[sql_start:sql_end].strip()

        # Extract notes
        if 'NOTES:' in response_text:
            notes_start = response_text.index('NOTES:') + len('NOTES:')
            result['notes'] = response_text[notes_start:].strip()

    except Exception as e:
        result['success'] = False
        result['error'] = f"Could not parse AI response: {str(e)}"

    return result
```

### Error Handling Messages

```python
ERROR_SUGGESTIONS = {
    'technology': "Try specifying the technology more clearly. You can use:\n- IPC codes (e.g., 'F03D for wind motors')\n- Plain descriptions (e.g., 'electric vehicle batteries')",
    'geography': "Try specifying the region differently:\n- Country codes (DE, US, CN)\n- Full names (Germany, United States)\n- Regions (EU, Asia)",
    'general': "Try rephrasing your request with:\n- Specific technology or industry\n- Clear geographic scope\n- Time period\n- What metric you want (counts, trends, comparisons)"
}
```

### Query Quality Checks

```python
def check_query_quality(sql: str) -> list:
    """Check for potential query issues."""
    warnings = []

    # Check for missing LIMIT
    if 'LIMIT' not in sql.upper():
        warnings.append("⚠️ No LIMIT clause - query may return many rows")

    # Check for multiple JOINs
    join_count = sql.upper().count(' JOIN ')
    if join_count > 3:
        warnings.append(f"⚠️ Query has {join_count} JOINs - may be slow")

    # Check for table scans
    if 'WHERE' not in sql.upper():
        warnings.append("⚠️ No WHERE clause - full table scan may be slow")

    return warnings
```

### Project Structure Notes

- AI response handling in: `ai_builder.py`
- Reuse st.code for SQL display
- Store generated results in session state for refinement flow

### References

- [Source: PRD FR31] AI-generated SQL
- [Source: PRD FR32] Plain language explanation
- [Source: Story 4.1] AI integration foundation
- [Source: UX Design - Journey 4] Results display patterns

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
