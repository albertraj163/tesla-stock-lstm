#!/usr/bin/env bash
pkill -f "cloudflared tunnel" 2>/dev/null || true
pkill -f "gunicorn app:app" 2>/dev/null && echo "Server stopped." || echo "Server was not running."
