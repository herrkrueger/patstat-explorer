"""
PATSTAT Queries organized by Stakeholder.

Structure:
QUERIES = {
    "Stakeholder Name": {
        "Query Name": {
            "description": "What this query does",
            "sql": "SELECT ... FROM ..."
        },
        ...
    },
    ...
}

TODO: Add your BigQuery queries here, converted to PostgreSQL syntax.
Key differences from BigQuery to PostgreSQL:
- Use LIMIT instead of LIMIT in subqueries
- Use || for string concatenation instead of CONCAT()
- Use TO_CHAR() for date formatting instead of FORMAT_DATE()
- Use COALESCE() instead of IFNULL()
- Standard SQL JOINs work the same
"""

QUERIES = {
    "Overview": {
        "Database Tables": {
            "description": "List all tables in the PATSTAT database",
            "sql": """
                SELECT table_name, table_type
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """
        },
        "Sample Patents": {
            "description": "Get a sample of 100 patents from tls201_appln",
            "sql": """
                SELECT *
                FROM tls201_appln
                LIMIT 100
            """
        },
    },
    # TODO: Add your stakeholder queries below
    # Example structure:
    #
    # "Research & Development": {
    #     "Patent Applications by Year": {
    #         "description": "Count of patent applications per year",
    #         "sql": """
    #             SELECT
    #                 EXTRACT(YEAR FROM appln_filing_date) AS year,
    #                 COUNT(*) AS application_count
    #             FROM tls201_appln
    #             WHERE appln_filing_date IS NOT NULL
    #             GROUP BY EXTRACT(YEAR FROM appln_filing_date)
    #             ORDER BY year DESC
    #             LIMIT 20
    #         """
    #     },
    # },
}
