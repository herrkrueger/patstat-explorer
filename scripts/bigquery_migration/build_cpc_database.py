#!/usr/bin/env python3
"""
Build CPC Classification SQLite Database.

Creates a CPC classification database analogous to patent-classification-2025.db (IPC),
using the official CPC release files from the EPO/USPTO.

Usage:
    python build_cpc_database.py /path/to/cpc_analysis/

Input files (in the specified directory):
    - CPCSymbolList202601.zip (or .csv) - Symbol hierarchy with levels
    - CPCTitleList202601.zip - English titles per section

Output:
    - cpc-classification-2026.db in the same directory
"""

import argparse
import csv
import io
import re
import sqlite3
import zipfile
from pathlib import Path


def extract_or_read_csv(directory: Path) -> list[dict]:
    """Read CPC symbol list from ZIP or CSV."""
    csv_file = directory / "CPCSymbolList202601.csv"
    zip_file = directory / "CPCSymbolList202601.zip"

    if csv_file.exists():
        print(f"Reading: {csv_file}")
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    elif zip_file.exists():
        print(f"Extracting: {zip_file}")
        with zipfile.ZipFile(zip_file, "r") as zf:
            with zf.open("CPCSymbolList202601.csv") as f:
                text = io.TextIOWrapper(f, encoding="utf-8")
                reader = csv.DictReader(text)
                return list(reader)
    else:
        raise FileNotFoundError("CPCSymbolList202601.csv or .zip not found")


def extract_titles(directory: Path) -> dict[str, str]:
    """Read CPC titles from all section files in the ZIP."""
    zip_file = directory / "CPCTitleList202601.zip"

    if not zip_file.exists():
        raise FileNotFoundError(f"{zip_file} not found")

    print(f"Extracting titles: {zip_file}")
    titles = {}

    with zipfile.ZipFile(zip_file, "r") as zf:
        for name in zf.namelist():
            if name.endswith(".txt"):
                with zf.open(name) as f:
                    text = io.TextIOWrapper(f, encoding="utf-8")
                    for line in text:
                        line = line.rstrip("\n\r")
                        if not line:
                            continue

                        # Format: SYMBOL<tab>LEVEL<tab>TITLE or SYMBOL<tab>TITLE
                        parts = line.split("\t")
                        if len(parts) >= 2:
                            symbol = parts[0].strip()
                            # Title is always the last part
                            title = parts[-1].strip()
                            # Remove curly braces from titles (CPC uses {notes})
                            title = re.sub(r"\{[^}]*\}", "", title).strip()
                            # Clean up extra spaces
                            title = re.sub(r"\s+", " ", title).strip()
                            titles[symbol] = title

    print(f"  Loaded {len(titles):,} titles")
    return titles


def symbol_to_short(symbol: str) -> str:
    """Convert PATSTAT space-padded symbol to short format.

    'A01B   1/02' -> 'A01B1/02'
    """
    return symbol.replace(" ", "")


def symbol_to_zeropad(symbol: str) -> str:
    """Convert PATSTAT or short symbol to zero-padded format.

    'A01B   1/02' -> 'A01B0001020000'
    'A01B' -> 'A01B'
    """
    short = symbol_to_short(symbol)

    if "/" not in short:
        return short

    slash_pos = short.index("/")
    subclass = short[:4]
    group_str = short[4:slash_pos]
    subgroup_str = short[slash_pos + 1:]

    group_zp = group_str.zfill(4)
    subgroup_zp = subgroup_str.ljust(6, "0")

    return f"{subclass}{group_zp}{subgroup_zp}"


def determine_kind(level: int) -> str:
    """Determine kind code from level."""
    if level == 2:
        return "s"  # section
    elif level == 4:
        return "c"  # class
    elif level == 5:
        return "u"  # subclass
    elif level == 7:
        return "m"  # main group
    else:
        depth = level - 7
        return str(min(depth, 9))


def build_database(directory: Path):
    """Build the CPC SQLite database."""
    # Read symbol list
    symbols = extract_or_read_csv(directory)
    print(f"  Loaded {len(symbols):,} symbols")

    # Read titles
    titles = extract_titles(directory)

    # Prepare database
    db_path = directory / "cpc-classification-2026.db"
    print(f"\nCreating database: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create schema
    cur.execute("DROP TABLE IF EXISTS cpc")
    cur.execute("""
        CREATE TABLE cpc (
            symbol TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            parent TEXT NOT NULL,
            level INTEGER NOT NULL,
            symbol_short TEXT,
            parent_short TEXT,
            symbol_patstat TEXT,
            title_en TEXT,
            not_allocatable INTEGER DEFAULT 0,
            additional_only INTEGER DEFAULT 0,
            status TEXT,
            size INTEGER DEFAULT 0,
            size_percent REAL DEFAULT 0.0
        )
    """)

    # Add root node
    cur.execute("""
        INSERT INTO cpc (symbol, kind, parent, level, symbol_short, title_en)
        VALUES ('CPC', 'r', '', 1, 'CPC', 'Cooperative Patent Classification')
    """)

    # Track last symbol at each level for parent assignment
    # CPC symbols are sorted, so the parent of a level-N entry is the
    # most recent level-(N-1) entry in the same branch
    last_at_level = {}

    # Process symbols (they're already sorted hierarchically)
    rows_inserted = 0
    batch = []

    for row in symbols:
        symbol = row["SYMBOL"].strip()
        level = int(row["level"])
        not_allocatable = 1 if row.get("not-allocatable", "FALSE") == "TRUE" else 0
        additional_only = 1 if row.get("additional-only", "FALSE") == "TRUE" else 0
        status = row.get("status", "published")

        # Derive fields
        symbol_short = symbol_to_short(symbol)
        symbol_zp = symbol_to_zeropad(symbol)
        symbol_patstat = symbol if "/" in symbol else None
        kind = determine_kind(level)

        # Determine parent based on level
        if level == 2:
            # Section -> parent is root
            parent_zp = "CPC"
            parent_short = "CPC"
        elif level == 4:
            # Class (A01) -> parent is section (A)
            parent_short = symbol_short[0]
            parent_zp = parent_short
        elif level == 5:
            # Subclass (A01B) -> parent is class (A01)
            parent_short = symbol_short[:3]
            parent_zp = parent_short
        elif level == 7:
            # Main group -> parent is subclass
            parent_short = symbol_short[:4]
            parent_zp = parent_short
        else:
            # Subgroup -> parent is last symbol at level-1
            parent_symbol = last_at_level.get(level - 1, symbol_short[:4])
            parent_short = symbol_to_short(parent_symbol)
            parent_zp = symbol_to_zeropad(parent_symbol)

        # Update last_at_level
        last_at_level[level] = symbol

        # Get title
        title = titles.get(symbol_short) or titles.get(symbol) or ""

        batch.append((
            symbol_zp, kind, parent_zp, level, symbol_short, parent_short,
            symbol_patstat, title, not_allocatable, additional_only, status
        ))

        rows_inserted += 1
        if len(batch) >= 10000:
            cur.executemany("""
                INSERT INTO cpc
                (symbol, kind, parent, level, symbol_short, parent_short,
                 symbol_patstat, title_en, not_allocatable, additional_only, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
            batch = []
            print(f"  Processed {rows_inserted:,} rows...")

    # Insert remaining
    if batch:
        cur.executemany("""
            INSERT INTO cpc
            (symbol, kind, parent, level, symbol_short, parent_short,
             symbol_patstat, title_en, not_allocatable, additional_only, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)

    # Create indices after bulk insert (faster)
    print("  Creating indices...")
    cur.execute("CREATE INDEX idx_cpc_level ON cpc(level)")
    cur.execute("CREATE INDEX idx_cpc_parent ON cpc(parent)")
    cur.execute("CREATE INDEX idx_cpc_kind ON cpc(kind)")
    cur.execute("CREATE INDEX idx_cpc_symbol_short ON cpc(symbol_short)")
    cur.execute("CREATE INDEX idx_cpc_symbol_patstat ON cpc(symbol_patstat)")

    conn.commit()

    # Stats
    cur.execute("SELECT COUNT(*) FROM cpc")
    total = cur.fetchone()[0]

    cur.execute("SELECT level, COUNT(*) FROM cpc GROUP BY level ORDER BY level")
    level_dist = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM cpc WHERE title_en != '' AND title_en IS NOT NULL")
    with_title = cur.fetchone()[0]

    conn.close()

    print(f"\n  Total rows: {total:,}")
    print(f"  With titles: {with_title:,}")
    print(f"\n  Level distribution:")
    for level, count in level_dist:
        print(f"    Level {level}: {count:,}")

    print(f"\n  Database saved to: {db_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Build CPC classification SQLite database"
    )
    parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Directory containing CPC ZIP files (default: current directory)"
    )

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}")
        return 1

    build_database(args.directory)
    return 0


if __name__ == "__main__":
    exit(main())
