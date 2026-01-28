import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
import time
import json
from queries_bq import QUERIES

# =============================================================================
# COLOR PALETTE (Story 1.4 - UX Design Spec)
# =============================================================================
COLOR_PRIMARY = "#1E3A5F"
COLOR_SECONDARY = "#0A9396"
COLOR_ACCENT = "#FFB703"
COLOR_PALETTE = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, "#E63946", "#457B9D"]

# Load environment variables
load_dotenv()


# =============================================================================
# SESSION STATE & NAVIGATION (Story 1.1)
# =============================================================================

# Default parameter values (DRY - single source of truth)
DEFAULT_YEAR_START = 2015
DEFAULT_YEAR_END = 2024
DEFAULT_JURISDICTIONS = ["EP", "US", "CN"]
DEFAULT_TECH_FIELD = None


def init_session_state():
    """Initialize session state for page navigation and parameters.

    Sets default values only if keys don't already exist.
    Navigation state:
    - current_page: 'landing' or 'detail'
    - selected_query: query ID when on detail page
    - selected_category: preserves category filter across navigation

    Parameter state (Story 1.2):
    - year_start, year_end: year range for queries
    - jurisdictions: list of patent office codes
    - tech_field: WIPO technology field code or None
    """
    # Navigation state
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'landing'
    if 'selected_query' not in st.session_state:
        st.session_state['selected_query'] = None
    if 'selected_category' not in st.session_state:
        st.session_state['selected_category'] = None

    # Parameter state (Story 1.2)
    if 'year_start' not in st.session_state:
        st.session_state['year_start'] = DEFAULT_YEAR_START
    if 'year_end' not in st.session_state:
        st.session_state['year_end'] = DEFAULT_YEAR_END
    if 'jurisdictions' not in st.session_state:
        st.session_state['jurisdictions'] = DEFAULT_JURISDICTIONS.copy()
    if 'tech_field' not in st.session_state:
        st.session_state['tech_field'] = DEFAULT_TECH_FIELD


def go_to_landing():
    """Navigate to landing page, preserving category selection (AC #5).

    Resets parameter state to defaults (Story 1.2 AC #2).
    """
    st.session_state['current_page'] = 'landing'
    st.session_state['selected_query'] = None
    # Keep selected_category for state restoration

    # Reset parameter state to defaults (Story 1.2 AC #2)
    st.session_state['year_start'] = DEFAULT_YEAR_START
    st.session_state['year_end'] = DEFAULT_YEAR_END
    st.session_state['jurisdictions'] = DEFAULT_JURISDICTIONS.copy()
    st.session_state['tech_field'] = DEFAULT_TECH_FIELD

    st.rerun()


def go_to_detail(query_id: str):
    """Navigate to detail page for a specific query (AC #4).

    Args:
        query_id: Must be a valid key in QUERIES dict
    """
    if query_id not in QUERIES:
        return  # Invalid query_id, don't navigate
    st.session_state['current_page'] = 'detail'
    st.session_state['selected_query'] = query_id
    st.rerun()


# Category definitions for landing page pills (AC #1)
CATEGORIES = ["Competitors", "Trends", "Regional", "Technology"]

# =============================================================================
# PARAMETER REFERENCE DATA (Story 1.2)
# =============================================================================

# Available jurisdictions for multiselect
JURISDICTIONS = ["EP", "US", "CN", "JP", "KR", "DE", "FR", "GB", "WO"]

# WIPO Technology Fields with sector grouping
# Source: WIPO IPC-Technology Concordance
TECH_FIELDS = {
    1: ("Electrical machinery, apparatus, energy", "Electrical engineering"),
    2: ("Audio-visual technology", "Electrical engineering"),
    3: ("Telecommunications", "Electrical engineering"),
    4: ("Digital communication", "Electrical engineering"),
    5: ("Basic communication processes", "Electrical engineering"),
    6: ("Computer technology", "Electrical engineering"),
    7: ("IT methods for management", "Electrical engineering"),
    8: ("Semiconductors", "Electrical engineering"),
    9: ("Optics", "Instruments"),
    10: ("Measurement", "Instruments"),
    11: ("Analysis of biological materials", "Instruments"),
    12: ("Control", "Instruments"),
    13: ("Medical technology", "Instruments"),
    14: ("Organic fine chemistry", "Chemistry"),
    15: ("Biotechnology", "Chemistry"),
    16: ("Pharmaceuticals", "Chemistry"),
    17: ("Macromolecular chemistry, polymers", "Chemistry"),
    18: ("Food chemistry", "Chemistry"),
    19: ("Basic materials chemistry", "Chemistry"),
    20: ("Materials, metallurgy", "Chemistry"),
    21: ("Surface technology, coating", "Chemistry"),
    22: ("Micro-structural and nano-technology", "Chemistry"),
    23: ("Chemical engineering", "Chemistry"),
    24: ("Environmental technology", "Chemistry"),
    25: ("Handling", "Mechanical engineering"),
    26: ("Machine tools", "Mechanical engineering"),
    27: ("Engines, pumps, turbines", "Mechanical engineering"),
    28: ("Textile and paper machines", "Mechanical engineering"),
    29: ("Other special machines", "Mechanical engineering"),
    30: ("Thermal processes and apparatus", "Mechanical engineering"),
    31: ("Mechanical elements", "Mechanical engineering"),
    32: ("Transport", "Mechanical engineering"),
    33: ("Furniture, games", "Other fields"),
    34: ("Other consumer goods", "Other fields"),
    35: ("Civil engineering", "Other fields"),
}


def render_parameter_block():
    """Render the parameter block with Time → Geography → Technology → Action order.

    Returns:
        tuple: (year_start, year_end, jurisdictions, tech_field, run_clicked)
    """
    with st.container(border=True):
        # Use columns for horizontal layout: Time | Geography | Technology | Action
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

        with col1:
            # Time: Year range slider
            year_range = st.slider(
                "Year Range",
                min_value=1990,
                max_value=2024,
                value=(st.session_state.get('year_start', DEFAULT_YEAR_START),
                       st.session_state.get('year_end', DEFAULT_YEAR_END)),
                help="Select the filing year range for analysis"
            )
            year_start, year_end = year_range

        with col2:
            # Geography: Jurisdiction multiselect
            jurisdictions = st.multiselect(
                "Jurisdictions",
                options=JURISDICTIONS,
                default=st.session_state.get('jurisdictions', DEFAULT_JURISDICTIONS),
                help="Select patent offices to include"
            )
            # Validation: warn if no jurisdictions selected
            if not jurisdictions:
                st.warning("Select at least one jurisdiction")

        with col3:
            # Technology: Tech field selectbox with sector grouping
            tech_options = [None] + list(TECH_FIELDS.keys())
            current_tech = st.session_state.get('tech_field', DEFAULT_TECH_FIELD)
            default_index = 0 if current_tech is None else tech_options.index(current_tech)

            tech_field = st.selectbox(
                "Technology Field",
                options=tech_options,
                index=default_index,
                format_func=lambda x: "All fields" if x is None else f"{TECH_FIELDS[x][0]} ({TECH_FIELDS[x][1]})",
                help="Filter by WIPO technology field"
            )

        with col4:
            # Action: Run button (with vertical spacing to align)
            st.write("")  # Spacing to align with other controls
            run_clicked = st.button("Run Analysis", type="primary", use_container_width=True)

    # Update session state
    st.session_state['year_start'] = year_start
    st.session_state['year_end'] = year_end
    st.session_state['jurisdictions'] = jurisdictions
    st.session_state['tech_field'] = tech_field

    return year_start, year_end, jurisdictions, tech_field, run_clicked

# =============================================================================
# INSIGHT & VISUALIZATION (Story 1.4)
# =============================================================================

def generate_insight_headline(df, query_info):
    """Generate an insight headline based on query results (Story 1.4).

    Returns a bold sentence summarizing the key finding.
    """
    if df.empty:
        return None

    category = query_info.get("category", "")
    title = query_info.get("title", "")

    # Generate headline based on data shape and category
    if len(df) == 1 and len(df.columns) == 2:
        # Single metric result
        return f"**{df.iloc[0, 0]}: {df.iloc[0, 1]}**"

    if "count" in df.columns[-1].lower() or "total" in df.columns[-1].lower():
        # Ranking/count data - highlight top result
        top_row = df.iloc[0]
        top_name = top_row.iloc[0]
        top_value = top_row.iloc[-1]
        if isinstance(top_value, (int, float)):
            return f"**{top_name} leads with {top_value:,.0f}**"

    if "year" in df.columns[0].lower():
        # Time series - show trend
        if len(df) > 1:
            first_val = df.iloc[0, -1] if pd.notna(df.iloc[0, -1]) else 0
            last_val = df.iloc[-1, -1] if pd.notna(df.iloc[-1, -1]) else 0
            if first_val > 0:
                change = ((last_val - first_val) / first_val) * 100
                trend = "increased" if change > 0 else "decreased"
                return f"**{title}: {trend} by {abs(change):.1f}% over the period**"

    # Default: row count summary
    return f"**Found {len(df):,} results for {title}**"


def render_chart(df, query_info):
    """Render an Altair chart based on query results (Story 1.4).

    Auto-detects chart type based on data shape.
    """
    if df.empty or len(df.columns) < 2:
        return None

    # Determine chart type based on data
    x_col = df.columns[0]
    y_col = df.columns[-1] if len(df.columns) > 1 else df.columns[0]

    # Check if x is temporal
    is_temporal = "year" in x_col.lower() or "date" in x_col.lower()

    # Check if we have a category column for color
    color_col = None
    if len(df.columns) >= 3:
        # Middle column might be category
        potential_color = df.columns[1]
        if df[potential_color].nunique() <= 10:
            color_col = potential_color

    try:
        if is_temporal and len(df) > 1:
            # Line chart for time series
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(f"{x_col}:O", title=x_col.replace("_", " ").title()),
                y=alt.Y(f"{y_col}:Q", title=y_col.replace("_", " ").title()),
                color=alt.Color(f"{color_col}:N", scale=alt.Scale(range=COLOR_PALETTE)) if color_col else alt.value(COLOR_PRIMARY),
                tooltip=list(df.columns)
            ).properties(height=400)
        else:
            # Bar chart for categorical data
            chart = alt.Chart(df.head(20)).mark_bar().encode(
                x=alt.X(f"{x_col}:N", title=x_col.replace("_", " ").title(), sort="-y"),
                y=alt.Y(f"{y_col}:Q", title=y_col.replace("_", " ").title()),
                color=alt.value(COLOR_PRIMARY),
                tooltip=list(df.columns)
            ).properties(height=400)

        return chart
    except Exception:
        return None


def render_metrics(df, query_info):
    """Render metric cards with delta indicators (Story 1.4)."""
    if df.empty:
        return

    # For single-row metric results, display as metric cards
    if len(df) <= 5 and len(df.columns) == 2:
        cols = st.columns(len(df))
        for i, (_, row) in enumerate(df.iterrows()):
            with cols[i]:
                label = str(row.iloc[0])
                value = row.iloc[1]
                if isinstance(value, (int, float)):
                    st.metric(label=label, value=f"{value:,.0f}")
                else:
                    st.metric(label=label, value=str(value))


def get_contextual_spinner_message(query_info):
    """Generate contextual spinner message based on query (Story 1.3)."""
    category = query_info.get("category", "")
    title = query_info.get("title", "")

    messages = {
        "Competitors": f"Finding competitive intelligence...",
        "Trends": f"Analyzing patent trends...",
        "Regional": f"Gathering regional data...",
        "Technology": f"Scanning technology landscape...",
    }
    return messages.get(category, f"Running {title}...")


# Popular queries for "Common Questions" section (AC #3)
# Selection criteria: One query per category for balanced representation
# - Q06: Competitors (Country Patent Activity)
# - Q07: Trends (Green Technology Trends)
# - Q08: Technology (Most Active Technology Fields)
# - Q11: Competitors (Top Patent Applicants)
# - Q15: Regional (German States - Medical Tech)
COMMON_QUESTIONS = ["Q06", "Q07", "Q08", "Q11", "Q15"]


def render_landing_page():
    """Render the landing page with category pills and query list (AC #1, #2, #3).

    Displays:
    - Title: "What do you want to know?"
    - Category pills for filtering
    - Common Questions section with popular queries
    - Full query list filtered by selected category
    """
    # Page title (AC #1)
    st.header("What do you want to know?")

    ''  # Spacing

    # Category pills (AC #1, #2)
    selected = st.pills(
        "Categories",
        options=CATEGORIES,
        default=st.session_state.get('selected_category'),
        selection_mode="single",
        key="category_pills"
    )

    # Update session state if category changed
    if selected != st.session_state.get('selected_category'):
        st.session_state['selected_category'] = selected

    ''  # Spacing

    # Common Questions section (AC #3)
    st.subheader("Common Questions")

    cols = st.columns(len(COMMON_QUESTIONS))
    for i, query_id in enumerate(COMMON_QUESTIONS):
        if query_id in QUERIES:
            query_info = QUERIES[query_id]
            with cols[i]:
                # Display as clickable card with question-style title
                if st.button(
                    query_info['title'],
                    key=f"common_{query_id}",
                    use_container_width=True
                ):
                    go_to_detail(query_id)

    ''  # Spacing
    st.divider()

    # Full query list with filtering (AC #2)
    render_query_list(selected)


def render_query_list(category_filter):
    """Render query list filtered by category (AC #2).

    Args:
        category_filter: Category name to filter by, or None for all queries
    """
    filtered_queries = QUERIES
    if category_filter:
        filtered_queries = {
            qid: qinfo for qid, qinfo in QUERIES.items()
            if qinfo.get("category") == category_filter
        }

    if not filtered_queries:
        st.info(f"No queries in category: {category_filter}")
        return

    for query_id, query_info in filtered_queries.items():
        if st.button(
            f"{query_id}: {query_info['title']}",
            key=f"query_{query_id}",
            use_container_width=True
        ):
            go_to_detail(query_id)


def render_detail_page(query_id: str):
    """Render detail page for a specific query (Story 1.1 AC #4, #5, Story 1.2 AC #1).

    Displays:
    - Back button to return to landing page
    - Parameter block with Time → Geography → Technology → Action (Story 1.2)
    - Query title and description
    - Query execution and results

    Args:
        query_id: The ID of the query to display (e.g., 'Q01')
    """
    # Back button (AC #4, #5)
    if st.button("← Back to Questions", key="back_to_landing"):
        go_to_landing()
        return  # Exit early since we're navigating

    # Get query info first to check validity
    if query_id not in QUERIES:
        st.error(f"Query '{query_id}' not found.")
        return

    query_info = QUERIES[query_id]

    # Header with ID and title
    st.header(f"{query_id}: {query_info['title']}")

    # Tags as pills
    tag_colors = {"PATLIB": "#1f77b4", "BUSINESS": "#2ca02c", "UNIVERSITY": "#9467bd"}
    tags_html = " ".join([
        f'<span style="background-color: {tag_colors.get(t, "#666")}; '
        f'color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.85em; margin-right: 6px;">{t}</span>'
        for t in query_info.get("tags", [])
    ])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown("")

    # Query description
    st.markdown(f"**{query_info.get('description', '')}**")

    ''  # Spacing

    # Parameter block (Story 1.2 AC #1)
    year_start, year_end, jurisdictions, tech_field, run_clicked = render_parameter_block()

    ''  # Spacing

    # Show explanation in an expander
    if "explanation" in query_info:
        with st.expander("Details", expanded=False):
            st.markdown(query_info["explanation"])

            if "key_outputs" in query_info:
                st.markdown("**Key Outputs:**")
                for output in query_info["key_outputs"]:
                    st.markdown(f"- {output}")

    # Show estimated time
    estimated_cached = query_info.get("estimated_seconds_cached", 0)
    estimated_first = query_info.get("estimated_seconds_first_run", estimated_cached)
    if estimated_first > 0:
        if estimated_first != estimated_cached:
            st.caption(f"Estimated: ~{format_time(estimated_cached)} (cached) / ~{format_time(estimated_first)} (first run)")
        else:
            st.caption(f"Estimated: ~{format_time(estimated_cached)}")

    # Show the SQL query with parameter substitution (Story 1.6)
    with st.expander("View SQL Query", expanded=False):
        # Display SQL with current parameter values substituted for clarity
        display_sql = query_info["sql"]
        # Show parameter context
        st.caption(f"Parameters: Years {year_start}-{year_end} | Jurisdictions: {', '.join(jurisdictions) if jurisdictions else 'None'} | Tech Field: {tech_field or 'All'}")
        st.code(display_sql.strip(), language="sql")

    # Methodology note if available (Story 1.6)
    if "methodology" in query_info:
        with st.expander("Methodology", expanded=False):
            st.markdown(query_info["methodology"])

    st.divider()

    # Execute when Run Analysis clicked (from parameter block)
    if run_clicked:
        # Get or create client
        client = get_bigquery_client()
        if client is None:
            st.error("Could not connect to BigQuery.")
            return

        # Contextual spinner message (Story 1.3)
        spinner_msg = get_contextual_spinner_message(query_info)
        estimated_seconds = query_info.get("estimated_seconds_cached", 1)

        with st.spinner(f"{spinner_msg} (~{format_time(estimated_seconds)})"):
            try:
                df, execution_time = run_query(client, query_info["sql"])

                # Empty results handling (Story 1.3)
                if df.empty:
                    st.warning("No results found for your query.")
                    st.info("**Suggestions:** Try broadening the year range or selecting different jurisdictions.")
                    return

                # Insight headline (Story 1.4) - appears FIRST
                headline = generate_insight_headline(df, query_info)
                if headline:
                    st.markdown(headline)
                    ''  # Spacing

                # Execution metrics row
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Results", f"{len(df):,} rows")
                with col2:
                    st.metric("Execution", format_time(execution_time))
                with col3:
                    if estimated_seconds > 0:
                        diff = execution_time - estimated_seconds
                        delta_str = f"{'+' if diff > 0 else ''}{format_time(abs(diff))}"
                        st.metric("vs. Est.", delta_str,
                                 delta=f"{'slower' if diff > 0 else 'faster'}",
                                 delta_color="inverse")

                ''  # Spacing

                # Chart visualization (Story 1.4)
                chart = render_chart(df, query_info)
                if chart:
                    st.altair_chart(chart, use_container_width=True)

                # Metric cards for small datasets (Story 1.4)
                if len(df) <= 5 and len(df.columns) == 2:
                    render_metrics(df, query_info)

                # Data table in expander (Story 1.3)
                with st.expander("View Data Table", expanded=False):
                    st.dataframe(df, use_container_width=True, height=400)

                st.divider()

                # Download buttons (Story 1.5)
                col1, col2 = st.columns(2)
                timestamp = time.strftime("%Y%m%d")
                base_filename = f"{query_id}_{query_info['title'].lower().replace(' ', '_').replace('-', '_')}"

                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Data (CSV)",
                        data=csv,
                        file_name=f"{base_filename}_{timestamp}.csv",
                        mime="text/csv",
                        key="download_csv"
                    )

                with col2:
                    # Chart download as HTML (Altair interactive)
                    if chart:
                        chart_html = chart.to_html()
                        st.download_button(
                            label="📊 Download Chart (HTML)",
                            data=chart_html,
                            file_name=f"{base_filename}_{timestamp}_chart.html",
                            mime="text/html",
                            key="download_chart"
                        )

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Page config
st.set_page_config(
    page_title="PATSTAT Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PATSTAT Explorer")
st.caption("Patent Analysis Platform - EPO PATSTAT 2025 Autumn on BigQuery by mtc")


@st.cache_resource
def get_bigquery_client():
    """Create and cache BigQuery client."""
    project = os.getenv("BIGQUERY_PROJECT", "patstat-mtc")

    # Check for Streamlit Cloud secrets first
    try:
        if "gcp_service_account" in st.secrets:
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"]
            )
            return bigquery.Client(credentials=credentials, project=project)
    except FileNotFoundError:
        pass  # No secrets.toml file, try other methods

    # Check for service account JSON in environment (local dev or Streamlit Cloud)
    service_account_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if service_account_json:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(service_account_json)
        )
        return bigquery.Client(credentials=credentials, project=project)

    # Fall back to Application Default Credentials
    return bigquery.Client(project=project)


def run_query(client, query):
    """Execute a query and return results as DataFrame with execution time."""
    project = os.getenv("BIGQUERY_PROJECT", "patstat-mtc")
    dataset = os.getenv("BIGQUERY_DATASET", "patstat")

    # Set default dataset so queries don't need fully qualified table names
    job_config = bigquery.QueryJobConfig(
        default_dataset=f"{project}.{dataset}"
    )

    start_time = time.time()
    result = client.query(query, job_config=job_config).to_dataframe()
    execution_time = time.time() - start_time
    return result, execution_time


def format_time(seconds: float) -> str:
    """Format seconds into human-readable string."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"


def main():
    """Main application entry point with session-state based routing (Story 1.1).

    Routes between:
    - Landing page: Category pills + query list + common questions
    - Detail page: Query parameters + execution + results
    """
    # Initialize session state for navigation
    init_session_state()

    client = get_bigquery_client()

    if client is None:
        st.stop()

    # Route based on current_page session state (Task 6)
    if st.session_state.get('current_page') == 'detail':
        # Detail page: Show selected query (AC #4)
        query_id = st.session_state.get('selected_query')
        if query_id:
            render_detail_page(query_id)
        else:
            # Fallback to landing if no query selected
            st.session_state['current_page'] = 'landing'
            render_landing_page()
    else:
        # Landing page: Show categories and query list (AC #1, #2, #3)
        render_landing_page()


if __name__ == "__main__":
    main()
