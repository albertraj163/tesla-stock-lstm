#!/usr/bin/env bash
pkill -f "cloudflared tunnel" 2>/dev/null
pkill -f "gunicorn app:app" 2>/dev/null && echo "Server and public link stopped." || echo "Server was not running."
