#!/usr/bin/env python3
"""Migrate the local SQLite database into Firestore.

The two SQLite tables are merged into a single Firestore collection holding one
document per stock. The document ID is the stock symbol and every property
becomes a field on that document:

    stock(symbol, name)            -> field "name"
    keyvalue(symbol, key, value)   -> field <key>

So ``stock/AAPL`` ends up as::

    {"name": "Apple", "market_cap": 3500000000000, "share_price": 234.56}

Numeric properties are stored as Firestore numbers rather than strings so that
they can be sorted and range-filtered server-side.

Re-running the migration overwrites existing documents rather than duplicating
them.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "data" / "value.db"
DEFAULT_CREDENTIALS = REPO_ROOT / "keys" / "value-firestore.json"
DEFAULT_COLLECTION = "stock"

# Firestore accepts at most 500 operations per batched write.
MAX_BATCH_SIZE = 500

# SQLite stores every property as TEXT. These are written to Firestore as
# numbers instead, using the given type so that each field has one consistent
# type across all documents.
NUMERIC_FIELDS: dict[str, type] = {
    "market_cap": int,
    "share_price": float,
    "dividend": float,
    "dividend_pct": float,
    "eps": float,
    "revenue_per_share": float,
    "week_52_high": float,
    "week_52_low": float,
    "pe_ratio": float,
}


def to_number(raw: str, kind: type) -> int | float:
    """Parse a TEXT property into an int or a float.

    Raises ValueError if the text is not a number.
    """
    text = raw.strip()
    if kind is int:
        try:
            return int(text)
        except ValueError:
            # Tolerate values written in decimal or exponent form.
            return round(float(text))
    return float(text)


def read_stocks(db_path: Path) -> tuple[dict[str, dict[str, object]], list[str]]:
    """Return one field map per symbol, plus a list of values that would not
    parse as numbers."""
    if not db_path.exists():
        sys.exit(f"ERROR: database not found: {db_path}")

    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
        stocks = conn.execute("SELECT symbol, name FROM stock").fetchall()
        keyvalues = conn.execute(
            "SELECT symbol, key, value FROM keyvalue"
        ).fetchall()

    documents: dict[str, dict[str, object]] = {}
    for symbol, name in stocks:
        fields = documents.setdefault(symbol, {})
        if name is not None:
            fields["name"] = name

    skipped: list[str] = []
    for symbol, key, value in keyvalues:
        if value is None:
            continue
        # Ignore properties for symbols that are absent from the stock table.
        if symbol not in documents:
            continue

        kind = NUMERIC_FIELDS.get(key)
        if kind is None:
            documents[symbol][key] = str(value)
            continue

        try:
            documents[symbol][key] = to_number(str(value), kind)
        except ValueError:
            # Leave the field off the document rather than storing text in a
            # numeric field; the app renders a missing value as a dash.
            skipped.append(f"{symbol}.{key}={value!r}")

    return documents, skipped


def connect(credentials: Path, project: str | None):
    import firebase_admin
    from firebase_admin import credentials as admin_credentials
    from firebase_admin import firestore

    if credentials.exists():
        cred = admin_credentials.Certificate(str(credentials))
    elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        cred = admin_credentials.ApplicationDefault()
    else:
        sys.exit(
            f"ERROR: no credentials at {credentials} and "
            "GOOGLE_APPLICATION_CREDENTIALS is unset."
        )

    options = {"projectId": project} if project else None
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, options)
    return firestore.client()


def write_documents(
    client, collection: str, documents: dict[str, dict[str, object]]
) -> None:
    ref = client.collection(collection)
    symbols = sorted(documents)
    written = 0

    for start in range(0, len(symbols), MAX_BATCH_SIZE):
        chunk = symbols[start : start + MAX_BATCH_SIZE]
        batch = client.batch()
        for symbol in chunk:
            batch.set(ref.document(symbol), documents[symbol])
        batch.commit()
        written += len(chunk)
        print(f"  wrote {written}/{len(symbols)} documents", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--project", default="value-619ef")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Summarise what would be written without contacting Firestore.",
    )
    args = parser.parse_args()

    documents, skipped = read_stocks(args.db)
    fields = sorted({field for doc in documents.values() for field in doc})
    print(f"{len(documents)} documents with fields {fields}")

    if skipped:
        print(f"WARNING: {len(skipped)} non-numeric value(s) omitted:")
        for entry in skipped[:10]:
            print(f"  {entry}")

    if args.dry_run:
        for symbol in sorted(documents)[:5]:
            print(f"  {symbol} -> {documents[symbol]}")
        print("Dry run: nothing written.")
        return

    client = connect(args.credentials, args.project)
    print(f"Writing to {args.project}/{args.collection}...")
    write_documents(client, args.collection, documents)
    print("Migration complete.")


if __name__ == "__main__":
    main()
