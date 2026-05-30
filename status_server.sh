#!/usr/bin/env bash
PORT="${PORT:-5555}"
SERVER_IP=$(hostname -I | tr ' ' '\n' | grep '^192\.' | head -1)
if [ -z "$SERVER_IP" ]; then
  SERVER_IP=$(hostname -I | awk '{print $1}')
fi

if pgrep -f "gunicorn app:app" >/dev/null; then
  echo "Server is RUNNING"
  echo ""
  echo "  LAN only:  http://$SERVER_IP:$PORT"
  if [ -f public_url.txt ]; then
    echo "  PUBLIC:    $(cat public_url.txt)  (enga irunthalum work)"
  else
    echo "  PUBLIC:    Not set. Run: ./run_public.sh"
  fi
  echo ""
  pgrep -af "gunicorn app:app"
else
  echo "Server is NOT running. Start with: ./run_public.sh"
fi
