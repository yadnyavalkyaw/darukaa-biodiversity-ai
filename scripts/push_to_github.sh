#!/bin/bash
set -e

REPO_URL="https://github.com/yadnyavalkyaw/darukaa-biodiversity-intelligence.git"

echo "=== Darukaa.Earth GitHub Sync ==="
echo "Target remote: $REPO_URL"

# Ensure origin is set
git remote set-url origin "$REPO_URL" 2>/dev/null || git remote add origin "$REPO_URL"

echo "Checking remote status..."
if git ls-remote --exit-code origin &>/dev/null; then
    echo "Remote repository exists! Pushing main branch..."
    git push -u origin main
    echo "Successfully pushed to $REPO_URL!"
else
    echo "Remote repository not found yet on GitHub."
    echo "Please create the repository first at: https://github.com/new?name=darukaa-biodiversity-intelligence"
    echo "Once created, re-run this script: bash scripts/push_to_github.sh"
fi
