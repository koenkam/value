#!/usr/bin/env python3
"""Delete every document in a Firestore collection.

Used to retire collections that are no longer part of the data model, such as
the flat ``stock_values`` collection that ``stock`` replaced:

    ./scripts/drop_collection.py stock_values
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CREDENTIALS = REPO_ROOT / "keys" / "value-firestore.json"

# Firestore accepts at most 500 operations per batched write.
MAX_BATCH_SIZE = 500

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_to_firestore import connect  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", help="Name of the collection to delete.")
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--project", default="value-619ef")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt.",
    )
    args = parser.parse_args()

    client = connect(args.credentials, args.project)
    ref = client.collection(args.collection)

    if not args.yes:
        answer = input(
            f"Delete every document in {args.project}/{args.collection}? [y/N] "
        )
        if answer.strip().lower() not in {"y", "yes"}:
            print("Aborted.")
            return

    deleted = 0
    while True:
        docs = list(ref.limit(MAX_BATCH_SIZE).stream())
        if not docs:
            break
        batch = client.batch()
        for doc in docs:
            batch.delete(doc.reference)
        batch.commit()
        deleted += len(docs)
        print(f"  deleted {deleted} documents", flush=True)

    print(f"Collection '{args.collection}' is empty ({deleted} deleted).")


if __name__ == "__main__":
    main()
