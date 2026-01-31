# PATSTAT Explorer - Utility Functions
# Pure helper functions with no UI or state dependencies

import re


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


def detect_sql_parameters(sql: str) -> list:
    """Extract @parameter names from SQL (Story 3.2)."""
    pattern = r'@(\w+)'
    return list(set(re.findall(pattern, sql)))


def format_sql_for_tip(sql: str, params: dict) -> str:
    """Format SQL for use in TIP by substituting actual parameter values.

    TIP uses PatstatClient which executes raw SQL directly, so we need to
    replace @param placeholders with actual values.
    """
    formatted_sql = sql

    # Remove backticks from table names (TIP doesn't need them)
    formatted_sql = re.sub(r'`([^`]+)`', r'\1', formatted_sql)

    # Substitute year parameters
    if params.get('year_start') is not None:
        formatted_sql = formatted_sql.replace('@year_start', str(params['year_start']))
    if params.get('year_end') is not None:
        formatted_sql = formatted_sql.replace('@year_end', str(params['year_end']))

    # Substitute jurisdictions array - convert UNNEST(@jurisdictions) to IN ('EP', 'US', 'DE')
    if params.get('jurisdictions'):
        jurisdiction_list = ", ".join([f"'{j}'" for j in params['jurisdictions']])
        # Replace UNNEST(@jurisdictions) pattern with IN clause
        formatted_sql = re.sub(
            r'IN\s+UNNEST\s*\(\s*@jurisdictions\s*\)',
            f"IN ({jurisdiction_list})",
            formatted_sql,
            flags=re.IGNORECASE
        )

    # Substitute tech_field (integer)
    if params.get('tech_field') is not None:
        formatted_sql = formatted_sql.replace('@tech_field', str(params['tech_field']))

    # Substitute tech_sector (string)
    if params.get('tech_sector') is not None:
        formatted_sql = formatted_sql.replace('@tech_sector', f"'{params['tech_sector']}'")

    # Substitute applicant_name (string)
    if params.get('applicant_name') is not None:
        # Escape single quotes in the name
        safe_name = params['applicant_name'].replace("'", "''")
        formatted_sql = formatted_sql.replace('@applicant_name', f"'{safe_name}'")

    # Substitute ipc_class (string)
    if params.get('ipc_class') is not None:
        formatted_sql = formatted_sql.replace('@ipc_class', f"'{params['ipc_class']}'")

    # Substitute competitors array
    if params.get('competitors'):
        competitors_list = ", ".join([f"'{c}'" for c in params['competitors']])
        formatted_sql = re.sub(
            r'UNNEST\s*\(\s*@competitors\s*\)',
            f"({competitors_list})",
            formatted_sql,
            flags=re.IGNORECASE
        )

    # Clean up whitespace
    formatted_sql = formatted_sql.strip()

    return formatted_sql
