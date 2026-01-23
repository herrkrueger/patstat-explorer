#!/usr/bin/env python3
"""Test all PATSTAT queries and report errors."""

import os
import sys
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from queries import QUERIES

load_dotenv()

def test_all_queries():
    """Test all queries and return results."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL not set")
        sys.exit(1)

    engine = create_engine(database_url)

    results = []
    total = 0
    passed = 0
    failed = 0

    for stakeholder, queries in QUERIES.items():
        print(f"\n{'='*60}")
        print(f"Testing: {stakeholder}")
        print('='*60)

        for query_name, query_info in queries.items():
            total += 1
            sql = query_info["sql"]

            try:
                start = time.time()
                with engine.connect() as conn:
                    result = conn.execute(text(sql))
                    rows = result.fetchall()
                elapsed = time.time() - start

                print(f"  ✓ {query_name}: {len(rows)} rows in {elapsed:.2f}s")
                passed += 1
                results.append({
                    "stakeholder": stakeholder,
                    "query": query_name,
                    "status": "PASS",
                    "rows": len(rows),
                    "time": elapsed,
                    "error": None
                })
            except Exception as e:
                print(f"  ✗ {query_name}: ERROR")
                print(f"    {str(e)[:200]}")
                failed += 1
                results.append({
                    "stakeholder": stakeholder,
                    "query": query_name,
                    "status": "FAIL",
                    "rows": 0,
                    "time": 0,
                    "error": str(e)
                })

    print(f"\n{'='*60}")
    print(f"SUMMARY: {passed}/{total} passed, {failed} failed")
    print('='*60)

    if failed > 0:
        print("\nFailed queries:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"\n[{r['stakeholder']}] {r['query']}")
                print(f"Error: {r['error']}")

    return results

if __name__ == "__main__":
    test_all_queries()
