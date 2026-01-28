---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
status: complete
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-patstat-2026-01-28.md
  - docs/index.md
  - docs/project-overview.md
  - docs/query-catalog.md
  - docs/bigquery-schema.md
  - docs/data-loading.md
  - context/streamlit_examples/gdp_streamlit_app.py
  - context/streamlit_examples/stock_streamlit_app.py
  - context/streamlit_examples/ai_assis_streamlit_app.py
  - app.py (current implementation)
researchReferences:
  - Streamlit theming documentation
  - Custom CSS styling approaches
  - Altair/Plotly interactive chart patterns
date: 2026-01-28
author: Arne
project: patstat
---

# UX Design Specification: PATSTAT Explorer

**Author:** Arne
**Date:** 2026-01-28

---

## Executive Summary

### Project Vision

PATSTAT Explorer makes patent intelligence accessible to non-technical professionals. The core UX principle is **zero cognitive load** - users should understand what they're seeing at first glance, navigate without thinking, and always know why the information matters to their business context.

### Target Users

**Primary (90%): Maria - The Generalist PATLIB Professional**
- Needs to deliver insights to clients without technical struggle
- Success = "I understood it immediately and my client was impressed"
- UX implication: Hide complexity, lead with relevance

**Secondary (10%): Klaus - The Data Enthusiast**
- Wants to contribute and see "under the hood"
- Success = "I can share my expertise with 300 centres"
- UX implication: Power features available but not prominent

**Downstream: End Clients (SMEs, researchers, politicians)**
- Never touch the tool directly
- Receive exports from Maria
- UX implication: Charts must be self-explanatory when extracted

### Key Design Challenges

1. **First-Glance Comprehension** - Every screen answers "what does this mean?" instantly
2. **Effortless Navigation** - 40+ queries organized by user intent, not technical category
3. **Business Relevance** - Plain language, insight headlines, "so what?" always answered
4. **Progressive Complexity** - Simple by default, details available on demand

### Design Opportunities

1. **Insight-First Results** - Lead with headline summaries, not raw data
2. **Question-Based Query Names** - "Who are my competitors?" not "Q12: Competitor Filing Strategy"
3. **Contextual Explanations** - Brief "Why this matters" for every analysis
4. **Clean Export Path** - One-click to presentation-ready output

## Core User Experience

### Defining Experience

The core experience is **answering client questions**. PATSTAT Explorer is a transactional tool - users arrive with a specific need, find the answer, and deliver it to their client. This is not an exploration or learning tool; it's a question-answering machine.

**Core Loop:** Client Question → Find Analysis → Personalize Parameters → Get Answer → Deliver to Client

### Platform Strategy

- **Web-only** via Streamlit Cloud (permanent deployment)
- **Desktop-first** optimized for training rooms and office use
- **Mouse/keyboard** interaction (not touch-optimized)
- **Always online** requiring BigQuery connection
- **No authentication** - open access, zero friction

### Effortless Interactions

| Interaction | Design Goal |
|-------------|-------------|
| Finding the right query | Organized by client question type, not technical category |
| Understanding results | Insight headline appears before any data table |
| Setting parameters | Smart defaults, minimal required input |
| Exporting for clients | One-click to presentation-ready format |

### Critical Success Moments

1. **Query Discovery** - "This is exactly the analysis I needed"
2. **Insight Clarity** - "I understood the answer immediately"
3. **Client Delivery** - "The export looked professional without editing"

The defining success moment: **Maria sees the insight headline and knows it answers her client's question.**

### Experience Principles

1. **Question-First** - Navigation organized by what clients ask, not by technical query structure
2. **Speed to Answer** - Minimum clicks between need and insight
3. **Insight Over Data** - Lead with meaning, data available on demand
4. **Client-Ready** - Every output suitable for immediate client delivery

## Desired Emotional Response

### Primary Emotional Goals

| Emotion | Description |
|---------|-------------|
| **Competent** | Maria feels like a data expert, even without technical skills |
| **Confident** | "I know this answer is correct, I can stand behind it" |
| **Efficient** | "I got what I needed without wasted time" |

**Core emotional shift:** From "I'm intimidated by patent data analysis" → "I'm the person who delivers patent intelligence"

### Emotional Journey Mapping

| Stage | Desired Feeling |
|-------|-----------------|
| **Arrival** | "I know exactly where to go" |
| **Query Selection** | "This matches my client's question" |
| **Parameter Setting** | "Smart defaults make sense" |
| **Viewing Results** | "I understand immediately" |
| **Export** | "My client will be impressed" |
| **Error/No Data** | "Clear guidance on what to do next" |

### Emotions to Avoid

- **Overwhelmed** - too many options, too much data
- **Confused** - "what does this mean?"
- **Embarrassed** - "I don't understand this tool"

### Design Implications

| Desired Emotion | UX Approach |
|-----------------|-------------|
| **Competent** | Plain language, no jargon, "Why this matters" explanations |
| **Confident** | Show data source credibility, clear methodology notes |
| **Efficient** | Minimal clicks, smart defaults, fast load times |
| **Not Overwhelmed** | Progressive disclosure, hide complexity by default |
| **Not Confused** | Insight headlines first, data tables secondary |

### Emotional Design Principle

**"This tool makes me look good to my clients."**

Every design decision should be evaluated against this principle. If a feature or interaction doesn't contribute to Maria feeling competent, confident, and efficient in front of her clients, it should be reconsidered.

## UX Pattern Analysis & Inspiration

### Inspiring Products Analysis

**Source: Streamlit Example Gallery** - Three production-quality Streamlit apps demonstrating best practices for data dashboards.

#### GDP Dashboard Patterns
- Slider-first interaction for time ranges
- Multiselect for entity comparison (countries → jurisdictions)
- Metric cards with delta indicators showing growth
- Clean section dividers with gray headers
- Color-coded chart series

#### Stock Peer Analysis Patterns
- Wide layout for data-heavy views
- Bordered containers for visual grouping
- Pills component for quick categorical selection
- Altair charts with custom styling and tooltips
- Comparison pattern: entity vs. benchmark average

#### AI Assistant Patterns
- Suggestion pills for common starting points
- Clean header row with title + action alignment
- Contextual loading states
- Progressive disclosure of complexity

### Transferable UX Patterns

| Pattern | Source | PATSTAT Application |
|---------|--------|---------------------|
| **Slider-first** | GDP Dashboard | Year range selection for all queries |
| **Multiselect comparison** | GDP Dashboard | Jurisdiction/company comparison |
| **Metric cards with delta** | GDP Dashboard | Patent counts + growth indicators |
| **Wide layout** | Stock Analysis | Results view for data tables |
| **Bordered containers** | Stock Analysis | Group parameters and results |
| **Pills navigation** | Stock/AI Assistant | Query category quick-select |
| **Suggestion chips** | AI Assistant | "Common client questions" quick-start |
| **Contextual spinners** | AI Assistant | "Finding competitors in MedTech..." |

### Anti-Patterns to Avoid

- **Data table first** - Lead with insight headline instead
- **Technical query IDs** - Use question-based naming
- **Generic loading states** - Use contextual, specific messages
- **Flat visual hierarchy** - Bold insights, mute metadata
- **Too many navigation options** - Consolidate by user intent

### Design Inspiration Strategy

**Adopt directly:**
- Metric cards with delta indicators
- Slider + multiselect parameter pattern
- Bordered containers for grouping
- Wide layout for results

**Adapt for PATSTAT:**
- Pills → use for query categories by client question type
- Comparison pattern → "Your region vs. EU average"
- Suggestion chips → "Common client questions" landing experience

**Avoid:**
- Raw data tables as primary output
- Technical naming conventions
- Cluttered multi-tab navigation

## Design System Foundation

### Design System Choice

**Primary Approach:** Streamlit Native + Light CSS + Altair Charts

**Fallback:** Pure Streamlit Native (if customization creates friction)

### Rationale for Selection

| Factor | Decision Driver |
|--------|-----------------|
| **Platform constraint** | Streamlit Cloud = work with the framework, not against it |
| **Development speed** | MVP timeline = leverage native components |
| **Export quality** | Altair charts export better than st.line_chart |
| **Maintenance** | Small codebase = keep dependencies minimal |
| **User expectations** | Business users expect polished but not flashy |

### Implementation Approach

**Layer 1: Theming** (`.streamlit/config.toml`)
- Primary color palette
- Background and text colors
- Font configuration

**Layer 2: Native Components**
- `st.metric` for KPI cards with delta
- `st.slider` and `st.multiselect` for parameters
- `st.container(border=True)` for visual grouping
- `st.expander` for progressive disclosure

**Layer 3: Charting** (Altair)
- Consistent color palette across all visualizations
- Proper legends, tooltips, axis labels
- Export-friendly sizing for client presentations

**Layer 4: Light CSS** (minimal, targeted)
- Insight headline emphasis
- Visual hierarchy adjustments
- Hide distracting Streamlit defaults (hamburger menu, footer)

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Altair adds complexity** | If charting becomes a bottleneck, fall back to `st.line_chart` / `st.bar_chart` |
| **CSS breaks on Streamlit updates** | Keep CSS minimal and well-documented; test after updates |
| **Customization scope creep** | Timebox styling work; "good enough" beats "perfect" |

**Decision rule:** If any customization takes more than 2 hours to implement correctly, fall back to pure Streamlit native approach.

### Customization Strategy

**Color Palette (to be defined):**
- Primary: TBD (consider EPO blue)
- Secondary: TBD
- Accent: TBD
- Success/Growth: Green
- Warning/Decline: Red
- Neutral: Gray scale

**Chart Standards:**
- All charts use same color palette
- Consistent axis formatting (years, percentages, counts)
- Tooltips show context, not just values
- Legends positioned for clarity

## Defining User Interaction

### The Defining Experience

**"Select → Personalize → Understand → Export"**

The 4-step answer machine that transforms client questions into shareable insights in under 60 seconds.

### User Mental Model

Users arrive with a client question in mind. They expect:
- To find an analysis that matches their question (not learn a query system)
- To adjust parameters to their context (not build from scratch)
- To understand the answer immediately (not interpret raw data)
- To deliver something professional to their client (not do post-processing)

**Mental model:** "This is a smart assistant that answers patent questions" - not "This is a database query tool."

### Success Criteria

| Step | Success Indicator |
|------|-------------------|
| **Select** | User finds matching query within 10 seconds |
| **Personalize** | Defaults are sensible; user makes 0-2 changes |
| **Understand** | User grasps the insight without scrolling |
| **Export** | Output requires no editing before client delivery |

**Overall:** Returning users complete the full loop in under 60 seconds.

### Experience Mechanics

**Select Phase:**
- Question-based categories replace technical tabs
- Search for power users
- "Common questions" pills for quick start

**Personalize Phase:**
- Year range slider with smart defaults
- Jurisdiction multiselect with regional defaults
- Technology dropdown grouped by sector
- All queries runnable with zero changes

**Understand Phase:**
- Contextual loading message
- Insight headline appears first (bold, prominent)
- Supporting visualization second
- Data table in expander (collapsed)
- "Why this matters" context available

**Export Phase:**
- "Download for presentation" (PNG/PDF)
- "Download data" (CSV)
- "View SQL" collapsed for Klaus persona

## Visual Design Foundation

### Color System

**Primary Palette:**

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary** | Deep Blue | #1E3A5F | Headers, primary buttons, links |
| **Secondary** | Teal | #0A9396 | Secondary actions, accents |
| **Accent** | Amber | #FFB703 | Highlights, attention draws |
| **Background** | White | #FFFFFF | Page background |
| **Surface** | Light Gray | #F8F9FA | Cards, containers |
| **Text** | Dark Gray | #1D1D1D | Body text |
| **Text Muted** | Medium Gray | #6C757D | Captions, metadata |

**Semantic Colors:**

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Success** | Green | #2A9D8F | Growth indicators, positive deltas |
| **Warning** | Orange | #F77F00 | Caution states |
| **Error** | Red | #D62828 | Errors, negative deltas |

**Chart Color Palette (Jurisdictions):**

| Entity | Color | Hex |
|--------|-------|-----|
| EP | Deep Blue | #1E3A5F |
| US | Teal | #0A9396 |
| CN | Red | #D62828 |
| JP | Orange | #F77F00 |
| KR | Green | #2A9D8F |
| DE | Amber | #FFB703 |

### Typography System

**Streamlit Native Fonts** (no custom fonts to maintain simplicity)

| Element | Purpose | Style |
|---------|---------|-------|
| **H1** | Page title only | Default, single instance per page |
| **H2** | Major sections | With `divider='gray'` |
| **H3** | Subsections | Sparingly used |
| **Body** | Descriptions, explanations | Regular weight |
| **Bold** | Insight headlines | **Prominent, attention-grabbing** |
| **Caption** | Metadata, timing estimates | `st.caption()` - small, muted |

**Hierarchy Principle:** Maximum 3 levels visible at once. Insight headlines use bold body text, not headers.

### Spacing & Layout Foundation

**Layout Strategy:**

| Context | Approach |
|---------|----------|
| **Overall** | `layout="wide"` for data-rich pages |
| **Section separation** | `st.header(..., divider='gray')` + empty lines |
| **Visual grouping** | `st.container(border=True)` for related elements |
| **Parameter blocks** | Grouped in bordered containers |
| **Results display** | Full width, breathing room above/below |

**Spacing Patterns:**

| Pattern | Implementation |
|---------|----------------|
| **Between sections** | Two empty strings `''` + `''` |
| **Within sections** | One empty string `''` |
| **Tight grouping** | No extra spacing (Streamlit default) |

**Column Usage:**

| Purpose | Pattern |
|---------|---------|
| **Metric cards** | `st.columns(4)` for KPI row |
| **Parameters + Button** | `st.columns([1, 5])` for button + caption |
| **Side-by-side comparison** | `st.columns(2)` or `st.columns(3)` |

### Accessibility Considerations

| Requirement | Implementation |
|-------------|----------------|
| **Color contrast** | All text meets WCAG AA (4.5:1 ratio) |
| **Not color-only** | Charts include labels, not just colors |
| **Readable text** | Use Streamlit defaults (proven accessible) |
| **Interactive targets** | Native Streamlit components are accessible |
| **Screen readers** | Use descriptive labels on all inputs |

**Chart Accessibility:**
- Always include axis labels
- Tooltips provide exact values
- Legend included for multi-series charts
- Consider color-blind friendly palette for future iteration

## Design Direction Decision

### Design Directions Explored

Three layout approaches were evaluated for PATSTAT Explorer:

| Direction | Description | Trade-offs |
|-----------|-------------|------------|
| **A: Sidebar Navigator** | Traditional Streamlit pattern with sidebar query list | Familiar but cluttered with 40+ queries |
| **B: Landing + Detail** | Question-first landing page, then full-width results | Best UX, requires good navigation |
| **C: Tabs + Cards** | Dashboard with query cards in category tabs | Visual but complex to implement |

### Chosen Direction

**Direction B: Landing + Detail**

A two-phase experience:
1. **Landing Phase** - Question-based navigation, category pills, common questions
2. **Detail Phase** - Full-width results with insight headline, chart, and export options

### Design Rationale

| Principle | How Direction B Supports It |
|-----------|----------------------------|
| **Question-First** | Landing page organized by client question types, not technical categories |
| **Zero Cognitive Load** | One query visible at a time, no sidebar distraction |
| **Speed to Answer** | Common questions on landing for quick access |
| **Client-Ready Output** | Full-width results area maximizes chart/export visibility |
| **Progressive Disclosure** | Complexity hidden until user selects a specific query |

### Implementation Approach

**Landing Page Structure:**
```
┌──────────────────────────────────────────────────────────┐
│  PATSTAT Explorer                           [Search...]  │
│  ─────────────────────────────────────────────────────── │
│                                                          │
│  What do you want to know?                               │
│                                                          │
│  [Competitors] [Trends] [Regional] [Technology]          │
│                                                          │
│  Common Questions:                                       │
│  ○ Who are the top filers in my field?                   │
│  ○ How is my region performing vs. others?               │
│  ○ What's the patent trend over time?                    │
└──────────────────────────────────────────────────────────┘
```

**Detail Page Structure:**
```
┌──────────────────────────────────────────────────────────┐
│  ← Back to Questions                    [Change Query ▼] │
│  ─────────────────────────────────────────────────────── │
│  Who are the top filers in Medical Tech?                 │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Parameters: [2018-2023] [EP, US, CN] [Run Analysis] │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  **Medtronic leads with 2,340 patents (23% share)**      │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                     CHART                           │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  [Download Chart] [Download Data]  [▸ View Data Table]   │
│                                            [▸ View SQL]  │
└──────────────────────────────────────────────────────────┘
```

**Streamlit Implementation Notes:**
- Use `st.session_state` to track current page (landing vs. detail)
- Landing uses `st.pills()` for categories, clickable query list
- Detail uses full-width layout with `st.container(border=True)` for parameters
- "Back" button clears session state and returns to landing
- No sidebar in either view (cleaner experience)

## User Journey Flows

### Journey 1: Answer a Client Question (Maria)

**Scenario:** Client asks "Who are the main patent filers in electric vehicle batteries?"

**Flow:**
1. Maria opens PATSTAT Explorer → Landing page
2. Scans category pills → Clicks "Competitors"
3. Sees query list → Clicks "Top filers in a technology field"
4. Detail page loads → Reviews default parameters
5. Adjusts if needed: Technology = EV Batteries, Years = 2019-2024
6. Clicks "Run Analysis" → Loading with contextual message
7. **Insight headline appears** → Reviews chart
8. Clicks "Download Chart" → Sends PNG to client
9. **Client impressed**

**Success Criteria:**
- Query discovery: <10 seconds
- Insight headline directly answers question
- Export requires no editing

### Journey 2: Training Demo (Elena)

**Scenario:** EPO Academy training on patent landscape analysis

**Flow:**
1. Elena opens PATSTAT Explorer on projector → Landing page
2. Explains tool purpose to students
3. Demonstrates: "Trends" → "Patent filing trend over time"
4. Shows parameters, explains each one
5. Adjusts to Germany + MedTech as example
6. Runs analysis, interprets results for class
7. Students replicate on their own devices
8. Each student adjusts to their own country
9. Discussion of emerging patterns

**Success Criteria:**
- Students replicate demo within 30 seconds
- Parameters clearly visible for instruction
- Different results for different parameters (learning moment)

### Journey 3: Explore the SQL (Klaus)

**Scenario:** Klaus wants to understand and adapt a query

**Flow:**
1. Klaus opens PATSTAT Explorer → Landing page
2. Searches for relevant query
3. Runs query with test parameters
4. Clicks "▸ View SQL" expander
5. Studies query structure
6. Copies SQL to clipboard
7. Adapts in BigQuery console for own needs

**Success Criteria:**
- SQL accessible but not prominent
- SQL readable and well-commented
- Copy function works reliably

### Journey Patterns

| Pattern | Description |
|---------|-------------|
| **Category → Query → Detail** | Consistent navigation across all journeys |
| **Smart Defaults → Adjust → Run** | All queries runnable with zero input |
| **Insight First → Chart → Data** | Progressive disclosure of complexity |
| **Back Navigation** | "← Back to Questions" always visible |

### Flow Optimization Principles

| Principle | Implementation |
|-----------|----------------|
| **Minimum clicks to value** | 3 clicks from landing to insight |
| **Always runnable** | Default parameters on every query |
| **Clear progress** | Contextual loading messages |
| **Non-destructive** | Back preserves state; adjustments don't lose results |
| **Graceful failure** | "No data" includes helpful suggestions |

## Component Strategy

### Streamlit Native Components

| Component | API | Usage |
|-----------|-----|-------|
| Page Title | `st.title()` | App header |
| Section Headers | `st.header(..., divider='gray')` | Section separation |
| Category Pills | `st.pills()` | Query category navigation |
| Sliders | `st.slider()` | Year range parameters |
| Multiselect | `st.multiselect()` | Jurisdiction selection |
| Selectbox | `st.selectbox()` | Technology field |
| Buttons | `st.button()` | Actions (Run, Back) |
| Metric Cards | `st.metric()` | KPI display with delta |
| Altair Charts | `st.altair_chart()` | Visualizations |
| Expanders | `st.expander()` | Progressive disclosure |
| Download | `st.download_button()` | Export functions |
| Containers | `st.container(border=True)` | Visual grouping |
| Columns | `st.columns()` | Layout |
| Spinner | `st.spinner()` | Loading states |
| Caption | `st.caption()` | Metadata, context |

### Custom Composite Components

#### Insight Headline
- **Purpose:** Display key takeaway from query results
- **Composition:** Bold markdown + caption with data context
- **Spec:** First element after loading, readable as standalone sentence

#### Query Card
- **Purpose:** Clickable query option on landing page
- **Composition:** Bordered container + question title + description + button
- **Spec:** Question-style naming, clear call-to-action

#### Parameter Block
- **Purpose:** Consistent parameter layout across all queries
- **Composition:** Bordered container with columns (Time → Geography → Topic → Action)
- **Spec:** Smart defaults, Run button always visible

#### Results Display
- **Purpose:** Consistent presentation of query results
- **Composition:** Insight → Chart → Expanders → Downloads
- **Spec:** Fixed order, insight visible without scrolling

### Implementation Roadmap

| Phase | Components | Priority |
|-------|------------|----------|
| **Phase 1** | Insight Headline, Parameter Block, Results Display | Core loop |
| **Phase 2** | Query Cards, Landing Layout, Navigation | Full experience |
| **Phase 3** | Enhanced Altair charts, Export polish | User delight |

## UX Consistency Patterns

### Button Hierarchy

| Type | Style | Usage |
|------|-------|-------|
| **Primary** | `type="primary"` | "Run Analysis" - one per page max |
| **Secondary** | Default button | "← Back", navigation actions |
| **Download** | `st.download_button()` | Export functions |
| **Disclosure** | `st.expander()` | "View Data", "View SQL" |

**Rule:** One primary action per screen. Primary changes based on context.

### Feedback Patterns

| State | Component | Message Style |
|-------|-----------|---------------|
| **Loading** | `st.spinner()` | Contextual: "Finding top filers in MedTech..." |
| **Success** | Insight headline | No explicit message - content is the feedback |
| **No Data** | `st.warning()` | Include suggestions: "Try broadening year range..." |
| **Error** | `st.error()` | Include recovery action |
| **Info** | `st.info()` | Methodology, data freshness notes |

**Rule:** Never generic messages. Always specific, always actionable.

### Navigation Patterns

| Transition | Implementation |
|------------|----------------|
| Landing → Detail | Session state update, explicit click |
| Detail → Landing | "← Back" button, preserve context |
| Parameter changes | No navigation, in-place updates |
| Run Analysis | Stay on page, show results |

**Rule:** Navigation is explicit (user clicks), never automatic.

### Empty & Loading States

| State | User Sees |
|-------|-----------|
| **Landing** | "What do you want to know?" + categories |
| **Pre-run** | Parameters + "Click Run Analysis" hint |
| **Loading** | Contextual spinner message |
| **Results** | Insight headline + visualization |
| **No data** | Warning + suggestions to adjust |

### Parameter Patterns

| Pattern | Standard |
|---------|----------|
| **Order** | Time → Geography → Technology → Action |
| **Defaults** | Always present, always sensible |
| **Layout** | Horizontal in bordered container |
| **Help** | `st.caption()` only when needed |

## Responsive Design & Accessibility

### Responsive Strategy

**Approach:** Desktop-first, accept Streamlit's default responsive behavior.

| Device | Priority | Notes |
|--------|----------|-------|
| **Desktop** | Primary (90%) | `layout="wide"`, full feature set |
| **Tablet** | Secondary | Streamlit stacking works acceptably |
| **Mobile** | Functional | Not optimized, not primary use case |

**Implementation:**
- `layout="wide"` for all pages
- `st.columns()` layouts that stack gracefully
- Charts with `use_container_width=True`
- No fixed-width elements

### Accessibility Strategy

**Target:** WCAG 2.1 Level AA compliance

**Built-in (Streamlit provides):**
- Keyboard navigation on all native components
- Focus indicators on interactive elements
- Semantic HTML structure

**Manual Requirements:**
- Descriptive labels on all inputs
- Chart captions explaining visualizations
- Error messages that don't rely on color alone
- Sufficient color contrast (4.5:1 minimum)

### Accessibility Checklist

| Requirement | Implementation |
|-------------|----------------|
| **Color Contrast** | All text meets 4.5:1 ratio |
| **Keyboard Access** | All actions reachable via Tab/Enter |
| **Screen Readers** | Descriptive labels and captions |
| **Focus Visible** | Streamlit default focus styles |
| **Error Identification** | Text messages, not color-only |

### Testing Strategy

| Test | Method |
|------|--------|
| **Responsive** | Chrome DevTools device emulation |
| **Keyboard** | Complete flow without mouse |
| **Screen Reader** | macOS VoiceOver walkthrough |
| **Contrast** | Browser dev tools verification |

### Pre-Release Checklist

- [ ] Full user journey completable via keyboard
- [ ] All inputs have descriptive labels
- [ ] Charts have explanatory captions
- [ ] Error states include actionable text
- [ ] No color-only information
