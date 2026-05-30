#!/usr/bin/env bash
set -e

export PATH="$HOME/.local/bin:$PATH"
REPO_NAME="tesla-stock-lstm"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$PROJECT_DIR"

if ! command -v gh >/dev/null 2>&1; then
  echo "Installing GitHub CLI..."
  mkdir -p "$HOME/.local/bin"
  curl -sL "https://github.com/cli/cli/releases/download/v2.86.0/gh_2.86.0_linux_amd64.tar.gz" -o /tmp/gh.tar.gz
  tar -xzf /tmp/gh.tar.gz -C /tmp
  cp /tmp/gh_2.86.0_linux_amd64/bin/gh "$HOME/.local/bin/gh"
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub login required. Complete login in browser:"
  gh auth login --hostname github.com --git-protocol https --web
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "Remote already set. Pushing..."
  git push -u origin main
else
  echo "Creating GitHub repo: $REPO_NAME"
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
fi

echo ""
echo "Done! Your repo:"
gh repo view --web 2>/dev/null || gh repo view --json url -q .url
