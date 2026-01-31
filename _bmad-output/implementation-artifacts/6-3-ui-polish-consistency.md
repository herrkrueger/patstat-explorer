---
status: deferred
epic: 6
story: 3
name: ui-polish-consistency
---

# Story 6.3: UI Polish & Consistency

**As a** user,
**I want** the visual hierarchy on the landing page to be balanced and readable,
**So that** I can quickly scan questions and choose what to explore.

## Problem Statement

The current landing page query cards have poor visual hierarchy:
- **Question title**: Tiny (~12px) because it's inside a `st.button()`
- **Execution time**: Huge (~24px) because it uses `st.metric()`
- **Result**: Secondary info dominates, primary content is hard to read

## Acceptance Criteria

### 1. Query Card Visual Hierarchy Fixed
- **Given** the landing page query list
- **When** viewing query cards
- **Then** the question title is displayed in **large text** (comparable to the time estimate)
- **And** the title is NOT inside a button
- **And** a separate "Load" button is provided for navigation
- **And** the time estimate remains visible but doesn't dominate

### 2. Card Layout Specification
- **Given** a query card
- **When** rendered
- **Then** it follows this layout:

```
┌────────────────────────────────────────────────────────────────────────┐
│  Q01: What are the overall PATSTAT database statistics?     ~1.0s     │
│  ───────────────────────────────────────────────────────    Trends    │
│  Overall PATSTAT database statistics and key metrics...               │
│  [PATLIB] [BUSINESS]                                      [▶ Load]    │
└────────────────────────────────────────────────────────────────────────┘
```

- Title + time estimate on same row, similar visual weight
- Description below title
- Tags + Load button on bottom row

### 3. No Regression
- **Given** the updated UI
- **When** clicking "Load" button
- **Then** navigation to detail page works exactly as before
- **And** all other landing page features (search, filter, categories) work

## Tasks/Subtasks

### Phase 1: Redesign Query Card Layout
- [ ] Replace `st.button()` title with `st.markdown()` using larger font
- [ ] Change column layout from `[4, 1]` to better proportions (e.g., `[3, 1, 1]` or custom)
- [ ] Move time estimate to same visual line as title
- [ ] Add separate "Load" or "▶" button for navigation
- [ ] Keep description and tags below

### Phase 2: Style Adjustments
- [ ] Ensure title font size matches or exceeds time estimate
- [ ] Use CSS or st.markdown with HTML to control typography if needed
- [ ] Verify tags still render correctly
- [ ] Check mobile/narrow viewport behavior

### Phase 3: Verification
- [ ] Visual review: Title is prominent, time is secondary
- [ ] Click "Load" → navigates to correct detail page
- [ ] Search/filter still works
- [ ] Category pills still work
- [ ] Common Questions section still works

## Implementation Notes

### Current Code Location
`app.py` lines 750-810 in `render_query_list()`:

```python
# CURRENT (problematic)
col1, col2 = st.columns([4, 1])
with col1:
    if st.button(f"**{query_id}:** {query_info['title']}", ...):  # Title in button = tiny
        go_to_detail(query_id)
with col2:
    st.metric("", f"~{format_time(est_time)}", ...)  # Metric = huge
```

### Proposed Approach

**Option A: Use st.markdown with HTML styling**
```python
col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    # Large title using markdown
    st.markdown(f"### {query_id}: {query_info['title']}")
    st.caption(description)
    st.markdown(tags_html, unsafe_allow_html=True)
with col2:
    st.caption(f"~{format_time(est_time)}")
    st.caption(query_info.get('category', ''))
with col3:
    if st.button("▶ Load", key=f"load_{query_id}"):
        go_to_detail(query_id)
```

**Option B: Custom CSS for consistent sizing**
```python
# At top of file
st.markdown("""
<style>
.query-title { font-size: 1.2rem; font-weight: 600; }
.query-time { font-size: 1.2rem; color: #666; }
</style>
""", unsafe_allow_html=True)

# In card rendering
st.markdown(f'<span class="query-title">{query_id}: {title}</span>', ...)
st.markdown(f'<span class="query-time">~{time}</span>', ...)
```

### Decision for Dev
- Prefer Option A (simpler, uses Streamlit's built-in `###` heading)
- Fall back to Option B if Option A doesn't give enough control
- Button label: "Load", "View", or "▶" - dev's choice based on what looks best

## Out of Scope
- Changing the detail page layout (that was rejected in previous attempt)
- Adding new features
- Changing color scheme

## File List
- app.py (or modules/ui.py if 6.2 is done first)
  - Modify `render_query_list()` function

## Dependencies
- None (can be done before or after 6.2)
- If 6.2 is done first, edit `modules/ui.py` instead of `app.py`

## Change Log
- 2026-01-30: Story created
- 2026-01-30: First implementation attempt reverted per user feedback (3-column header, gradient)
- 2026-01-31: Story rewritten with specific query card layout fix based on user feedback
- 2026-01-31: Partial implementation (3-column layout with Load button) - deferred to future UI epic for more refined work
