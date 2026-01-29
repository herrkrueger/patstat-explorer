# Story 4.1: Natural Language Input Interface

Status: ready-for-dev

## Story

As a PATLIB professional,
I want to describe my analysis need in plain English,
so that I can get custom queries without knowing SQL.

## Acceptance Criteria

1. **Given** a user navigates to "AI Query Builder"
   **When** the interface loads
   **Then** a text area is available for natural language input
   **And** placeholder text provides an example (e.g., "Show me the top 10 companies in Germany with wind energy patents...")
   **And** helpful prompts suggest what information to include

2. **Given** a user enters a natural language request
   **When** they click "Generate Query"
   **Then** a loading state indicates AI is processing
   **And** the request is sent to Claude API via MCP
   **And** user cannot submit empty requests

3. **Given** the AI integration is being configured
   **When** API credentials are not available
   **Then** a helpful message explains how to set up MCP/Claude API
   **And** feature is gracefully disabled rather than erroring

## Tasks / Subtasks

- [ ] Task 1: Create AI Query Builder page/section (AC: #1)
  - [ ] Add navigation option from landing page
  - [ ] Create dedicated section or page
  - [ ] Design header with clear purpose explanation

- [ ] Task 2: Implement natural language input area (AC: #1)
  - [ ] Add st.text_area with generous height
  - [ ] Create engaging placeholder text
  - [ ] Add character count indicator (optional)

- [ ] Task 3: Add guidance prompts (AC: #1)
  - [ ] Create expandable section with tips
  - [ ] Example queries users might ask
  - [ ] What makes a good natural language request
  - [ ] Information to include: technology, region, time, metrics

- [ ] Task 4: Implement "Generate Query" button and loading (AC: #2)
  - [ ] Primary button with clear label
  - [ ] Validate input not empty
  - [ ] Show spinner with contextual message during generation
  - [ ] Disable button during processing

- [ ] Task 5: Set up Claude API integration foundation (AC: #2, #3)
  - [ ] Create API client wrapper
  - [ ] Handle authentication via environment/secrets
  - [ ] Graceful fallback if API unavailable
  - [ ] Error handling for API failures

- [ ] Task 6: Handle missing API configuration (AC: #3)
  - [ ] Check for API key in secrets/env
  - [ ] Display setup instructions if missing
  - [ ] Disable feature gracefully
  - [ ] Link to documentation

## Dev Notes

### Page Layout

```
┌──────────────────────────────────────────────────────────┐
│  ← Back to Questions                                     │
│  ─────────────────────────────────────────────────────── │
│  🤖 AI Query Builder                                     │
│                                                          │
│  Describe what you want to analyze in plain English.     │
│  Our AI will generate the SQL query for you.             │
│                                                          │
│  [▸ Tips for better results]                             │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Show me the top 10 companies filing wind energy   │  │
│  │ patents in Germany since 2018, with their filing  │  │
│  │ trends over time and comparison to EU average...  │  │
│  │                                                    │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  [Generate Query]                                        │
└──────────────────────────────────────────────────────────┘
```

### Guidance Tips Content

```markdown
**Tips for better results:**

1. **Be specific about technology**
   - Use IPC codes if you know them (e.g., "F03D for wind motors")
   - Or describe technology clearly (e.g., "battery storage for EVs")

2. **Specify geography**
   - Country codes (DE, US, CN) or full names
   - Regions if relevant (e.g., "Bavaria" or "EU member states")

3. **Define time period**
   - "Since 2018" or "between 2015 and 2023"
   - "Last 5 years" works too

4. **Clarify what you want to see**
   - "Top 10 companies by patent count"
   - "Filing trend over time"
   - "Comparison between countries"

**Example requests:**
- "Who are the main competitors in medical imaging technology in Europe since 2020?"
- "Show patent filing trends for AI/machine learning in US, CN, and EP over the last 10 years"
- "Which universities collaborate most with industry on battery research?"
```

### Claude API Integration

```python
import anthropic
import os

def get_claude_client():
    """Get Claude API client if configured."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        # Try Streamlit secrets
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY")
        except:
            pass

    if not api_key:
        return None

    return anthropic.Anthropic(api_key=api_key)

def is_ai_available():
    """Check if AI features are available."""
    return get_claude_client() is not None
```

### System Prompt for SQL Generation

```python
PATSTAT_SYSTEM_PROMPT = """You are an expert SQL query writer for EPO PATSTAT on BigQuery.

You have access to these main tables:
- tls201_appln: Patent applications (main table)
- tls206_person: Applicants and inventors
- tls207_pers_appln: Links persons to applications
- tls209_appln_ipc: IPC classifications
- tls224_appln_cpc: CPC classifications
- tls211_pat_publn: Publications
- tls212_citation: Citation data
- tls230_appln_techn_field: WIPO technology fields
- tls901_techn_field_ipc: Technology field definitions
- tls801_country: Country codes

Key columns in tls201_appln:
- appln_id, appln_auth (authority), appln_filing_year
- granted ('Y'/'N'), docdb_family_id, docdb_family_size

Generate BigQuery-compatible SQL that:
1. Uses proper table names with backticks
2. Includes appropriate JOINs
3. Has sensible LIMIT (default 50)
4. Handles NULLs appropriately
5. Returns results within 15 seconds typically

Also provide a brief explanation of what the query does."""
```

### Project Structure Notes

- New file recommended: `ai_builder.py` for AI functionality
- API key in: Streamlit secrets or .env file
- System prompt for PATSTAT context
- Error handling for API failures

### References

- [Source: PRD FR30] Natural language input
- [Source: PRD NFR6] MCP/Claude API authentication
- [Source: UX Design - Journey 4] Maria's AI query journey
- [Source: docs/bigquery-schema.md] Table structure for system prompt

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
