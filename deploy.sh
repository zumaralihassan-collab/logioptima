#!/usr/bin/env bash
# LogiOptima — one-shot GitHub deploy helper.
# Usage:  ./deploy.sh <github-username> <repo-name>
# Requires: git installed, and you signed in to GitHub (browser or `gh auth login`).
set -e

USER="${1:?Pass your GitHub username: ./deploy.sh <username> <repo>}"
REPO="${2:-logioptima}"

cd "$(dirname "$0")"

git init -b main 2>/dev/null || git checkout -B main
git add .
git commit -m "Deploy LogiOptima global logistics optimization tool" || echo "Nothing new to commit."

# Create the repo automatically if GitHub CLI is available, else create it manually on github.com first.
if command -v gh >/dev/null 2>&1; then
  gh repo create "$REPO" --public --source=. --remote=origin --push 2>/dev/null || {
    git remote add origin "https://github.com/$USER/$REPO.git" 2>/dev/null || true
    git push -u origin main
  }
  gh api -X POST "repos/$USER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" 2>/dev/null \
    && echo "GitHub Pages enabled." || echo "Enable Pages in Settings → Pages (main / root)."
else
  echo "GitHub CLI not found."
  echo "1) Create an EMPTY repo at https://github.com/new named '$REPO' (no README)."
  echo "2) Re-run, or run:"
  git remote add origin "https://github.com/$USER/$REPO.git" 2>/dev/null || true
  git push -u origin main
  echo "3) Then Settings → Pages → Source: main / (root)."
fi

echo "Done. Live at: https://$USER.github.io/$REPO/"
