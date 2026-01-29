# Story 5.2: TIP/Jupyter Export Instructions

Status: ready-for-dev

## Story

As an EPO Academy trainer (Elena),
I want detailed instructions for using queries in TIP,
so that students can successfully replicate analyses in the full platform.

## Acceptance Criteria

1. **Given** a user views "Take to TIP" instructions
   **When** the instructions display
   **Then** step-by-step guidance is provided for:
     - Accessing TIP and opening Jupyter
     - Creating a new notebook
     - Setting up BigQuery connection
     - Pasting and running the query
   **And** instructions include screenshots or visual aids where helpful
   **And** common troubleshooting tips are included

2. **Given** a user follows the instructions
   **When** they reach TIP
   **Then** they can successfully run the query
   **And** the output matches what they saw in Explorer

3. **Given** different skill levels of users
   **When** reading the instructions
   **Then** beginners can follow without prior Jupyter experience
   **And** advanced users can skip to the relevant section

## Tasks / Subtasks

- [ ] Task 1: Write comprehensive TIP instructions (AC: #1)
  - [ ] Access and login steps
  - [ ] Navigate to Jupyter
  - [ ] Create new notebook
  - [ ] BigQuery connection setup
  - [ ] Run query steps

- [ ] Task 2: Create visual aids (AC: #1)
  - [ ] Screenshot key TIP interface elements
  - [ ] Create simple diagrams if helpful
  - [ ] Annotate screenshots with callouts

- [ ] Task 3: Add troubleshooting section (AC: #1)
  - [ ] Common errors and solutions
  - [ ] Authentication issues
  - [ ] Query timeout handling
  - [ ] Data type mismatches

- [ ] Task 4: Create expandable instruction sections (AC: #3)
  - [ ] Quick start for experienced users
  - [ ] Detailed instructions for beginners
  - [ ] Use expanders to manage length

- [ ] Task 5: Include code templates (AC: #1, #2)
  - [ ] Python code for BigQuery connection
  - [ ] Code cell templates for pasting SQL
  - [ ] Output display code

## Dev Notes

### Instruction Content

```markdown
## Quick Start (Experienced Users)

1. Login to [TIP](https://tip.epo.org)
2. Open Jupyter → New Python 3 Notebook
3. Paste the code below and run:

```python
from google.cloud import bigquery
client = bigquery.Client()

query = """
[YOUR SQL HERE]
"""

df = client.query(query).to_dataframe()
df
```

## Detailed Instructions (Step-by-Step)

### Step 1: Access TIP

1. Go to [tip.epo.org](https://tip.epo.org)
2. Login with your EPO account
3. If you don't have an account, click "Register" (EPO Academy provides access for training participants)

### Step 2: Open Jupyter Notebooks

1. From the TIP dashboard, click "Notebooks"
2. Select "JupyterLab" or "Jupyter Notebook"
3. Wait for the environment to load (may take 30 seconds)

### Step 3: Create a New Notebook

1. In Jupyter, click "File" → "New" → "Notebook"
2. Select "Python 3" as the kernel
3. A new blank notebook opens

### Step 4: Set Up BigQuery Connection

Copy and paste this code into the first cell:

```python
# Cell 1: Setup
from google.cloud import bigquery
import pandas as pd

# TIP provides authentication automatically
client = bigquery.Client()
print("Connected to BigQuery!")
```

Run the cell (Shift + Enter). You should see "Connected to BigQuery!"

### Step 5: Run Your Query

Copy and paste this code into the second cell:

```python
# Cell 2: Your Query
query = """
[PASTE YOUR SQL HERE]
"""

# Execute query
df = client.query(query).to_dataframe()

# Display results
print(f"Found {len(df)} rows")
df.head(20)
```

Run the cell. Your results should appear!

### Step 6: Visualize Results (Optional)

```python
# Cell 3: Visualization (optional)
import matplotlib.pyplot as plt

# For bar charts
df.plot(kind='bar', x='column_name', y='count_column')
plt.title("Your Title")
plt.show()
```

## Troubleshooting

### "Permission denied" error
- Make sure you're logged into TIP
- Your EPO account may need PATSTAT access enabled
- Contact EPO Academy support

### Query takes too long
- Add LIMIT 1000 to test
- Check if year range is too wide
- Some queries are slower than others

### "Table not found" error
- Check table name spelling
- Use full path: `patstat-mtc.patstat.table_name`
- PATSTAT tables start with tls (e.g., tls201_appln)

### Results look different from Explorer
- Check parameter values match
- Verify you copied the complete SQL
- Time-based queries may show different data due to database updates
```

### Instruction Layout in App

```
┌──────────────────────────────────────────────────────────┐
│  📚 TIP/Jupyter Instructions                             │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  [▸ Quick Start (5 steps)]                               │
│                                                          │
│  [▸ Detailed Instructions (with screenshots)]            │
│                                                          │
│  [▸ Code Templates]                                      │
│                                                          │
│  [▸ Troubleshooting]                                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Screenshot Placeholders

If screenshots aren't available, use descriptive text boxes:
```python
st.info("""
📷 **Screenshot: TIP Dashboard**
You'll see a navigation menu on the left with options including 'Notebooks'.
Click 'Notebooks' to access Jupyter.
""")
```

### Code Template for Export

```python
JUPYTER_TEMPLATE = '''# PATSTAT Explorer Query - {query_title}
# Generated: {date}

from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

# Query: {query_title}
# {description}
query = """
{sql}
"""

# Execute and display
df = client.query(query).to_dataframe()
print(f"Found {{len(df)}} results")
df
'''

def generate_notebook_code(query_info: dict, sql: str) -> str:
    """Generate ready-to-paste Jupyter notebook code."""
    return JUPYTER_TEMPLATE.format(
        query_title=query_info.get('title', 'Custom Query'),
        date=datetime.now().strftime('%Y-%m-%d'),
        description=query_info.get('description', ''),
        sql=sql.strip()
    )
```

### Project Structure Notes

- Instructions can be in markdown file: `docs/tip-instructions.md`
- Or embedded in Python file as constants
- Screenshots in: `assets/` or `docs/images/`

### References

- [Source: PRD FR37] TIP/Jupyter instructions
- [Source: UX Design - Journey 2] Elena's training demo flow
- [Source: PRD - Training Integration] Instructions for TIP/Jupyter
- [Source: Story 5.1] "Take to TIP" panel where instructions display

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
