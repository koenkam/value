#!/bin/bash
# Sync the code base and deploy the value Flutter web app to Firebase Hosting.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
flutter_dir="$repo_root/flutter"

function checkin() {
    cd "$repo_root" || exit 1

    # 1. Stage changes first so we can check if there is anything to commit
    git add .

    # 2. Check if there are differences between the index and the last commit
    if git diff --staged --quiet; then
        echo "No changes detected since last commit."
    else
        default_commit_message=$(git log -1 --pretty=%B)
        echo "Enter your commit message [${default_commit_message}] (30s timeout): "

        # 3. Read input with a 30-second timeout (-t 30)
        if ! read -t 30 commit_message; then
            echo "" # Print a newline if the timer runs out
            echo "Timeout reached. Using previous commit message."
        fi

        commit_message=${commit_message:-$default_commit_message}
        git commit -m "$commit_message"
    fi

    # 4. Push changes (works even if no new commit was made, in case of previous local commits)
    git push
}

function deploy_rules() {
    cd "$flutter_dir" || { echo "Failed to cd to flutter directory"; exit 1; }
    echo "Deploying Firestore rules..."
    firebase deploy --only firestore:rules || { echo "Firestore rules deploy failed"; exit 1; }
}

function deploy_app() {
    cd "$flutter_dir" || { echo "Failed to cd to flutter directory"; exit 1; }

    echo "Cleaning Flutter build..."
    flutter clean

    echo "Getting Flutter dependencies..."
    flutter pub get

    echo "Building Flutter web app..."
    if ! flutter build web --release; then
        echo "Flutter build failed!"
        exit 1
    fi

    if [ ! -d "build/web" ]; then
        echo "ERROR: build/web directory not found after build"
        exit 1
    fi

    echo "Build successful. Deploying to Firebase Hosting..."
    firebase deploy --only hosting || { echo "Firebase deploy failed"; exit 1; }
}

function migrate() {
    cd "$repo_root" || exit 1
    echo "Migrating data/value.db into Firestore..."
    .venv/bin/python scripts/migrate_to_firestore.py || { echo "Migration failed"; exit 1; }
}

# --- Declarative Configuration ---
# Map arguments to a space-separated list of functions to execute
cmd_app="deploy_app"
cmd_rules="deploy_rules"
cmd_migrate="migrate"
cmd_all="deploy_rules deploy_app"

# --- Main Dispatcher ---
target=${1:-help}

action_var="cmd_$target"
actions=${!action_var}

if [ -z "$actions" ]; then
    echo "No valid deployment flag provided: '$1'"
    echo "Available commands: all, app, rules, migrate"
    exit 1
fi

echo "Deploying target: $target"
checkin
for action in $actions; do
    $action
done

exit 0
