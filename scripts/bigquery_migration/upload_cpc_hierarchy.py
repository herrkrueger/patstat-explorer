#!/usr/bin/env python3
"""
Upload CPC Hierarchy to BigQuery.

Reads the CPC classification hierarchy from SQLite and uploads it to BigQuery
as the `tls_cpc_hierarchy` reference table, enabling JOINs to PATSTAT tables.

Usage:
    python upload_cpc_hierarchy.py /path/to/cpc-classification-2026.db
    python upload_cpc_hierarchy.py /path/to/cpc-classification-2026.db --dry-run

Prerequisites:
    pip install google-cloud-bigquery python-dotenv
    Service account JSON in .env as GOOGLE_APPLICATION_CREDENTIALS_JSON
    Or: gcloud auth application-default login
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account


# BigQuery target
PROJECT_ID = "patstat-mtc"
DATASET_ID = "patstat"
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.tls_cpc_hierarchy"

# Schema for the target table
SCHEMA = [
    bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("symbol_short", "STRING"),
    bigquery.SchemaField("symbol_patstat", "STRING"),
    bigquery.SchemaField("kind", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("level", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("parent", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("parent_short", "STRING"),
    bigquery.SchemaField("title_en", "STRING"),
    bigquery.SchemaField("title_full", "STRING"),
    bigquery.SchemaField("not_allocatable", "BOOL"),
    bigquery.SchemaField("additional_only", "BOOL"),
    bigquery.SchemaField("status", "STRING"),
]


def get_bigquery_client(project_id: str) -> bigquery.Client:
    """Create BigQuery client using gcloud default credentials or service account from .env."""
    import google.auth

    # Try gcloud default credentials first (has write access after `gcloud auth application-default login`)
    try:
        credentials, _ = google.auth.default()
        print("  Using gcloud application-default credentials")
        return bigquery.Client(project=project_id, credentials=credentials)
    except google.auth.exceptions.DefaultCredentialsError:
        pass

    # Fall back to service account from .env (read-only)
    project_root = Path(__file__).parent.parent.parent
    load_dotenv(project_root / ".env")

    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not creds_json:
        raise ValueError(
            "No credentials found. Run `gcloud auth application-default login` "
            "or add GOOGLE_APPLICATION_CREDENTIALS_JSON to .env"
        )

    creds_info = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(creds_info)
    print("  Using service account from .env")

    return bigquery.Client(project=project_id, credentials=credentials)


def read_sqlite_database(db_path: Path) -> dict:
    """Read all CPC entries from SQLite and return as lookup dict."""
    print(f"Reading SQLite database: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT symbol, symbol_short, symbol_patstat, kind, level, parent, parent_short,
               title_en, not_allocatable, additional_only, status
        FROM cpc
        WHERE symbol != 'CPC'
    """)

    rows = cur.fetchall()
    conn.close()

    print(f"  Loaded {len(rows):,} entries")

    # Build lookup dict
    lookup = {}
    for (symbol, symbol_short, symbol_patstat, kind, level, parent, parent_short,
         title_en, not_allocatable, additional_only, status) in rows:
        lookup[symbol] = {
            "symbol_short": symbol_short,
            "symbol_patstat": symbol_patstat,
            "kind": kind,
            "level": level,
            "parent": parent,
            "parent_short": parent_short,
            "title_en": title_en,
            "not_allocatable": bool(not_allocatable),
            "additional_only": bool(additional_only),
            "status": status,
        }

    return lookup


def build_title_full(symbol: str, lookup: dict, from_level: int = 7) -> str:
    """Build concatenated title from main group level (7) downwards.

    Example: 'Y02E0010440000' -> 'Energy generation through renewable energy sources > Solar thermal energy > Heat exchange systems'
    """
    chain = []
    current = symbol

    while current in lookup:
        entry = lookup[current]
        if entry["level"] < from_level:
            break
        if entry["title_en"]:
            chain.append(entry["title_en"])
        current = entry["parent"]

    chain.reverse()
    return " > ".join(chain) if chain else lookup.get(symbol, {}).get("title_en", "")


def prepare_bigquery_rows(lookup: dict) -> list:
    """Convert lookup dict to list of BigQuery row dicts."""
    print("Preparing rows for BigQuery...")

    bq_rows = []

    for symbol, data in lookup.items():
        # Generate full title chain
        title_full = build_title_full(symbol, lookup)

        bq_rows.append({
            "symbol": symbol,
            "symbol_short": data["symbol_short"],
            "symbol_patstat": data["symbol_patstat"],
            "kind": data["kind"],
            "level": data["level"],
            "parent": data["parent"],
            "parent_short": data["parent_short"],
            "title_en": data["title_en"],
            "title_full": title_full,
            "not_allocatable": data["not_allocatable"],
            "additional_only": data["additional_only"],
            "status": data["status"],
        })

    print(f"  Prepared {len(bq_rows):,} rows")

    # Stats
    with_patstat = sum(1 for r in bq_rows if r["symbol_patstat"])
    with_title_full = sum(1 for r in bq_rows if r["title_full"])
    print(f"  Rows with symbol_patstat: {with_patstat:,}")
    print(f"  Rows with title_full: {with_title_full:,}")

    return bq_rows


def upload_to_bigquery(bq_rows: list, dry_run: bool = False):
    """Upload rows to BigQuery."""
    if dry_run:
        print(f"\n[DRY RUN] Would upload {len(bq_rows):,} rows to {TABLE_ID}")
        print("\nSample rows:")
        for row in bq_rows[:3]:
            title = row['title_en'] or "(no title)"
            print(f"  {row['symbol_short']}: {title[:50]}...")
            print(f"    symbol_patstat: {row['symbol_patstat']}")
            if row['title_full']:
                print(f"    title_full: {row['title_full'][:80]}...")
        return

    print(f"\nUploading to BigQuery: {TABLE_ID}")

    client = get_bigquery_client(PROJECT_ID)

    job_config = bigquery.LoadJobConfig(
        schema=SCHEMA,
        write_disposition="WRITE_TRUNCATE",
    )

    job = client.load_table_from_json(bq_rows, TABLE_ID, job_config=job_config)
    job.result()  # Wait for completion

    print(f"  Loaded {job.output_rows:,} rows into {TABLE_ID}")
    print("  Done!")


def print_validation_queries():
    """Print validation queries to run after upload."""
    print("\n" + "=" * 60)
    print("VALIDATION QUERIES - Run these in BigQuery Console:")
    print("=" * 60)

    queries = [
        ("Row count (expect ~254,249)",
         "SELECT COUNT(*) as cnt FROM `patstat-mtc.patstat.tls_cpc_hierarchy`"),

        ("Level distribution",
         """SELECT level, COUNT(*) as cnt
FROM `patstat-mtc.patstat.tls_cpc_hierarchy`
GROUP BY level ORDER BY level"""),

        ("JOIN test with tls225_docdb_fam_cpc",
         """SELECT c.docdb_family_id, c.cpc_class_symbol, h.title_en
FROM `patstat-mtc.patstat.tls225_docdb_fam_cpc` c
JOIN `patstat-mtc.patstat.tls_cpc_hierarchy` h
  ON c.cpc_class_symbol = h.symbol_patstat
WHERE c.cpc_value = 'I'
LIMIT 5"""),

        ("Y02 green tech codes",
         """SELECT symbol_short, title_en, title_full
FROM `patstat-mtc.patstat.tls_cpc_hierarchy`
WHERE symbol_short LIKE 'Y02E%' AND level = 8
LIMIT 5"""),
    ]

    for name, sql in queries:
        print(f"\n-- {name}")
        print(sql)


def main():
    parser = argparse.ArgumentParser(
        description="Upload CPC hierarchy from SQLite to BigQuery"
    )
    parser.add_argument(
        "db_path",
        type=Path,
        help="Path to cpc-classification-2026.db"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without uploading"
    )

    args = parser.parse_args()

    if not args.db_path.exists():
        print(f"Error: Database not found: {args.db_path}")
        sys.exit(1)

    # Read SQLite
    lookup = read_sqlite_database(args.db_path)

    # Prepare rows
    bq_rows = prepare_bigquery_rows(lookup)

    # Upload
    upload_to_bigquery(bq_rows, dry_run=args.dry_run)

    # Print validation queries
    print_validation_queries()


if __name__ == "__main__":
    main()
