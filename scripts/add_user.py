#!/usr/bin/env python3
"""Grant or revoke access to the value app.

The app has no self-service registration: an email can only sign in once a
document with that email as its ID exists in the ``users`` collection.

    ./scripts/add_user.py koen.kam@gmail.com
    ./scripts/add_user.py koen.kam@gmail.com --remove
    ./scripts/add_user.py --list
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CREDENTIALS = REPO_ROOT / "keys" / "value-firestore.json"
USERS_COLLECTION = "users"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_to_firestore import connect  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email", nargs="?", help="Email address to grant access to.")
    parser.add_argument("--remove", action="store_true", help="Revoke access.")
    parser.add_argument("--list", action="store_true", help="List allowed users.")
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--project", default="value-619ef")
    args = parser.parse_args()

    if not args.list and not args.email:
        parser.error("provide an email address, or use --list")

    client = connect(args.credentials, args.project)
    users = client.collection(USERS_COLLECTION)

    if args.list:
        docs = list(users.stream())
        if not docs:
            print("No users have access.")
        for doc in docs:
            print(doc.id)
        return

    email = args.email.strip().lower()
    if args.remove:
        users.document(email).delete()
        print(f"Revoked access for {email}.")
        return

    from firebase_admin import firestore

    users.document(email).set(
        {"email": email, "createdAt": firestore.SERVER_TIMESTAMP},
        merge=True,
    )
    print(f"Granted access to {email}.")


if __name__ == "__main__":
    main()
