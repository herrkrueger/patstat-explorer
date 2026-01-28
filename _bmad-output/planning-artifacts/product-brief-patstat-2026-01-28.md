---
stepsCompleted: [1, 2, 3, 4, 5, 6]
status: complete
inputDocuments:
  - context/BPM001977_Technical_Specifications__TIP4PATLIB.pdf
  - context/streamlit_examples/gdp_streamlit_app.py
  - context/streamlit_examples/stock_streamlit_app.py
  - context/streamlit_examples/ai_assis_streamlit_app.py
  - context/medtech/medtech_comparison_analysis.py
  - context/medtech/medtech_multi_jurisdiction.py
  - context/ree_notebooks/01_REE_Ranking_Applicants_ENHANCED.ipynb
  - docs/index.md
  - docs/project-overview.md
  - docs/query-catalog.md
  - docs/bigquery-schema.md
referenceDocuments:
  - context/epo_patstat_training/* (57 PDFs - EPO training materials)
  - context/medtech/* (4 Python scripts)
  - context/ree_notebooks/* (5 Jupyter notebooks)
date: 2026-01-28
author: Arne
project: patstat
---

# Product Brief: PATSTAT Explorer / TIP4PATLIB

## Executive Summary

**PATSTAT Explorer** transforms complex patent intelligence into accessible, actionable insights for the 300+ PATLIB centres across Europe. As part of the EPO PATLIB2028 initiative, this platform eliminates the technical barriers that prevent patent information professionals from leveraging PATSTAT's powerful analytics capabilities.

The platform converts proven, EPO-validated patent queries into an intuitive web interface where PATLIB staff can perform regional, sectoral, and comparative analyses without writing code, accessing TIP, or reading GitHub repositories. Beyond consumption, the platform enables PATLIBs to contribute and share queries, building a community-driven library of patent intelligence use cases.

**Target:** EPO Academy training program for PATLIB staff
**Reach:** 300+ PATLIB centres across Europe
**Value:** From overwhelmed to empowered in patent analytics

---

## Core Vision

### Problem Statement

PATLIB staff face **decision paralysis** when trying to help their SME clients, researchers, and regional authorities with patent intelligence. The question is not "how do I analyze patents?" but rather:

- *"Which tool do I choose - Orbit, Patbase, TIP, or PATSTAT?"*
- *"How do I code Python to answer my client's question?"*
- *"How do I use AI tools like Claude Code effectively?"*

The result: powerful patent analytics capabilities remain locked behind technical complexity, while PATLIB professionals feel overwhelmed rather than empowered.

### Problem Impact

- **For PATLIB Staff:** Inability to independently deliver advanced patent insights to clients
- **For SME Clients:** Delayed or simplified answers instead of comprehensive intelligence
- **For Regional Innovation:** Underutilized patent data that could drive economic development
- **For EPO:** PATLIB2028 goals at risk if staff cannot confidently use TIP

### Why Existing Solutions Fall Short

| Solution | Limitation |
|----------|------------|
| **TIP/PATSTAT directly** | Requires Python skills, overwhelming interface |
| **Jupyter notebooks** | "Ugly," code-heavy, intimidating for non-coders |
| **GitHub repositories** | Requires technical navigation, version control knowledge |
| **Training alone** | Knowledge fades without accessible tools to practice |

The validated queries exist - in EPO training notebooks, in medtech analysis scripts, in REE research - but they're trapped in formats that exclude 90% of potential users.

### Proposed Solution

**PATSTAT Explorer** provides:

1. **Zero-Friction Access:** Web-based interface - no TIP login, no code, no GitHub
2. **Proven Query Library:** 50+ validated queries from EPO training, medtech, and REE research
3. **Dynamic Parameters:** All queries become interactive - adjust jurisdiction, year range, technology field
4. **Relatable Examples:** "Your university's inventions," "Your region's patent leaders," "Your client's competitors"
5. **Community Contribution:** PATLIBs can add, share, and discover queries from peers
6. **AI-Assisted Query Building:** Generate new queries through natural language (MCP integration)
7. **Training Integration:** Direct pathway from EPO Academy training to practical application

### Key Differentiators

| Differentiator | Why It Matters |
|----------------|----------------|
| **EPO-Endorsed Content** | Queries validated by patent experts, not random internet code |
| **300 PATLIB Reach** | Single platform serves entire European PATLIB network |
| **Contribution Model** | PATLIBs become creators, not just consumers |
| **Personal Relevance** | "My university" not "patent statistics" |
| **Zero Technical Barrier** | No Python, no TIP, no GitHub - just insights |

---

## Target Users

### Primary Users

#### Maria - The Generalist PATLIB Professional (90% of users)

**Profile:** Patent Information Specialist at a regional PATLIB centre in Spain. 15 years experience navigating Espacenet, Orbit, and national patent databases. Knows the intricacies of EP vs. US vs. CN filing procedures better than most patent attorneys.

**Current Frustration:** When a local SME asks "Who are my competitors in medical device packaging?" Maria can find individual patents, but transforming that into a strategic picture requires skills she doesn't have. She's tried Jupyter notebooks from EPO training - too code-heavy. She's seen what's possible but can't replicate it.

**Success Moment:** Maria runs a competitor analysis query, exports a polished chart showing filing trends by jurisdiction, and presents it to her client the same afternoon. The SME owner says "This is exactly what I needed." Maria looks like a data expert - without writing a single line of code.

**Tool Relationship:** Consumer of queries. Exports results to PowerPoint/Word for client reports. Values clear explanations of what each query reveals.

---

#### Klaus - The PATLIB Data Enthusiast (10% of users)

**Profile:** Senior Patent Analyst at a German PATLIB centre with a side passion for data. Self-taught SQL, builds dashboards in Tableau for internal use. Frustrated that his queries live on his laptop where nobody else can use them.

**Current Frustration:** Klaus has written 20+ useful PATSTAT queries over the years. Colleagues ask him for help constantly, but he can't scale himself. He wants to share his work but there's no platform for it.

**Success Moment:** Klaus contributes his "Regional Innovation Hotspots" query to PATSTAT Explorer. Three months later, he sees it being used in an EPO Academy training session. His expertise now helps 300 PATLIB centres, not just his own.

**Tool Relationship:** Both consumer and contributor. Wants to see the SQL, might suggest improvements, uploads new queries for peer review.

---

#### Dr. Elena Vasquez - The EPO Academy Trainer

**Profile:** Senior Training Officer at EPO Academy. Responsible for the TIP4PATLIB curriculum. Measured by student engagement scores and post-training competency assessments.

**Current Frustration:** Training sessions on PATSTAT/TIP get mixed reviews. Students are impressed by what's *possible* but overwhelmed by *how* to do it. They leave inspired but not empowered.

**Success Moment:** Elena demos PATSTAT Explorer during training. Students immediately replicate the analysis with their own region's data. Post-training surveys show 4.8/5 stars. Students write: "Finally, I can actually *do* this back at my centre."

**Tool Relationship:** Uses app as training demonstration platform. Success = students who become confident users. All credit flows to EPO Academy program.

---

### Secondary Users

#### The End Client (SME owners, IP managers, researchers, press, politicians)

These users never touch PATSTAT Explorer directly. They have the *real* questions:

- **SME Owner:** "What's the filing strategy of my competitors?"
- **IP Manager:** "How is our technology field developing?"
- **Researcher:** "Who are the key players in rare earth element patents?"
- **Journalist:** "Which countries lead in green technology patents?"
- **Regional Politician:** "How does our state compare to others in medical tech innovation?"

**Their Experience:** They receive polished charts and short, memorable insights from their PATLIB contact. They never see the query or the data tables - just the story the data tells.

**What They Need:** Beautiful visualizations. One-sentence takeaways. Data that supports decisions or headlines.

---

### User Journey

| Stage | Maria (Generalist) | Klaus (Data Enthusiast) |
|-------|-------------------|------------------------|
| **Discovery** | EPO Academy training session | Colleague mentions it, or finds via EPO channels |
| **First Use** | Runs a familiar query (competitor analysis) with her region's parameters | Browses query library, checks SQL to understand approach |
| **Aha Moment** | "I just did in 5 minutes what used to take me a full day" | "I can finally share my queries with everyone" |
| **Core Usage** | Weekly client reports, exports charts to presentations | Contributes queries, refines existing ones, helps colleagues |
| **Long-term** | Go-to tool for any data question from clients | Becomes a recognized contributor in the PATLIB community |

---

## Success Metrics

### User Success Metrics

| Persona | Success Indicator | Measurement |
|---------|------------------|-------------|
| **Maria (Generalist)** | Client satisfaction with insights delivered | Qualitative feedback, repeat usage |
| **Klaus (Data Enthusiast)** | Queries contributed to library | Count of submitted queries |
| **Klaus (Data Enthusiast)** | Queries reused by peers | Usage count per contributed query |
| **Elena (EPO Trainer)** | Training engagement scores | Post-session ratings (target: 4.5+/5) |
| **Elena (EPO Trainer)** | Post-training TIP adoption | Students who click "Take to TIP" within 30 days |

### Business Objectives

#### The Gateway Strategy

PATSTAT Explorer operates as a **TIP adoption accelerator** - a free, accessible entry point that demonstrates value and funnels users toward EPO's TIP platform.

| Timeframe | Objective | Why It Matters |
|-----------|-----------|----------------|
| **3 months** | EPO Academy adopts tool for TIP4PATLIB training | Validates training use case |
| **6 months** | Measurable increase in "Take to TIP" conversions | Proves gateway strategy works |
| **12 months** | TIP usage increase attributable to Explorer users | Ultimate success for EPO |

#### Strategic Success

- **For EPO:** TIP adoption rises because PATLIB staff saw accessible examples first
- **For PATLIB Centres:** Staff confidently use TIP after Explorer on-ramp
- **For Arne:** Positive feedback flows to EPO Academy (not personal credit)

### Key Performance Indicators

| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| **Query Library Growth** | 50+ queries in library | Count of validated queries |
| **Training Sessions Using Explorer** | Used in EPO Academy curriculum | EPO Academy confirmation |
| **"Take to TIP" Clicks** | 20% of query executions result in TIP export | Button click tracking |
| **Contributor Engagement** | 10+ unique PATLIB contributors | Submitted query count by author |
| **PATLIB Centre Reach** | 50+ centres with active users | Unique centre identification |

### Leading Indicators (Early Signals)

- Users who run >3 queries in first session (engagement)
- Users who return within 7 days (retention)
- Users who click "View SQL" (pathway to contribution/TIP)
- Training attendees who access Explorer same week (activation)

---

## MVP Scope

### Core Features (All Required for Launch)

#### Query Library Expansion
- **Current:** 19 queries (18 static + 1 dynamic)
- **MVP Target:** ~40 queries (add ~20 from EPO training materials)
- **Selection Criteria:** Most useful/relatable queries from 57 EPO training PDFs

#### Dynamic Query Conversion
- Convert all 18 static queries to parameterized/dynamic
- User-adjustable parameters: jurisdiction, year range, technology field, etc.
- Consistent pattern across all queries (like the recently enhanced DQ01)

#### UI Beautification
- Streamlit styling improvements for professional appearance
- Beautiful charts suitable for client presentations
- Clear, scannable layouts for training demos

#### Query Contribution Model
- Interface for data enthusiasts (Klaus persona) to submit queries
- Simple submission flow (no approval workflow in MVP)
- SQL visibility for transparency and learning

#### AI-Assisted Query Building
- Natural language to SQL via MCP integration
- Users describe what they want, AI generates query
- Lowers barrier for custom analyses

#### TIP Gateway
- "Take to TIP" button (existing - GitHub link + README)
- Clear pathway from Explorer demo to TIP adoption

### Out of Scope for MVP

| Feature | Rationale |
|---------|-----------|
| **User Authentication** | Open access - no login barriers |
| **Query Moderation Workflow** | Trust-based contribution, no approval queue |
| **Multi-Language Support** | English only for initial launch |
| **Mobile Optimization** | Desktop-first (training room use case) |
| **Custom Analytics Dashboard** | Rely on Streamlit Cloud built-in stats |
| **Full EPO Training Import** | 20 queries now, remaining 37 PDFs post-MVP |
| **Production Architecture** | Streamlit.app is the permanent home |

### Architecture Decision

**Streamlit.app = Final Destination**

This is explicitly a demo/training tool, not production enterprise software. The architecture choice is intentional:
- Zero infrastructure maintenance
- Instant deployment
- Good enough for training and client demos
- No scaling concerns (not built for 1000 concurrent users)

### MVP Success Criteria

| Criterion | Validation |
|-----------|------------|
| **EPO Academy Adoption** | Tool used in at least one TIP4PATLIB training session |
| **Query Library Complete** | 40+ queries available and documented |
| **All Queries Dynamic** | Every query has user-adjustable parameters |
| **"Take to TIP" Conversions** | At least 10% of users click the TIP export |
| **Trainer Satisfaction** | Elena persona gives positive feedback |

### Future Vision (Post-MVP)

If successful, potential enhancements:
- Import remaining 37 EPO training queries
- Community voting on most useful queries
- Regional PATLIB customizations (local examples)
- Integration showcases with other EPO tools
- Expanded AI capabilities (query explanation, optimization suggestions)

**Note:** Future features are opportunities, not commitments. MVP success determines next steps.
