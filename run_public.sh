#!/usr/bin/env bash
# Public internet link — works from ANY network (not just same LAN)

cd "$(dirname "$0")"
PORT="${PORT:-5555}"
export PATH="$HOME/.local/bin:$PATH"

install_cloudflared() {
  if command -v cloudflared >/dev/null 2>&1; then
    return
  fi
  echo "Installing cloudflared (one time)..."
  mkdir -p "$HOME/.local/bin"
  curl -sL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64" \
    -o "$HOME/.local/bin/cloudflared"
  chmod +x "$HOME/.local/bin/cloudflared"
}

install_cloudflared
./run_server.sh

pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 1
rm -f tunnel.log public_url.txt

echo "Creating public link..."
nohup cloudflared tunnel --url "http://127.0.0.1:$PORT" > tunnel.log 2>&1 &

for _ in $(seq 1 30); do
  URL=$(grep -oE 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' tunnel.log | head -1)
  if [ -n "$URL" ]; then
    echo "$URL" > public_url.txt
    echo ""
    echo "=========================================="
    echo "  PUBLIC LINK — enga irunthalum open aagum"
    echo "=========================================="
    echo ""
    echo "  $URL"
    echo ""
    echo "  Itha vera server, phone (mobile data),"
    echo "  office — ellam open panna mudiyum!"
    echo ""
    echo "  Stop: ./stop_server.sh"
    echo "=========================================="
    exit 0
  fi
  sleep 1
done

echo "Tunnel starting... 5 sec wait pannitu run pannunga:"
echo "  cat public_url.txt"
echo "  or: grep trycloudflare tunnel.log"
