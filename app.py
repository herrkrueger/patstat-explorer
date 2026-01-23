import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from queries import QUERIES

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="PATSTAT Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PATSTAT Explorer")


@st.cache_resource
def get_database_connection():
    """Create and cache database connection."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        st.error("DATABASE_URL not configured. Please check your .env file.")
        return None
    return create_engine(database_url)


def run_query(engine, query: str) -> pd.DataFrame:
    """Execute a query and return results as DataFrame."""
    with engine.connect() as conn:
        result = pd.read_sql(text(query), conn)
    return result


def main():
    engine = get_database_connection()

    if engine is None:
        st.stop()

    # Sidebar for navigation
    st.sidebar.header("Navigation")

    # Stakeholder selection
    stakeholders = list(QUERIES.keys())
    selected_stakeholder = st.sidebar.selectbox(
        "Select Stakeholder",
        stakeholders,
        index=0 if stakeholders else None
    )

    if selected_stakeholder:
        st.header(f"Queries for: {selected_stakeholder}")

        # Get queries for selected stakeholder
        stakeholder_queries = QUERIES[selected_stakeholder]
        query_names = list(stakeholder_queries.keys())

        # Query selection
        selected_query = st.selectbox(
            "Select Query",
            query_names,
            index=0 if query_names else None
        )

        if selected_query:
            query_info = stakeholder_queries[selected_query]

            # Show query description
            if "description" in query_info:
                st.info(query_info["description"])

            # Show the SQL query in an expander
            with st.expander("View SQL Query"):
                st.code(query_info["sql"], language="sql")

            # Execute button
            if st.button("Execute Query", type="primary"):
                with st.spinner("Running query..."):
                    try:
                        df = run_query(engine, query_info["sql"])

                        # Show results
                        st.success(f"Query returned {len(df)} rows")

                        # Display dataframe
                        st.dataframe(df, use_container_width=True)

                        # Download button
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{selected_query.lower().replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Error executing query: {str(e)}")
    else:
        st.info("Please select a stakeholder from the sidebar.")


if __name__ == "__main__":
    main()
