# Story 5.1: Enhanced "Take to TIP" Button

Status: ready-for-dev

## Story

As an EPO Academy trainer (Elena),
I want a clear pathway from Explorer to TIP,
so that students can continue their learning journey in the full platform.

## Acceptance Criteria

1. **Given** any query is displayed on detail page
   **When** user clicks "Take to TIP"
   **Then** a modal/panel opens with clear instructions
   **And** instructions explain how to use the query in TIP's Jupyter environment
   **And** the SQL query is prominently displayed and copyable
   **And** a link to the TIP platform is provided

2. **Given** the "Take to TIP" panel is open
   **When** user views the content
   **Then** step-by-step instructions are clearly numbered
   **And** the current query SQL is shown with parameter values substituted
   **And** "Copy SQL" button is prominent and functional

3. **Given** user wants to use the query in TIP
   **When** they click the TIP platform link
   **Then** link opens in a new tab
   **And** user doesn't lose their place in Explorer

## Tasks / Subtasks

- [ ] Task 1: Add "Take to TIP" button to detail page (AC: #1)
  - [ ] Position button in export/action area
  - [ ] Style appropriately (secondary button)
  - [ ] Add EPO/TIP branding if appropriate

- [ ] Task 2: Create TIP instructions modal/expander (AC: #1, #2)
  - [ ] Design clear modal or expanded panel
  - [ ] Include EPO TIP logo/branding
  - [ ] Structure with numbered steps

- [ ] Task 3: Display query SQL with parameters (AC: #2)
  - [ ] Show SQL with current parameter values substituted
  - [ ] Format for readability
  - [ ] Prominent copy button

- [ ] Task 4: Add step-by-step instructions (AC: #2)
  - [ ] Write clear instructions for TIP/Jupyter workflow
  - [ ] Include screenshots or diagrams if helpful
  - [ ] Keep concise but complete

- [ ] Task 5: Add TIP platform link (AC: #1, #3)
  - [ ] Link to TIP platform (tip.epo.org or similar)
  - [ ] Open in new tab (target="_blank")
  - [ ] Include brief explanation of what TIP offers

## Dev Notes

### Button Placement

Add to detail page after download buttons:
```python
# In render_detail_page(), after download buttons
col1, col2, col3 = st.columns(3)
with col1:
    st.download_button("📥 Download Data (CSV)", ...)
with col2:
    st.download_button("📊 Download Chart (HTML)", ...)
with col3:
    if st.button("🎓 Take to TIP", key="take_to_tip"):
        st.session_state['show_tip_panel'] = True
```

### TIP Panel Layout

```
┌──────────────────────────────────────────────────────────┐
│  🎓 Take This Query to EPO's TIP Platform                │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  TIP (Training Intelligence Portal) lets you run        │
│  this same query in a full Jupyter environment with     │
│  more flexibility and your own customizations.          │
│                                                          │
│  ────────────────────────────────────────────────────────│
│  📋 Your SQL Query (ready to copy):                      │
│  ┌────────────────────────────────────────────────────┐  │
│  │ SELECT                                            │  │
│  │   p.person_name AS company,                       │  │
│  │   COUNT(DISTINCT a.appln_id) AS patents           │  │
│  │ FROM `patstat-mtc.patstat.tls201_appln` a         │  │
│  │ ...                                               │  │
│  │ -- Parameters: Years 2015-2024, DE, US, CN        │  │
│  └────────────────────────────────────────────────────┘  │
│  [📋 Copy SQL to Clipboard]                              │
│                                                          │
│  ────────────────────────────────────────────────────────│
│  📝 Quick Start in TIP:                                  │
│                                                          │
│  1. Log in to TIP → tip.epo.org                         │
│  2. Open Jupyter Notebooks                               │
│  3. Create a new Python notebook                         │
│  4. Paste the SQL and run!                               │
│                                                          │
│  [▸ Detailed Instructions]                               │
│                                                          │
│  [Open TIP Platform ↗]  [Close]                          │
└──────────────────────────────────────────────────────────┘
```

### SQL with Full Table Names

For TIP, include fully qualified table names:
```python
def format_sql_for_tip(sql: str, params: dict) -> str:
    """Format SQL for use in TIP with full table names and parameters."""
    project = "patstat-mtc"  # Or appropriate project
    dataset = "patstat"

    # Add full table references
    tables = ['tls201_appln', 'tls206_person', 'tls207_pers_appln',
              'tls209_appln_ipc', 'tls211_pat_publn', 'tls212_citation',
              'tls224_appln_cpc', 'tls230_appln_techn_field',
              'tls901_techn_field_ipc', 'tls801_country', 'tls904_nuts']

    formatted_sql = sql
    for table in tables:
        formatted_sql = formatted_sql.replace(
            f'`{table}`',
            f'`{project}.{dataset}.{table}`'
        )
        formatted_sql = formatted_sql.replace(
            f' {table} ',
            f' `{project}.{dataset}.{table}` '
        )

    # Add parameter comment
    param_comment = f"\n-- Parameters: Years {params.get('year_start', 'N/A')}-{params.get('year_end', 'N/A')}"
    if params.get('jurisdictions'):
        param_comment += f", Jurisdictions: {', '.join(params['jurisdictions'])}"

    return formatted_sql + param_comment
```

### TIP Platform URL

```python
TIP_PLATFORM_URL = "https://tip.epo.org"  # Confirm actual URL
TIP_JUPYTER_URL = "https://tip.epo.org/jupyter"  # If direct link available
```

### Copy to Clipboard

Use Streamlit's built-in clipboard functionality:
```python
# st.code has a copy button built in
st.code(formatted_sql, language="sql")

# Or explicit button
if st.button("📋 Copy SQL to Clipboard"):
    st.write("SQL copied!")  # Streamlit handles clipboard via st.code
```

### Project Structure Notes

- TIP instructions can be in separate markdown file
- SQL formatting function in app.py or new utils.py
- TIP URL should be configurable (env var or config)

### References

- [Source: PRD FR36] "Take to TIP" pathway
- [Source: UX Design - Journey 2] Elena's training demo
- [Source: app.py:419-587] Detail page for button placement
- [Source: PRD - Success Criteria] 20% "Take to TIP" conversion target

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
