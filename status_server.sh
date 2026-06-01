#!/usr/bin/env bash
cd "$(dirname "$0")"
source "$(dirname "$0")/server_env.sh"

if pgrep -f "gunicorn app:app" >/dev/null; then
  echo "Server is RUNNING"
  echo ""
  echo "  Open: $APP_URL"
  echo ""
  pgrep -af "gunicorn app:app"
else
  echo "Server is NOT running."
  echo ""
  echo "  Start: ./run_server.sh   (background)"
  echo "     or: ./start.sh        (foreground)"
fi
