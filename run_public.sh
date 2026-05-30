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

update_pages_redirect() {
  local url="$1"
  mkdir -p docs

  cat > docs/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=$url">
  <title>Tesla Stock Forecaster</title>
  <script>location.replace("$url");</script>
</head>
<body>
  <p>Loading app… <a href="$url">Click here</a></p>
</body>
</html>
EOF

  if [ -f README.md ]; then
    sed -i "s|Current live tunnel:.*|Current live tunnel: $url|" README.md
  fi

  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    return
  fi

  if git diff --quiet docs/index.html README.md 2>/dev/null; then
    return
  fi

  git add docs/index.html README.md
  git commit -m "Update GitHub Pages redirect to current tunnel URL." >/dev/null 2>&1 || return
  git push origin main >/dev/null 2>&1 && echo "  GitHub Pages redirect updated and pushed."
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
    update_pages_redirect "$URL"
    echo ""
    echo "=========================================="
    echo "  PUBLIC LINK — enga irunthalum open aagum"
    echo "=========================================="
    echo ""
    echo "  $URL"
    echo ""
    echo "  GitHub Pages:"
    echo "  https://albertraj163.github.io/tesla-stock-lstm/"
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
