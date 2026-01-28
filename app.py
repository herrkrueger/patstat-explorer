import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
import time
import json
from queries_bq import QUERIES, STAKEHOLDERS

# Load environment variables
load_dotenv()


# =============================================================================
# SESSION STATE & NAVIGATION (Story 1.1)
# =============================================================================

def init_session_state():
    """Initialize session state for page navigation.

    Sets default values only if keys don't already exist.
    - current_page: 'landing' or 'detail'
    - selected_query: query ID when on detail page
    - selected_category: preserves category filter across navigation
    """
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'landing'
    if 'selected_query' not in st.session_state:
        st.session_state['selected_query'] = None
    if 'selected_category' not in st.session_state:
        st.session_state['selected_category'] = None


def go_to_landing():
    """Navigate to landing page, preserving category selection (AC #5)."""
    st.session_state['current_page'] = 'landing'
    st.session_state['selected_query'] = None
    # Keep selected_category for state restoration
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
    """Render detail page for a specific query (AC #4, #5).

    Displays:
    - Back button to return to landing page
    - Query title and description
    - Query execution interface (reuses render_query_panel logic)

    Args:
        query_id: The ID of the query to display (e.g., 'Q01')
    """
    # Back button (AC #4, #5)
    if st.button("← Back to Questions", key="back_to_landing"):
        go_to_landing()
        return  # Exit early since we're navigating

    st.divider()

    # Get query info
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

    # Show the SQL query in an expander
    with st.expander("View SQL Query", expanded=False):
        st.code(query_info["sql"], language="sql")

    st.divider()

    # Execute button - requires BigQuery client
    col1, col2 = st.columns([1, 5])
    with col1:
        execute_button = st.button("Run Query", type="primary", key="exec_detail")

    if execute_button:
        # Get or create client
        client = get_bigquery_client()
        if client is None:
            st.error("Could not connect to BigQuery.")
            return

        estimated_seconds = query_info.get("estimated_seconds_cached", 1)
        with st.spinner(f"Running query... (~{format_time(estimated_seconds)})"):
            try:
                df, execution_time = run_query(client, query_info["sql"])

                # Show results metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", f"{len(df):,}")
                with col2:
                    st.metric("Execution time", format_time(execution_time))
                with col3:
                    if estimated_seconds > 0:
                        diff = execution_time - estimated_seconds
                        delta_str = f"{'+' if diff > 0 else ''}{format_time(abs(diff))}"
                        st.metric("vs. Estimate", delta_str,
                                 delta=f"{'slower' if diff > 0 else 'faster'}",
                                 delta_color="inverse")

                st.divider()

                # Display dataframe
                st.dataframe(df, use_container_width=True, height=400)

                # Download button
                csv = df.to_csv(index=False)
                filename = f"{query_id}_{query_info['title'].lower().replace(' ', '_').replace('-', '_')}.csv"
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=filename,
                    mime="text/csv",
                    key="download_detail"
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


def run_query(client: bigquery.Client, query: str) -> tuple[pd.DataFrame, float]:
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
